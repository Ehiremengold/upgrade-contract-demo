from brownie import Box, Contract, ProxyAdmin, TransparentUpgradeableProxy
from scripts.utils import get_account, encode_function_initializer_data
import time


def test_can_delegate_call():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encode_function_intializer = encode_function_initializer_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin, box_encode_function_intializer, {"from": account}
    )
    proxy_box = Contract.from_abi("Box", proxy.address, box.abi)
    assert proxy_box.retrieve() == 0
    transaction = proxy_box.store(23, {"from": account})
    transaction.wait(1)
    assert proxy_box.retrieve() == 23
