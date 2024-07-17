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
module: object_storage_cluster_info
short_description: Get information about the Vultr object storage clusters
version_added: "1.14.0"
description:
  - Get infos about object storage clusters available.
author:
  - "jasites (@jasites)"
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
- name: Get Vultr object_storage_cluster infos
  vultr.cloud.object_storage_cluster_info:
  register: result

- name: Print the infos
  ansible.builtin.debug:
    var: result.vultr_object_storage_cluster_info
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
vultr_object_storage_cluster_info:
  description: Response from Vultr API as list.
  returned: success
  type: list
  contains:
    id:
      description: ID of the object storage cluster.
      returned: success
      type: int
      sample: 2
    region:
      description: Region in which the object storage cluster is located.
      returned: success
      type: str
      sample: ewr
    deploy:
      description: Status about the ability to create new object stores on this cluster.
      returned: success
      type: str
      sample: yes
    hostname:
      description: The Cluster hostname for this object storage.
      returned: success
      type: str
      sample: ewr1.vultrobjects.com
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
        namespace="vultr_object_storage_cluster_info",
        resource_path="/object-storage/clusters",
        ressource_result_key_singular="cluster",
    )

    vultr.get_result(vultr.query_list())


if __name__ == "__main__":
    main()
