## distcc cygwin setup instructions

#### Install cygwin, cygwinports
Follow instructions to install cygwin (for 32-bit) and the cygwin ports from here: http://cygwinports.org/

* **Note:** Select all the pre-requisite packages during the installation of the following packages.
  - Install ```distcc (version 2.18.3 at the time of writing)``` from one of the mirros
  (e.g. http://sourceware.mirrors.tds.net/pub/sourceware.org/cygwin/x86/release/distcc/)
  * Install ```linux-x86_64-binutils, linux-x86_64-gcc```
  (e.g. ftp://ftp.cygwinports.org/pub/cygwinports/x86/release/linux-x86_64-binutils/
  ftp://ftp.cygwinports.org/pub/cygwinports/x86/release/linux-x86_64-gcc/)

#### .bashrc changes
Add the following entry in .bashrc
```
export TMPDIR=C:/temp
```

#### Register the 'distcc' as windows service:
```
cygrunsrv.exe -I distccd -a "--daemon --no-detach --allow 107.108.0.0/16 --allow 107.109.0.0/16 --jobs 16" -p /usr/bin/distccd.exe
```
