#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018, Yanis Guenane <yanis+ansible@guenane.org>
# Copyright (c) 2021, René Moser <mail@renemoser.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: plan_info
short_description: Gather information about the Vultr plans available.
description:
  - Gather information about plans available to boot servers.
version_added: "1.0.0"
author:
  - "Yanis Guenane (@Spredzy)"
  - "René Moser (@resmo)"
extends_documentation_fragment:
- vultr.cloud.vultr_v2
"""

EXAMPLES = """
- name: Gather Vultr plans information
  vultr.cloud.plan_info:
  register: result

- name: Print the gathered information
  debug:
    var: result.vultr_plan_info
"""

RETURN = """
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
vultr_plan_info:
  description: Response from Vultr API as list
  returned: success
  type: complex
  contains:
    plan:
      description: List of the plans available.
      returned: success
      type: list
      sample: [{
        "bandwidth": 1024,
        "disk": 25,
        "disk_count": 1,
        "id": "vc2-1c-1gb",
        "locations": ["ewr", "ord", "dfw", "sea", "lax", "atl", "ams", "lhr", "fra", "sjc", "syd", "yto", "cdg", "nrt", "icn", "mia", "sgp", "sto", "mex"],
        "monthly_cost": 5,
        "ram": 1024,
        "type": "vc2",
        "vcpu_count": 1
        }]
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.vultr_v2 import AnsibleVultr, vultr_argument_spec


def main():
    argument_spec = vultr_argument_spec()

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    vultr = AnsibleVultr(
        module=module,
        namespace="vultr_plan_info",
        resource_path="/plans",
        ressource_result_key_singular="plan",
    )

    vultr.get_result(vultr.query_list())


if __name__ == "__main__":
    main()
