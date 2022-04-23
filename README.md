[![Collection integration](https://github.com/vultr/ansible-collection-vultr/actions/workflows/integration.yml/badge.svg?branch=main)](https://github.com/vultr/ansible-collection-vultr/actions/workflows/integration.yml)
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

### Clone the source

```
git clone git@github.com:vultr/ansible-collection-vultr.git
cd ansible-collection-vultr
```

### Create a virtual environent

```
python3 -m venv .venv
source .venv/bin/activate
```

### Install ansible for ansible-test
```
pip install ansible
```

### Setup your Vultr API key

```
cp tests/integration/cloud-config-vultr.ini.origin tests/integration/cloud-config-vultr.ini
edit tests/integration/cloud-config-vultr.ini
```

### Runs tests in Docker

All vultr tests:

```
ansible-test integration --docker --diff -v cloud/vultr/
```

Specific vultr test e.g. ssh_key_info:

```
ansible-test integration --docker --diff -v cloud/vultr/ssh_key_info
```

## Releasing

### Update Changelog

The changelog is managed using the `antsibull` tool. You can install
it using `pip install antsibull`

1. Set version in galaxy.yml
2. Create a release summary fragment and store in in _changelog/fragements/<version>.yml_:
```yaml
release_summary: |
  In this release...
```
3. Generate changelog of all fragments using antsibull
```
antsibull-changelog release
```
Modify or delete the release summary in
4. Commit changelog and new version
```
git commit -m "Release version X.Y.Z" galaxy.yml CHANGELOG.rst changelogs/
```

### Tag the release

1. Tag the release. Preferably create GPG signed tag if you have a GPG
key. Version tags should be prefixed with "v".
```
git tag -s -m "Release X.Y.Z" vX.Y.Z
```
2. Push the release and tag
```
git push origin main vX.Y.Z
```

### Publish to Ansible Galaxy

After the _GitHub Release_ has been created the CI job _publish_ gets triggered which pushes the release to _Ansible Galaxy_.

1. Draft a new _GitHub Release_
2. Select the tag `vX.Y.Z`.
3. Set the title:
```
Release vX.Y.Z
```
3. Set the content:
```
See changelog for more information https://github.com/vultr/ansible-collection-vultr/blob/vX.Y.Z/CHANGELOG.rst#vX.Y.Z
```
4. Verify the release is [processed by CI](https://github.com/vultr/ansible-collection-vultr/actions/workflows/publish.yml)


## License

GNU General Public License v3.0

See [COPYING](COPYING) to see the full text.
