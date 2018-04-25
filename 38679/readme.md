Problem
=======

If user specifies multiple disks and CDROM while using vmware_guest module for creating a new VM, then vmware_guest fails with

```
"Failed to create a virtual machine : Number of virtual devices exceeds the maximum for a given controller."
```

Resolution
==========

While creation of SCSI and IDE Controller specify unique random key for device key. Please see 'key' section in https://github.com/vmware/pyvmomi/blob/575ab56eb56f32f53c98f40b9b496c6219c161da/docs/vim/vm/device/VirtualDevice.rst

