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
module: object_storage_info
short_description: Get information about the Vultr object stores
version_added: "1.14.0"
description:
  - Get infos about object storages available.
author:
  - "jasites (@jasites)"
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
- name: Get Vultr object_storage infos
  vultr.cloud.object_storage_info:
  register: result

- name: Print the infos
  ansible.builtin.debug:
    var: result.vultr_object_storage_info
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
    api_endpoint:
      description: Endpoint used for the API requests.
      returned: success
      type: str
      sample: "https://api.vultr.com/v2"
vultr_object_storage_info:
  description: Response from Vultr API as list.
  returned: success
  type: list
  contains:
    cluster_id:
      description: The ID of the Cluster on which this object store is located.
      returned: success
      type: int
      sample: 2
    date_created:
      description: Date when the object store was created.
      returned: success
      type: str
      sample: "2023-02-06T16:41:48+00:00"
    id:
      description: ID of the object store.
      returned: success
      type: str
      sample: cb676a46-66fd-4dfb-b839-443f2e6c0b60
    label:
      description: Label of the object store.
      returned: success
      type: str
      sample: my object store
    region:
      description: Region in which the object store is located.
      returned: success
      type: str
      sample: ewr
    status:
      description: Status about the deployment of the object store.
      returned: success
      type: str
      sample: active
    s3_hostname:
      description: The Cluster hostname for this object storage.
      returned: success
      type: str
      sample: ewr1.vultrobjects.com
    s3_access_key:
      description: The object storage access key.
      returned: success
      type: str
      sample: 00example11223344
    s3_secret_key:
      description: The object storage secret key.
      returned: success
      type: str
      sample: 00example1122334455667788990011
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
        namespace="vultr_object_storage_info",
        resource_path="/object-storage",
        ressource_result_key_singular="object_storage",
    )

    vultr.get_result(vultr.query_list())


if __name__ == "__main__":
    main()
