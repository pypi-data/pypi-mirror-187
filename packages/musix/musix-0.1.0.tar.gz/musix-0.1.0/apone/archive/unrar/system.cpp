#include "rar.hpp"

#ifndef _WIN_CE
static int SleepTime=0;

void InitSystemOptions(int SleepTime)
{
  ::SleepTime=SleepTime;
}
#endif


#if !defined(SFX_MODULE) && !defined(_WIN_CE)
void SetPriority(int Priority)
{
#ifdef _WIN_32
  uint PriorityClass;
  int PriorityLevel;
  if (Priority<1 || Priority>15)
    return;

  if (Priority==1)
  {
    PriorityClass=IDLE_PRIORITY_CLASS;
    PriorityLevel=THREAD_PRIORITY_IDLE;
  }
  else
    if (Priority<7)
    {
      PriorityClass=IDLE_PRIORITY_CLASS;
      PriorityLevel=Priority-4;
    }
    else
      if (Priority==7)
      {
        PriorityClass=BELOW_NORMAL_PRIORITY_CLASS;
        PriorityLevel=THREAD_PRIORITY_ABOVE_NORMAL;
      }
      else
        if (Priority<10)
        {
          PriorityClass=NORMAL_PRIORITY_CLASS;
          PriorityLevel=Priority-7;
        }
        else
          if (Priority==10)
          {
            PriorityClass=ABOVE_NORMAL_PRIORITY_CLASS;
            PriorityLevel=THREAD_PRIORITY_NORMAL;
          }
          else
          {
            PriorityClass=HIGH_PRIORITY_CLASS;
            PriorityLevel=Priority-13;
          }
  SetPriorityClass(GetCurrentProcess(),PriorityClass);
  SetThreadPriority(GetCurrentThread(),PriorityLevel);

//  Background mode for Vista, too slow for real life use.
//  if (WinNT()>=6 && Priority==1)
//    SetPriorityClass(GetCurrentProcess(),PROCESS_MODE_BACKGROUND_BEGIN);

#endif
}
#endif


void Wait()
{
#if defined(_WIN_32) && !defined(_WIN_CE) && !defined(SFX_MODULE)
  if (SleepTime!=0)
    Sleep(SleepTime);
#endif
}




#if defined(_WIN_32) && !defined(_WIN_CE) && !defined(SFX_MODULE) && !defined(SHELL_EXT)

void Shutdown()
{
  HANDLE hToken;
  TOKEN_PRIVILEGES tkp;
  if (OpenProcessToken(GetCurrentProcess(),TOKEN_ADJUST_PRIVILEGES|TOKEN_QUERY,&hToken))
  {
    LookupPrivilegeValue(NULL,SE_SHUTDOWN_NAME,&tkp.Privileges[0].Luid);
    tkp.PrivilegeCount = 1;
    tkp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;

    AdjustTokenPrivileges(hToken,FALSE,&tkp,0,(PTOKEN_PRIVILEGES)NULL,0);
  }
  ExitWindowsEx(EWX_SHUTDOWN|EWX_FORCE|EWX_POWEROFF,SHTDN_REASON_FLAG_PLANNED);
}
#endif
