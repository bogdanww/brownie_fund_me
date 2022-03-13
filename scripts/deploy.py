from brownie import FundMe, MockV3Aggregator, network, config
from scripts.fund_and_withdraw import fund
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKHAINE_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract

    # if we are on a persistent network like rinkeby, use the accociated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKHAINE_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
