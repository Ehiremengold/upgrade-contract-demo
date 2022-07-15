from codecs import encode
import eth_utils
from brownie import config, network, accounts
import time

local_dev_env = ["development", "hardhat", "ganache"]


def get_account(id=None, index=None):
    if id:
        return accounts.load(id)
    if index:
        return accounts[index]
    if network.show_active() in local_dev_env:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def encode_function_initializer_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_data = encode_function_initializer_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_function_data,
                {"from": account},
            )
            transaction.wait(1)
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address, {"from": account}
            )
            transaction.wait(1)
    else:
        if initializer:
            encoded_function_data = encode_function_initializer_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeToAndCall(
                new_implementation_address,
                encoded_function_data,
                {"from": account},
            )
            transaction.wait(1)
        else:
            transaction = proxy_admin_contract.upgradeTo(
                new_implementation_address, {"from": account}
            )
            transaction.wait(1)
    return transaction
