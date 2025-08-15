#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) jasites <jsites@vultr.com>
# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: plan_container_registry_info
short_description: Get information about the Vultr container registry plans
version_added: "1.15.0"
description:
  - Gather information about container registry plans available
author:
  - "jasites (@jasites)"
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
- name: Get Vultr container registry plan information
  vultr.cloud.plan_container_registry_info:
  register: result

- name: Print the infos
  ansible.builtin.debug:
    var: result.vultr_plan_container_registry_info
"""

RETURN = """
---
vultr_api:
  description: Response from Vultr API with a few additions/modification.
  returned: success
  type: dict
  contains:
    api_timeout:
      description: Timeout used for the API requests.
      returned: success
      type: int
      sample: 60
    api_retries:
      description: Amount of max retries for the API requests.
      returned: success
      type: int
      sample: 5
    api_retry_max_delay:
      description: Exponential backoff delay in seconds between retries up to this max delay value.
      returned: success
      type: int
      sample: 12
    api_results_per_page:
      description: Number of results returned per call to API.
      returned: success
      type: int
      sample: 100
    api_endpoint:
      description: Endpoint used for the API requests.
      returned: success
      type: str
      sample: "https://api.vultr.com/v2"
vultr_plan_container_registry_info:
  description: Response from Vultr API as list.
  returned: success
  type: list
  contains:
    id:
      description: ID of the plan.
      returned: success
      type: str
      sample: start_up
    vanity_name:
      description: Stylized plan name
      returned: success
      type: str
      sample: Start Up
    max_storage_mb:
      description: Total allocated storage allowed by plan
      returned: success
      type: int
      sample: 10240
    monthly_price:
      description: Monthly price for this plan
      returned: success
      type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import dict_merge

from ..module_utils.vultr_v2 import AnsibleVultr, vultr_argument_spec


class AnsibleVultrPlanContainerRegistryInfo(AnsibleVultr):
    def transform_result(self, resource):
        result = []
        if resource:
            for plan in resource.get("plans", {}).keys():
                result.append(dict_merge(dict(id=plan), resource.get("plans", {}).get(plan, {})))
        return result


def main():
    argument_spec = vultr_argument_spec()

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    vultr = AnsibleVultrPlanContainerRegistryInfo(
        module=module,
        namespace="vultr_plan_container_registry_info",
        resource_path="/registry/plan/list",
        ressource_result_key_singular="plan",
    )

    vultr.get_result(vultr.api_query(vultr.resource_path))


if __name__ == "__main__":
    main()
