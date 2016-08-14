from subprocess import call
dir = r"C:\\Users\\Madmilla\\Downloads\\"
cmdline = "cmd /C Flyleaf.rar"
rc = call(cmdline, cwd=dir)
