#!/usr/bin/python
#
# Copyright (c) 2026, Rene Moser <mail@renemoser.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: cdn_zone_info
short_description: Gather information about Vultr CDN zones
description:
  - Gather information about Vultr CDN pull and push zones.
version_added: "1.15.0"
author:
  - "Rene Moser (@resmo)"
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
- name: Gather Vultr CDN zone information
  vultr.cloud.cdn_zone_info:
  register: result

- name: Print pull zones
  ansible.builtin.debug:
    var: result.vultr_cdn_zone_info.pull_zones

- name: Print push zones
  ansible.builtin.debug:
    var: result.vultr_cdn_zone_info.push_zones
"""

RETURN = """
---
vultr_api:
  description: Response from Vultr API with a few additions/modification.
  returned: success
  type: dict
vultr_cdn_zone_info:
  description: Response from Vultr API.
  returned: success
  type: dict
  contains:
    pull_zones:
      description: List of CDN pull zones.
      returned: success
      type: list
    push_zones:
      description: List of CDN push zones.
      returned: success
      type: list
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.vultr_v2 import AnsibleVultr, vultr_argument_spec


def main():
    argument_spec = vultr_argument_spec()

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    pull_vultr = AnsibleVultr(
        module=module,
        namespace="vultr_cdn_zone_info",
        resource_path="/cdns/pull-zones",
        ressource_result_key_singular="pull_zone",
        ressource_result_key_plural="pull_zones",
    )

    push_vultr = AnsibleVultr(
        module=module,
        namespace="vultr_cdn_zone_info",
        resource_path="/cdns/push-zones",
        ressource_result_key_singular="push_zone",
        ressource_result_key_plural="push_zones",
    )

    pull_zones = pull_vultr.query_list()
    push_zones = push_vultr.query_list()

    pull_vultr.result["vultr_cdn_zone_info"] = {
        "pull_zones": pull_zones,
        "push_zones": push_zones,
    }
    module.exit_json(**pull_vultr.result)


if __name__ == "__main__":
    main()
