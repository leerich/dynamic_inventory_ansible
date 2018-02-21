#!/usr/bin/env python
# coding: utf-8

'''
PuppetDB Inventory Script
=======================
PuppetDB url parameters must be specified via the `PUPPETDB_URL` environmental
variable.  Failure to provide this will result in an empty inventory.
ex:  https://puppetdb:8081/pdb/query/v4/facts

If you specify the environmental variable `PUPPETDB_QUERY` then you can limit the 
hosts based upon facts specified
ex: '{"query":["=","certname","puppetclient1"]}'
Examples can be found here
https://puppet.com/docs/puppetdb/5.1/api/query/tutorial.html



PUPPETDB_CA_CERT
PUPPETDB_CERT
PUPPETDB_KEY


'''

import os
import sys
import argparse
import urllib3

try:
  import json
except ImportError:
  import simplejson as json



class PuppetDBInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        if os.environ.get('PUPPETDB_URL', ''):
          self.puppetdb_url = os.environ['PUPPETDB_URL']
        else:
          print json.dumps(self.empty_inventory())
          sys.exit(0)

        if os.environ.get('PUPPETDB_CA_CERT', ''):
          self.puppetdb_ca = os.environ['PUPPETDB_CA_CERT']
        else:
          print json.dumps(self.empty_inventory())
          sys.exit(0)

        if os.environ.get('PUPPETDB_CERT', ''):
          self.puppetdb_ca = os.environ['PUPPETDB_CERT']
        else:
          print json.dumps(self.empty_inventory())
          sys.exit(0)

        if os.environ.get('PUPPETDB_KEY', ''):
          self.puppetdb_key = os.environ['PUPPETDB_KEY']
        else:
          print json.dumps(self.empty_inventory())
          sys.exit(0)

        if os.environ.get('PUPPETDB_QUERY', ''):
          self.puppetdb_query = os.environ['PUPPETDB_QUERY']
        else:
          self.puppetdb_query = None

        # Called with '--list'.
        if self.args.list:
          self.inventory = self.puppetdb_inventory()
        # Called with '--host [hostname]'.
        elif self.args.host:
          # Not implemented, since we return _meta info '--list'.
          self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
          self.inventory = self.empty_inventory()

        print json.dumps(self.inventory)

    def puppetdb_inventory(self):

      inv_data = {}
      inv_data.update({ '_meta': { 'hostvars': {} } })

      conn = urllib3.connection_from_url(self.puppetdb_url, cert_file=self.puppetdb_cert, key_file=self.puppetdb_key, ca_certs=self.puppetdb_ca, cert_reqs='REQUIRED')
      response = conn.request('GET', self.puppetdb_url, headers={"Content-Type" : "application/json"})

      facts = response.data
      facts = json.loads(facts)

      for fact in facts:
        env = fact['environment']
        if env not in inv_data:
          inv_data.update({ env: { 'hosts': [], 'vars': {} } })
        if fact['certname'] not in inv_data[env]['hosts']:
          inv_data[env]['hosts'].append(fact['certname'])

        if fact['name'] == "os":
          os = fact['value']['name']
          if os not in inv_data:
            inv_data.update({ os: { 'hosts': [], 'vars': {} } })
          inv_data[os]['hosts'].append(fact['certname'])

        if fact['name'] == "virtual":
          virtual = fact['value']
          if virtual not in inv_data:
            inv_data.update({ virtual: { 'hosts': [], 'vars': {} } })
          inv_data[virtual]['hosts'].append(fact['certname'])

        if fact['certname'] not in inv_data['_meta']['hostvars']:
          inv_data['_meta']['hostvars'][fact['certname']] = {}
        inv_data['_meta']['hostvars'][fact['certname']].update({ fact['name'] : fact['value'] })         

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
PuppetDBInventory()
