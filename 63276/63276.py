from pyVim.connect import SmartConnect, Disconnect
import ssl
import atexit
from pyVmomi import vim, vmodl
import click


def connect(hostname, username, password, port):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    si = SmartConnect(host=hostname,
                      user=username,
                      pwd=password,
                      port=port, sslContext=context)
    atexit.register(Disconnect, si)
    return si, si.RetrieveContent()

def get_managed_objects_properties(content, vim_type, properties=None):
    # Get Root Folder
    root_folder = content.rootFolder

    if properties is None:
        properties = ['name']

    # Create Container View with default root folder
    mor = content.viewManager.CreateContainerView(root_folder, [vim_type], True)

    # Create Traversal spec
    traversal_spec = vmodl.query.PropertyCollector.TraversalSpec(
        name="traversal_spec",
        path='view',
        skip=False,
        type=vim.view.ContainerView
    )

    # Create Property Spec
    property_spec = vmodl.query.PropertyCollector.PropertySpec(
        type=vim_type,  # Type of object to retrieved
        all=False,
        pathSet=properties
    )

    # Create Object Spec
    object_spec = vmodl.query.PropertyCollector.ObjectSpec(
        obj=mor,
        skip=True,
        selectSet=[traversal_spec]
    )

    # Create Filter Spec
    filter_spec = vmodl.query.PropertyCollector.FilterSpec(
        objectSet=[object_spec],
        propSet=[property_spec],
        reportMissingObjectsInResults=False
    )

    return content.propertyCollector.RetrieveContents([filter_spec])


def main():
    hostname='10.65.200.241'
    username='administrator@vsphere.local'
    password='Esxi@123$%'
    port = 443
    template_name = "TEMPLATE_2016"
    template_name = "Win2k16"

    templates = []
    si, content = connect(hostname, username, password, port)
    all_vms = get_managed_objects_properties(content=content, vim_type=vim.VirtualMachine, properties=['name'])
    print(all_vms)
    for temp_vm_object in all_vms:
        if len(temp_vm_object.propSet) != 1:
            continue
        for temp_vm_object_property in temp_vm_object.propSet:
            if temp_vm_object_property.val == template_name:
                templates.append(temp_vm_object.obj)
                break
        
    print(templates)
    
if __name__ == "__main__":
    main()
