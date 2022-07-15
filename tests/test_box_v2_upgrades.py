from scripts.utils import get_account, upgrade, encode_function_initializer_data
from brownie import (
    Box,
    exceptions,
    Contract,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
)
import pytest


def test_box_v2_upgrade():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_function_data = encode_function_initializer_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin.address, box_encoded_function_data, {"from": account}
    )
    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, box_v2.abi)
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})
    print("Contract Upgrade...")
    assert proxy_box.retrieve() == 0
    upgrade(account, proxy, box_v2.address, proxy_admin_contract=proxy_admin)
    increment_tx = proxy_box.increment({"from": account})
    increment_tx.wait(1)
    assert proxy_box.retrieve() == 1
