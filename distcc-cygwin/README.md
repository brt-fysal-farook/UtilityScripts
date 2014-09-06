## Distcc cygwin setup instructions

#### Install cygwin, cygwinports->distcc
Follow instructions to install cygwin (for 32-bit) and the cygwin ports from here: http://cygwinports.org/


#### .bashrc changes
Add the following entry in .bashrc
```
export TMPDIR=C:/temp
```

#### Register the 'distcc' as windows service:
```
cygrunsrv.exe -I distccd -a "--daemon --no-detach --allow 107.108.0.0/16 --allow 107.109.0.0/16 --jobs 16" -p /usr/bin/distccd.exe
```
