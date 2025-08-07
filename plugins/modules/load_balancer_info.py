#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2025, Garrett Haughawout <garrett.james.haughawout@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: load_balancer_info
short_description: Get information about Vultr load balancers
version_added: "1.13.0"
description:
  - Retrieve details about load balancers on Vultr.
author:
  - "Garrett Haughawout (@ghaughawout)"
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
---
- name: Get Vultr load balancer information
  vultr.cloud.load_balancer_info:
  register: result

- name: Print the information
  ansible.builtin.debug:
  var: result.vultr_load_balancer_info
"""

RETURN = """
---
vultr_api:
  description: Response from Vultr API with additional details.
  returned: success
  type: dict
  contains:
    id:
      description: Unique ID of the load balancer.
      returned: success
      type: str
      sample: "cb67a646-66fd-4dfb-b839-443f2e6c0b60"
    date_created:
      description: Date and time when the load balancer was created.
      returned: success
      type: str
      sample: "2020-10-10T01:56:20+00:00"
    region:
      description: Region of the load balancer.
      returned: success
      type: str
      sample: "ewr"
    label:
      description: Label of the load balancer.
      returned: success
      type: str
      sample: "Example Load Balancer"
    status:
      description: Status of the load balancer.
      returned: success
      type: str
      sample: "pending"
    ipv4:
      description: IPv4 address of the load balancer.
      returned: success
      type: str
      sample: "192.0.2.1"
    ipv6:
      description: IPv6 address of the load balancer.
      returned: success
      type: str
      sample: "2001:db8::1"
    generic_info:
      description: Generic information about the load balancer.
      returned: success
      type: dict
    health_check:
      description: Health check configuration for the load balancer.
      returned: success
      type: dict
    has_ssl:
      description: Whether SSL is enabled for the load balancer.
      returned: success
      type: bool
      sample: false
    http2:
      description: Whether HTTP/2 is enabled.
      returned: success
      type: bool
      sample: false
    http3:
      description: Whether HTTP/3 is enabled.
      returned: success
      type: bool
      sample: false
    nodes:
      description: Number of nodes in the load balancer.
      returned: success
      type: int
      sample: 1
    forwarding_rules:
      description: List of forwarding rules for the load balancer.
      returned: success
      type: list
      elements: dict
    firewall_rules:
      description: Firewall rules applied to the load balancer.
      returned: success
      type: list
      elements: dict
    instances:
      description: List of instances attached to the load balancer.
      returned: success
      type: list
      elements: str
    node_ips:
      description: List of node IPs in the load balancer.
      returned: success
      type: list
      elements: str
    auto_ssl:
      description: Auto SSL configuration for the load balancer.
      returned: success
      type: dict
    global_regions:
      description: Global regions configuration for the load balancer.
      returned: success
      type: list
      elements: str
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
        namespace="vultr_load_balancer_info",
        resource_path="/load-balancers",
        ressource_result_key_singular="load_balancer",
    )

    vultr.get_result(vultr.query_list())


if __name__ == "__main__":
    main()
