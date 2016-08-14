import os, sys

def spawn_as_administrator():
    """ Spawn ourself with administrator rights and wait for new process to exit
        Make the new process use the same console as the old one.
          Raise Exception() if we could not get a handle for the new re-run the process
          Raise pywintypes.error() if we could not re-spawn
        Return the exit code of the new process,
          or return None if already running the second admin process. """
    #pylint: disable=no-name-in-module,import-error
    import win32event, win32api, win32process
    import win32com.shell.shell as shell
    if '--admin' in sys.argv:
        return None
    print(sys.argv)
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + sys.argv[1:] + ['--admin'])
    SEE_MASK_NO_CONSOLE = 0x00008000
    SEE_MASK_NOCLOSE_PROCESS = 0x00000040
    process = shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params, fMask=SEE_MASK_NO_CONSOLE|SEE_MASK_NOCLOSE_PROCESS)

    hProcess = process['hProcess']
    if not hProcess:
        raise Exception("Could not identify administrator process to install drivers")
    # It is necessary to wait for the elevated process or else
    #  stdin lines are shared between 2 processes: they get one line each
    INFINITE = -1
    win32event.WaitForSingleObject(hProcess, INFINITE)
    exitcode = win32process.GetExitCodeProcess(hProcess)
    win32api.CloseHandle(hProcess)
    return exitcode


if __name__ == "__main__":
    if '--admin' in sys.argv:
        print(sys.argv)
        if(sys.argv[1] == "server"):
            os.system("netsh int ip set address \"Local Area Network\" static 10.0.0.1")
            os.system("netsh int ip set address \"Ethernet\" static 10.0.0.1")  
        if(sys.argv[1] == "client1"):
            os.system("netsh int ip set address \"Ethernet\" static 10.0.0.2")
            os.system("netsh int ip set address \"Local Area Network\" static 10.0.0.2")
        if(sys.argv[1] == "client2"):
            os.system("netsh int ip set address \"Ethernet\" static 192.168.0.3")
        if(sys.argv[1] == "client3"):
            os.system("netsh int ip set address \"Ethernet\" static 192.168.0.4")
        if(sys.argv[1] == "client4"):
            os.system("netsh int ip set address \"Ethernet\" static 192.168.0.5")
        if(sys.argv[1] == "dhcp"):
            os.system("netsh int ip set address \"Ethernet\" dhcp")
        #os.exit()
    else:
        #print(sys.argv[1])
        spawn_as_administrator()
