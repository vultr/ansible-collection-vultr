#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2025, Garrett Haughawout Garrett.james.haughawout@gmail.com
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: load_balancer
short_description: Manages load balancers on Vultr
description:
  - Create, update, or delete load balancers on Vultr.
version_added: "1.13.0"
author:
  - "Garrett Haughawout (@ghaughawout)"
options:
  label:
    description:
      - The label for your Load Balancer.
    type: str
    required: true
    aliases: [ name ]
  region:
    description:
      - Region where the load balancer will be created.
    required: true
    type: str
  state:
    description:
      - State of the load balancer.
    default: present
    choices: [ present, absent ]
    type: str
  forwarding_rules:
    description:
      - An array of forwarding rule objects.
    type: list
    elements: dict
    suboptions:
      frontend_protocol:
        description:
          - Protocol on the frontend.
        required: true
        type: str
      frontend_port:
        description:
          - Port on the frontend.
        required: true
        type: int
      backend_protocol:
        description:
          - Protocol on the backend.
        required: true
        type: str
      backend_port:
        description:
          - Port on the backend.
        required: true
        type: int
  balancing_algorithm:
    description:
      - The balancing algorithm.
    type: str
    choices: [ roundrobin, leastconn ]
    default: roundrobin
  ssl_redirect:
    description:
      - If true, this will redirect all HTTP traffic to HTTPS.
      - You must have an HTTPS rule and SSL certificate installed on the load balancer to enable this option.
    type: bool
  http2:
    description:
      - If true, this will enable HTTP2 traffic.
      - You must have an HTTPS forwarding rule combo (HTTPS -> HTTPS) to enable this option.
    type: bool
  http3:
    description:
      - If true, this will enable HTTP3/QUIC traffic.
      - You must have HTTP2 enabled.
    type: bool
  nodes:
    description:
      - The number of nodes to add to the load balancer (1-99), must be an odd number. Defaults to 1.
    type: int
    default: 1
  timeout:
    description:
      - The maximum time allowed for the connection to remain inactive before timing out in seconds. Defaults to 600.
    type: int
    default: 600
  health_check:
    description:
      - The health check configuration.
    type: dict
    suboptions:
      protocol:
        description:
          - Protocol used for health checks.
        type: str
      port:
        description:
          - Port used for health checks.
        type: int
      path:
        description:
          - Path used for health checks.
        type: str
      check_interval:
        description:
          - Interval between health checks in seconds.
        type: int
      response_timeout:
        description:
          - Timeout for health check responses in seconds.
        type: int
      unhealthy_threshold:
        description:
          - Number of failed health checks before marking as unhealthy.
        type: int
      healthy_threshold:
        description:
          - Number of successful health checks before marking as healthy.
        type: int
  proxy_protocol:
    description:
      - If true, you must configure backend nodes to accept Proxy protocol.
    type: bool
    default: false
  sticky_session:
    description:
      - Enables sticky sessions for your load balancer when a cookie_name is provided.
    type: dict
  instances:
    description:
      - Array of Instance IDs to attach to this Load Balancer. Instances will be attached or detached to match your array.
    type: list
    elements: str
  vpc:
    description:
      - ID of the VPC you wish to use. If omitted, defaults to the public network.
    type: str
  firewall_rules:
    description:
      - An array of firewall rule objects.
    type: list
    elements: dict
  auto_ssl:
    description:
      - The Auto SSL configuration. Must be using Vultr DNS for Auto SSL.
    type: dict
    suboptions:
      domain_zone:
        description:
          - The domain zone (ex. example.com)
        type: str
      domain_sub:
        description:
          - Subdomain to append to the domain zone
        type: str
  global_regions:
    description:
      - Array of Region ids to deploy child Load Balancers to.
    type: list
    elements: str
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
---
- name: Create a basic load balancer
  vultr.cloud.load_balancer:
    label: "example-lb"
    region: "ewr"
    forwarding_rules:
      - frontend_protocol: "http"
        frontend_port: 80
        backend_protocol: "http"
        backend_port: 80
      - frontend_protocol: "https"
        frontend_port: 443
        backend_protocol: "https"
        backend_port: 443
    balancing_algorithm: "roundrobin"
    ssl_redirect: true
    http2: true
    http3: false
    nodes: 1
    timeout: 600
    health_check:
      protocol: "http"
      port: 80
      path: "/"
      check_interval: 15
      response_timeout: 5
      unhealthy_threshold: 3
      healthy_threshold: 2
    proxy_protocol: false
    sticky_session: {}
    instances: []
    vpc: null
    firewall_rules: []
    auto_ssl: {}
    global_regions: []
    state: present

- name: Delete a load balancer
  vultr.cloud.load_balancer:
    label: "example-lb"
    region: "ewr"
    state: absent
"""

RETURN = """
---
vultr_api:
  description: Response from Vultr API with a few additions/modification.
  returned: success
  type: dict
  contains:
    api_account:
      description: Account used in the ini file to select the key.
      returned: success
      type: str
      sample: default
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
vultr_load_balancer:
  description: Response from Vultr API.
  returned: success
  type: dict
  contains:
    id:
      description: Unique identifier for the load balancer.
      type: str
      sample: "cb676a46-66fd-4dfb-b839-443f2e6c0b60"
    date_created:
      description: Date and time when the load balancer was created.
      type: str
      sample: "2020-10-10T01:56:20+00:00"
    region:
      description: Region code where the load balancer is deployed.
      type: str
      sample: "ewr"
    label:
      description: Name/label of the load balancer.
      type: str
      sample: "Example Load Balancer"
    status:
      description: Current status of the load balancer.
      type: str
      sample: "active"
    ipv4:
      description: IPv4 address assigned to the load balancer.
      type: str
      sample: "192.0.2.123"
    ipv6:
      description: IPv6 address assigned to the load balancer.
      type: str
      sample: "2001:0db8:5:4973:ffff:ffff:ffff:ffff"
    generic_info:
      description: Additional generic information about the load balancer.
      type: dict
    health_check:
      description: Health check configuration for the load balancer.
      type: dict
    has_ssl:
      description: Whether SSL is enabled.
      type: bool
      sample: false
    http2:
      description: Whether HTTP/2 is enabled.
      type: bool
      sample: false
    http3:
      description: Whether HTTP/3 is enabled.
      type: bool
      sample: false
    nodes:
      description: Number of nodes in the load balancer.
      type: int
      sample: 1
    forwarding_rules:
      description: List of forwarding rules.
      type: list
      elements: dict
    firewall_rules:
      description: List of firewall rules.
      type: list
      elements: dict
    instances:
      description: List of instances attached to the load balancer.
      type: list
      elements: str
    node_ips:
      description: IP addresses of the nodes.
      type: dict
    auto_ssl:
      description: Auto SSL configuration.
      type: dict
    global_regions:
      description: List of global regions for the load balancer.
      type: list
      elements: str
"""


from ansible.module_utils.basic import AnsibleModule
from ..module_utils.vultr_v2 import AnsibleVultr, vultr_argument_spec


class AnsibleVultrLoadBalancer(AnsibleVultr):
    def configure(self):
        super(AnsibleVultrLoadBalancer, self).configure()

    def create_or_update(self):
        resource = super(AnsibleVultrLoadBalancer, self).create_or_update()
        if resource:
            resource = self.wait_for_state(
                resource=resource, key="status", states=["active"]
            )
        return resource


def main():
    argument_spec = vultr_argument_spec()
    argument_spec.update(
        dict(
            label=dict(type="str", required=True, aliases=["name"]),
            region=dict(type="str", required=True),
            state=dict(type="str", choices=["present", "absent"], default="present"),
            forwarding_rules=dict(
                type="list",
                elements="dict",
                options=dict(
                    frontend_protocol=dict(type="str", required=True),
                    frontend_port=dict(type="int", required=True),
                    backend_protocol=dict(type="str", required=True),
                    backend_port=dict(type="int", required=True),
                ),
            ),
            timeout=dict(type="int", default=600),
            balancing_algorithm=dict(
                type="str",
                choices=["roundrobin", "leastconn"],
                default="roundrobin",
            ),
            ssl_redirect=dict(type="bool"),
            http2=dict(type="bool"),
            http3=dict(type="bool"),
            nodes=dict(type="int", default=1),
            health_check=dict(
                type="dict",
                options=dict(
                    protocol=dict(type="str"),
                    port=dict(type="int"),
                    path=dict(type="str"),
                    check_interval=dict(type="int"),
                    response_timeout=dict(type="int"),
                    unhealthy_threshold=dict(type="int"),
                    healthy_threshold=dict(type="int"),
                ),
            ),
            proxy_protocol=dict(type="bool", default=False),
            sticky_session=dict(type="dict"),
            instances=dict(type="list", elements="str"),
            vpc=dict(type="str"),
            firewall_rules=dict(type="list", elements="dict"),
            auto_ssl=dict(
                type="dict",
                options=dict(
                    domain_zone=dict(type="str"),
                    domain_sub=dict(type="str"),
                ),
            ),
            global_regions=dict(type="list", elements="str"),
        )
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    vultr = AnsibleVultrLoadBalancer(
        module=module,
        namespace="vultr_load_balancer",
        resource_path="/load-balancers",
        ressource_result_key_singular="load_balancer",
        resource_create_param_keys=[
            "region",
            "balancing_algorithm",
            "ssl_redirect",
            "http2",
            "http3",
            "nodes",
            "proxy_protocol",
            "timeout",
            "label",
            "health_check",
            "forwarding_rules",
            "firewall_rules",
            "vpc",
            "global_regions",
        ],
        resource_update_param_keys=[
            "ssl",
            "sticky_session",
            "forwarding_rules",
            "firewall_rules",
            "health_check",
            "proxy_protocol",
            "timeout",
            "ssl_redirect",
            "http2",
            "http3",
            "nodes",
            "balancing_algorithm",
            "instances",
            "vpc",
            "auto_ssl",
            "global_regions",
        ],
        resource_key_name="label",
    )

    if module.params.get("state") == "absent":
        vultr.absent()
    else:
        vultr.present()


if __name__ == "__main__":
    main()
