#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2026, Joel Wilson <jwilson@vultr.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: dns_record_info
short_description: Gather information about the Vultr DNS records
description:
  - Gather information about DNS records of a domain.
version_added: "1.15.0"
author: "Joel Wilson (@jwilson)"
options:
  domain:
    description:
      - The domain the records are related to.
    required: true
    type: str
  name:
    description:
      - Filter by record name.
      - The value is relative to the domain, e.g. C(www) and not C(www.example.com).
      - An empty value matches the domain apex.
    type: str
  type:
    description:
      - Filter by record type.
    choices:
      - A
      - AAAA
      - CNAME
      - NS
      - MX
      - SRV
      - TXT
      - CAA
      - SSHFP
    aliases: [ record_type ]
    type: str
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
- name: Gather Vultr DNS records information
  vultr.cloud.dns_record_info:
    domain: example.com
  register: result

- name: Print the gathered information
  ansible.builtin.debug:
    var: result.vultr_dns_record_info

- name: Gather the A records for a single name
  vultr.cloud.dns_record_info:
    domain: example.com
    name: www
    type: A
  register: result
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
vultr_dns_record_info:
  description: Response from Vultr API as list.
  returned: success
  type: list
  contains:
    id:
      description: The ID of the DNS record.
      returned: success
      type: str
      sample: cb676a46-66fd-4dfb-b839-443f2e6c0b60
    name:
      description: The name of the DNS record.
      returned: success
      type: str
      sample: www
    type:
      description: The type of the DNS record.
      returned: success
      type: str
      sample: A
    data:
      description: Data of the DNS record.
      returned: success
      type: str
      sample: 10.10.10.10
    priority:
      description: Priority of the DNS record.
      returned: success
      type: int
      sample: 10
    ttl:
      description: Time to live of the DNS record.
      returned: success
      type: int
      sample: 300
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.vultr_v2 import AnsibleVultr, vultr_argument_spec

RECORD_TYPES = ["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SRV", "CAA", "SSHFP"]


class AnsibleVultrDnsRecordInfo(AnsibleVultr):
    def configure(self):
        # Set the domain to the resource path
        self.resource_path = self.resource_path % self.module.params.get("domain")

    def query_list(self, path=None, result_key=None):
        query_params = dict()
        for param in ("name", "type"):
            value = self.module.params.get(param)
            if value is not None:
                query_params[param] = value

        return super(AnsibleVultrDnsRecordInfo, self).query_list(
            path=path,
            result_key=result_key,
            query_params=query_params,
        )


def main():
    argument_spec = vultr_argument_spec()
    argument_spec.update(
        dict(
            domain=dict(type="str", required=True),
            name=dict(type="str"),
            type=dict(type="str", choices=RECORD_TYPES, aliases=["record_type"]),
        )  # type: ignore
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    vultr = AnsibleVultrDnsRecordInfo(
        module=module,
        namespace="vultr_dns_record_info",
        resource_path="/domains/%s/records",
        resource_result_key_singular="record",
    )

    vultr.get_result(vultr.query_list())


if __name__ == "__main__":
    main()
