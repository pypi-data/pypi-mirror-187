/* table.c - EMU68 generated code by
 * gen68 2009-06-12 07:20:25
 * Copyright (C) 1998-2009 Benjamin Gerard
 *
 * $Id: table.c 117 2009-06-29 02:24:08Z benjihan $
 */

/* Line 10: d[reg0] */

#include "../struct68.h"

#ifndef EMU68_MONOLITIC
EMU68_EXTERN linefunc68_t
  line000,line001,line002,line003,line004,line005,line006,line007,
  line008,line009,line00A,line00B,line00C,line00D,line00E,line00F,
  line010,line011,line012,line013,line014,line015,line016,line017,
  line018,line019,line01A,line01B,line01C,line01D,line01E,line01F,
  line020,line021,line022,line023,line024,line025,line026,line027,
  line028,line029,line02A,line02B,line02C,line02D,line02E,line02F,
  line030,line031,line032,line033,line034,line035,line036,line037,
  line038,line039,line03A,line03B,line03C,line03D,line03E,line03F,
  line100,line101,line102,line103,line104,line105,line106,line107,
  line108,line109,line10A,line10B,line10C,line10D,line10E,line10F,
  line110,line111,line112,line113,line114,line115,line116,line117,
  line118,line119,line11A,line11B,line11C,line11D,line11E,line11F,
  line120,line121,line122,line123,line124,line125,line126,line127,
  line128,line129,line12A,line12B,line12C,line12D,line12E,line12F,
  line130,line131,line132,line133,line134,line135,line136,line137,
  line138,line139,line13A,line13B,line13C,line13D,line13E,line13F,
  line200,line201,line202,line203,line204,line205,line206,line207,
  line208,line209,line20A,line20B,line20C,line20D,line20E,line20F,
  line210,line211,line212,line213,line214,line215,line216,line217,
  line218,line219,line21A,line21B,line21C,line21D,line21E,line21F,
  line220,line221,line222,line223,line224,line225,line226,line227,
  line228,line229,line22A,line22B,line22C,line22D,line22E,line22F,
  line230,line231,line232,line233,line234,line235,line236,line237,
  line238,line239,line23A,line23B,line23C,line23D,line23E,line23F,
  line300,line301,line302,line303,line304,line305,line306,line307,
  line308,line309,line30A,line30B,line30C,line30D,line30E,line30F,
  line310,line311,line312,line313,line314,line315,line316,line317,
  line318,line319,line31A,line31B,line31C,line31D,line31E,line31F,
  line320,line321,line322,line323,line324,line325,line326,line327,
  line328,line329,line32A,line32B,line32C,line32D,line32E,line32F,
  line330,line331,line332,line333,line334,line335,line336,line337,
  line338,line339,line33A,line33B,line33C,line33D,line33E,line33F,
  line400,line401,line402,line403,line404,line405,line406,line407,
  line408,line409,line40A,line40B,line40C,line40D,line40E,line40F,
  line410,line411,line412,line413,line414,line415,line416,line417,
  line418,line419,line41A,line41B,line41C,line41D,line41E,line41F,
  line420,line421,line422,line423,line424,line425,line426,line427,
  line428,line429,line42A,line42B,line42C,line42D,line42E,line42F,
  line430,line431,line432,line433,line434,line435,line436,line437,
  line438,line439,line43A,line43B,line43C,line43D,line43E,line43F,
  line500,line501,line502,line503,line504,line505,line506,line507,
  line508,line509,line50A,line50B,line50C,line50D,line50E,line50F,
  line510,line511,line512,line513,line514,line515,line516,line517,
  line518,line519,line51A,line51B,line51C,line51D,line51E,line51F,
  line520,line521,line522,line523,line524,line525,line526,line527,
  line528,line529,line52A,line52B,line52C,line52D,line52E,line52F,
  line530,line531,line532,line533,line534,line535,line536,line537,
  line538,line539,line53A,line53B,line53C,line53D,line53E,line53F,
  line600,line601,line602,line603,line604,line605,line606,line607,
  line608,line609,line60A,line60B,line60C,line60D,line60E,line60F,
  line610,line611,line612,line613,line614,line615,line616,line617,
  line618,line619,line61A,line61B,line61C,line61D,line61E,line61F,
  line620,line621,line622,line623,line624,line625,line626,line627,
  line628,line629,line62A,line62B,line62C,line62D,line62E,line62F,
  line630,line631,line632,line633,line634,line635,line636,line637,
  line638,line639,line63A,line63B,line63C,line63D,line63E,line63F,
  line700,line701,line702,line703,line704,line705,line706,line707,
  line708,line709,line70A,line70B,line70C,line70D,line70E,line70F,
  line710,line711,line712,line713,line714,line715,line716,line717,
  line718,line719,line71A,line71B,line71C,line71D,line71E,line71F,
  line720,line721,line722,line723,line724,line725,line726,line727,
  line728,line729,line72A,line72B,line72C,line72D,line72E,line72F,
  line730,line731,line732,line733,line734,line735,line736,line737,
  line738,line739,line73A,line73B,line73C,line73D,line73E,line73F,
  line800,line801,line802,line803,line804,line805,line806,line807,
  line808,line809,line80A,line80B,line80C,line80D,line80E,line80F,
  line810,line811,line812,line813,line814,line815,line816,line817,
  line818,line819,line81A,line81B,line81C,line81D,line81E,line81F,
  line820,line821,line822,line823,line824,line825,line826,line827,
  line828,line829,line82A,line82B,line82C,line82D,line82E,line82F,
  line830,line831,line832,line833,line834,line835,line836,line837,
  line838,line839,line83A,line83B,line83C,line83D,line83E,line83F,
  line900,line901,line902,line903,line904,line905,line906,line907,
  line908,line909,line90A,line90B,line90C,line90D,line90E,line90F,
  line910,line911,line912,line913,line914,line915,line916,line917,
  line918,line919,line91A,line91B,line91C,line91D,line91E,line91F,
  line920,line921,line922,line923,line924,line925,line926,line927,
  line928,line929,line92A,line92B,line92C,line92D,line92E,line92F,
  line930,line931,line932,line933,line934,line935,line936,line937,
  line938,line939,line93A,line93B,line93C,line93D,line93E,line93F,
  lineA00,lineA01,lineA02,lineA03,lineA04,lineA05,lineA06,lineA07,
  lineA08,lineA09,lineA0A,lineA0B,lineA0C,lineA0D,lineA0E,lineA0F,
  lineA10,lineA11,lineA12,lineA13,lineA14,lineA15,lineA16,lineA17,
  lineA18,lineA19,lineA1A,lineA1B,lineA1C,lineA1D,lineA1E,lineA1F,
  lineA20,lineA21,lineA22,lineA23,lineA24,lineA25,lineA26,lineA27,
  lineA28,lineA29,lineA2A,lineA2B,lineA2C,lineA2D,lineA2E,lineA2F,
  lineA30,lineA31,lineA32,lineA33,lineA34,lineA35,lineA36,lineA37,
  lineA38,lineA39,lineA3A,lineA3B,lineA3C,lineA3D,lineA3E,lineA3F,
  lineB00,lineB01,lineB02,lineB03,lineB04,lineB05,lineB06,lineB07,
  lineB08,lineB09,lineB0A,lineB0B,lineB0C,lineB0D,lineB0E,lineB0F,
  lineB10,lineB11,lineB12,lineB13,lineB14,lineB15,lineB16,lineB17,
  lineB18,lineB19,lineB1A,lineB1B,lineB1C,lineB1D,lineB1E,lineB1F,
  lineB20,lineB21,lineB22,lineB23,lineB24,lineB25,lineB26,lineB27,
  lineB28,lineB29,lineB2A,lineB2B,lineB2C,lineB2D,lineB2E,lineB2F,
  lineB30,lineB31,lineB32,lineB33,lineB34,lineB35,lineB36,lineB37,
  lineB38,lineB39,lineB3A,lineB3B,lineB3C,lineB3D,lineB3E,lineB3F,
  lineC00,lineC01,lineC02,lineC03,lineC04,lineC05,lineC06,lineC07,
  lineC08,lineC09,lineC0A,lineC0B,lineC0C,lineC0D,lineC0E,lineC0F,
  lineC10,lineC11,lineC12,lineC13,lineC14,lineC15,lineC16,lineC17,
  lineC18,lineC19,lineC1A,lineC1B,lineC1C,lineC1D,lineC1E,lineC1F,
  lineC20,lineC21,lineC22,lineC23,lineC24,lineC25,lineC26,lineC27,
  lineC28,lineC29,lineC2A,lineC2B,lineC2C,lineC2D,lineC2E,lineC2F,
  lineC30,lineC31,lineC32,lineC33,lineC34,lineC35,lineC36,lineC37,
  lineC38,lineC39,lineC3A,lineC3B,lineC3C,lineC3D,lineC3E,lineC3F,
  lineD00,lineD01,lineD02,lineD03,lineD04,lineD05,lineD06,lineD07,
  lineD08,lineD09,lineD0A,lineD0B,lineD0C,lineD0D,lineD0E,lineD0F,
  lineD10,lineD11,lineD12,lineD13,lineD14,lineD15,lineD16,lineD17,
  lineD18,lineD19,lineD1A,lineD1B,lineD1C,lineD1D,lineD1E,lineD1F,
  lineD20,lineD21,lineD22,lineD23,lineD24,lineD25,lineD26,lineD27,
  lineD28,lineD29,lineD2A,lineD2B,lineD2C,lineD2D,lineD2E,lineD2F,
  lineD30,lineD31,lineD32,lineD33,lineD34,lineD35,lineD36,lineD37,
  lineD38,lineD39,lineD3A,lineD3B,lineD3C,lineD3D,lineD3E,lineD3F,
  lineE00,lineE01,lineE02,lineE03,lineE04,lineE05,lineE06,lineE07,
  lineE08,lineE09,lineE0A,lineE0B,lineE0C,lineE0D,lineE0E,lineE0F,
  lineE10,lineE11,lineE12,lineE13,lineE14,lineE15,lineE16,lineE17,
  lineE18,lineE19,lineE1A,lineE1B,lineE1C,lineE1D,lineE1E,lineE1F,
  lineE20,lineE21,lineE22,lineE23,lineE24,lineE25,lineE26,lineE27,
  lineE28,lineE29,lineE2A,lineE2B,lineE2C,lineE2D,lineE2E,lineE2F,
  lineE30,lineE31,lineE32,lineE33,lineE34,lineE35,lineE36,lineE37,
  lineE38,lineE39,lineE3A,lineE3B,lineE3C,lineE3D,lineE3E,lineE3F,
  lineF00,lineF01,lineF02,lineF03,lineF04,lineF05,lineF06,lineF07,
  lineF08,lineF09,lineF0A,lineF0B,lineF0C,lineF0D,lineF0E,lineF0F,
  lineF10,lineF11,lineF12,lineF13,lineF14,lineF15,lineF16,lineF17,
  lineF18,lineF19,lineF1A,lineF1B,lineF1C,lineF1D,lineF1E,lineF1F,
  lineF20,lineF21,lineF22,lineF23,lineF24,lineF25,lineF26,lineF27,
  lineF28,lineF29,lineF2A,lineF2B,lineF2C,lineF2D,lineF2E,lineF2F,
  lineF30,lineF31,lineF32,lineF33,lineF34,lineF35,lineF36,lineF37,
  lineF38,lineF39,lineF3A,lineF3B,lineF3C,lineF3D,lineF3E,lineF3F;
#endif


linefunc68_t *line_func[1024] = 
{
  line000,line001,line002,line003,line004,line005,line006,line007,
  line008,line009,line00A,line00B,line00C,line00D,line00E,line00F,
  line010,line011,line012,line013,line014,line015,line016,line017,
  line018,line019,line01A,line01B,line01C,line01D,line01E,line01F,
  line020,line021,line022,line023,line024,line025,line026,line027,
  line028,line029,line02A,line02B,line02C,line02D,line02E,line02F,
  line030,line031,line032,line033,line034,line035,line036,line037,
  line038,line039,line03A,line03B,line03C,line03D,line03E,line03F,
  line100,line101,line102,line103,line104,line105,line106,line107,
  line108,line109,line10A,line10B,line10C,line10D,line10E,line10F,
  line110,line111,line112,line113,line114,line115,line116,line117,
  line118,line119,line11A,line11B,line11C,line11D,line11E,line11F,
  line120,line121,line122,line123,line124,line125,line126,line127,
  line128,line129,line12A,line12B,line12C,line12D,line12E,line12F,
  line130,line131,line132,line133,line134,line135,line136,line137,
  line138,line139,line13A,line13B,line13C,line13D,line13E,line13F,
  line200,line201,line202,line203,line204,line205,line206,line207,
  line208,line209,line20A,line20B,line20C,line20D,line20E,line20F,
  line210,line211,line212,line213,line214,line215,line216,line217,
  line218,line219,line21A,line21B,line21C,line21D,line21E,line21F,
  line220,line221,line222,line223,line224,line225,line226,line227,
  line228,line229,line22A,line22B,line22C,line22D,line22E,line22F,
  line230,line231,line232,line233,line234,line235,line236,line237,
  line238,line239,line23A,line23B,line23C,line23D,line23E,line23F,
  line300,line301,line302,line303,line304,line305,line306,line307,
  line308,line309,line30A,line30B,line30C,line30D,line30E,line30F,
  line310,line311,line312,line313,line314,line315,line316,line317,
  line318,line319,line31A,line31B,line31C,line31D,line31E,line31F,
  line320,line321,line322,line323,line324,line325,line326,line327,
  line328,line329,line32A,line32B,line32C,line32D,line32E,line32F,
  line330,line331,line332,line333,line334,line335,line336,line337,
  line338,line339,line33A,line33B,line33C,line33D,line33E,line33F,
  line400,line401,line402,line403,line404,line405,line406,line407,
  line408,line409,line40A,line40B,line40C,line40D,line40E,line40F,
  line410,line411,line412,line413,line414,line415,line416,line417,
  line418,line419,line41A,line41B,line41C,line41D,line41E,line41F,
  line420,line421,line422,line423,line424,line425,line426,line427,
  line428,line429,line42A,line42B,line42C,line42D,line42E,line42F,
  line430,line431,line432,line433,line434,line435,line436,line437,
  line438,line439,line43A,line43B,line43C,line43D,line43E,line43F,
  line500,line501,line502,line503,line504,line505,line506,line507,
  line508,line509,line50A,line50B,line50C,line50D,line50E,line50F,
  line510,line511,line512,line513,line514,line515,line516,line517,
  line518,line519,line51A,line51B,line51C,line51D,line51E,line51F,
  line520,line521,line522,line523,line524,line525,line526,line527,
  line528,line529,line52A,line52B,line52C,line52D,line52E,line52F,
  line530,line531,line532,line533,line534,line535,line536,line537,
  line538,line539,line53A,line53B,line53C,line53D,line53E,line53F,
  line600,line601,line602,line603,line604,line605,line606,line607,
  line608,line609,line60A,line60B,line60C,line60D,line60E,line60F,
  line610,line611,line612,line613,line614,line615,line616,line617,
  line618,line619,line61A,line61B,line61C,line61D,line61E,line61F,
  line620,line621,line622,line623,line624,line625,line626,line627,
  line628,line629,line62A,line62B,line62C,line62D,line62E,line62F,
  line630,line631,line632,line633,line634,line635,line636,line637,
  line638,line639,line63A,line63B,line63C,line63D,line63E,line63F,
  line700,line701,line702,line703,line704,line705,line706,line707,
  line708,line709,line70A,line70B,line70C,line70D,line70E,line70F,
  line710,line711,line712,line713,line714,line715,line716,line717,
  line718,line719,line71A,line71B,line71C,line71D,line71E,line71F,
  line720,line721,line722,line723,line724,line725,line726,line727,
  line728,line729,line72A,line72B,line72C,line72D,line72E,line72F,
  line730,line731,line732,line733,line734,line735,line736,line737,
  line738,line739,line73A,line73B,line73C,line73D,line73E,line73F,
  line800,line801,line802,line803,line804,line805,line806,line807,
  line808,line809,line80A,line80B,line80C,line80D,line80E,line80F,
  line810,line811,line812,line813,line814,line815,line816,line817,
  line818,line819,line81A,line81B,line81C,line81D,line81E,line81F,
  line820,line821,line822,line823,line824,line825,line826,line827,
  line828,line829,line82A,line82B,line82C,line82D,line82E,line82F,
  line830,line831,line832,line833,line834,line835,line836,line837,
  line838,line839,line83A,line83B,line83C,line83D,line83E,line83F,
  line900,line901,line902,line903,line904,line905,line906,line907,
  line908,line909,line90A,line90B,line90C,line90D,line90E,line90F,
  line910,line911,line912,line913,line914,line915,line916,line917,
  line918,line919,line91A,line91B,line91C,line91D,line91E,line91F,
  line920,line921,line922,line923,line924,line925,line926,line927,
  line928,line929,line92A,line92B,line92C,line92D,line92E,line92F,
  line930,line931,line932,line933,line934,line935,line936,line937,
  line938,line939,line93A,line93B,line93C,line93D,line93E,line93F,
  lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,
  lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,
  lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,
  lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,
  lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,
  lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,
  lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,
  lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,lineA00,
  lineB00,lineB01,lineB02,lineB03,lineB04,lineB05,lineB06,lineB07,
  lineB08,lineB09,lineB0A,lineB0B,lineB0C,lineB0D,lineB0E,lineB0F,
  lineB10,lineB11,lineB12,lineB13,lineB14,lineB15,lineB16,lineB17,
  lineB18,lineB19,lineB1A,lineB1B,lineB1C,lineB1D,lineB1E,lineB1F,
  lineB20,lineB21,lineB22,lineB23,lineB24,lineB25,lineB26,lineB27,
  lineB28,lineB29,lineB2A,lineB2B,lineB2C,lineB2D,lineB2E,lineB2F,
  lineB30,lineB31,lineB32,lineB33,lineB34,lineB35,lineB36,lineB37,
  lineB38,lineB39,lineB3A,lineB3B,lineB3C,lineB3D,lineB3E,lineB3F,
  lineC00,lineC01,lineC02,lineC03,lineC04,lineC05,lineC06,lineC07,
  lineC08,lineC09,lineC0A,lineC0B,lineC0C,lineC0D,lineC0E,lineC0F,
  lineC10,lineC11,lineC12,lineC13,lineC14,lineC15,lineC16,lineC17,
  lineC18,lineC19,lineC1A,lineC1B,lineC1C,lineC1D,lineC1E,lineC1F,
  lineC20,lineC21,lineC22,lineC23,lineC24,lineC25,lineC26,lineC27,
  lineC28,lineC29,lineC2A,lineC2B,lineC2C,lineC2D,lineC2E,lineC2F,
  lineC30,lineC31,lineC32,lineC33,lineC34,lineC35,lineC36,lineC37,
  lineC38,lineC39,lineC3A,lineC3B,lineC3C,lineC3D,lineC3E,lineC3F,
  lineD00,lineD01,lineD02,lineD03,lineD04,lineD05,lineD06,lineD07,
  lineD08,lineD09,lineD0A,lineD0B,lineD0C,lineD0D,lineD0E,lineD0F,
  lineD10,lineD11,lineD12,lineD13,lineD14,lineD15,lineD16,lineD17,
  lineD18,lineD19,lineD1A,lineD1B,lineD1C,lineD1D,lineD1E,lineD1F,
  lineD20,lineD21,lineD22,lineD23,lineD24,lineD25,lineD26,lineD27,
  lineD28,lineD29,lineD2A,lineD2B,lineD2C,lineD2D,lineD2E,lineD2F,
  lineD30,lineD31,lineD32,lineD33,lineD34,lineD35,lineD36,lineD37,
  lineD38,lineD39,lineD3A,lineD3B,lineD3C,lineD3D,lineD3E,lineD3F,
  lineE00,lineE01,lineE02,lineE03,lineE04,lineE05,lineE06,lineE07,
  lineE08,lineE09,lineE0A,lineE0B,lineE0C,lineE0D,lineE0E,lineE0F,
  lineE10,lineE11,lineE12,lineE13,lineE14,lineE15,lineE16,lineE17,
  lineE18,lineE19,lineE1A,lineE1B,lineE1C,lineE1D,lineE1E,lineE1F,
  lineE20,lineE21,lineE22,lineE23,lineE24,lineE25,lineE26,lineE27,
  lineE28,lineE29,lineE2A,lineE2B,lineE2C,lineE2D,lineE2E,lineE2F,
  lineE30,lineE31,lineE32,lineE33,lineE34,lineE35,lineE36,lineE37,
  lineE38,lineE39,lineE3A,lineE3B,lineE3C,lineE3D,lineE3E,lineE3F,
  lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,
  lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,
  lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,
  lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,
  lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,
  lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,
  lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,
  lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,lineF00,
};

