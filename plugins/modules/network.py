#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018, Yanis Guenane <yanis+ansible@guenane.org>
# Copyright (c) 2021, René Moser <mail@renemoser.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
---
module: network
short_description: Manages networks on Vultr.
description:
  - Manage networks on Vultr. A network cannot be updated. It needs to be deleted and re-created.
version_added: "1.0.0"
author:
  - "Yanis Guenane (@Spredzy)"
  - "René Moser (@resmo)"
options:
  description:
    description:
      - Name of the network.
    required: true
    aliases: [ name ]
    type: str
  v4_subnet:
    description:
      - The IPv4 network. Required if I(state=present).
    type: str
  v4_subnet_mask:
    description:
      - The IPv4 network mask. Required if I(state=present).
    type: int
    default: 24
  region:
    description:
      - Region the network is deployed into. Required if I(state=present).
    type: str
  state:
    description:
      - State of the network.
    default: present
    choices: [ present, absent ]
    type: str
extends_documentation_fragment:
- vultr.cloud.vultr_v2
'''

EXAMPLES = '''
- name: Ensure a network is present
  vultr.cloud.network:
    name: mynet
    v4_subnet: 192.168.42.0
    v4_subnet_mask: 24
    region: ams

- name: Ensure a network is absent
  vultr.cloud.network:
    name: mynet
    state: absent
'''

RETURN = '''
---
vultr_api:
  description: Response from Vultr API with a few additions/modification
  returned: success
  type: complex
  contains:
    api_timeout:
      description: Timeout used for the API requests
      returned: success
      type: int
      sample: 60
    api_retries:
      description: Amount of max retries for the API requests
      returned: success
      type: int
      sample: 5
    api_retry_max_delay:
      description: Exponential backoff delay in seconds between retries up to this max delay value.
      returned: success
      type: int
      sample: 12
    api_endpoint:
      description: Endpoint used for the API requests
      returned: success
      type: str
      sample: "https://api.vultr.com/v2"
network:
  description: Response from Vultr API
  returned: success
  type: complex
  contains:
    id:
      description: ID of the network
      returned: success
      type: str
      sample: "cb676a46-66fd-4dfb-b839-443f2e6c0b60"
    description:
      description: Description of the network
      returned: success
      type: str
      sample: "mynetwork"
    date_created:
      description: Date when the network was created
      returned: success
      type: str
      sample: "2020-10-10T01:56:20+00:00"
    region:
      description: Region ID the network was deployed into
      returned: success
      type: str
      sample: "ams"
    v4_subnet:
      description: IPv4 Network address
      returned: success
      type: str
      sample: "192.168.42.0"
    v4_subnet_mask:
      description: Ipv4 Network mask
      returned: success
      type: int
      sample: 24
'''

from ansible.module_utils.basic import AnsibleModule
from ..module_utils.vultr_v2 import (
    AnsibleVultr,
    vultr_argument_spec,
)


def main():
    argument_spec = vultr_argument_spec()
    argument_spec.update(dict(
        description=dict(type='str', required=True, aliases=['name']),
        v4_subnet=dict(type='str',),
        v4_subnet_mask=dict(type='int', default=24),
        region=dict(type='str',),
        state=dict(choices=['present', 'absent'], default='present'),
    ))

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[['state', 'present', ['v4_subnet', 'v4_subnet_mask', 'region']]]
    )

    vultr = AnsibleVultr(
        module=module,
        namespace="vultr_network",
        resource_path="/private-networks",
        ressource_result_key_singular="network",
        resource_create_param_keys=['region', 'description', 'v4_subnet', 'v4_subnet_mask'],
        resource_update_param_keys=['description'],
        resource_key_name="description",
        resource_update_method="PUT",
    )

    if module.params.get('state') == "absent":
        vultr.absent()
    else:
        vultr.present()


if __name__ == '__main__':
    main()
