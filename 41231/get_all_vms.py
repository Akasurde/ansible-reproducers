from pyVim.connect import SmartConnect, Disconnect
import ssl
import atexit
from pyVmomi import vim, vmodl

def connect(hostname, username, password):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    si = SmartConnect(host=hostname,
                      user=username,
                      pwd=password,
                      port=443, sslContext=context)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    return content

def get_all_objs(content, vimtype):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        obj.update({c: c.name})

    container.Destroy()
    return obj

def get_vm_path(content, vm_name):
        folder_name = None
        folder = vm_name.parent
        if folder:
            folder_name = folder.name
            fp = folder.parent
            # climb back up the tree to find our path, stop before the root folder
            while fp is not None and fp.name is not None and fp != content.rootFolder:
                folder_name = fp.name + '/' + folder_name
                try:
                    fp = fp.parent
                except BaseException:
                    break
            folder_name = '/' + folder_name
        return folder_name

hostname = 'xx.xx.xx.xx'
username = 'administrator@vsphere.local'
password = 'Esxi@123$%'
vm_name = "VM_0001"

content = connect(hostname, username, password)

all_vms = get_all_objs(content, [vim.VirtualMachine])
for vm_n in all_vms.keys():
    if all_vms[vm_n] == vm_name:
        print("VM Name: " + all_vms[vm_n])
        print("VM Path: " + get_vm_path(content, vm_n))
