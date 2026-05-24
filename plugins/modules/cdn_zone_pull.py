#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2026, Rene Moser <mail@renemoser.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: cdn_zone_pull
short_description: Manages CDN pull zones on Vultr
description:
  - Create, update and remove CDN pull zones.
version_added: "1.15.0"
author: "Rene Moser (@resmo)"
options:
  label:
    description:
      - The label of the CDN pull zone.
    required: true
    aliases: [ name ]
    type: str
  origin_scheme:
    description:
      - URI scheme of the pull origin domain.
      - Required if I(state=present).
    choices: [ http, https ]
    type: str
  origin_domain:
    description:
      - Origin domain from which content is pulled.
      - Required if I(state=present).
    type: str
  vanity_domain:
    description:
      - Optional domain used to access cached files.
    type: str
  ssl_cert:
    description:
      - Base64 encoded SSL certificate content for I(vanity_domain).
    type: str
  ssl_cert_key:
    description:
      - Base64 encoded SSL private key content for I(vanity_domain).
    type: str
  cors:
    description:
      - Enable CORS support.
    type: bool
  gzip:
    description:
      - Enable Gzip compression.
    type: bool
  block_ai:
    description:
      - Block AI bots.
    type: bool
  block_bad_bots:
    description:
      - Block potentially malicious bots.
    type: bool
  regions:
    description:
      - Regions to serve traffic from.
      - Applied during updates.
    type: list
    elements: str
  state:
    description:
      - State of the CDN pull zone.
    default: present
    choices: [ present, absent ]
    type: str
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
- name: Ensure a CDN pull zone is present
  vultr.cloud.cdn_zone_pull:
    label: my-pull-zone
    origin_scheme: https
    origin_domain: www.vultr.com
    gzip: true

- name: Ensure a CDN pull zone is absent
  vultr.cloud.cdn_zone_pull:
    label: my-pull-zone
    state: absent
"""

RETURN = """
---
vultr_api:
  description: Response from Vultr API with a few additions/modification.
  returned: success
  type: dict
vultr_cdn_zone_pull:
  description: Response from Vultr API.
  returned: success
  type: dict
  contains:
    id:
      description: ID of the CDN pull zone.
      returned: success
      type: str
    label:
      description: Label of the CDN pull zone.
      returned: success
      type: str
    status:
      description: Current CDN pull zone status.
      returned: success
      type: str
    origin_scheme:
      description: URI scheme of the origin domain.
      returned: success
      type: str
    origin_domain:
      description: Origin domain used by the pull zone.
      returned: success
      type: str
    cdn_url:
      description: Generated CDN URL.
      returned: success
      type: str
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.vultr_v2 import AnsibleVultr, vultr_argument_spec


def main():
    argument_spec = vultr_argument_spec()
    argument_spec.update(
        dict(
            label=dict(type="str", required=True, aliases=["name"]),
            origin_scheme=dict(type="str", choices=["http", "https"]),
            origin_domain=dict(type="str"),
            vanity_domain=dict(type="str"),
            ssl_cert=dict(type="str", no_log=True),
            ssl_cert_key=dict(type="str", no_log=True),
            cors=dict(type="bool"),
            gzip=dict(type="bool"),
            block_ai=dict(type="bool"),
            block_bad_bots=dict(type="bool"),
            regions=dict(type="list", elements="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        )  # type: ignore
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[
            ("state", "present", ["origin_scheme", "origin_domain"]),
        ],
        supports_check_mode=True,
    )

    vultr = AnsibleVultr(
        module=module,
        namespace="vultr_cdn_zone_pull",
        resource_path="/cdns/pull-zones",
        ressource_result_key_singular="pull_zone",
        ressource_result_key_plural="pull_zones",
        resource_create_param_keys=[
            "label",
            "origin_scheme",
            "origin_domain",
            "vanity_domain",
            "ssl_cert",
            "ssl_cert_key",
            "cors",
            "gzip",
            "block_ai",
            "block_bad_bots",
        ],
        resource_update_param_keys=[
            "label",
            "vanity_domain",
            "ssl_cert",
            "ssl_cert_key",
            "cors",
            "gzip",
            "block_ai",
            "block_bad_bots",
            "regions",
        ],
        resource_key_name="label",
        resource_update_method="PUT",
    )

    if module.params.get("state") == "absent":  # type: ignore
        vultr.absent()
    else:
        vultr.present()


if __name__ == "__main__":
    main()
