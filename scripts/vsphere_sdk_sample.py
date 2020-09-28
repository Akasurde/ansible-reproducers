from vmware.vapi.vsphere.client import create_vsphere_client
import requests

session = requests.Session()
session.verify = False

hostname = "10.65.201.177"
username = "administrator@vsphere.local"
password = "Esxi@123$%"

client = create_vsphere_client(server=hostname,
                               username=username,
                               password=password,
                               session=session)
print(client)
