## Distcc cygwin setup instructions


#### Register the 'distcc' as windows service:
```
cygrunsrv.exe -I distccd -a "--daemon --no-detach --allow 107.108.0.0/16 --allow 107.109.0.0/16 --jobs 16" -p /usr/bin/distccd.exe
```
