from pyVim.connect import SmartConnect, Disconnect
import ssl
import atexit
from pyVmomi import vim, vmodl

def connect(hostname, username, password):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    si = SmartConnect(host=hostname, user=username,
                      pwd=password, port=443, sslContext=context)
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

def get_folder_path(obj):
    paths = []
    if isinstance(obj, vim.Folder):
        paths.append(obj.name)

    thisobj = obj
    while hasattr(thisobj, 'parent'):
        thisobj = thisobj.parent
        try:
            moid = thisobj._moId
        except AttributeError:
            moid = None
        if moid in ['group-d1', 'ha-folder-root']:
            break
        if isinstance(thisobj, vim.Folder):
            paths.append(thisobj.name)

    paths.reverse()
    return paths

hostname = '127.0.0.1'
username = 'user'
password = 'pass'

content = connect(hostname, username, password)

all_vms = get_all_objs(content, [vim.VirtualMachine])
for item in list(all_vms.keys()):
    print(get_folder_path(item))
