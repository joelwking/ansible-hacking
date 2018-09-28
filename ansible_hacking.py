#!/usr/bin/env python
"""
     Copyright (c) 2017 World Wide Technology, Inc.
     All rights reserved.

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
    NO = ("n","N", "no", "No", "NO", "False", "FALSE", "false", "off", "Off", "OFF")
    YES = ("y", "Y", "yes", "Yes", "YES", "True", "TRUE", "true", "on", "On", "ON")


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

        try:
            jsonfile = open(fname, 'r')
        except IOError:
            print "input file: %s not found!" % fname
            sys.exit(1)

        infile = jsonfile.read()
        jsonfile.close()
        
        # BOOLEAN logic
        params = json.loads(infile)
        for key, value in params.items():
            if value in AnsibleModule.NO:
                params[key] = False
            if value in AnsibleModule.YES:
                params[key] = True

        return params

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
