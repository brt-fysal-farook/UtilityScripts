<h4>Speeding up linux file access</h4>

Edit the */etc/fstab* file as -
<pre>
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
# / was on /dev/sda1 during installation
UUID=fe831f64-aed4-455a-b85e-b315b4356afa /               ext4    errors=remount-ro 0       1
# /home was on /dev/sda3 during installation
UUID=0847a1ee-4aaa-4822-9899-e371447f119f /home           ext4    defaults,noatime,nodiratime        0       2
# swap was on /dev/sda5 during installation
UUID=bc4e6a13-79bb-4508-a3dd-c83ab341958d none            swap    sw              0       0
</pre>
