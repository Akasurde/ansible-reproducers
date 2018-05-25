from pyVim.connect import SmartConnect, Disconnect
import ssl
import atexit
from pyVmomi import vim, vmodl, VmomiSupport
import time


def connect():
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    si = SmartConnect(host='xx.xx.xx.xx', user='administrator@vsphere.local', pwd='password', port=443, sslContext=context)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    return content

def get_obj(content, vimtype, name):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    if name in ['', None]:
        obj = []
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj.append(c)

    container.Destroy()
    return obj

content = connect()

host = get_obj(content, [vim.HostSystem], None)[0]
option_manager = host.configManager.advancedOption
option = vim.option.OptionValue()
option.key = 'UserVars.ESXiShellInteractiveTimeOut'
option.value = VmomiSupport.vmodlTypes['long'](12)
option_manager.UpdateOptions(changedValue=[option])
for option in option_manager.QueryOptions():
    if option.key == 'UserVars.ESXiShellInteractiveTimeOut':
        print(option.value)
