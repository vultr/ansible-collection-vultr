#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2025, Samuel Hunter <samuel (at) shunter (dot) xyz>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: vfs_info
short_description: Get information about Vultr VFS subscriptions
version_added: "1.14.0"
description:
  - Get infos about Vultr virtual file system subscriptions available.
author:
  - "Samuel Hunter (@samuel-hunter)"
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
- name: Get Vultr vfs infos
  vultr.cloud.vfs_info:
  register: result

- name: Print the infos
  ansible.builtin.debug:
    var: result.vultr_vfs_info
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
vultr_vfs_info:
  description: Response from Vultr API as list.
  returned: success
  type: list
  contains:
    billing:
      description: Billing info
      returned: success
      type: dict
      contains:
        charges:
          description: Current billing charges
          returned: success
          type: float
          sample: 10.5
        monthly:
          description: Monthly billing amount
          returned: success
          type: float
          sample: 30
    date_created:
      description: Creation timestamp of the VFS
      returned: success
      type: str
      sample: "2024-01-01T12:00:00Z"
    disk_type:
      description: Type of storage disk
      returned: success
      type: str
      sample: nvme
    label:
      description: User-defined label for the VFS
      returned: success
      type: str
      sample: my file system
    id:
      description: Unique identifier for the VFS
      returned: success
      type: str
      sample: cb676a46-66fd-4dfb-b839-443f2e6c0b60
    region:
      description: Region identifier where the VFS is located
      returned: success
      type: str
      sample: ewr
    status:
      description: Current status of the VFS
      returned: success
      type: str
      sample: active
    storage_size:
      description: Storage provisioned for the VFS
      returned: success
      type: dict
      contains:
        bytes:
          description: Size in bytes
          returned: success
          type: int
          sample: 10737418240
        gb:
          description: Size in gigabytes
          returned: success
          type: int
          sample: 10
    storage_used:
      description: Storage used
      returned: success
      type: dict
      contains:
        bytes:
          description: Size in bytes
          returned: success
          type: int
          sample: 10737418240
        gb:
          description: Size in gigabytes
          returned: success
          type: int
          sample: 10
    tags:
      description: List of tags associated with the VFS
      returned: success
      type: list
      elements: str
      sample: [ prod, web ]
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
        namespace="vultr_vfs_info",
        resource_path="/vfs",
        ressource_result_key_singular="vfs",
        ressource_result_key_plural="vfs",
    )

    vultr.get_result(vultr.query_list())


if __name__ == "__main__":
    main()
