# PuppetDB
An Ansible Dynamic Inventory Script for ingesting Hosts and Facts from PuppetDB

This script requires that several environmental variables exist.  You can either place these in the "ENVIRONMENT VARIABLES" section of the Inventory Source in Ansible Tower, or you can create a Custom Credential Type to include these.  

Since PuppetDB authenticates with Certificates, you will need the CA Cert, and the Client cert and private key.  They must exist as files on the Tower Server and you must add the exclusion in Tower to be able to access these certs.  An easy way to create these certs, is to install the Puppet Agent on your Tower server or pull them from a working system.

Alternatively, you can enable HTTP access to PuppetDB (not recommended) and it will require no authentication to pull any data.

```
PUPPETDB_URL: http://10.0.101.101:8080/pdb/query/v4/facts
PUPPETDB_QUERY: '{"query":["=","certname","puppetclient1.lab.rhlabs.net"]}'
PUPPETDB_CA_CERT: /path/to/cacert
PUPPETDB_CERT: /path/to/cert
PUPPETDB_KEY: /path/to/privatekey
```
