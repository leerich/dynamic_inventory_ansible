#!/usr/bin/env python
# coding: utf-8

import os
import sys
import argparse
import ldap
from ldap import LDAPError

try:
  import json
except ImportError:
  import simplejson as json

class ActiveDirectoryInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        if os.environ.get('AD_DC', ''):
          self.dc = os.environ['AD_DC']
        else:
          print json.dumps(self.empty_inventory())
          sys.exit(0)

        if os.environ.get('AD_BIND_USER', ''):
          self.username = os.environ['AD_BIND_USER']
        else:
          print json.dumps(self.empty_inventory())
          sys.exit(0)

        if os.environ.get('AD_BIND_PASS', ''):
          self.password = os.environ['AD_BIND_PASS']
        else:
          print json.dumps(self.empty_inventory())
          sys.exit(0)

        if os.environ.get('AD_BASE_DN', ''):
          self.base_dn = os.environ['AD_BASE_DN']
        else:
          print json.dumps(self.empty_inventory())
          sys.exit(0)

        # Called with '--list'.
        if self.args.list:
          self.inventory = self.activedirectory_inventory()
        # Called with '--host [hostname]'.
        elif self.args.host:
          # Not implemented, since we return _meta info '--list'.
          self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
          self.inventory = self.empty_inventory()

        print json.dumps(self.inventory)

    def activedirectory_inventory(self):
      inv_data = {}
      inv_data.update({ '_meta': { 'hostvars': {} } })

      attrs = ['cn', 'dNSHostName', 'operatingSystem', 'operatingSystemVersion', 'operatingSystemServicePack']
      attrs = ['*']
      objectFilter = '(objectClass=Computer)'

      try:
        con = ldap.initialize(self.dc)
        con.set_option(ldap.OPT_REFERRALS, 0)
        con.simple_bind_s(self.username, self.password)
      except ldap.INVALID_CREDENTIALS:
        sys.exit('[!] Error: invalid credentials')
      except ldap.LDAPError, e:
        sys.exit("[!] {}".format(e))

      msgid = con.search_ext(self.base_dn, ldap.SCOPE_SUBTREE, objectFilter, attrs)
      result_type, rawResults, message_id, server_controls = con.result3(msgid)

      for pc in rawResults:
        if ('dNSHostName' in pc[1]):
          name = pc[1]['dNSHostName'][0]

          if name not in inv_data['_meta']['hostvars']:
            inv_data['_meta']['hostvars'][name] = {}

          if 'operatingSystem' in pc[1]:
            os = pc[1]['operatingSystem'][0]
            if os not in inv_data:
              inv_data.update({ os: { 'hosts': [], 'vars': {} } })
            inv_data[os]['hosts'].append(name)

          if 'cn' in pc[1]:
            inv_data['_meta']['hostvars'][name].update({ 'cn' : pc[1]['cn'][0] })
          if 'operatingSystemVersion' in pc[1]:
            inv_data['_meta']['hostvars'][name].update({ 'operatingSystemVersion' : pc[1]['operatingSystemVersion'][0] })

      return inv_data

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

# Get the inventory.
ActiveDirectoryInventory()

