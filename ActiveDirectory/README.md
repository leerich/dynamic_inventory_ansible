# Active Directory
An Ansible Dynamic Inventory Script for ingesting Hosts from Active Directory


To utilize this script, you will need to create a new Credential Type in Ansible Tower.   Below is the form you will need to create.

#### INPUT CONFIGURATION:
```
fields:
  - type: string
    id: dc
    label: 'Active Directory URL (ex: ldap://labdc01:389)'
  - type: string
    id: username
    label: Username
  - secret: true
    type: string
    id: password
    label: Password
  - type: string
    id: base_dn
    label: Base Search DN
required:
  - username
  - password
  - dc
  - base_dn
```

#### INJECTOR CONFIGURATION
```
env:
  AD_BASE_DN: '{{ base_dn }}'
  AD_BIND_PASS: '{{ password }}'
  AD_BIND_USER: '{{ username }}'
  AD_DC: '{{ dc }}'
```

## Additional Packages
You may require additional packages on your Machine for this to work.  For RHEL 7, just issue these commands
```
yum install openldap-devel
pip install --upgrade setuptools
pip install python-ldap
```
