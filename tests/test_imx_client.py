from imx_objects import *
from utils import SafeNumber
import time


class TestUtility:
    def test_okay_user_registered(self, client):
        res = client.register()
        res = res.result()
        assert res["status"] == "success"

    def test_okay_project_created(self, client):
        params = CreateProjectParams(
            name="test_proj", company_name="test_company", contact_email="test@test.com"
        )
        res = client.create_project(params)
        res = res.result()

        assert res["status"] == "success"
        assert res["result"]["id"]

    def test_okay_collection_created_and_updated(self, client, project_id, random_addr):
        return

        # imx now returns an error when the contract_addr does not contain byte code
        # therefore one can't use random_addr anymore
        params = CreateCollectionParams(
            name="test",
            contract_addr=random_addr,
            owner_public_key="test",
            project_id=project_id,
            metadata_api_url="https://test.com",
            description="test",
            icon_url="https://test.com/icon",
            collection_image_url="https://test.com/collection_image",
        )
        res = client.create_collection(params)
        res = res.result()

        assert res["status"] == "success"
        assert res["result"]["address"] == random_addr

        params = UpdateCollectionParams(name="test2", contract_addr=random_addr)
        res = client.update_collection(params)
        res = res.result()

        # TODO somehow imx returns the wrong values, but they have been updated
        # normally, just retry and see what happens
        res = client.update_collection(params)
        res = res.result()

        assert res["status"] == "success"
        assert res["result"]["name"] == "test2"

    # TODO
    def test_okay_metadata_schema_added(self):
        pass


class TestTransfer:
    def get_balance(self, client, addr):
        res = client.db.balances(addr)
        return int(res["result"][0]["balance"])

    def test_okay_simple_eth(self, client, acc1, acc2):
        params = TransferParams(
            sender=acc1.addr,
            receiver=acc2.addr,
            token=ETH(quantity="0.00001"),
        )
        res = client.transfer(params)
        res = res.result()

        assert res["status"] == "success"
        assert res["result"]["transfer_id"]

    def test_okay_simple_erc721(self, client, token_id, acc1, acc2, contract_addr):
        params = TransferParams(
            sender=acc1.addr,
            receiver=acc2.addr,
            token=ERC721(token_id=token_id, contract_addr=contract_addr),
        )
        res = client.transfer(params)
        res = res.result()

        assert res["status"] == "success"
        assert res["result"]["transfer_id"]

    # TODO
    def test_okay_simple_erc20(self, client, acc1, acc2):
        pass

    def test_fails_not_enough_balance(self, client, acc1, acc2):
        params = TransferParams(
            sender=acc1.addr, receiver=acc2.addr, token=ETH(quantity=100000)
        )
        res = client.transfer(params, max_retries=1)
        res = res.result()

        assert res["status"] == "error"
        assert "insufficient balance" in res["result"]


class TestMint:
    def random_token_id(self):
        import random

        return random.randint(0, 1000000000000000000000000000000)

    def test_okay_multiple_targets_and_override_global_royalties(
        self, client, acc1, acc2, acc3, contract_addr
    ):
        tid1 = self.random_token_id()
        tid2 = self.random_token_id()
        tid3 = self.random_token_id()

        tid1 = self.random_token_id()

        params = MintParams(
            contract_addr=contract_addr,
            royalties=[Royalty(recipient=acc1.addr, percentage=1.0)],
            targets=[
                MintTarget(
                    addr=acc2.addr,
                    tokens=[
                        MintableToken(
                            id=tid1,
                            blueprint="1",
                            # tests override global royalties
                            royalties=[Royalty(recipient=acc2.addr, percentage=2.0)],
                        ),
                        # tests multiple token mints at a time
                        MintableToken(id=tid2, blueprint="2"),
                    ],
                ),
                # tests multiple user targets at a time
                MintTarget(
                    addr=acc3.addr, tokens=[MintableToken(id=tid3, blueprint="3")]
                ),
            ],
        )
        res = client.mint(params, max_retries=1)
        res = res.result()

        assert res["status"] == "success"

    def test_fails_unregistered_contract_addr(
        self, client, acc1, unregistered_contract_addr
    ):
        params = MintParams(
            contract_addr=unregistered_contract_addr,
            targets=[
                MintTarget(
                    addr=acc1.addr,
                    tokens=[
                        MintableToken(
                            id=self.random_token_id(),
                            blueprint="1",
                        ),
                    ],
                ),
            ],
        )
        res = client.mint(params, max_retries=1)
        res = res.result()

        assert res["status"] == "error"
        assert "no contract code at given address" in res["result"]

    def test_fails_duplicate_asset(self, client, contract_addr, acc1):
        params = MintParams(
            contract_addr=contract_addr,
            targets=[
                MintTarget(
                    addr=acc1.addr,
                    tokens=[
                        MintableToken(
                            id=0,
                            blueprint="0",
                        )
                    ],
                )
            ],
        )
        res = client.mint(params, max_retries=1)
        res = res.result()

        assert res["status"] == "error"
        assert "asset, duplicate id" in res["result"]


class TestBurn:
    def test_okay_burn(self, client, acc1, contract_addr, minted_nft_id):
        # sends the nft to the burn addr, which is <TODO>
        params = BurnParams(
            sender=acc1.addr,
            token=ERC721(token_id=minted_nft_id, contract_addr=contract_addr),
        )
        res = client.burn(params)
        res = res.result()

        assert res["status"] == "success"
        assert res["result"]["transfer_id"]


class TestWithdrawal:
    def test_okay_prepare(self, client, acc1):
        params = PrepareWithdrawalParams(
            sender=acc1.addr, token=ETH(quantity="0.0000001")
        )
        res = client.prepare_withdrawal(params)
        res = res.result()

        assert res["status"] == "success"
        assert res["result"]["withdrawal_id"]

    def test_okay_complete_withdrawal(self, client, acc1):
        # this test is a bit weird, since it can only run if we have
        # run prepare_withdrawal before that

        balance = client.db.balances(acc1.addr)
        withdrawable = int(balance["result"][0]["withdrawable"])
        if not withdrawable:
            msg = "[WARNING] 'test_okay_complete_withdrawal', can't run since there is "
            msg += "no asset to withdraw."
            print(msg)
            return

        params = CompleteWithdrawalParams(token=ETH())
        res = client.complete_withdrawal(params)
        res = res.result()

        # always returns success so no help here
        assert res["status"] == "success"
        # TODO the result with each withdrawal a new "random" address dunno why yet tho.
        # assert res["result"] == acc1.addr


class TestTrading:
    def test_okay_order_sell(self, client, acc1, minted_nft_id, contract_addr):
        # imx db takes a bit time after the asset was minted
        time.sleep(1)
        params = CreateOrderParams(
            sender=acc1.addr,
            token_sell=ERC721(token_id=minted_nft_id, contract_addr=contract_addr),
            token_buy=ETH(quantity="0.000001"),
        )
        res = client.create_order(params)
        res = res.result()

        assert res["status"] == "success"
        assert res["result"]["order_id"]

    def test_okay_order_buy(self):
        # TODO I think this didn't work for serveral people, just let it here as
        # a reminder to test at some point
        pass
