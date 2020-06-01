from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = '''
    lookup: MyLookup

    short_description: Custom Lookup

    description: Nothing here
'''

EXAMPLES = """#
"""

RETURN = """
#
"""

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError


class MyLookup():

    def __init__(self):
        pass
    def fail(self, msg=None):
        raise AnsibleError(msg)

    def run(self, terms, variables=None, **kwargs):
        self.params = kwargs
        return [{1,2,3}]


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        return MyLookup().run(terms, variables=variables, **kwargs)
