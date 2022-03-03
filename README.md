![Collection integration](https://github.com/vultr/ansible-collection-vultr/workflows/Collection%20integration/badge.svg)
 [![Codecov](https://img.shields.io/codecov/c/github/vultr/ansible-collection-vultr)](https://codecov.io/gh/vultr/ansible-collection-vultr)
[![License](https://img.shields.io/badge/license-GPL%20v3.0-brightgreen.svg)](LICENSE)

# Ansible Collection for Vultr Cloud

This collection provides a series of Ansible modules and plugins for interacting with the [Vultr](https://www.vultr.com) Cloud.

## Requirements

- ansible version >= 2.9

## Installation

To install the collection hosted in Galaxy:

```bash
ansible-galaxy collection install vultr.cloud
```

To upgrade to the latest version of the collection:

```bash
ansible-galaxy collection install vultr.cloud --force
```

## Usage

### Playbooks

To use a module from Vultr collection, please reference the full namespace, collection name, and modules name that you want to use:

```yaml
---
- name: Using Vultr collection
  hosts: localhost
  tasks:
    - vultr.cloud.instance:
      ...
```

## Contributing

There are many ways in which you can participate in the project, for example:

- Submit bugs and feature requests, and help us verify as they are checked in
- Review source code changes
- Review the documentation and make pull requests for anything from typos to new content
- If you are interested in fixing issues and contributing directly to the code base, please see the [CONTRIBUTING](CONTRIBUTING.md) document.

## Run Tests

```
# For ansible-test we need to source the ansible repo
git clone git@github.com:ansible/ansible.git
cd ansible && source ./hacking/env-setup

git clone git@github.com:vultr/ansible-collection-vultr.git
cd ansible-collection-vultr

# Key to use
cp tests/integration/cloud-config-vultr.ini.origin tests/integration/cloud-config-vultr.ini
edit tests/integration/cloud-config-vultr.ini

# Runs all tests
ansible-test integration --docker --diff -v cloud/vultr/

# Runs one test e.g. ssh_key_info
ansible-test integration --docker --diff -v cloud/vultr/ssh_key_info
```

## License

GNU General Public License v3.0

See [COPYING](COPYING) to see the full text.
