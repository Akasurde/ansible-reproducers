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


hostname = ''
username = 'administrator@vsphere.local'
password = 'Esxi@123$%'

content = connect(hostname, username, password)

all_vms = get_all_objs(content, [vim.VirtualMachine])
print(all_vms)
#for item in all_vms.items():
#    print(item[0].config.name)
