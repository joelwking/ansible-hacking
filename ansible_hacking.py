#!/usr/bin/env python
#
"""
     Copyright (c) 2017 World Wide Technology, Inc.
     All rights reserved.

     Revision history:
     11 May 2017  |  1.0 - initial release
                     1.1 - doc formatting

     module: ansible_hacking.py
     author: Joel W. King, (@joelwking) World Wide Technology
     short_description: A mock object to simulate the Ansible environment for remote debugging
     reference: http://docs.ansible.com/ansible/dev_guide/developing_modules_general.html
     description:  This code provides an alternative to using the Ansible hacking/test-module
"""
import sys
import json

class AnsibleModule(object):
    """ Mock class for testing Ansible modules outside of the Ansible framework.
    """
    INPUT_JSON = "ansible_hacking.json"

    def __init__(self, **kwargs):
        """ Ansible internally saves arguments to an arguments file,
            we read from our own JSON file.
        """
        print "Entered ansible_hacking, AnsibleModule \n%s" % (json.dumps(kwargs, indent=4))
        self.params = self.read_params(AnsibleModule.INPUT_JSON)
        print "params:\n%s\nExiting AnsibleModule __init__" % (json.dumps(self.params, indent=4))

    def read_params(self, fname):
        """ Arguments for testing are read from JSON format file.
        """
        print "loading params from %s" % fname
        try:
            jsonfile = open(fname, 'r')
        except IOError:
            print "input file: %s not found!" % fname
            sys.exit(1)

        infile = jsonfile.read()
        jsonfile.close()

        return json.loads(infile)

    def exit_json(self, **kwargs):
        """ Modules return information to Ansible by printing a JSON string
            to stdout before exiting.
        """
        print "%s" % (json.dumps(kwargs, indent=4))
        sys.exit(0)

    def fail_json(self, msg):
        """Fail with a message formatted in JSON.
        """
        print json.dumps({'msg': msg}, indent=4)
        sys.exit(1)
