from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import os.path

import ansible_collections.vultr.cloud.plugins.inventory.vultr as module_under_test
import pytest
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.inventory.data import InventoryData
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
from ansible_collections.vultr.cloud.plugins.inventory.vultr import \
    InventoryModule

default_options = {
    "api_endpoint": "https://test.api.vultr.com/v2",
    "api_key": "TEST_VULTR_API_KEY",
    "api_results_per_page": 100,
    "api_timeout": 60,
    "attributes": ["id", "region", "label", "plan", "hostname", "main_ip", "tags", "internal_ip"],
    "filters": [],
    "plugin": "vultr.cloud.vultr",
    "variable_prefix": "vultr_",
    "validate_certs": True,
}


def get_option(opts):
    def func(option):
        return opts.get(option, False)

    return func


def load_fixture(filename):
    return open(os.path.join(os.path.dirname(__file__), "fixtures", filename))


def get_paginated_json_response(url):
    cursor = "page1"
    if "&cursor=" in url:
        cursor = "page2"
    return load_fixture("vultr_inventory_{0}.json".format(cursor))


@pytest.fixture()
def inventory():
    r = InventoryModule()
    r.inventory = InventoryData()
    r.templar = Templar(loader=DataLoader())
    return r


@pytest.fixture()
def instances():
    return json.load(load_fixture("vultr_inventory.json"))


def test_verify_file_no_filename(inventory):
    assert inventory.verify_file("") is False


def test_verify_file_valid_filename(tmp_path, inventory):
    valid_config = tmp_path / "vultr.yaml"
    valid_config.touch()
    assert inventory.verify_file(str(valid_config)) is True


def test_verify_file_invalid_filename(tmp_path, inventory):
    invalid_config = tmp_path / "vultr.notyaml"
    invalid_config.touch()
    assert inventory.verify_file(str(invalid_config)) is False


@pytest.mark.parametrize("cache_option", [True, False])
def test_parse(tmp_path, inventory, mocker, cache_option):
    inventory_file = tmp_path / "vultr.yaml"
    inventory_file.write_text("---\nplugin: vultr.cloud.vultr")

    plugin_cache_dir = tmp_path / "cache"

    opts = default_options.copy()
    opts.update(
        {
            "cache": cache_option,
            "cache_connection": plugin_cache_dir,
            "cache_plugin": "jsonfile",
        }
    )
    inventory.get_option = mocker.MagicMock(side_effect=get_option(opts))

    mocker.patch("{0}.Request".format(module_under_test.__name__))
    RequestMock = module_under_test.Request

    req = RequestMock.return_value
    req.get.side_effect = get_paginated_json_response

    inventory._redirected_names = ["vultr.cloud.vultr", "vultr"]
    inventory._load_name = "vultr.cloud.vultr"
    inventory.parse(inventory.inventory, DataLoader(), str(inventory_file))

    if cache_option:
        RequestMock.reset_mock()

        inventory.parse(inventory.inventory, DataLoader(), str(inventory_file))
        RequestMock.assert_not_called()

    assert len(inventory.inventory.hosts.items()) > 0


def test_parse_non_plugin_invalid_parameter(inventory):
    try:
        inventory.parse(None, DataLoader(), "")
        assert False, "Expected parse() to raise AnsibleParserError"
    except AnsibleParserError:
        pass


def test_get_instances(inventory, mocker):
    inventory.get_option = mocker.MagicMock(side_effect=get_option(default_options))

    mocker.patch("{0}.Request".format(module_under_test.__name__))
    RequestMock = module_under_test.Request

    req = RequestMock.return_value
    req.get.side_effect = get_paginated_json_response

    instance_list = inventory._get_instances()
    assert len(instance_list) == 8


def test_get_instances_invalid_api_key(inventory, mocker):
    inventory.get_option = mocker.MagicMock(side_effect=get_option(default_options))

    mocker.patch("{0}.Request".format(module_under_test.__name__))
    RequestMock = module_under_test.Request

    req = RequestMock.return_value
    req.get.return_value = load_fixture("unauthorized_vultr_inventory.json")

    try:
        inventory._get_instances()
        assert False, "Expected _get_instances() to raise AnsibleParserError"
    except AnsibleParserError:
        pass


def test_get_instances_templated_api_key(inventory, mocker):
    opts = default_options.copy()
    opts.update({"api_key": '{{ lookup("random_choice", "TEST_VULTR_API_KEY") }}'})

    inventory.get_option = mocker.MagicMock(side_effect=get_option(opts))

    mocker.patch("{0}.Request".format(module_under_test.__name__))
    RequestMock = module_under_test.Request

    req = RequestMock.return_value
    req.get.return_value = load_fixture("empty_vultr_inventory.json")

    inventory._get_instances()

    req_headers = RequestMock.call_args.kwargs["headers"]
    assert req_headers.get("Authorization") == "Bearer TEST_VULTR_API_KEY"


def test_populate(inventory, instances, mocker):
    inventory.get_option = mocker.MagicMock(side_effect=get_option(default_options))
    inventory._populate(instances)

    assert len(inventory.inventory.hosts.items()) > 0


def test_populate_with_empty_response(inventory, mocker):
    inventory.get_option = mocker.MagicMock(side_effect=get_option(default_options))

    mocker.patch("{0}.Request".format(module_under_test.__name__))
    RequestMock = module_under_test.Request

    req = RequestMock.return_value
    req.get.return_value = load_fixture("empty_vultr_inventory.json")

    inventory._populate(inventory._get_instances())

    assert len(inventory.inventory.hosts.items()) == 0


def test_populate_host_variables(inventory, instances, mocker):
    inventory.get_option = mocker.MagicMock(side_effect=get_option(default_options))
    inventory._populate(instances)

    windows_host = inventory.inventory.get_host("windows-guest")
    assert windows_host.vars["vultr_plan"] == "vhp-1c-2gb-amd"
    assert windows_host.vars["vultr_region"] == "fra"
    assert windows_host.vars["vultr_id"] == "2db0bb8c-9d83-4e62-86ef-b3d999960d72"


def test_populate_host_variables_with_filters(inventory, instances, mocker):
    opts = default_options.copy()
    opts.update({"filters": ['vultr_id == "37d67f9f-17f0-4c56-879b-507355dc5174"']})

    inventory.get_option = mocker.MagicMock(side_effect=get_option(opts))
    inventory._populate(instances)

    unfiltered_host = inventory.inventory.get_host("openbsd-guest")
    filtered_host = inventory.inventory.get_host("debian-guest")

    for host in inventory.inventory.hosts:
        this_host = inventory.inventory.get_host(host)
        assert "vultr_id" in this_host.vars
        assert this_host.vars["vultr_id"] == "37d67f9f-17f0-4c56-879b-507355dc5174"

    assert len(inventory.inventory.hosts.items()) == 1
    assert unfiltered_host.vars["vultr_plan"] == "voc-g-1c-4gb-30s-amd"
    assert filtered_host is None


def test_passes_filters_invalid_filter_not_strict(inventory):
    try:
        inventory._passes_filters(["invalid filter"], {}, "host", False)
        assert True
    except AnsibleError:
        assert False, "unexpected AnsibleError from _passes_filters()"


def test_passes_filters_invalid_filter_strict(inventory):
    try:
        inventory._passes_filters(["invalid filter"], {}, "host", True)
        assert False, "expected _passes_filters() to raise AnsibleError"
    except AnsibleError:
        pass
