from sys import implementation
from scripts.utils import get_account, encode_function_initializer_data, upgrade
from brownie import (
    config,
    network,
    Box,
    BoxV2,
    Contract,
    ProxyAdmin,
    TransparentUpgradeableProxy,
)
import time


def main():
    account = get_account()

    # implementation contract
    box = Box.deploy(
        {"from": account},
        publish_source=True,
    )

    # proxy admin
    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
        publish_source=True,
    )

    box_encoded_function_intializer = encode_function_initializer_data()

    # proxy
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_function_intializer,
        {"from": account, "gas_limit": 1000000},
        publish_source=True,
    )
    print(f"Proxy has been created at {proxy}, you can now upgrade to v2!")
    # proxy contract
    proxy_box = Contract.from_abi("Box", proxy.address, box.abi)
    transaction = proxy_box.store(2, {"from": account})
    transaction.wait(1)

    # new implementation
    box_v2 = BoxV2.deploy(
        {"from": account},
        publish_source=True,
    )
    upgrade_transaction = upgrade(account, proxy, box_v2.address, proxy_admin)
    print("upgrading proxy")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, box_v2.abi)
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve())
