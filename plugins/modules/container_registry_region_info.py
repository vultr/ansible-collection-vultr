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
module: container_registry_region_info
short_description: Get information about the Vultr container registry regions
version_added: "1.15.0"
description:
  - Gather information about container registry regions available
author:
  - "jasites (@jasites)"
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
- name: Get Vultr container registry region information
  vultr.cloud.container_registry_region_info:
  register: result

- name: Print the infos
  ansible.builtin.debug:
    var: result.vultr_container_registry_region_info
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
vultr_container_registry_region_info:
  description: Response from Vultr API as list.
  returned: success
  type: list
  contains:
    id:
      description: ID of the region.
      returned: success
      type: int
      sample: 3
    name:
      description: Region name
      returned: success
      type: str
      sample: sjc
    urn:
      description: Base URN (URL without connection scheme, i.e., 'https://') for this region
      returned: success
      type: str
      sample: sjc.vultrcr.com
    base_url:
      description: Base URL for registries deployed to this region
      returned: success
      type: str
      sample: https://sjc.vultrcr.com
    public:
      description: True if this region is generally available for new registries to be created
      returned: success
      type: bool
    added_at:
      description: Date of when this region was added
      returned: success
      type: str
      sample: 2023-09-14 09:09:16
    updated_at:
      description: Date of when this region was last updated
      returned: success
      type: str
      sample: 2023-09-14 09:09:16
    data_center:
      description: Additional details regarding this region
      returned: success
      type: dict
      contains:
        id:
          description: ID of this data center
          returned: success
          type: int
          sample: 12
        name:
          description: Name of data center
          returned: success
          type: str
          sample: Silicon Valley
        site_code:
          description: Code used to differentiate data centers within a region
          returned: success
          type: str
          sample: SJC2
        region:
          description: Geographical description of the placement of this data center within the region
          returned: success
          type: str
          sample: West
        country:
          description: Two letter country code (ISO 3166-1 alpha-2) of country containing this data center
          returned: success
          type: str
          sample: US
        continent:
          description: Continent containing this data center
          returned: success
          type: str
          sample: North America
        description:
          description: Additional descriptive data for this data center
          returned: success
          type: str
          sample: Silicon Valley, California
        airport:
          description: IATA airport code
          returned: success
          type: str
          sample: SJC
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
        namespace="vultr_container_registry_region_info",
        resource_path="/registry/region/list",
        ressource_result_key_singular="region",
    )

    vultr.get_result(vultr.query_list())


if __name__ == "__main__":
    main()
