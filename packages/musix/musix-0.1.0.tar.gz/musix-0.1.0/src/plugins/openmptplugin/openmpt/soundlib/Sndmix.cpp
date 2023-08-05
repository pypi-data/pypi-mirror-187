/*
 * Sndmix.cpp
 * -----------
 * Purpose: Pattern playback, effect processing
 * Notes  : (currently none)
 * Authors: Olivier Lapicque
 *          OpenMPT Devs
 * The OpenMPT source code is released under the BSD license. Read LICENSE for more details.
 */


#include "stdafx.h"

#include "Sndfile.h"
#include "MixerLoops.h"
#include "MIDIEvents.h"
#include "tuning.h"
#include "Tables.h"
#ifdef MODPLUG_TRACKER
#include "../mptrack/TrackerSettings.h"
#endif // MODPLUG_TRACKER
#ifndef NO_PLUGINS
#include "plugins/PlugInterface.h"
#endif // NO_PLUGINS
#include "OPL.h"

OPENMPT_NAMESPACE_BEGIN

// VU-Meter
#define VUMETER_DECAY		4

// Log tables for pre-amp
// Pre-amp (or more precisely: Pre-attenuation) depends on the number of channels,
// Which this table takes care of.
static const uint8 PreAmpTable[16] =
{
	0x60, 0x60, 0x60, 0x70,	// 0-7
	0x80, 0x88, 0x90, 0x98,	// 8-15
	0xA0, 0xA4, 0xA8, 0xAC,	// 16-23
	0xB0, 0xB4, 0xB8, 0xBC,	// 24-31
};

#ifndef NO_AGC
static const uint8 PreAmpAGCTable[16] =
{
	0x60, 0x60, 0x60, 0x64,
	0x68, 0x70, 0x78, 0x80,
	0x84, 0x88, 0x8C, 0x90,
	0x92, 0x94, 0x96, 0x98,
};
#endif


// Compensate frequency slide LUTs depending on whether we are handling periods or frequency - "up" and "down" in function name are seen from frequency perspective.
static uint32 GetLinearSlideDownTable    (const CSoundFile *sndFile, uint32 i) { MPT_ASSERT(i < CountOf(LinearSlideDownTable));     return sndFile->m_playBehaviour[kHertzInLinearMode] ? LinearSlideDownTable[i]     : LinearSlideUpTable[i]; }
static uint32 GetLinearSlideUpTable      (const CSoundFile *sndFile, uint32 i) { MPT_ASSERT(i < CountOf(LinearSlideDownTable));     return sndFile->m_playBehaviour[kHertzInLinearMode] ? LinearSlideUpTable[i]       : LinearSlideDownTable[i]; }
static uint32 GetFineLinearSlideDownTable(const CSoundFile *sndFile, uint32 i) { MPT_ASSERT(i < CountOf(FineLinearSlideDownTable)); return sndFile->m_playBehaviour[kHertzInLinearMode] ? FineLinearSlideDownTable[i] : FineLinearSlideUpTable[i]; }
static uint32 GetFineLinearSlideUpTable  (const CSoundFile *sndFile, uint32 i) { MPT_ASSERT(i < CountOf(FineLinearSlideDownTable)); return sndFile->m_playBehaviour[kHertzInLinearMode] ? FineLinearSlideUpTable[i]   : FineLinearSlideDownTable[i]; }


void CSoundFile::SetMixerSettings(const MixerSettings &mixersettings)
{
	SetPreAmp(mixersettings.m_nPreAmp); // adjust agc
	bool reset = false;
	if(
		(mixersettings.gdwMixingFreq != m_MixerSettings.gdwMixingFreq)
		||
		(mixersettings.gnChannels != m_MixerSettings.gnChannels)
		||
		(mixersettings.MixerFlags != m_MixerSettings.MixerFlags))
		reset = true;
	m_MixerSettings = mixersettings;
	InitPlayer(reset);
}


void CSoundFile::SetResamplerSettings(const CResamplerSettings &resamplersettings)
{
	m_Resampler.m_Settings = resamplersettings;
	m_Resampler.UpdateTables();
	InitAmigaResampler();
}


void CSoundFile::InitPlayer(bool bReset)
{
	if(bReset)
	{
		ResetMixStat();
		gnDryLOfsVol = 0;
		gnDryROfsVol = 0;
		InitAmigaResampler();
	}
	m_Resampler.UpdateTables();
#ifndef NO_REVERB
	m_Reverb.Initialize(bReset, m_MixerSettings.gdwMixingFreq);
#endif
#ifndef NO_DSP
	m_Surround.Initialize(bReset, m_MixerSettings.gdwMixingFreq);
#endif
#ifndef NO_DSP
	m_MegaBass.Initialize(bReset, m_MixerSettings.gdwMixingFreq);
#endif
#ifndef NO_EQ
	m_EQ.Initialize(bReset, m_MixerSettings.gdwMixingFreq);
#endif
#ifndef NO_AGC
	m_AGC.Initialize(bReset, m_MixerSettings.gdwMixingFreq);
#endif
	if(m_opl)
	{
		m_opl->Initialize(m_MixerSettings.gdwMixingFreq);
	}
}


bool CSoundFile::FadeSong(uint32 msec)
{
	samplecount_t nsamples = Util::muldiv(msec, m_MixerSettings.gdwMixingFreq, 1000);
	if (nsamples <= 0) return false;
	if (nsamples > 0x100000) nsamples = 0x100000;
	m_PlayState.m_nBufferCount = nsamples;
	int32 nRampLength = static_cast<int32>(m_PlayState.m_nBufferCount);
	// Ramp everything down
	for (uint32 noff=0; noff < m_nMixChannels; noff++)
	{
		ModChannel &pramp = m_PlayState.Chn[m_PlayState.ChnMix[noff]];
		pramp.newRightVol = pramp.newLeftVol = 0;
		pramp.leftRamp = (-pramp.leftVol << VOLUMERAMPPRECISION) / nRampLength;
		pramp.rightRamp = (-pramp.rightVol << VOLUMERAMPPRECISION) / nRampLength;
		pramp.rampLeftVol = pramp.leftVol << VOLUMERAMPPRECISION;
		pramp.rampRightVol = pramp.rightVol << VOLUMERAMPPRECISION;
		pramp.nRampLength = nRampLength;
		pramp.dwFlags.set(CHN_VOLUMERAMP);
	}
	return true;
}


// Apply stereo separation factor on an interleaved stereo/quad stream.
// count = Number of stereo sample pairs to process
// separation = -256...256 (negative values = swap L/R, 0 = mono, 128 = normal)
static void ApplyStereoSeparation(mixsample_t *mixBuf, std::size_t count, int32 separation)
{
#ifdef MPT_INTMIXER
	const mixsample_t factor_num = separation; // 128 =^= 1.0f
	const mixsample_t factor_den = MixerSettings::StereoSeparationScale; // 128
	const mixsample_t normalize_den = 2; // mid/side pre/post normalization
	const mixsample_t mid_den = normalize_den;
	const mixsample_t side_num = factor_num;
	const mixsample_t side_den = factor_den * normalize_den;
#else
	const float normalize_factor = 0.5f; // cumulative mid/side normalization factor (1/sqrt(2))*(1/sqrt(2))
	const float factor = static_cast<float>(separation) / static_cast<float>(MixerSettings::StereoSeparationScale); // sep / 128
	const float mid_factor = normalize_factor;
	const float side_factor = factor * normalize_factor;
#endif
	for(std::size_t i = 0; i < count; i++)
	{
		mixsample_t l = mixBuf[0];
		mixsample_t r = mixBuf[1];
		mixsample_t m = l + r;
		mixsample_t s = l - r;
#ifdef MPT_INTMIXER
		m /= mid_den;
		s = Util::muldiv(s, side_num, side_den);
#else
		m *= mid_factor;
		s *= side_factor;
#endif
		l = m + s;
		r = m - s;
		mixBuf[0] = l;
		mixBuf[1] = r;
		mixBuf += 2;
	}
}


static void ApplyStereoSeparation(mixsample_t *SoundFrontBuffer, mixsample_t *SoundRearBuffer, std::size_t channels, std::size_t countChunk, int32 separation)
{
	if(separation == MixerSettings::StereoSeparationScale)
	{ // identity
		return;
	}
	if(channels >= 2) ApplyStereoSeparation(SoundFrontBuffer, countChunk, separation);
	if(channels >= 4) ApplyStereoSeparation(SoundRearBuffer , countChunk, separation);
}


void CSoundFile::ProcessInputChannels(IAudioSource &source, std::size_t countChunk)
{
	for(std::size_t channel = 0; channel < NUMMIXINPUTBUFFERS; ++channel)
	{
		std::fill(&(MixInputBuffer[channel][0]), &(MixInputBuffer[channel][countChunk]), 0);
	}
	mixsample_t * buffers[NUMMIXINPUTBUFFERS];
	for(std::size_t channel = 0; channel < NUMMIXINPUTBUFFERS; ++channel)
	{
		buffers[channel] = MixInputBuffer[channel];
	}
	source.FillCallback(buffers, m_MixerSettings.NumInputChannels, countChunk);
}


CSoundFile::samplecount_t CSoundFile::Read(samplecount_t count, IAudioReadTarget &target, IAudioSource &source)
{
	MPT_ASSERT_ALWAYS(m_MixerSettings.IsValid());

	bool mixPlugins = false;
#ifndef NO_PLUGINS
	for(const auto &plug : m_MixPlugins)
	{
		if(plug.pMixPlugin)
		{
			mixPlugins = true;
			break;
		}
	}
#endif // NO_PLUGINS

	samplecount_t countRendered = 0;
	samplecount_t countToRender = count;

	while(!m_SongFlags[SONG_ENDREACHED] && countToRender > 0)
	{

		// Update Channel Data
		if(!m_PlayState.m_nBufferCount)
		{
			// Last tick or fade completely processed, find out what to do next

			if(m_SongFlags[SONG_FADINGSONG])
			{
				// Song was faded out
				m_SongFlags.set(SONG_ENDREACHED);
			} else if(ReadNote())
			{
				// Render next tick (normal progress)
				MPT_ASSERT(m_PlayState.m_nBufferCount > 0);
				#ifdef MODPLUG_TRACKER
					// Save pattern cue points for WAV rendering here (if we reached a new pattern, that is.)
					if(m_PatternCuePoints != nullptr && (m_PatternCuePoints->empty() || m_PlayState.m_nCurrentOrder != m_PatternCuePoints->back().order))
					{
						PatternCuePoint cue;
						cue.offset = countRendered;
						cue.order = m_PlayState.m_nCurrentOrder;
						cue.processed = false;	// We don't know the base offset in the file here. It has to be added in the main conversion loop.
						m_PatternCuePoints->push_back(cue);
					}
				#endif
			} else
			{
				// No new pattern data
				#ifdef MODPLUG_TRACKER
					if((m_nMaxOrderPosition) && (m_PlayState.m_nCurrentOrder >= m_nMaxOrderPosition))
					{
						m_SongFlags.set(SONG_ENDREACHED);
					}
				#endif // MODPLUG_TRACKER
				if(IsRenderingToDisc())
				{
					// Disable song fade when rendering or when requested in libopenmpt.
					m_SongFlags.set(SONG_ENDREACHED);
				} else
				{ // end of song reached, fade it out
					if(FadeSong(FADESONGDELAY)) // sets m_nBufferCount xor returns false
					{ // FadeSong sets m_nBufferCount here
						MPT_ASSERT(m_PlayState.m_nBufferCount > 0);
						m_SongFlags.set(SONG_FADINGSONG);
					} else
					{
						m_SongFlags.set(SONG_ENDREACHED);
					}
				}
			}

		}

		if(m_SongFlags[SONG_ENDREACHED])
		{
			// Mix done.

			// If we decide to continue the mix (possible in libopenmpt), the tick count
			// is valid right now (0), meaning that no new row data will be processed.
			// This would effectively prolong the last played row.
			m_PlayState.m_nTickCount = GetNumTicksOnCurrentRow();
			break;
		}

		MPT_ASSERT(m_PlayState.m_nBufferCount > 0); // assert that we have actually something to do

		const samplecount_t countChunk = std::min<samplecount_t>({ MIXBUFFERSIZE, m_PlayState.m_nBufferCount, countToRender });

		if(m_MixerSettings.NumInputChannels > 0)
		{
			ProcessInputChannels(source, countChunk);
		}

		CreateStereoMix(countChunk);

		if(m_opl)
		{
			m_opl->Mix(MixSoundBuffer, countChunk, m_OPLVolumeFactor * m_nVSTiVolume / 48);
		}

		#ifndef NO_REVERB
			m_Reverb.Process(MixSoundBuffer, countChunk);
		#endif // NO_REVERB

		if(mixPlugins)
		{
			ProcessPlugins(countChunk);
		}

		if(m_MixerSettings.gnChannels == 1)
		{
			MonoFromStereo(MixSoundBuffer, countChunk);
		}

		if(m_PlayConfig.getGlobalVolumeAppliesToMaster())
		{
			ProcessGlobalVolume(countChunk);
		}

		if(m_MixerSettings.m_nStereoSeparation != MixerSettings::StereoSeparationScale)
		{
			ProcessStereoSeparation(countChunk);
		}

		if(m_MixerSettings.DSPMask)
		{
			ProcessDSP(countChunk);
		}

		if(m_MixerSettings.gnChannels == 4)
		{
			InterleaveFrontRear(MixSoundBuffer, MixRearBuffer, countChunk);
		}

		target.DataCallback(MixSoundBuffer, m_MixerSettings.gnChannels, countChunk);

		// Buffer ready
		countRendered += countChunk;
		countToRender -= countChunk;
		m_PlayState.m_nBufferCount -= countChunk;
		m_PlayState.m_lTotalSampleCount += countChunk;		// increase sample count for VSTTimeInfo.

#ifdef MODPLUG_TRACKER
		if(IsRenderingToDisc())
		{
			// Stop playback on F00 if no more voices are active.
			// F00 sets the tick count to 65536 in FT2, so it just generates a reaaaally long row.
			// Usually this command can be found at the end of a song to effectively stop playback.
			// Since we don't want to render hours of silence, we are going to check if there are
			// still any channels playing, and if that is no longer the case, we stop playback at
			// the end of the next tick.
			if(m_PlayState.m_nMusicSpeed == uint16_max && (m_nMixStat == 0 || m_PlayState.m_nGlobalVolume == 0) && GetType() == MOD_TYPE_XM && !m_PlayState.m_nBufferCount)
			{
				m_SongFlags.set(SONG_ENDREACHED);
			}
		}
#endif // MODPLUG_TRACKER
	}

	// mix done

	return countRendered;

}


void CSoundFile::ProcessDSP(uint32 countChunk)
{
	#ifndef NO_DSP
		if(m_MixerSettings.DSPMask & SNDDSP_SURROUND)
		{
			m_Surround.Process(MixSoundBuffer, MixRearBuffer, countChunk, m_MixerSettings.gnChannels);
		}
	#endif // NO_DSP

	#ifndef NO_DSP
		if(m_MixerSettings.DSPMask & SNDDSP_MEGABASS)
		{
			m_MegaBass.Process(MixSoundBuffer, MixRearBuffer, countChunk, m_MixerSettings.gnChannels);
		}
	#endif // NO_DSP

	#ifndef NO_EQ
		if(m_MixerSettings.DSPMask & SNDDSP_EQ)
		{
			m_EQ.Process(MixSoundBuffer, MixRearBuffer, countChunk, m_MixerSettings.gnChannels);
		}
	#endif // NO_EQ

	#ifndef NO_AGC
		if(m_MixerSettings.DSPMask & SNDDSP_AGC)
		{
			m_AGC.Process(MixSoundBuffer, MixRearBuffer, countChunk, m_MixerSettings.gnChannels);
		}
	#endif // NO_AGC
	#if defined(NO_DSP) && defined(NO_EQ) && defined(NO_AGC)
		MPT_UNREFERENCED_PARAMETER(countChunk);
	#endif
}


/////////////////////////////////////////////////////////////////////////////
// Handles navigation/effects

bool CSoundFile::ProcessRow()
{
	while(++m_PlayState.m_nTickCount >= GetNumTicksOnCurrentRow())
	{
		// When having an EEx effect on the same row as a Dxx jump, the target row is not played in ProTracker.
		// Test case: DelayBreak.mod (based on condom_corruption by Travolta)
		const bool ignoreRow = m_PlayState.m_nPatternDelay != 0 && m_SongFlags[SONG_BREAKTOROW] && GetType() == MOD_TYPE_MOD;

		// Done with the last row of the pattern or jumping somewhere else
		const bool patternTransition = m_PlayState.m_nNextRow == 0 || m_SongFlags[SONG_BREAKTOROW];
		if(patternTransition)
		{
			if(GetType() == MOD_TYPE_S3M)
			{
				// Reset pattern loop start
				// Test case: LoopReset.s3m
				for(CHANNELINDEX i = 0; i < GetNumChannels(); i++)
				{
					m_PlayState.Chn[i].nPatternLoop = 0;
				}
			}
		}

		m_PlayState.m_nPatternDelay = 0;
		m_PlayState.m_nFrameDelay = 0;
		m_PlayState.m_nTickCount = 0;
		m_PlayState.m_nRow = m_PlayState.m_nNextRow;
		// Reset Pattern Loop Effect
		m_PlayState.m_nCurrentOrder = m_PlayState.m_nNextOrder;

#ifdef MODPLUG_TRACKER
		if(patternTransition)
		{
			HandlePatternTransitionEvents();
		}
		// "Lock row" editing feature
		if(m_lockRowStart != ROWINDEX_INVALID && (m_PlayState.m_nRow < m_lockRowStart || m_PlayState.m_nRow > m_lockRowEnd) && !IsRenderingToDisc())
		{
			m_PlayState.m_nRow = m_lockRowStart;
		}
		// "Lock order" editing feature
		if(Order().IsPositionLocked(m_PlayState.m_nCurrentOrder) && !IsRenderingToDisc())
		{
			m_PlayState.m_nCurrentOrder = m_lockOrderStart;
		}
#endif // MODPLUG_TRACKER

		// Check if pattern is valid
		if(!m_SongFlags[SONG_PATTERNLOOP])
		{
			m_PlayState.m_nPattern = (m_PlayState.m_nCurrentOrder < Order().size()) ? Order()[m_PlayState.m_nCurrentOrder] : Order.GetInvalidPatIndex();
			if (m_PlayState.m_nPattern < Patterns.Size() && !Patterns[m_PlayState.m_nPattern].IsValid()) m_PlayState.m_nPattern = Order.GetIgnoreIndex();
			while (m_PlayState.m_nPattern >= Patterns.Size())
			{
				// End of song?
				if ((m_PlayState.m_nPattern == Order.GetInvalidPatIndex()) || (m_PlayState.m_nCurrentOrder >= Order().size()))
				{

					//if (!m_nRepeatCount) return false;

					ORDERINDEX restartPosOverride = Order().GetRestartPos();
					if(restartPosOverride == 0 && m_PlayState.m_nCurrentOrder <= Order().size() && m_PlayState.m_nCurrentOrder > 0)
					{
						// Subtune detection. Subtunes are separated by "---" order items, so if we're in a
						// subtune and there's no restart position, we go to the first order of the subtune
						// (i.e. the first order after the previous "---" item)
						for(ORDERINDEX ord = m_PlayState.m_nCurrentOrder - 1; ord > 0; ord--)
						{
							if(Order()[ord] == Order.GetInvalidPatIndex())
							{
								// Jump back to first order of this subtune
								restartPosOverride = ord + 1;
								break;
							}
						}
					}

					// If channel resetting is disabled in MPT, we will emulate a pattern break (and we always do it if we're not in MPT)
#ifdef MODPLUG_TRACKER
					if(!(TrackerSettings::Instance().m_dwPatternSetup & PATTERN_RESETCHANNELS))
#endif // MODPLUG_TRACKER
					{
						m_SongFlags.set(SONG_BREAKTOROW);
					}

					if (restartPosOverride == 0 && !m_SongFlags[SONG_BREAKTOROW])
					{
						//rewbs.instroVSTi: stop all VSTi at end of song, if looping.
						StopAllVsti();
						m_PlayState.m_nMusicSpeed = m_nDefaultSpeed;
						m_PlayState.m_nMusicTempo = m_nDefaultTempo;
						m_PlayState.m_nGlobalVolume = m_nDefaultGlobalVolume;
						for(CHANNELINDEX i = 0; i < MAX_CHANNELS; i++)
						{
							m_PlayState.Chn[i].dwFlags.set(CHN_NOTEFADE | CHN_KEYOFF);
							m_PlayState.Chn[i].nFadeOutVol = 0;

							if (i < m_nChannels)
							{
								m_PlayState.Chn[i].nGlobalVol = ChnSettings[i].nVolume;
								m_PlayState.Chn[i].nVolume = ChnSettings[i].nVolume;
								m_PlayState.Chn[i].nPan = ChnSettings[i].nPan;
								m_PlayState.Chn[i].nPanSwing = m_PlayState.Chn[i].nVolSwing = 0;
								m_PlayState.Chn[i].nCutSwing = m_PlayState.Chn[i].nResSwing = 0;
								m_PlayState.Chn[i].nOldVolParam = 0;
								m_PlayState.Chn[i].oldOffset = 0;
								m_PlayState.Chn[i].nOldHiOffset = 0;
								m_PlayState.Chn[i].nPortamentoDest = 0;

								if (!m_PlayState.Chn[i].nLength)
								{
									m_PlayState.Chn[i].dwFlags = ChnSettings[i].dwFlags;
									m_PlayState.Chn[i].nLoopStart = 0;
									m_PlayState.Chn[i].nLoopEnd = 0;
									m_PlayState.Chn[i].pModInstrument = nullptr;
									m_PlayState.Chn[i].pModSample = nullptr;
								}
							}
						}
					}

					//Handle Repeat position
					//if (m_nRepeatCount > 0) m_nRepeatCount--;
					m_PlayState.m_nCurrentOrder = restartPosOverride;
					m_SongFlags.reset(SONG_BREAKTOROW);
					//If restart pos points to +++, move along
					while(m_PlayState.m_nCurrentOrder < Order().size() && Order()[m_PlayState.m_nCurrentOrder] == Order.GetIgnoreIndex())
					{
						m_PlayState.m_nCurrentOrder++;
					}
					//Check for end of song or bad pattern
					if (m_PlayState.m_nCurrentOrder >= Order().size()
						|| !Order().IsValidPat(m_PlayState.m_nCurrentOrder))
					{
						visitedSongRows.Initialize(true);
						return false;
					}
				} else
				{
					m_PlayState.m_nCurrentOrder++;
				}

				if (m_PlayState.m_nCurrentOrder < Order().size())
					m_PlayState.m_nPattern = Order()[m_PlayState.m_nCurrentOrder];
				else
					m_PlayState.m_nPattern = Order.GetInvalidPatIndex();

				if (m_PlayState.m_nPattern < Patterns.Size() && !Patterns[m_PlayState.m_nPattern].IsValid())
					m_PlayState.m_nPattern = Order.GetIgnoreIndex();
			}
			m_PlayState.m_nNextOrder = m_PlayState.m_nCurrentOrder;

#ifdef MODPLUG_TRACKER
			if ((m_nMaxOrderPosition) && (m_PlayState.m_nCurrentOrder >= m_nMaxOrderPosition)) return false;
#endif // MODPLUG_TRACKER
		}

		// Weird stuff?
		if (!Patterns.IsValidPat(m_PlayState.m_nPattern))
			return false;
		// Did we jump to an invalid row?
		if (m_PlayState.m_nRow >= Patterns[m_PlayState.m_nPattern].GetNumRows()) m_PlayState.m_nRow = 0;

		// Has this row been visited before? We might want to stop playback now.
		// But: We will not mark the row as modified if the song is not in loop mode but
		// the pattern loop (editor flag, not to be confused with the pattern loop effect)
		// flag is set - because in that case, the module would stop after the first pattern loop...
		const bool overrideLoopCheck = (m_nRepeatCount != -1) && m_SongFlags[SONG_PATTERNLOOP];
		if(!overrideLoopCheck && visitedSongRows.IsVisited(m_PlayState.m_nCurrentOrder, m_PlayState.m_nRow, true))
		{
			if(m_nRepeatCount)
			{
				// repeat count == -1 means repeat infinitely.
				if(m_nRepeatCount > 0)
				{
					m_nRepeatCount--;
				}
				// Forget all but the current row.
				visitedSongRows.Initialize(true);
				visitedSongRows.Visit(m_PlayState.m_nCurrentOrder, m_PlayState.m_nRow);
			} else
			{
#ifdef MODPLUG_TRACKER
				// Let's check again if this really is the end of the song.
				// The visited rows vector might have been screwed up while editing...
				// This is of course not possible during rendering to WAV, so we ignore that case.
				GetLengthType t = GetLength(eNoAdjust).back();
				if(IsRenderingToDisc() || (t.lastOrder == m_PlayState.m_nCurrentOrder && t.lastRow == m_PlayState.m_nRow))
				{
					// This is really the song's end!
					visitedSongRows.Initialize(true);
					return false;
				} else
				{
					// Ok, this is really dirty, but we have to update the visited rows vector...
					GetLength(eAdjustOnSuccess, GetLengthTarget(m_PlayState.m_nCurrentOrder, m_PlayState.m_nRow));
				}
#else
				if(m_SongFlags[SONG_PLAYALLSONGS])
				{
					// When playing all subsongs consecutively, first search for any hidden subsongs...
					if(!visitedSongRows.GetFirstUnvisitedRow(m_PlayState.m_nCurrentOrder, m_PlayState.m_nRow, true))
					{
						// ...and then try the next sequence.
						m_PlayState.m_nNextOrder = m_PlayState.m_nCurrentOrder = 0;
						m_PlayState.m_nNextRow = m_PlayState.m_nRow = 0;
						if(Order.GetCurrentSequenceIndex() >= Order.GetNumSequences() - 1)
						{
							Order.SetSequence(0);
							visitedSongRows.Initialize(true);
							return false;
						}
						Order.SetSequence(Order.GetCurrentSequenceIndex() + 1);
						visitedSongRows.Initialize(true);
					}
					// When jumping to the next subsong, stop all playing notes from the previous song...
					for(CHANNELINDEX i = 0; i < MAX_CHANNELS; i++)
						m_PlayState.Chn[i].Reset(ModChannel::resetSetPosFull, *this, i);
					StopAllVsti();
					// ...and the global playback information.
					m_PlayState.m_nMusicSpeed = m_nDefaultSpeed;
					m_PlayState.m_nMusicTempo = m_nDefaultTempo;
					m_PlayState.m_nGlobalVolume = m_nDefaultGlobalVolume;

					m_PlayState.m_nNextOrder = m_PlayState.m_nCurrentOrder;
					m_PlayState.m_nNextRow = m_PlayState.m_nRow;
					if(Order().size() > m_PlayState.m_nCurrentOrder)
						m_PlayState.m_nPattern = Order()[m_PlayState.m_nCurrentOrder];
					visitedSongRows.Visit(m_PlayState.m_nCurrentOrder, m_PlayState.m_nRow);
					if (!Patterns.IsValidPat(m_PlayState.m_nPattern))
						return false;
				} else
				{
					visitedSongRows.Initialize(true);
					return false;
				}
#endif // MODPLUG_TRACKER
			}
		}

		m_PlayState.m_nNextRow = m_PlayState.m_nRow + 1;
		if (m_PlayState.m_nNextRow >= Patterns[m_PlayState.m_nPattern].GetNumRows())
		{
			if (!m_SongFlags[SONG_PATTERNLOOP]) m_PlayState.m_nNextOrder = m_PlayState.m_nCurrentOrder + 1;
			m_PlayState.m_nNextRow = 0;

			// FT2 idiosyncrasy: When E60 is used on a pattern row x, the following pattern also starts from row x
			// instead of the beginning of the pattern, unless there was a Bxx or Dxx effect.
			if(m_playBehaviour[kFT2LoopE60Restart])
			{
				m_PlayState.m_nNextRow = m_PlayState.m_nNextPatStartRow;
				m_PlayState.m_nNextPatStartRow = 0;
			}
		}

		// Reset channel values
		ModCommand *m = Patterns[m_PlayState.m_nPattern].GetRow(m_PlayState.m_nRow);
		for (ModChannel *pChn = m_PlayState.Chn, *pEnd = pChn + m_nChannels; pChn != pEnd; pChn++, m++)
		{
			// First, handle some quirks that happen after the last tick of the previous row...
			if(m_playBehaviour[KST3PortaAfterArpeggio]
				&& pChn->nCommand == CMD_ARPEGGIO	// Previous row state!
				&& (m->command == CMD_PORTAMENTOUP || m->command == CMD_PORTAMENTODOWN))
			{
				// In ST3, a portamento immediately following an arpeggio continues where the arpeggio left off.
				// Test case: PortaAfterArp.s3m
				pChn->nPeriod = GetPeriodFromNote(pChn->nArpeggioLastNote, pChn->nFineTune, pChn->nC5Speed);
			}

			if(m_playBehaviour[kMODOutOfRangeNoteDelay]
				&& !m->IsNote()
				&& pChn->rowCommand.IsNote()
				&& pChn->rowCommand.command == CMD_MODCMDEX && (pChn->rowCommand.param & 0xF0) == 0xD0
				&& (pChn->rowCommand.param & 0x0Fu) >= m_PlayState.m_nMusicSpeed)
			{
				// In ProTracker, a note triggered by an out-of-range note delay can be heard on the next row
				// if there is no new note on that row.
				// Test case: NoteDelay-NextRow.mod
				pChn->nPeriod = GetPeriodFromNote(pChn->rowCommand.note, pChn->nFineTune, 0);
			}
			if(m_playBehaviour[kMODTempoOnSecondTick] && !m_playBehaviour[kMODVBlankTiming] && m_PlayState.m_nMusicSpeed == 1 && pChn->rowCommand.command == CMD_TEMPO)
			{
				// ProTracker sets the tempo after the first tick. This block handles the case of one tick per row.
				// Test case: TempoChange.mod
				m_PlayState.m_nMusicTempo = TEMPO(pChn->rowCommand.param, 0);
			}

			pChn->rowCommand = *m;

			pChn->rightVol = pChn->newRightVol;
			pChn->leftVol = pChn->newLeftVol;
			pChn->dwFlags.reset(CHN_VIBRATO | CHN_TREMOLO);
			if(!m_playBehaviour[kITVibratoTremoloPanbrello]) pChn->nPanbrelloOffset = 0;
			pChn->nCommand = CMD_NONE;
			pChn->m_plugParamValueStep = 0;
		}

		// Now that we know which pattern we're on, we can update time signatures (global or pattern-specific)
		UpdateTimeSignature();

		if(ignoreRow)
		{
			m_PlayState.m_nTickCount = m_PlayState.m_nMusicSpeed;
			continue;
		}
		break;
	}
	// Should we process tick0 effects?
	if (!m_PlayState.m_nMusicSpeed) m_PlayState.m_nMusicSpeed = 1;

	//End of row? stop pattern step (aka "play row").
#ifdef MODPLUG_TRACKER
	if (m_PlayState.m_nTickCount >= GetNumTicksOnCurrentRow() - 1)
	{
		if(m_SongFlags[SONG_STEP])
		{
			m_SongFlags.reset(SONG_STEP);
			m_SongFlags.set(SONG_PAUSED);
		}
	}
#endif // MODPLUG_TRACKER

	if (m_PlayState.m_nTickCount)
	{
		m_SongFlags.reset(SONG_FIRSTTICK);
		if(!(GetType() & (MOD_TYPE_XM | MOD_TYPE_MT2)) && m_PlayState.m_nTickCount < GetNumTicksOnCurrentRow())
		{
			// Emulate first tick behaviour if Row Delay is set.
			// Test cases: PatternDelaysRetrig.it, PatternDelaysRetrig.s3m, PatternDelaysRetrig.xm, PatternDelaysRetrig.mod
			if(!(m_PlayState.m_nTickCount % (m_PlayState.m_nMusicSpeed + m_PlayState.m_nFrameDelay)))
			{
				m_SongFlags.set(SONG_FIRSTTICK);
			}
		}
	} else
	{
		m_SongFlags.set(SONG_FIRSTTICK);
		m_SongFlags.reset(SONG_BREAKTOROW);
	}

	// Update Effects
	return ProcessEffects();
}


////////////////////////////////////////////////////////////////////////////////////////////
// Channel effect processing


// Calculate delta for Vibrato / Tremolo / Panbrello effect
int CSoundFile::GetVibratoDelta(int type, int position) const
{
	// IT compatibility: IT has its own, more precise tables
	if(m_playBehaviour[kITVibratoTremoloPanbrello])
	{
		position &= 0xFF;
		switch(type & 0x03)
		{
		case 0:	// Sine
		default:
			return ITSinusTable[position];
		case 1:	// Ramp down
			return 64 - (position + 1) / 2;
		case 2:	// Square
			return position < 128 ? 64 : 0;
		case 3:	// Random
			return mpt::random<int, 7>(AccessPRNG()) - 0x40;
		}
	} else if(GetType() & (MOD_TYPE_DIGI | MOD_TYPE_DBM))
	{
		// Other waveforms are not supported.
		static const int8 DBMSinus[] =
		{
			33, 52, 69, 84, 96, 107, 116, 122,  125, 127,  125, 122, 116, 107, 96, 84,
			69, 52, 33, 13, -8, -31, -54, -79, -104,-128, -104, -79, -54, -31, -8, 13,
		};
		return DBMSinus[(position / 2u) & 0x1F];
	} else
	{
		position &= 0x3F;
		switch(type & 0x03)
		{
		case 0:	// Sine
		default:
			return ModSinusTable[position];
		case 1:	// Ramp down
			return (position < 32 ? 0 : 255) - position * 4;
		case 2:	// Square
			return position < 32 ? 127 : -127;
		case 3:	// Random
			return ModRandomTable[position];
		}
	}
}


void CSoundFile::ProcessVolumeSwing(ModChannel &chn, int &vol) const
{
	if(m_playBehaviour[kITSwingBehaviour])
	{
		vol += chn.nVolSwing;
		Limit(vol, 0, 64);
	} else if(m_playBehaviour[kMPTOldSwingBehaviour])
	{
		vol += chn.nVolSwing;
		Limit(vol, 0, 256);
	} else
	{
		chn.nVolume += chn.nVolSwing;
		Limit(chn.nVolume, 0, 256);
		vol = chn.nVolume;
		chn.nVolSwing = 0;
	}
}


void CSoundFile::ProcessPanningSwing(ModChannel &chn) const
{
	if(m_playBehaviour[kITSwingBehaviour] || m_playBehaviour[kMPTOldSwingBehaviour])
	{
		chn.nRealPan = chn.nPan + chn.nPanSwing;
		Limit(chn.nRealPan, 0, 256);
	} else
	{
		chn.nPan += chn.nPanSwing;
		Limit(chn.nPan, 0, 256);
		chn.nPanSwing = 0;
		chn.nRealPan = chn.nPan;
	}
}


void CSoundFile::ProcessTremolo(ModChannel &chn, int &vol) const
{
	if (chn.dwFlags[CHN_TREMOLO])
	{
		if(m_SongFlags.test_all(SONG_FIRSTTICK | SONG_PT_MODE))
		{
			// ProTracker doesn't apply tremolo nor advance on the first tick.
			// Test case: VibratoReset.mod
			return;
		}

		// IT compatibility: Why would you not want to execute tremolo at volume 0?
		if(vol > 0 || m_playBehaviour[kITVibratoTremoloPanbrello])
		{
			// IT compatibility: We don't need a different attenuation here because of the different tables we're going to use
			const uint8 attenuation = ((GetType() & (MOD_TYPE_XM | MOD_TYPE_MOD)) || m_playBehaviour[kITVibratoTremoloPanbrello]) ? 5 : 6;

			int delta = GetVibratoDelta(chn.nTremoloType, chn.nTremoloPos);
			if((chn.nTremoloType & 0x03) == 1 && m_playBehaviour[kFT2TremoloRampWaveform])
			{
				// FT2 compatibility: Tremolo ramp down / triangle implementation is weird and affected by vibrato position (copypaste bug)
				// Test case: TremoloWaveforms.xm, TremoloVibrato.xm
				uint8 ramp = (chn.nTremoloPos * 4u) & 0x7F;
				// Volume-colum vibrato gets executed first in FT2, so we may need to advance the vibrato position first
				uint32 vibPos = chn.nVibratoPos;
				if(!m_SongFlags[SONG_FIRSTTICK] && chn.dwFlags[CHN_VIBRATO])
					vibPos += chn.nVibratoSpeed;
				if((vibPos & 0x3F) >= 32)
					ramp ^= 0x7F;
				if((chn.nTremoloPos & 0x3F) >= 32)
					delta = -ramp;
				else
					delta = ramp;
			}
			if(GetType() != MOD_TYPE_DMF)
			{
				vol += (delta * chn.nTremoloDepth) / (1 << attenuation);
			} else
			{
				// Tremolo in DMF always attenuates by a percentage of the current note volume
				vol -= (vol * chn.nTremoloDepth * (64 - delta)) / (128 * 64);
			}
		}
		if(!m_SongFlags[SONG_FIRSTTICK] || ((GetType() & (MOD_TYPE_IT|MOD_TYPE_MPT)) && !m_SongFlags[SONG_ITOLDEFFECTS]))
		{
			// IT compatibility: IT has its own, more precise tables
			if(m_playBehaviour[kITVibratoTremoloPanbrello])
				chn.nTremoloPos += 4 * chn.nTremoloSpeed;
			else
				chn.nTremoloPos += chn.nTremoloSpeed;
		}
	}
}


void CSoundFile::ProcessTremor(CHANNELINDEX nChn, int &vol)
{
	ModChannel &chn = m_PlayState.Chn[nChn];

	if(m_playBehaviour[kFT2Tremor])
	{
		// FT2 Compatibility: Weird XM tremor.
		// Test case: Tremor.xm
		if(chn.nTremorCount & 0x80)
		{
			if(!m_SongFlags[SONG_FIRSTTICK] && chn.nCommand == CMD_TREMOR)
			{
				chn.nTremorCount &= ~0x20;
				if(chn.nTremorCount == 0x80)
				{
					// Reached end of off-time
					chn.nTremorCount = (chn.nTremorParam >> 4) | 0xC0;
				} else if(chn.nTremorCount == 0xC0)
				{
					// Reached end of on-time
					chn.nTremorCount = (chn.nTremorParam & 0x0F) | 0x80;
				} else
				{
					chn.nTremorCount--;
				}

				chn.dwFlags.set(CHN_FASTVOLRAMP);
			}

			if((chn.nTremorCount & 0xE0) == 0x80)
			{
				vol = 0;
			}
		}
	} else if(chn.nCommand == CMD_TREMOR)
	{
		// IT compatibility 12. / 13.: Tremor
		if(m_playBehaviour[kITTremor])
		{
			if((chn.nTremorCount & 0x80) && chn.nLength)
			{
				if (chn.nTremorCount == 0x80)
					chn.nTremorCount = (chn.nTremorParam >> 4) | 0xC0;
				else if (chn.nTremorCount == 0xC0)
					chn.nTremorCount = (chn.nTremorParam & 0x0F) | 0x80;
				else
					chn.nTremorCount--;
			}

			if((chn.nTremorCount & 0xC0) == 0x80)
				vol = 0;
		} else
		{
			uint8 ontime = chn.nTremorParam >> 4;
			uint8 n = ontime + (chn.nTremorParam & 0x0F);	// Total tremor cycle time (On + Off)
			if ((!(GetType() & (MOD_TYPE_IT | MOD_TYPE_MPT))) || m_SongFlags[SONG_ITOLDEFFECTS])
			{
				n += 2;
				ontime++;
			}
			uint8 tremcount = chn.nTremorCount;
			if(!(GetType() & MOD_TYPE_XM))
			{
				if (tremcount >= n) tremcount = 0;
				if (tremcount >= ontime) vol = 0;
				chn.nTremorCount = tremcount + 1;
			} else
			{
				if(m_SongFlags[SONG_FIRSTTICK])
				{
					// tremcount is only 0 on the first tremor tick after triggering a note.
					if(tremcount > 0)
					{
						tremcount--;
					}
				} else
				{
					chn.nTremorCount = tremcount + 1;
				}
				if (tremcount % n >= ontime) vol = 0;
			}
		}
		chn.dwFlags.set(CHN_FASTVOLRAMP);
	}

#ifndef NO_PLUGINS
	// Plugin tremor
	if(chn.nCommand == CMD_TREMOR && chn.pModInstrument && chn.pModInstrument->nMixPlug
		&& !chn.pModInstrument->dwFlags[INS_MUTE]
		&& !chn.dwFlags[CHN_MUTE | CHN_SYNCMUTE]
		&& ModCommand::IsNote(chn.nLastNote))
	{
		const ModInstrument *pIns = chn.pModInstrument;
		IMixPlugin *pPlugin =  m_MixPlugins[pIns->nMixPlug - 1].pMixPlugin;
		if(pPlugin)
		{
			const bool isPlaying = pPlugin->IsNotePlaying(chn.nLastNote, nChn);
			if(vol == 0 && isPlaying)
				pPlugin->MidiCommand(*pIns, chn.nLastNote + NOTE_MAX_SPECIAL, 0, nChn);
			else if(vol != 0 && !isPlaying)
				pPlugin->MidiCommand(*pIns, chn.nLastNote, static_cast<uint16>(chn.nVolume), nChn);
		}
	}
#endif // NO_PLUGINS
}


bool CSoundFile::IsEnvelopeProcessed(const ModChannel &chn, EnvelopeType env) const
{
	if(chn.pModInstrument == nullptr)
	{
		return false;
	}
	const InstrumentEnvelope &insEnv = chn.pModInstrument->GetEnvelope(env);

	// IT Compatibility: S77/S79/S7B do not disable the envelope, they just pause the counter
	// Test cases: s77.it, EnvLoops.xm, PanSustainRelease.xm
	bool playIfPaused = m_playBehaviour[kITEnvelopePositionHandling] || m_playBehaviour[kFT2PanSustainRelease];
	return ((chn.GetEnvelope(env).flags[ENV_ENABLED] || (insEnv.dwFlags[ENV_ENABLED] && playIfPaused))
		&& !insEnv.empty());
}


void CSoundFile::ProcessVolumeEnvelope(ModChannel &chn, int &vol) const
{
	if(IsEnvelopeProcessed(chn, ENV_VOLUME))
	{
		const ModInstrument *pIns = chn.pModInstrument;

		if(m_playBehaviour[kITEnvelopePositionHandling] && chn.VolEnv.nEnvPosition == 0)
		{
			// If the envelope is disabled at the very same moment as it is triggered, we do not process anything.
			return;
		}
		const int envpos = chn.VolEnv.nEnvPosition - (m_playBehaviour[kITEnvelopePositionHandling] ? 1 : 0);
		// Get values in [0, 256]
		int envval = pIns->VolEnv.GetValueFromPosition(envpos, 256);

		// if we are in the release portion of the envelope,
		// rescale envelope factor so that it is proportional to the release point
		// and release envelope beginning.
		if(chn.VolEnv.nEnvValueAtReleaseJump != NOT_YET_RELEASED)
		{
			int envValueAtReleaseJump = chn.VolEnv.nEnvValueAtReleaseJump;
			int envValueAtReleaseNode = pIns->VolEnv[pIns->VolEnv.nReleaseNode].value * 4;

			//If we have just hit the release node, force the current env value
			//to be that of the release node. This works around the case where
			// we have another node at the same position as the release node.
			if(envpos == pIns->VolEnv[pIns->VolEnv.nReleaseNode].tick)
				envval = envValueAtReleaseNode;

			if(m_playBehaviour[kLegacyReleaseNode])
			{
				// Old, hard to grasp release node behaviour (additive)
				int relativeVolumeChange = (envval - envValueAtReleaseNode) * 2;
				envval = envValueAtReleaseJump + relativeVolumeChange;
			} else
			{
				// New behaviour, truly relative to release node
				if(envValueAtReleaseNode > 0)
					envval = envValueAtReleaseJump * envval / envValueAtReleaseNode;
				else
					envval = 0;
			}
		}
		vol = (vol * Clamp(envval, 0, 512)) / 256;
	}

}


void CSoundFile::ProcessPanningEnvelope(ModChannel &chn) const
{
	if(IsEnvelopeProcessed(chn, ENV_PANNING))
	{
		const ModInstrument *pIns = chn.pModInstrument;

		if(m_playBehaviour[kITEnvelopePositionHandling] && chn.PanEnv.nEnvPosition == 0)
		{
			// If the envelope is disabled at the very same moment as it is triggered, we do not process anything.
			return;
		}

		const int envpos = chn.PanEnv.nEnvPosition - (m_playBehaviour[kITEnvelopePositionHandling] ? 1 : 0);
		// Get values in [-32, 32]
		const int envval = pIns->PanEnv.GetValueFromPosition(envpos, 64) - 32;

		int pan = chn.nRealPan;
		if(pan >= 128)
		{
			pan += (envval * (256 - pan)) / 32;
		} else
		{
			pan += (envval * (pan)) / 32;
		}
		chn.nRealPan = Clamp(pan, 0, 256);

	}
}


int CSoundFile::ProcessPitchFilterEnvelope(ModChannel &chn, int &period) const
{
	if(IsEnvelopeProcessed(chn, ENV_PITCH))
	{
		const ModInstrument *pIns = chn.pModInstrument;

		if(m_playBehaviour[kITEnvelopePositionHandling] && chn.PitchEnv.nEnvPosition == 0)
		{
			// If the envelope is disabled at the very same moment as it is triggered, we do not process anything.
			return -1;
		}

		const int envpos = chn.PitchEnv.nEnvPosition - (m_playBehaviour[kITEnvelopePositionHandling] ? 1 : 0);
		// Get values in [-256, 256]
#ifdef MODPLUG_TRACKER
		const int32 range = ENVELOPE_MAX;
		const int32 amp = 512;
#else
		// TODO: AMS2 envelopes behave differently when linear slides are off - emulate with 15 * (-128...127) >> 6
		// Copy over vibrato behaviour for that?
		const int32 range = GetType() == MOD_TYPE_AMS ? uint8_max : ENVELOPE_MAX;
		int32 amp;
		switch(GetType())
		{
		case MOD_TYPE_AMS: amp = 64; break;
		case MOD_TYPE_MDL: amp = 192; break;
		default: amp = 512;
		}
#endif
		const int envval = pIns->PitchEnv.GetValueFromPosition(envpos, amp, range) - amp / 2;

		if(chn.PitchEnv.flags[ENV_FILTER])
		{
			// Filter Envelope: controls cutoff frequency
			return SetupChannelFilter(chn, !chn.dwFlags[CHN_FILTER], envval);
		} else
		{
			// Pitch Envelope
			if(GetType() == MOD_TYPE_MPT && chn.pModInstrument && chn.pModInstrument->pTuning)
			{
				if(chn.nFineTune != envval)
				{
					chn.nFineTune = envval;
					chn.m_CalculateFreq = true;
					//Preliminary tests indicated that this behavior
					//is very close to original(with 12TET) when finestep count
					//is 15.
				}
			} else //Original behavior
			{
				const bool useFreq = PeriodsAreFrequencies();
				const uint32 (&upTable)[256] = useFreq ? LinearSlideUpTable : LinearSlideDownTable;
				const uint32 (&downTable)[256] = useFreq ? LinearSlideDownTable : LinearSlideUpTable;

				int l = envval;
				if(l < 0)
				{
					l = -l;
					LimitMax(l, 255);
					period = Util::muldiv(period, downTable[l], 65536);
				} else
				{
					LimitMax(l, 255);
					period = Util::muldiv(period, upTable[l], 65536);
				}
			} //End: Original behavior.
		}
	}
	return -1;
}


void CSoundFile::IncrementEnvelopePosition(ModChannel &chn, EnvelopeType envType) const
{
	ModChannel::EnvInfo &chnEnv = chn.GetEnvelope(envType);

	if(chn.pModInstrument == nullptr || !chnEnv.flags[ENV_ENABLED])
	{
		return;
	}

	// Increase position
	uint32 position = chnEnv.nEnvPosition + (m_playBehaviour[kITEnvelopePositionHandling] ? 0 : 1);

	const InstrumentEnvelope &insEnv = chn.pModInstrument->GetEnvelope(envType);
	if(insEnv.empty())
	{
		return;
	}

	bool endReached = false;

	if(!m_playBehaviour[kITEnvelopePositionHandling])
	{
		// FT2-style envelope processing.
		if(insEnv.dwFlags[ENV_LOOP])
		{
			// Normal loop active
			uint32 end = insEnv[insEnv.nLoopEnd].tick;
			if(!(GetType() & (MOD_TYPE_XM | MOD_TYPE_MT2))) end++;

			// FT2 compatibility: If the sustain point is at the loop end and the sustain loop has been released, don't loop anymore.
			// Test case: EnvLoops.xm
			const bool escapeLoop = (insEnv.nLoopEnd == insEnv.nSustainEnd && insEnv.dwFlags[ENV_SUSTAIN] && chn.dwFlags[CHN_KEYOFF] && m_playBehaviour[kFT2EnvelopeEscape]);

			if(position == end && !escapeLoop)
			{
				position = insEnv[insEnv.nLoopStart].tick;
			}
		}

		if(insEnv.dwFlags[ENV_SUSTAIN] && !chn.dwFlags[CHN_KEYOFF])
		{
			// Envelope sustained
			if(position == insEnv[insEnv.nSustainEnd].tick + 1u)
			{
				position = insEnv[insEnv.nSustainStart].tick;
				// FT2 compatibility: If the panning envelope reaches its sustain point before key-off, it stays there forever.
				// Test case: PanSustainRelease.xm
				if(m_playBehaviour[kFT2PanSustainRelease] && envType == ENV_PANNING && !chn.dwFlags[CHN_KEYOFF])
				{
					chnEnv.flags.reset(ENV_ENABLED);
				}
			}
		} else
		{
			// Limit to last envelope point
			if(position > insEnv.back().tick)
			{
				// Env of envelope
				position = insEnv.back().tick;
				endReached = true;
			}
		}
	} else
	{
		// IT envelope processing.
		// Test case: EnvLoops.it
		uint32 start, end;

		// IT compatiblity: OpenMPT processes the key-off flag earlier than IT. Grab the flag from the previous tick instead.
		// Test case: EnvOffLength.it
		if(insEnv.dwFlags[ENV_SUSTAIN] && !chn.dwOldFlags[CHN_KEYOFF] && (chnEnv.nEnvValueAtReleaseJump == NOT_YET_RELEASED || m_playBehaviour[kReleaseNodePastSustainBug]))
		{
			// Envelope sustained
			start = insEnv[insEnv.nSustainStart].tick;
			end = insEnv[insEnv.nSustainEnd].tick + 1;
		} else if(insEnv.dwFlags[ENV_LOOP])
		{
			// Normal loop active
			start = insEnv[insEnv.nLoopStart].tick;
			end = insEnv[insEnv.nLoopEnd].tick + 1;
		} else
		{
			// Limit to last envelope point
			start = end = insEnv.back().tick;
			if(position > end)
			{
				// Env of envelope
				endReached = true;
			}
		}

		if(position >= end)
		{
			position = start;
		}
	}

	if(envType == ENV_VOLUME && endReached)
	{
		// Special handling for volume envelopes at end of envelope
		if((GetType() & (MOD_TYPE_IT | MOD_TYPE_MPT)) || (chn.dwFlags[CHN_KEYOFF] && GetType() != MOD_TYPE_MDL))
		{
			chn.dwFlags.set(CHN_NOTEFADE);
		}

		if(insEnv.back().value == 0 && (chn.nMasterChn > 0 || (GetType() & (MOD_TYPE_IT | MOD_TYPE_MPT))))
		{
			// Stop channel if the last envelope node is silent anyway.
			chn.dwFlags.set(CHN_NOTEFADE);
			chn.nFadeOutVol = 0;
			chn.nRealVolume = 0;
			chn.nCalcVolume = 0;
		}
	}

	chnEnv.nEnvPosition = position + (m_playBehaviour[kITEnvelopePositionHandling] ? 1 : 0);

}


void CSoundFile::IncrementEnvelopePositions(ModChannel &chn) const
{
	IncrementEnvelopePosition(chn, ENV_VOLUME);
	IncrementEnvelopePosition(chn, ENV_PANNING);
	IncrementEnvelopePosition(chn, ENV_PITCH);
}


void CSoundFile::ProcessInstrumentFade(ModChannel &chn, int &vol) const
{
	// FadeOut volume
	if(chn.dwFlags[CHN_NOTEFADE] && chn.pModInstrument != nullptr)
	{
		const ModInstrument *pIns = chn.pModInstrument;

		uint32 fadeout = pIns->nFadeOut;
		if (fadeout)
		{
			chn.nFadeOutVol -= fadeout * 2;
			if (chn.nFadeOutVol <= 0) chn.nFadeOutVol = 0;
			vol = (vol * chn.nFadeOutVol) / 65536;
		} else if (!chn.nFadeOutVol)
		{
			vol = 0;
		}
	}
}


void CSoundFile::ProcessPitchPanSeparation(ModChannel &chn) const
{
	const ModInstrument *pIns = chn.pModInstrument;

	if ((pIns->nPPS) && (chn.nNote != NOTE_NONE))
	{
		// with PPS = 16 / PPC = C-5, E-6 will pan hard right (and D#6 will not)
		int pandelta = (int)chn.nRealPan + (int)((int)(chn.nNote - pIns->nPPC - NOTE_MIN) * (int)pIns->nPPS) / 2;
		chn.nRealPan = Clamp(pandelta, 0, 256);
	}
}


void CSoundFile::ProcessPanbrello(ModChannel &chn) const
{
	int pdelta = chn.nPanbrelloOffset;
	if(chn.rowCommand.command == CMD_PANBRELLO)
	{
		uint32 panpos;
		// IT compatibility: IT has its own, more precise tables
		if(m_playBehaviour[kITVibratoTremoloPanbrello])
			panpos = chn.nPanbrelloPos;
		else
			panpos = ((chn.nPanbrelloPos + 0x10) >> 2);

		pdelta = GetVibratoDelta(chn.nPanbrelloType, panpos);

		// IT compatibility: Sample-and-hold style random panbrello (tremolo and vibrato don't use this mechanism in IT)
		// Test case: RandomWaveform.it
		if(m_playBehaviour[kITSampleAndHoldPanbrello] && chn.nPanbrelloType == 3)
		{
			if(chn.nPanbrelloPos == 0 || chn.nPanbrelloPos >= chn.nPanbrelloSpeed)
			{
				chn.nPanbrelloPos = 0;
				chn.nPanbrelloRandomMemory = static_cast<int8>(pdelta);
			}
			chn.nPanbrelloPos++;
			pdelta = chn.nPanbrelloRandomMemory;
		} else
		{
			chn.nPanbrelloPos += chn.nPanbrelloSpeed;
		}
		// IT compatibility: Panbrello effect is active until next note or panning command.
		// Test case: PanbrelloHold.it
		if(m_playBehaviour[kITPanbrelloHold])
		{
			chn.nPanbrelloOffset = static_cast<int8>(pdelta);
		}
	}
	if(pdelta)
	{
		pdelta = ((pdelta * (int)chn.nPanbrelloDepth) + 2) / 8;
		pdelta += chn.nRealPan;
		chn.nRealPan = Clamp(pdelta, 0, 256);
	}
}


void CSoundFile::ProcessArpeggio(CHANNELINDEX nChn, int &period, Tuning::NOTEINDEXTYPE &arpeggioSteps)
{
	ModChannel &chn = m_PlayState.Chn[nChn];

#ifndef NO_PLUGINS
	// Plugin arpeggio
	if(chn.pModInstrument && chn.pModInstrument->nMixPlug
		&& !chn.pModInstrument->dwFlags[INS_MUTE]
		&& !chn.dwFlags[CHN_MUTE | CHN_SYNCMUTE])
	{
		const ModInstrument *pIns = chn.pModInstrument;
		IMixPlugin *pPlugin =  m_MixPlugins[pIns->nMixPlug - 1].pMixPlugin;
		if(pPlugin)
		{
			uint8 step = 0;
			const bool arpOnRow = (chn.rowCommand.command == CMD_ARPEGGIO);
			const ModCommand::NOTE lastNote = ModCommand::IsNote(chn.nLastNote) ? pIns->NoteMap[chn.nLastNote - NOTE_MIN] : NOTE_NONE;
			if(arpOnRow)
			{
				switch(m_PlayState.m_nTickCount % 3)
				{
				case 1: step = chn.nArpeggio >> 4; break;
				case 2: step = chn.nArpeggio & 0x0F; break;
				}
				chn.nArpeggioBaseNote = lastNote;
			}

			// Trigger new note:
			// - If there's an arpeggio on this row and
			//   - the note to trigger is not the same as the previous arpeggio note or
			//   - a pattern note has just been triggered on this tick
			// - If there's no arpeggio
			//   - but an arpeggio note is still active and
			//   - there's no note stop or new note that would stop it anyway
			if((arpOnRow && chn.nArpeggioLastNote != chn.nArpeggioBaseNote + step && (!m_SongFlags[SONG_FIRSTTICK] || !chn.rowCommand.IsNote()))
				|| (!arpOnRow && chn.rowCommand.note == NOTE_NONE && chn.nArpeggioLastNote != NOTE_NONE))
				SendMIDINote(nChn, chn.nArpeggioBaseNote + step, static_cast<uint16>(chn.nVolume));
			// Stop note:
			// - If some arpeggio note is still registered or
			// - When starting an arpeggio on a row with no other note on it, stop some possibly still playing note.
			if(chn.nArpeggioLastNote != NOTE_NONE)
				SendMIDINote(nChn, chn.nArpeggioLastNote + NOTE_MAX_SPECIAL, 0);
			else if(arpOnRow && m_SongFlags[SONG_FIRSTTICK] && !chn.rowCommand.IsNote() && ModCommand::IsNote(lastNote))
				SendMIDINote(nChn, lastNote + NOTE_MAX_SPECIAL, 0);

			if(chn.rowCommand.command == CMD_ARPEGGIO)
				chn.nArpeggioLastNote = chn.nArpeggioBaseNote + step;
			else
				chn.nArpeggioLastNote = NOTE_NONE;
		}
	}
#endif // NO_PLUGINS

	if(chn.nCommand == CMD_ARPEGGIO)
	{
		if((GetType() & MOD_TYPE_MPT) && chn.pModInstrument && chn.pModInstrument->pTuning)
		{
			switch(m_PlayState.m_nTickCount % 3)
			{
			case 0: arpeggioSteps = 0; break;
			case 1: arpeggioSteps = chn.nArpeggio >> 4; break;
			case 2: arpeggioSteps = chn.nArpeggio & 0x0F; break;
			}
			chn.m_CalculateFreq = true;
			chn.m_ReCalculateFreqOnFirstTick = true;
		} else
		{
			if(GetType() == MOD_TYPE_MT2 && m_SongFlags[SONG_FIRSTTICK])
			{
				// MT2 resets any previous portamento when an arpeggio occurs.
				chn.nPeriod = period = GetPeriodFromNote(chn.nNote, chn.nFineTune, chn.nC5Speed);
			}

			if(m_playBehaviour[kITArpeggio])
			{
				//IT playback compatibility 01 & 02

				// Pattern delay restarts tick counting. Not quite correct yet!
				const uint32 tick = m_PlayState.m_nTickCount % (m_PlayState.m_nMusicSpeed + m_PlayState.m_nFrameDelay);
				if(chn.nArpeggio != 0)
				{
					uint32 arpRatio = 65536;
					switch(tick % 3)
					{
					case 1: arpRatio = LinearSlideUpTable[(chn.nArpeggio >> 4) * 16]; break;
					case 2: arpRatio = LinearSlideUpTable[(chn.nArpeggio & 0x0F) * 16]; break;
					}
					if(PeriodsAreFrequencies())
						period = Util::muldivr(period, arpRatio, 65536);
					else
						period = Util::muldivr(period, 65536, arpRatio);
				}
			} else if(m_playBehaviour[kFT2Arpeggio])
			{
				// FastTracker 2: Swedish tracker logic (TM) arpeggio
				if(!m_SongFlags[SONG_FIRSTTICK])
				{
					// Arpeggio is added on top of current note, but cannot do it the IT way because of
					// the behaviour in ArpeggioClamp.xm.
					// Test case: ArpSlide.xm
					auto note = GetNoteFromPeriod(period, chn.nFineTune, chn.nC5Speed);

					// The fact that arpeggio behaves in a totally fucked up way at 16 ticks/row or more is that the arpeggio offset LUT only has 16 entries in FT2.
					// At more than 16 ticks/row, FT2 reads into the vibrato table, which is placed right after the arpeggio table.
					// Test case: Arpeggio.xm
					int arpPos = m_PlayState.m_nMusicSpeed - (m_PlayState.m_nTickCount % m_PlayState.m_nMusicSpeed);
					if(arpPos > 16) arpPos = 2;
					else if(arpPos == 16) arpPos = 0;
					else arpPos %= 3;
					switch(arpPos)
					{
					case 1: note += (chn.nArpeggio >> 4); break;
					case 2: note += (chn.nArpeggio & 0x0F); break;
					}

					period = GetPeriodFromNote(note, chn.nFineTune, chn.nC5Speed);

					// FT2 compatibility: FT2 has a different note limit for Arpeggio.
					// Test case: ArpeggioClamp.xm
					if(note >= 108 + NOTE_MIN && arpPos != 0)
					{
						period = std::max<uint32>(period, GetPeriodFromNote(108 + NOTE_MIN, 0, chn.nC5Speed));
					}

				}
			}
			// Other trackers
			else
			{
				uint32 tick = m_PlayState.m_nTickCount;

				// TODO other likely formats for MOD case: MED, OKT, etc
				uint8 note = (GetType() != MOD_TYPE_MOD) ? chn.nNote : static_cast<uint8>(GetNoteFromPeriod(period, chn.nFineTune, chn.nC5Speed));
				if(GetType() & (MOD_TYPE_DBM | MOD_TYPE_DIGI))
					tick += 2;
				switch(tick % 3)
				{
				case 1: note += (chn.nArpeggio >> 4); break;
				case 2: note += (chn.nArpeggio & 0x0F); break;
				}
				if(note != chn.nNote || (GetType() & (MOD_TYPE_DBM | MOD_TYPE_DIGI | MOD_TYPE_STM)) || m_playBehaviour[KST3PortaAfterArpeggio])
				{
					if(m_SongFlags[SONG_PT_MODE])
					{
						// Weird arpeggio wrap-around in ProTracker.
						// Test case: ArpWraparound.mod, and the snare sound in "Jim is dead" by doh.
						if(note == NOTE_MIDDLEC + 24)
						{
							period = int32_max;
							return;
						} else if(note > NOTE_MIDDLEC + 24)
						{
							note -= 37;
						}
					}
					period = GetPeriodFromNote(note, chn.nFineTune, chn.nC5Speed);

					if(GetType() & (MOD_TYPE_DBM | MOD_TYPE_DIGI | MOD_TYPE_PSM | MOD_TYPE_STM))
					{
						// The arpeggio note offset remains effective after the end of the current row in ScreamTracker 2.
						// This fixes the flute lead in MORPH.STM by Skaven, pattern 27.
						// Note that ScreamTracker 2.24 handles arpeggio slightly differently: It only considers the lower
						// nibble, and switches to that note halfway through the row.
						chn.nPeriod = period;
					} else if(m_playBehaviour[KST3PortaAfterArpeggio])
					{
						chn.nArpeggioLastNote = note;
					}
				}
			}
		}
	}
}


void CSoundFile::ProcessVibrato(CHANNELINDEX nChn, int &period, Tuning::RATIOTYPE &vibratoFactor)
{
	ModChannel &chn = m_PlayState.Chn[nChn];

	if(chn.dwFlags[CHN_VIBRATO])
	{
		if(GetType() == MOD_TYPE_669)
		{
			if(chn.nVibratoPos % 2u)
			{
				period += chn.nVibratoDepth * 167;	// Already multiplied by 4, and it seems like the real factor here is 669... how original =)
			}
			chn.nVibratoPos++;
			return;
		}

		// IT compatibility: IT has its own, more precise tables and pre-increments the vibrato position
		if(m_playBehaviour[kITVibratoTremoloPanbrello])
			chn.nVibratoPos += 4 * chn.nVibratoSpeed;

		int vdelta = GetVibratoDelta(chn.nVibratoType, chn.nVibratoPos);

		if(GetType() == MOD_TYPE_MPT && chn.pModInstrument && chn.pModInstrument->pTuning)
		{
			//Hack implementation: Scaling vibratofactor to [0.95; 1.05]
			//using figure from above tables and vibratodepth parameter
			vibratoFactor += 0.05f * (vdelta * chn.nVibratoDepth) / (128.0f * 60.0f);
			chn.m_CalculateFreq = true;
			chn.m_ReCalculateFreqOnFirstTick = false;

			if(m_PlayState.m_nTickCount + 1 == m_PlayState.m_nMusicSpeed)
				chn.m_ReCalculateFreqOnFirstTick = true;
		} else
		{
			// Original behaviour
			if(m_SongFlags.test_all(SONG_FIRSTTICK | SONG_PT_MODE) || ((GetType() & (MOD_TYPE_DIGI | MOD_TYPE_DBM)) && m_SongFlags[SONG_FIRSTTICK]))
			{
				// ProTracker doesn't apply vibrato nor advance on the first tick.
				// Test case: VibratoReset.mod
				return;
			} else if((GetType() & MOD_TYPE_XM) && (chn.nVibratoType & 0x03) == 1)
			{
				// FT2 compatibility: Vibrato ramp down table is upside down.
				// Test case: VibratoWaveforms.xm
				vdelta = -vdelta;
			}

			uint32 vdepth;
			// IT compatibility: correct vibrato depth
			if(m_playBehaviour[kITVibratoTremoloPanbrello])
			{
				// Yes, vibrato goes backwards with old effects enabled!
				if(m_SongFlags[SONG_ITOLDEFFECTS])
				{
					// Test case: vibrato-oldfx.it
					vdepth = 5;
				} else
				{
					// Test case: vibrato.it
					vdepth = 6;
					vdelta = -vdelta;
				}
			} else
			{
				if(m_SongFlags[SONG_S3MOLDVIBRATO])
					vdepth = 5;
				else if(GetType() == MOD_TYPE_DTM)
					vdepth = 8;
				else if(GetType() & (MOD_TYPE_DBM | MOD_TYPE_MTM))
					vdepth = 7;
				else if((GetType() & (MOD_TYPE_IT | MOD_TYPE_MPT)) && !m_SongFlags[SONG_ITOLDEFFECTS])
					vdepth = 7;
				else
					vdepth = 6;

				// ST3 compatibility: Do not distinguish between vibrato types in effect memory
				// Test case: VibratoTypeChange.s3m
				if(m_playBehaviour[kST3VibratoMemory] && chn.rowCommand.command == CMD_FINEVIBRATO)
					vdepth += 2;
			}

			vdelta = (vdelta * (int)chn.nVibratoDepth) / (1 << vdepth);
#ifndef NO_PLUGINS
			int16 midiDelta = static_cast<int16>(-vdelta);	// Periods are upside down
#endif // NO_PLUGINS

			if (m_SongFlags[SONG_LINEARSLIDES] && GetType() != MOD_TYPE_XM)
			{
				int l = vdelta;
				if (l < 0)
				{
					l = -l;
					vdelta = Util::muldiv(period, GetLinearSlideUpTable(this, l / 4u), 65536) - period;
					if (l & 0x03) vdelta += Util::muldiv(period, GetFineLinearSlideUpTable(this, l & 0x03), 65536) - period;
				} else
				{
					vdelta = Util::muldiv(period, GetLinearSlideDownTable(this, l / 4u), 65536) - period;
					if (l & 0x03) vdelta += Util::muldiv(period, GetFineLinearSlideDownTable(this, l & 0x03), 65536) - period;
				}
			}
			period += vdelta;

			// Process MIDI vibrato for plugins:
#ifndef NO_PLUGINS
			IMixPlugin *plugin = GetChannelInstrumentPlugin(nChn);
			if(plugin != nullptr)
			{
				// If the Pitch Wheel Depth is configured correctly (so it's the same as the plugin's PWD),
				// MIDI vibrato will sound identical to vibrato with linear slides enabled.
				int8 pwd = 2;
				if(chn.pModInstrument != nullptr)
				{
					pwd = chn.pModInstrument->midiPWD;
				}
				plugin->MidiVibrato(midiDelta, pwd, nChn);
			}
#endif // NO_PLUGINS
		}

		// Advance vibrato position - IT updates on every tick, unless "old effects" are enabled (in this case it only updates on non-first ticks like other trackers)
		if(!m_SongFlags[SONG_FIRSTTICK] || ((GetType() & (MOD_TYPE_IT | MOD_TYPE_MPT)) && !(m_SongFlags[SONG_ITOLDEFFECTS])))
		{
			// IT compatibility: IT has its own, more precise tables and pre-increments the vibrato position
			if(!m_playBehaviour[kITVibratoTremoloPanbrello])
				chn.nVibratoPos += chn.nVibratoSpeed;
		}
	} else if(chn.dwOldFlags[CHN_VIBRATO])
	{
		// Stop MIDI vibrato for plugins:
#ifndef NO_PLUGINS
		IMixPlugin *plugin = GetChannelInstrumentPlugin(nChn);
		if(plugin != nullptr)
		{
			plugin->MidiVibrato(0, 0, nChn);
		}
#endif // NO_PLUGINS
	}
}


void CSoundFile::ProcessSampleAutoVibrato(ModChannel &chn, int &period, Tuning::RATIOTYPE &vibratoFactor, int &nPeriodFrac) const
{
	// Sample Auto-Vibrato
	if(chn.pModSample != nullptr && chn.pModSample->nVibDepth)
	{
		const ModSample *pSmp = chn.pModSample;
		const bool alternativeTuning = chn.pModInstrument && chn.pModInstrument->pTuning;

		// In IT linear slide mode, we use frequencies, otherwise we use periods, which are upside down.
		// In this context, the "up" tables refer to the tables that increase frequency, and the down tables are the ones that decrease frequency.
		const bool useFreq = PeriodsAreFrequencies();
		const uint32 (&upTable)[256] = useFreq ? LinearSlideUpTable : LinearSlideDownTable;
		const uint32 (&downTable)[256] = useFreq ? LinearSlideDownTable : LinearSlideUpTable;
		const uint32 (&fineUpTable)[16] = useFreq ? FineLinearSlideUpTable : FineLinearSlideDownTable;
		const uint32 (&fineDownTable)[16] = useFreq ? FineLinearSlideDownTable : FineLinearSlideUpTable;

		// IT compatibility: Autovibrato is so much different in IT that I just put this in a separate code block, to get rid of a dozen IsCompatibilityMode() calls.
		if(m_playBehaviour[kITVibratoTremoloPanbrello] && !alternativeTuning && GetType() != MOD_TYPE_MT2)
		{
			if(!pSmp->nVibRate)
				return;

			// Schism's autovibrato code

			/*
			X86 Assembler from ITTECH.TXT:
			1) Mov AX, [SomeVariableNameRelatingToVibrato]
			2) Add AL, Rate
			3) AdC AH, 0
			4) AH contains the depth of the vibrato as a fine-linear slide.
			5) Mov [SomeVariableNameRelatingToVibrato], AX  ; For the next cycle.
			*/
			const int vibpos = chn.nAutoVibPos & 0xFF;
			int adepth = chn.nAutoVibDepth; // (1)
			adepth += pSmp->nVibSweep; // (2 & 3)
			LimitMax(adepth, static_cast<int>(pSmp->nVibDepth * 256u));
			chn.nAutoVibDepth = adepth; // (5)
			adepth /= 256; // (4)

			chn.nAutoVibPos += pSmp->nVibRate;

			int vdelta;
			switch(pSmp->nVibType)
			{
			case VIB_RANDOM:
				vdelta = mpt::random<int, 7>(AccessPRNG()) - 0x40;
				break;
			case VIB_RAMP_DOWN:
				vdelta = 64 - (vibpos + 1) / 2;
				break;
			case VIB_RAMP_UP:
				vdelta = ((vibpos + 1) / 2) - 64;
				break;
			case VIB_SQUARE:
				vdelta = vibpos < 128 ? 64 : 0;
				break;
			case VIB_SINE:
			default:
				vdelta = ITSinusTable[vibpos];
				break;
			}

			vdelta = (vdelta * adepth) / 64;
			uint32 l = mpt::abs(vdelta);
			LimitMax(period, Util::MaxValueOfType(period) / 256);
			period *= 256;
			if(vdelta < 0)
			{
				vdelta = Util::muldiv(period, downTable[l / 4u], 0x10000) - period;
				if (l & 0x03)
				{
					vdelta += Util::muldiv(period, fineDownTable[l & 0x03], 0x10000) - period;
				}
			} else
			{
				vdelta = Util::muldiv(period, upTable[l / 4u], 0x10000) - period;
				if (l & 0x03)
				{
					vdelta += Util::muldiv(period, fineUpTable[l & 0x03], 0x10000) - period;
				}
			}
			period = (period + vdelta) / 256;
			nPeriodFrac = vdelta & 0xFF;
		} else
		{
			// MPT's autovibrato code
			if (pSmp->nVibSweep == 0 && !(GetType() & (MOD_TYPE_IT | MOD_TYPE_MPT)))
			{
				chn.nAutoVibDepth = pSmp->nVibDepth * 256;
			} else
			{
				// Calculate current autovibrato depth using vibsweep
				if (GetType() & (MOD_TYPE_IT | MOD_TYPE_MPT))
				{
					chn.nAutoVibDepth += pSmp->nVibSweep * 2u;
				} else
				{
					if(!chn.dwFlags[CHN_KEYOFF])
					{
						chn.nAutoVibDepth += (pSmp->nVibDepth * 256u) / pSmp->nVibSweep;
					}
				}
				LimitMax(chn.nAutoVibDepth, static_cast<int>(pSmp->nVibDepth * 256u));
			}
			chn.nAutoVibPos += pSmp->nVibRate;
			int vdelta;
			switch(pSmp->nVibType)
			{
			case VIB_RANDOM:
				vdelta = ModRandomTable[chn.nAutoVibPos & 0x3F];
				chn.nAutoVibPos++;
				break;
			case VIB_RAMP_DOWN:
				vdelta = ((0x40 - (chn.nAutoVibPos / 2u)) & 0x7F) - 0x40;
				break;
			case VIB_RAMP_UP:
				vdelta = ((0x40 + (chn.nAutoVibPos / 2u)) & 0x7F) - 0x40;
				break;
			case VIB_SQUARE:
				vdelta = (chn.nAutoVibPos & 128) ? +64 : -64;
				break;
			case VIB_SINE:
			default:
				if(GetType() != MOD_TYPE_MT2)
				{
					vdelta = ft2VibratoTable[chn.nAutoVibPos & 0xFF];
				} else
				{
					// Fix flat-sounding pads in "another worlds" by Eternal Engine.
					// Vibrato starts at the maximum amplitude of the sine wave
					// and the vibrato frequency never decreases below the original note's frequency.
					vdelta = (ft2VibratoTable[(chn.nAutoVibPos + 192) & 0xFF] + 64) / 2;
				}
			}
			int n = (vdelta * chn.nAutoVibDepth) / 256;

			if(alternativeTuning)
			{
				//Vib sweep is not taken into account here.
				vibratoFactor += 0.05F * pSmp->nVibDepth * vdelta / 4096.0f; //4096 == 64^2
				//See vibrato for explanation.
				chn.m_CalculateFreq = true;
				/*
				Finestep vibrato:
				const float autoVibDepth = pSmp->nVibDepth * val / 4096.0f; //4096 == 64^2
				vibratoFineSteps += static_cast<CTuning::FINESTEPTYPE>(chn.pModInstrument->pTuning->GetFineStepCount() *  autoVibDepth);
				chn.m_CalculateFreq = true;
				*/
			}
			else //Original behavior
			{
				if (GetType() != MOD_TYPE_XM)
				{
					int df1, df2;
					if (n < 0)
					{
						n = -n;
						uint32 n1 = n / 256;
						df1 = downTable[n1];
						df2 = downTable[n1+1];
					} else
					{
						uint32 n1 = n / 256;
						df1 = upTable[n1];
						df2 = upTable[n1+1];
					}
					n /= 4;
					period = Util::muldiv(period, df1 + ((df2 - df1) * (n & 0x3F) / 64), 256);
					nPeriodFrac = period & 0xFF;
					period /= 256;
				} else
				{
					period += (n / 64);
				}
			} //Original MPT behavior
		}
	}
}


void CSoundFile::ProcessRamping(ModChannel &chn) const
{
	chn.leftRamp = chn.rightRamp = 0;
	if(chn.dwFlags[CHN_VOLUMERAMP] && (chn.leftVol != chn.newLeftVol || chn.rightVol != chn.newRightVol))
	{
		const bool rampUp = (chn.newLeftVol > chn.leftVol) || (chn.newRightVol > chn.rightVol);
		int32 rampLength, globalRampLength, instrRampLength = 0;
		rampLength = globalRampLength = (rampUp ? m_MixerSettings.GetVolumeRampUpSamples() : m_MixerSettings.GetVolumeRampDownSamples());
		//XXXih: add real support for bidi ramping here

		if(m_playBehaviour[kFT2VolumeRamping] && (GetType() & MOD_TYPE_XM))
		{
			// apply FT2-style super-soft volume ramping (5ms), overriding openmpt settings
			rampLength = globalRampLength = Util::muldivr(5, m_MixerSettings.gdwMixingFreq, 1000);
		}

		if(chn.pModInstrument != nullptr && rampUp)
		{
			instrRampLength = chn.pModInstrument->nVolRampUp;
			rampLength = instrRampLength ? (m_MixerSettings.gdwMixingFreq * instrRampLength / 100000) : globalRampLength;
		}
		const bool enableCustomRamp = (instrRampLength > 0);

		if(!rampLength)
		{
			rampLength = 1;
		}

		int32 leftDelta = ((chn.newLeftVol - chn.leftVol) * (1 << VOLUMERAMPPRECISION));
		int32 rightDelta = ((chn.newRightVol - chn.rightVol) * (1 << VOLUMERAMPPRECISION));
		if(!enableCustomRamp)
		{
			// Extra-smooth ramping, unless we're forced to use the default values
			if((chn.leftVol | chn.rightVol) && (chn.newLeftVol | chn.newRightVol) && !chn.dwFlags[CHN_FASTVOLRAMP])
			{
				rampLength = m_PlayState.m_nBufferCount;
				Limit(rampLength, globalRampLength, int32(1 << (VOLUMERAMPPRECISION - 1)));
			}
		}

		chn.leftRamp = leftDelta / rampLength;
		chn.rightRamp = rightDelta / rampLength;
		chn.leftVol = chn.newLeftVol - ((chn.leftRamp * rampLength) / (1 << VOLUMERAMPPRECISION));
		chn.rightVol = chn.newRightVol - ((chn.rightRamp * rampLength) / (1 << VOLUMERAMPPRECISION));

		if (chn.leftRamp|chn.rightRamp)
		{
			chn.nRampLength = rampLength;
		} else
		{
			chn.dwFlags.reset(CHN_VOLUMERAMP);
			chn.leftVol = chn.newLeftVol;
			chn.rightVol = chn.newRightVol;
		}
	} else
	{
		chn.dwFlags.reset(CHN_VOLUMERAMP);
		chn.leftVol = chn.newLeftVol;
		chn.rightVol = chn.newRightVol;
	}
	chn.rampLeftVol = chn.leftVol * (1 << VOLUMERAMPPRECISION);
	chn.rampRightVol = chn.rightVol * (1 << VOLUMERAMPPRECISION);
	chn.dwFlags.reset(CHN_FASTVOLRAMP);
}


SamplePosition CSoundFile::GetChannelIncrement(const ModChannel &chn, uint32 period, int periodFrac) const
{
	uint32 freq;

	const ModInstrument *pIns = chn.pModInstrument;
	if(GetType() != MOD_TYPE_MPT || pIns == nullptr || pIns->pTuning == nullptr)
	{
		freq = GetFreqFromPeriod(period, chn.nC5Speed, periodFrac);
	} else
	{
		freq = chn.m_Freq;
	}

	// Applying Pitch/Tempo lock.
	if(pIns && pIns->pitchToTempoLock.GetRaw())
	{
		freq = Util::muldivr(freq, m_PlayState.m_nMusicTempo.GetRaw(), pIns->pitchToTempoLock.GetRaw());
	}

	// Avoid increment to overflow and become negative with unrealisticly high frequencies.
	LimitMax(freq, uint32(int32_max));
	return SamplePosition::Ratio(freq, m_MixerSettings.gdwMixingFreq << FREQ_FRACBITS);
}


////////////////////////////////////////////////////////////////////////////////////////////
// Handles envelopes & mixer setup

bool CSoundFile::ReadNote()
{
#ifdef MODPLUG_TRACKER
	// Checking end of row ?
	if(m_SongFlags[SONG_PAUSED])
	{
		m_PlayState.m_nTickCount = 0;
		if (!m_PlayState.m_nMusicSpeed) m_PlayState.m_nMusicSpeed = 6;
		if (!m_PlayState.m_nMusicTempo.GetRaw()) m_PlayState.m_nMusicTempo.Set(125);
	} else
#endif // MODPLUG_TRACKER
	{
		if(!ProcessRow())
			return false;
	}
	////////////////////////////////////////////////////////////////////////////////////
	if (m_PlayState.m_nMusicTempo.GetRaw() == 0) return false;

	m_PlayState.m_nSamplesPerTick = GetTickDuration(m_PlayState);
	m_PlayState.m_nBufferCount = m_PlayState.m_nSamplesPerTick;

	// Master Volume + Pre-Amplification / Attenuation setup
	uint32 nMasterVol;
	{
		CHANNELINDEX nchn32 = Clamp(m_nChannels, CHANNELINDEX(1), CHANNELINDEX(31));

		uint32 mastervol;

		if (m_PlayConfig.getUseGlobalPreAmp())
		{
			int realmastervol = m_MixerSettings.m_nPreAmp;
			if (realmastervol > 0x80)
			{
				//Attenuate global pre-amp depending on num channels
				realmastervol = 0x80 + ((realmastervol - 0x80) * (nchn32 + 4)) / 16;
			}
			mastervol = (realmastervol * (m_nSamplePreAmp)) / 64;
		} else
		{
			//Preferred option: don't use global pre-amp at all.
			mastervol = m_nSamplePreAmp;
		}

		if (m_PlayConfig.getUseGlobalPreAmp())
		{
			uint32 attenuation =
#ifndef NO_AGC
				(m_MixerSettings.DSPMask & SNDDSP_AGC) ? PreAmpAGCTable[nchn32 / 2u] :
#endif
				PreAmpTable[nchn32 / 2u];
			if(attenuation < 1) attenuation = 1;
			nMasterVol = (mastervol << 7) / attenuation;
		} else
		{
			nMasterVol = mastervol;
		}
	}

	////////////////////////////////////////////////////////////////////////////////////
	// Update channels data
	m_nMixChannels = 0;
	for (CHANNELINDEX nChn = 0; nChn < MAX_CHANNELS; nChn++)
	{
		ModChannel &chn = m_PlayState.Chn[nChn];
		// FT2 Compatibility: Prevent notes to be stopped after a fadeout. This way, a portamento effect can pick up a faded instrument which is long enough.
		// This occurs for example in the bassline (channel 11) of jt_burn.xm. I hope this won't break anything else...
		// I also suppose this could decrease mixing performance a bit, but hey, which CPU can't handle 32 muted channels these days... :-)
		if(chn.dwFlags[CHN_NOTEFADE] && (!(chn.nFadeOutVol|chn.leftVol|chn.rightVol)) && !m_playBehaviour[kFT2ProcessSilentChannels])
		{
			chn.nLength = 0;
			chn.nROfs = chn.nLOfs = 0;
		}
		// Check for unused channel
		if(chn.dwFlags[CHN_MUTE] || (nChn >= m_nChannels && !chn.nLength))
		{
			if(nChn < m_nChannels)
			{
				// Process MIDI macros on channels that are currently muted.
				ProcessMacroOnChannel(nChn);
			}
			chn.nLeftVU = chn.nRightVU = 0;
			continue;
		}
		// Reset channel data
		chn.increment = SamplePosition(0);
		chn.nRealVolume = 0;
		chn.nCalcVolume = 0;

		chn.nRampLength = 0;

		//Aux variables
		Tuning::RATIOTYPE vibratoFactor = 1;
		Tuning::NOTEINDEXTYPE arpeggioSteps = 0;

		const ModInstrument *pIns = chn.pModInstrument;

		// Calc Frequency
		int period;

		// Also process envelopes etc. when there's a plugin on this channel, for possible fake automation using volume and pan data.
		// We only care about master channels, though, since automation only "happens" on them.
		const bool samplePlaying = (chn.nPeriod && chn.nLength);
		const bool plugAssigned = (nChn < m_nChannels) && (ChnSettings[nChn].nMixPlugin || (chn.pModInstrument != nullptr && chn.pModInstrument->nMixPlug));
		if (samplePlaying || plugAssigned)
		{
			int vol = chn.nVolume;
			int insVol = chn.nInsVol;		// This is the "SV * IV" value in ITTECH.TXT

			ProcessVolumeSwing(chn, m_playBehaviour[kITSwingBehaviour] ? insVol : vol);
			ProcessPanningSwing(chn);
			ProcessTremolo(chn, vol);
			ProcessTremor(nChn, vol);

			// Clip volume and multiply (extend to 14 bits)
			Limit(vol, 0, 256);
			vol <<= 6;

			// Process Envelopes
			if (pIns)
			{
				if(m_playBehaviour[kITEnvelopePositionHandling])
				{
					// In IT compatible mode, envelope position indices are shifted by one for proper envelope pausing,
					// so we have to update the position before we actually process the envelopes.
					// When using MPT behaviour, we get the envelope position for the next tick while we are still calculating the current tick,
					// which then results in wrong position information when the envelope is paused on the next row.
					// Test cases: s77.it
					IncrementEnvelopePositions(chn);
				}
				ProcessVolumeEnvelope(chn, vol);
				ProcessInstrumentFade(chn, vol);
				ProcessPanningEnvelope(chn);
				ProcessPitchPanSeparation(chn);
			} else
			{
				// No Envelope: key off => note cut
				if(chn.dwFlags[CHN_NOTEFADE]) // 1.41-: CHN_KEYOFF|CHN_NOTEFADE
				{
					chn.nFadeOutVol = 0;
					vol = 0;
				}
			}
			// vol is 14-bits
			if (vol)
			{
				// IMPORTANT: chn.nRealVolume is 14 bits !!!
				// -> Util::muldiv( 14+8, 6+6, 18); => RealVolume: 14-bit result (22+12-20)

				if(chn.dwFlags[CHN_SYNCMUTE])
				{
					chn.nRealVolume = 0;
				} else if (m_PlayConfig.getGlobalVolumeAppliesToMaster())
				{
					// Don't let global volume affect level of sample if
					// Global volume is going to be applied to master output anyway.
					chn.nRealVolume = Util::muldiv(vol * MAX_GLOBAL_VOLUME, chn.nGlobalVol * insVol, 1 << 20);
				} else
				{
					chn.nRealVolume = Util::muldiv(vol * m_PlayState.m_nGlobalVolume, chn.nGlobalVol * insVol, 1 << 20);
				}
			}

			chn.nCalcVolume = vol;	// Update calculated volume for MIDI macros

			// ST3 only clamps the final output period, but never the channel's internal period.
			// Test case: PeriodLimit.s3m
			if (chn.nPeriod < m_nMinPeriod
				&& GetType() != MOD_TYPE_S3M
				&& !PeriodsAreFrequencies())
			{
				chn.nPeriod = m_nMinPeriod;
			}
			if(m_playBehaviour[kFT2Periods]) Clamp(chn.nPeriod, 1, 31999);
			period = chn.nPeriod;

			// When glissando mode is set to semitones, clamp to the next halftone.
			if((chn.dwFlags & (CHN_GLISSANDO | CHN_PORTAMENTO)) == (CHN_GLISSANDO | CHN_PORTAMENTO)
				&& (!m_SongFlags[SONG_PT_MODE] || (chn.rowCommand.IsPortamento() && !m_SongFlags[SONG_FIRSTTICK])))
			{
				if(period != chn.cachedPeriod)
				{
					// Only recompute this whole thing in case the base period has changed.
					chn.cachedPeriod = period;
					chn.glissandoPeriod = GetPeriodFromNote(GetNoteFromPeriod(period, chn.nFineTune, chn.nC5Speed), chn.nFineTune, chn.nC5Speed);
				}
				period = chn.glissandoPeriod;
			}

			ProcessArpeggio(nChn, period, arpeggioSteps);

			// Preserve Amiga freq limits.
			// In ST3, the frequency is always clamped to periods 113 to 856, while in ProTracker,
			// the limit is variable, depending on the finetune of the sample.
			// The int32_max test is for the arpeggio wrap-around in ProcessArpeggio().
			// Test case: AmigaLimits.s3m, AmigaLimitsFinetune.mod
			if(m_SongFlags[SONG_AMIGALIMITS | SONG_PT_MODE] && period != int32_max)
			{
				int limitLow = 113 * 4, limitHigh = 856 * 4;
				if(GetType() != MOD_TYPE_S3M)
				{
					const int tableOffset = XM2MODFineTune(chn.nFineTune) * 12;
					limitLow = ProTrackerTunedPeriods[tableOffset +  11] / 2;
					limitHigh = ProTrackerTunedPeriods[tableOffset] * 2;
					// Amiga cannot actually keep up with lower periods
					if(limitLow < 113 * 4) limitLow = 113 * 4;
				}
				Limit(period, limitLow, limitHigh);
				Limit(chn.nPeriod, limitLow, limitHigh);
			}

			ProcessPanbrello(chn);
		}

		// IT Compatibility: Ensure that there is no pan swing, panbrello, panning envelopes, etc. applied on surround channels.
		// Test case: surround-pan.it
		if(chn.dwFlags[CHN_SURROUND] && !m_SongFlags[SONG_SURROUNDPAN] && m_playBehaviour[kITNoSurroundPan])
		{
			chn.nRealPan = 128;
		}

		// Now that all relevant envelopes etc. have been processed, we can parse the MIDI macro data.
		ProcessMacroOnChannel(nChn);

		// After MIDI macros have been processed, we can also process the pitch / filter envelope and other pitch-related things.
		if(samplePlaying)
		{
			int cutoff = ProcessPitchFilterEnvelope(chn, period);
			if(cutoff >= 0 && chn.dwFlags[CHN_ADLIB] && m_opl)
			{
				// Cutoff doubles as modulator intensity for FM instruments
				m_opl->Volume(nChn, static_cast<uint8>(cutoff / 4), true);
			}
		}

		if(chn.rowCommand.volcmd == VOLCMD_VIBRATODEPTH &&
			(chn.rowCommand.command == CMD_VIBRATO || chn.rowCommand.command == CMD_VIBRATOVOL || chn.rowCommand.command == CMD_FINEVIBRATO))
		{
			if(GetType() == MOD_TYPE_XM)
			{
				// XM Compatibility: Vibrato should be advanced twice (but not added up) if both volume-column and effect column vibrato is present.
				// Effect column vibrato parameter has precedence if non-zero.
				// Test case: VibratoDouble.xm
				if(!m_SongFlags[SONG_FIRSTTICK])
					chn.nVibratoPos += chn.nVibratoSpeed;
			} else if(GetType() & (MOD_TYPE_IT | MOD_TYPE_MPT))
			{
				// IT Compatibility: Vibrato should be applied twice if both volume-colum and effect column vibrato is present.
				// Volume column vibrato parameter has precedence if non-zero.
				// Test case: VibratoDouble.it
				Vibrato(chn, chn.rowCommand.vol);
				ProcessVibrato(nChn, period, vibratoFactor);
			}
		}
		// Plugins may also receive vibrato
		ProcessVibrato(nChn, period, vibratoFactor);

		if(samplePlaying)
		{
			int nPeriodFrac = 0;
			ProcessSampleAutoVibrato(chn, period, vibratoFactor, nPeriodFrac);

			// Final Period
			// ST3 only clamps the final output period, but never the channel's internal period.
			// Test case: PeriodLimit.s3m
			if (period <= m_nMinPeriod)
			{
				if(m_playBehaviour[kST3LimitPeriod]) chn.nLength = 0;	// Pattern 15 in watcha.s3m
				period = m_nMinPeriod;
			}

			if((chn.dwFlags & (CHN_ADLIB | CHN_MUTE | CHN_SYNCMUTE)) == CHN_ADLIB && m_opl)
			{
				const bool doProcess = m_playBehaviour[kOPLFlexibleNoteOff] || !chn.dwFlags[CHN_NOTEFADE] || GetType() == MOD_TYPE_S3M;
				if(doProcess && !(GetType() == MOD_TYPE_S3M && chn.dwFlags[CHN_KEYOFF]))
				{
					// In ST3, a sample rate of 8363 Hz is mapped to middle-C, which is 261.625 Hz in a tempered scale at A4 = 440.
					// Hence, we have to translate our "sample rate" into pitch.
					const auto freq = GetFreqFromPeriod(period, chn.nC5Speed, nPeriodFrac);
					const auto oplmilliHertz = Util::muldivr_unsigned(freq, 261625, 8363 << FREQ_FRACBITS);
					const bool keyOff = chn.dwFlags[CHN_KEYOFF] || (chn.dwFlags[CHN_NOTEFADE] && chn.nFadeOutVol == 0);
					m_opl->Frequency(nChn, oplmilliHertz, keyOff, m_playBehaviour[kOPLBeatingOscillators]);
				}
				if(doProcess)
				{
					// Scale volume to OPL range (0...63).
					m_opl->Volume(nChn, static_cast<uint8>(Util::muldivr_unsigned(chn.nCalcVolume * chn.nGlobalVol * chn.nInsVol, 63, 1 << 26)), false);
					chn.nRealPan = m_opl->Pan(nChn, chn.nRealPan) * 128 + 128;
				}

				// Deallocate OPL channels for notes that are most definitely never going to play again.
				const auto *ins = chn.pModInstrument;
				if(ins != nullptr
					&& (ins->VolEnv.dwFlags & (ENV_ENABLED | ENV_LOOP | ENV_SUSTAIN)) == ENV_ENABLED
					&& !ins->VolEnv.empty()
					&& chn.GetEnvelope(ENV_VOLUME).nEnvPosition >= ins->VolEnv.back().tick
					&& ins->VolEnv.back().value == 0)
				{
					m_opl->NoteCut(nChn);
					chn.dwFlags.set(CHN_NOTEFADE);
					chn.nFadeOutVol = 0;
				}
			}

			if(GetType() == MOD_TYPE_MPT && pIns != nullptr && pIns->pTuning != nullptr)
			{
				// In this case: GetType() == MOD_TYPE_MPT and using custom tunings.
				if(chn.m_CalculateFreq || (chn.m_ReCalculateFreqOnFirstTick && m_PlayState.m_nTickCount == 0))
				{
					ModCommand::NOTE note = chn.nNote;
					if(!ModCommand::IsNote(note)) note = chn.nLastNote;
					if(m_playBehaviour[kITRealNoteMapping] && note >= NOTE_MIN && note <= NOTE_MAX)
						note = pIns->NoteMap[note - NOTE_MIN];
					chn.m_Freq = mpt::saturate_round<uint32>((chn.nC5Speed << FREQ_FRACBITS) * vibratoFactor * pIns->pTuning->GetRatio(note - NOTE_MIDDLEC + arpeggioSteps, chn.nFineTune+chn.m_PortamentoFineSteps));
					if(!chn.m_CalculateFreq)
						chn.m_ReCalculateFreqOnFirstTick = false;
					else
						chn.m_CalculateFreq = false;
				}
			}

			SamplePosition ninc = GetChannelIncrement(chn, period, nPeriodFrac);
#ifndef MODPLUG_TRACKER
			ninc.MulDiv(m_nFreqFactor, 65536);
#endif // !MODPLUG_TRACKER
			if(ninc.IsZero())
			{
				ninc.Set(0, 1);
			}
			chn.increment = ninc;
		}

		// Increment envelope positions
		if(pIns != nullptr && !m_playBehaviour[kITEnvelopePositionHandling])
		{
			// In IT and FT2 compatible mode, envelope positions are updated above.
			// Test cases: s77.it, EnvLoops.xm
			IncrementEnvelopePositions(chn);
		}

		// Volume ramping
		chn.dwFlags.set(CHN_VOLUMERAMP, (chn.nRealVolume | chn.rightVol | chn.leftVol) != 0);

		if (chn.nLeftVU > VUMETER_DECAY) chn.nLeftVU -= VUMETER_DECAY; else chn.nLeftVU = 0;
		if (chn.nRightVU > VUMETER_DECAY) chn.nRightVU -= VUMETER_DECAY; else chn.nRightVU = 0;

		chn.newLeftVol = chn.newRightVol = 0;
		chn.pCurrentSample = (chn.pModSample && chn.pModSample->HasSampleData() && chn.nLength && chn.IsSamplePlaying()) ? chn.pModSample->samplev() : nullptr;
		if (chn.pCurrentSample || (chn.HasMIDIOutput() && !chn.dwFlags[CHN_KEYOFF | CHN_NOTEFADE]))
		{
			// Update VU-Meter (nRealVolume is 14-bit)
			uint32 vul = (chn.nRealVolume * chn.nRealPan) / (1 << 14);
			if (vul > 127) vul = 127;
			if (chn.nLeftVU > 127) chn.nLeftVU = (uint8)vul;
			vul /= 2;
			if (chn.nLeftVU < vul) chn.nLeftVU = (uint8)vul;
			uint32 vur = (chn.nRealVolume * (256-chn.nRealPan)) / (1 << 14);
			if (vur > 127) vur = 127;
			if (chn.nRightVU > 127) chn.nRightVU = (uint8)vur;
			vur /= 2;
			if (chn.nRightVU < vur) chn.nRightVU = (uint8)vur;
		} else
		{
			// Note change but no sample
			if (chn.nLeftVU > 128) chn.nLeftVU = 0;
			if (chn.nRightVU > 128) chn.nRightVU = 0;
		}

		if (chn.pCurrentSample)
		{
#ifdef MODPLUG_TRACKER
			const uint32 kChnMasterVol = chn.dwFlags[CHN_EXTRALOUD] ? (uint32)m_PlayConfig.getNormalSamplePreAmp() : nMasterVol;
#else
			const uint32 kChnMasterVol = nMasterVol;
#endif // MODPLUG_TRACKER

			// Adjusting volumes
			if (m_MixerSettings.gnChannels >= 2)
			{
				int32 pan = chn.nRealPan;
				Limit(pan, 0, 256);

				int32 realvol;
				if (m_PlayConfig.getUseGlobalPreAmp())
				{
					realvol = (chn.nRealVolume * kChnMasterVol) / 128;
				} else
				{
					// Extra attenuation required here if we're bypassing pre-amp.
					realvol = (chn.nRealVolume * kChnMasterVol) / 256;
				}

				const ForcePanningMode panningMode = m_PlayConfig.getForcePanningMode();
				if(panningMode == forceSoftPanning || (panningMode == dontForcePanningMode && (m_MixerSettings.MixerFlags & SNDMIX_SOFTPANNING)))
				{
					if (pan < 128)
					{
						chn.newLeftVol = (realvol * 128) / 256;
						chn.newRightVol = (realvol * pan) / 256;
					} else
					{
						chn.newLeftVol = (realvol * (256 - pan)) / 256;
						chn.newRightVol = (realvol * 128) / 256;
					}
				} else if(panningMode == forceFT2Panning)
				{
					// FT2 uses square root panning. There is a 257-entry LUT for this,
					// but FT2's internal panning ranges from 0 to 255 only, meaning that
					// you can never truly achieve 100% right panning in FT2, only 100% left.
					// Test case: FT2PanLaw.xm
					LimitMax(pan, 255);
					const int panL = pan > 0 ? XMPanningTable[256 - pan] : 65536;
					const int panR = XMPanningTable[pan];
					chn.newLeftVol = (realvol * panL) / 65536;
					chn.newRightVol = (realvol * panR) / 65536;
				} else
				{
					chn.newLeftVol = (realvol * (256 - pan)) / 256;
					chn.newRightVol = (realvol * pan) / 256;
				}

			} else
			{
				chn.newLeftVol = (chn.nRealVolume * kChnMasterVol) / 256;
				chn.newRightVol = chn.newLeftVol;
			}
			// Clipping volumes
			//if (chn.nNewRightVol > 0xFFFF) chn.nNewRightVol = 0xFFFF;
			//if (chn.nNewLeftVol > 0xFFFF) chn.nNewLeftVol = 0xFFFF;

			if(chn.pModInstrument && Resampling::IsKnownMode(chn.pModInstrument->nResampling))
			{
				// For defined resampling modes, use per-instrument resampling mode if set
				chn.resamplingMode = static_cast<uint8>(chn.pModInstrument->nResampling);
			} else if(Resampling::IsKnownMode(m_nResampling))
			{
				chn.resamplingMode = static_cast<uint8>(m_nResampling);
			} else if(m_SongFlags[SONG_ISAMIGA] && m_Resampler.m_Settings.emulateAmiga)
			{
				// Enforce Amiga resampler for Amiga modules
				chn.resamplingMode = SRCMODE_AMIGA;
			} else
			{
				// Default to global mixer settings
				chn.resamplingMode = static_cast<uint8>(m_Resampler.m_Settings.SrcMode);
			}

			if(chn.increment.IsUnity() && !(chn.dwFlags[CHN_VIBRATO] || chn.nAutoVibDepth || chn.resamplingMode == SRCMODE_AMIGA))
			{
				// Exact sample rate match, do not interpolate at all
				// - unless vibrato is applied, because in this case the constant enabling and disabling
				// of resampling can introduce clicks (this is easily observable with a sine sample
				// played at the mix rate).
				chn.resamplingMode = SRCMODE_NEAREST;
			}

			const int extraAttenuation = m_PlayConfig.getExtraSampleAttenuation();
			chn.newLeftVol /= (1 << extraAttenuation);
			chn.newRightVol /= (1 << extraAttenuation);

			// Dolby Pro-Logic Surround
			if(chn.dwFlags[CHN_SURROUND] && m_MixerSettings.gnChannels == 2) chn.newRightVol = - chn.newRightVol;

			// Checking Ping-Pong Loops
			if(chn.dwFlags[CHN_PINGPONGFLAG]) chn.increment.Negate();

			// Setting up volume ramp
			ProcessRamping(chn);

			// Adding the channel in the channel list
			if(!chn.dwFlags[CHN_ADLIB])
			{
				m_PlayState.ChnMix[m_nMixChannels++] = nChn;
			}
		} else
		{
			chn.rightVol = chn.leftVol = 0;
			chn.nLength = 0;
		}

		chn.dwOldFlags = chn.dwFlags;
	}

	// If there are more channels being mixed than allowed, order them by volume and discard the most quiet ones
	if(m_nMixChannels >= m_MixerSettings.m_nMaxMixChannels)
	{
		std::partial_sort(std::begin(m_PlayState.ChnMix), std::begin(m_PlayState.ChnMix) + m_MixerSettings.m_nMaxMixChannels, std::begin(m_PlayState.ChnMix) + m_nMixChannels,
			[this](CHANNELINDEX i, CHANNELINDEX j) { return (m_PlayState.Chn[i].nRealVolume > m_PlayState.Chn[j].nRealVolume); });
	}
	return true;
}


void CSoundFile::ProcessMacroOnChannel(CHANNELINDEX nChn)
{
	ModChannel &chn = m_PlayState.Chn[nChn];
	if(nChn < GetNumChannels())
	{
		// TODO evaluate per-plugin macros here
		//ProcessMIDIMacro(nChn, false, m_MidiCfg.szMidiGlb[MIDIOUT_PAN]);
		//ProcessMIDIMacro(nChn, false, m_MidiCfg.szMidiGlb[MIDIOUT_VOLUME]);

		if((chn.rowCommand.command == CMD_MIDI && m_SongFlags[SONG_FIRSTTICK]) || chn.rowCommand.command == CMD_SMOOTHMIDI)
		{
			if(chn.rowCommand.param < 0x80)
				ProcessMIDIMacro(nChn, (chn.rowCommand.command == CMD_SMOOTHMIDI), m_MidiCfg.szMidiSFXExt[chn.nActiveMacro], chn.rowCommand.param);
			else
				ProcessMIDIMacro(nChn, (chn.rowCommand.command == CMD_SMOOTHMIDI), m_MidiCfg.szMidiZXXExt[(chn.rowCommand.param & 0x7F)], 0);
		}
	}
}


#ifndef NO_PLUGINS

void CSoundFile::ProcessMidiOut(CHANNELINDEX nChn)
{
	ModChannel &chn = m_PlayState.Chn[nChn];

	// Do we need to process MIDI?
	// For now there is no difference between mute and sync mute with VSTis.
	if(chn.dwFlags[CHN_MUTE | CHN_SYNCMUTE] || !chn.HasMIDIOutput()) return;

	// Get instrument info and plugin reference
	const ModInstrument *pIns = chn.pModInstrument;	// Can't be nullptr at this point, as we have valid MIDI output.

	// No instrument or muted instrument?
	if(pIns->dwFlags[INS_MUTE])
	{
		return;
	}

	// Check instrument plugins
	const PLUGINDEX nPlugin = GetBestPlugin(nChn, PrioritiseInstrument, RespectMutes);
	IMixPlugin *pPlugin = nullptr;
	if(nPlugin > 0 && nPlugin <= MAX_MIXPLUGINS)
	{
		pPlugin = m_MixPlugins[nPlugin - 1].pMixPlugin;
	}

	// Couldn't find a valid plugin
	if(pPlugin == nullptr) return;

	const ModCommand::NOTE note = chn.rowCommand.note;
	// Check for volume commands
	uint8 vol = 0xFF;
	if(chn.rowCommand.volcmd == VOLCMD_VOLUME)
	{
		vol = std::min(chn.rowCommand.vol, uint8(64));
	} else if(chn.rowCommand.command == CMD_VOLUME)
	{
		vol = std::min(chn.rowCommand.param, uint8(64));
	}
	const bool hasVolCommand = (vol != 0xFF);

	if(m_playBehaviour[kMIDICCBugEmulation])
	{
		if(note != NOTE_NONE)
		{
			ModCommand::NOTE realNote = note;
			if(ModCommand::IsNote(note))
				realNote = pIns->NoteMap[note - NOTE_MIN];
			SendMIDINote(nChn, realNote, static_cast<uint16>(chn.nVolume));
		} else if(hasVolCommand)
		{
			pPlugin->MidiCC(MIDIEvents::MIDICC_Volume_Fine, vol, nChn);
		}
		return;
	}

	const uint32 defaultVolume = pIns->nGlobalVol;

	//If new note, determine notevelocity to use.
	if(note != NOTE_NONE)
	{
		int32 velocity = static_cast<int32>(4 * defaultVolume);
		switch(pIns->nPluginVelocityHandling)
		{
			case PLUGIN_VELOCITYHANDLING_CHANNEL:
				velocity = chn.nVolume;
			break;
		}

		int32 swing = chn.nVolSwing;
		if(m_playBehaviour[kITSwingBehaviour]) swing *= 4;
		velocity += swing;
		Limit(velocity, 0, 256);

		ModCommand::NOTE realNote = note;
		if(ModCommand::IsNote(note))
			realNote = pIns->NoteMap[note - NOTE_MIN];
		// Experimental VST panning
		//ProcessMIDIMacro(nChn, false, m_MidiCfg.szMidiGlb[MIDIOUT_PAN], 0, nPlugin);
		SendMIDINote(nChn, realNote, static_cast<uint16>(velocity));
	}


	const bool processVolumeAlsoOnNote = (pIns->nPluginVelocityHandling == PLUGIN_VELOCITYHANDLING_VOLUME);

	if((hasVolCommand && !note) || (note && processVolumeAlsoOnNote))
	{
		switch(pIns->nPluginVolumeHandling)
		{
			case PLUGIN_VOLUMEHANDLING_DRYWET:
				if(hasVolCommand) pPlugin->SetDryRatio(2 * vol);
				else pPlugin->SetDryRatio(2 * defaultVolume);
				break;

			case PLUGIN_VOLUMEHANDLING_MIDI:
				if(hasVolCommand) pPlugin->MidiCC(MIDIEvents::MIDICC_Volume_Coarse, std::min<uint8>(127u, 2u * vol), nChn);
				else pPlugin->MidiCC(MIDIEvents::MIDICC_Volume_Coarse, static_cast<uint8>(std::min<uint32>(127u, 2u * defaultVolume)), nChn);
				break;

		}
	}
}

#endif // NO_PLUGINS


template<int channels>
MPT_FORCEINLINE void ApplyGlobalVolumeWithRamping(int32 *SoundBuffer, int32 *RearBuffer, int32 lCount, int32 m_nGlobalVolume, int32 step, int32 &m_nSamplesToGlobalVolRampDest, int32 &m_lHighResRampingGlobalVolume)
{
	const bool isStereo = (channels >= 2);
	const bool hasRear = (channels >= 4);
	for(int pos = 0; pos < lCount; ++pos)
	{
		if(m_nSamplesToGlobalVolRampDest > 0)
		{
			// Ramping required
			m_lHighResRampingGlobalVolume += step;
			                          SoundBuffer[0] = Util::muldiv(SoundBuffer[0], m_lHighResRampingGlobalVolume, MAX_GLOBAL_VOLUME << VOLUMERAMPPRECISION);
			MPT_CONSTANT_IF(isStereo) SoundBuffer[1] = Util::muldiv(SoundBuffer[1], m_lHighResRampingGlobalVolume, MAX_GLOBAL_VOLUME << VOLUMERAMPPRECISION);
			MPT_CONSTANT_IF(hasRear)  RearBuffer[0]  = Util::muldiv(RearBuffer[0] , m_lHighResRampingGlobalVolume, MAX_GLOBAL_VOLUME << VOLUMERAMPPRECISION); else MPT_UNUSED_VARIABLE(RearBuffer);
			MPT_CONSTANT_IF(hasRear)  RearBuffer[1]  = Util::muldiv(RearBuffer[1] , m_lHighResRampingGlobalVolume, MAX_GLOBAL_VOLUME << VOLUMERAMPPRECISION); else MPT_UNUSED_VARIABLE(RearBuffer);
			m_nSamplesToGlobalVolRampDest--;
		} else
		{
			                          SoundBuffer[0] = Util::muldiv(SoundBuffer[0], m_nGlobalVolume, MAX_GLOBAL_VOLUME);
			MPT_CONSTANT_IF(isStereo) SoundBuffer[1] = Util::muldiv(SoundBuffer[1], m_nGlobalVolume, MAX_GLOBAL_VOLUME);
			MPT_CONSTANT_IF(hasRear)  RearBuffer[0]  = Util::muldiv(RearBuffer[0] , m_nGlobalVolume, MAX_GLOBAL_VOLUME); else MPT_UNUSED_VARIABLE(RearBuffer);
			MPT_CONSTANT_IF(hasRear)  RearBuffer[1]  = Util::muldiv(RearBuffer[1] , m_nGlobalVolume, MAX_GLOBAL_VOLUME); else MPT_UNUSED_VARIABLE(RearBuffer);
			m_lHighResRampingGlobalVolume = m_nGlobalVolume << VOLUMERAMPPRECISION;
		}
		SoundBuffer += isStereo ? 2 : 1;
		MPT_CONSTANT_IF(hasRear) RearBuffer += 2;
	}
}


void CSoundFile::ProcessGlobalVolume(long lCount)
{

	// should we ramp?
	if(IsGlobalVolumeUnset())
	{
		// do not ramp if no global volume was set before (which is the case at song start), to prevent audible glitches when default volume is > 0 and it is set to 0 in the first row
		m_PlayState.m_nGlobalVolumeDestination = m_PlayState.m_nGlobalVolume;
		m_PlayState.m_nSamplesToGlobalVolRampDest = 0;
		m_PlayState.m_nGlobalVolumeRampAmount = 0;
	} else if(m_PlayState.m_nGlobalVolumeDestination != m_PlayState.m_nGlobalVolume)
	{
		// User has provided new global volume

		// m_nGlobalVolume: the last global volume which got set e.g. by a pattern command
		// m_nGlobalVolumeDestination: the current target of the ramping algorithm
		const bool rampUp = m_PlayState.m_nGlobalVolume > m_PlayState.m_nGlobalVolumeDestination;

		m_PlayState.m_nGlobalVolumeDestination = m_PlayState.m_nGlobalVolume;
		m_PlayState.m_nSamplesToGlobalVolRampDest = m_PlayState.m_nGlobalVolumeRampAmount = rampUp ? m_MixerSettings.GetVolumeRampUpSamples() : m_MixerSettings.GetVolumeRampDownSamples();
	}

	// calculate ramping step
	int32 step = 0;
	if (m_PlayState.m_nSamplesToGlobalVolRampDest > 0)
	{

		// Still some ramping left to do.
		int32 highResGlobalVolumeDestination = static_cast<int32>(m_PlayState.m_nGlobalVolumeDestination) << VOLUMERAMPPRECISION;

		const long delta = highResGlobalVolumeDestination - m_PlayState.m_lHighResRampingGlobalVolume;
		step = delta / static_cast<long>(m_PlayState.m_nSamplesToGlobalVolRampDest);

		if(m_nMixLevels == mixLevels1_17RC2)
		{
			// Define max step size as some factor of user defined ramping value: the lower the value, the more likely the click.
			// If step is too big (might cause click), extend ramp length.
			// Warning: This increases the volume ramp length by EXTREME amounts (factors of 100 are easily reachable)
			// compared to the user-defined setting, so this really should not be used!
			int32 maxStep = std::max<int>(50, (10000 / (m_PlayState.m_nGlobalVolumeRampAmount + 1)));
			while(mpt::abs(step) > maxStep)
			{
				m_PlayState.m_nSamplesToGlobalVolRampDest += m_PlayState.m_nGlobalVolumeRampAmount;
				step = delta / static_cast<int32>(m_PlayState.m_nSamplesToGlobalVolRampDest);
			}
		}
	}

	// apply volume and ramping
	if(m_MixerSettings.gnChannels == 1)
	{
		ApplyGlobalVolumeWithRamping<1>(MixSoundBuffer, MixRearBuffer, lCount, m_PlayState.m_nGlobalVolume, step, m_PlayState.m_nSamplesToGlobalVolRampDest, m_PlayState.m_lHighResRampingGlobalVolume);
	} else if(m_MixerSettings.gnChannels == 2)
	{
		ApplyGlobalVolumeWithRamping<2>(MixSoundBuffer, MixRearBuffer, lCount, m_PlayState.m_nGlobalVolume, step, m_PlayState.m_nSamplesToGlobalVolRampDest, m_PlayState.m_lHighResRampingGlobalVolume);
	} else if(m_MixerSettings.gnChannels == 4)
	{
		ApplyGlobalVolumeWithRamping<4>(MixSoundBuffer, MixRearBuffer, lCount, m_PlayState.m_nGlobalVolume, step, m_PlayState.m_nSamplesToGlobalVolRampDest, m_PlayState.m_lHighResRampingGlobalVolume);
	}

}


void CSoundFile::ProcessStereoSeparation(long countChunk)
{
	ApplyStereoSeparation(MixSoundBuffer, MixRearBuffer, m_MixerSettings.gnChannels, countChunk, m_MixerSettings.m_nStereoSeparation);
}


OPENMPT_NAMESPACE_END
