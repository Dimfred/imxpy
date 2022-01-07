class TestRegistration:
    def test_okay_is_registered(self, client, acc1):
        assert client.db.is_registered(acc1.addr)

    def test_fail_is_registered(self, client, unregistered_addr):
        assert not client.db.is_registered(unregistered_addr)


class TestApplications:
    def test_okay_list_applications(self, client):
        res = client.db.applications()

        assert res[0]["id"]

    def test_okay_application_details(self, client):
        gog_id = "12f2d631-db48-8891-350c-c74647bb5b7f"
        res = client.db.application(gog_id)

        assert res["id"] == gog_id
        assert res["name"] == "Guilds Of Guardians"
        assert res["created_at"] == "2021-07-02T02:54:02.592523Z"


class TestAssets:
    def test_okay_list_assets(self, client):
        res = client.db.assets(page_size=10)

        assert res["result"][0]["token_address"]

    def test_okay_asset_details(self, client):
        token_id = "1081884248542"
        contract_addr = "0x21a8eba2687c99f5f67093b019bd8d9252b47638"

        res = client.db.asset(token_id, contract_addr)

        assert res["token_address"]


class TestBalances:
    def test_okay_as_wei(self, client, acc1):
        res = client.db.balances(acc1.addr)
        assert int(res["result"][0]["balance"]) > 800000

    def test_okay_token_balance(self, client, acc1, erc20_contract_addr):
        res = client.db.balances(acc1.addr, erc20_contract_addr)

        assert res["symbol"] == "GODS"
        assert res["balance"] == "0"


class TestCollections:
    def test_okay_list_collections(self, client):
        res = client.db.collections()

        assert res["result"][0]["address"]

    def test_okay_collection_details(self, client, contract_addr):
        res = client.db.collection(contract_addr)

        assert res["project_id"] == 864

    def test_okay_collection_filters(self, mainnet_client, gods_unchained_addr):
        res = mainnet_client.db.collection_filters(gods_unchained_addr)

        assert res

    def test_okay_collection_metadata_schema(self, client, contract_addr):
        res = client.db.collection_metadata_schema(contract_addr)

        assert any(item["name"] == "test" for item in res)


class TestDeposits:
    def test_okay_list_deposits(self, client):
        res = client.db.deposits()

        assert res["result"][0]["transaction_id"]

    def test_okay_deposit_details(self, client):
        res = client.db.deposit(49905)

        assert res["transaction_id"] == 49905


class TestOrders:
    def test_okay_list_orders(self, client):
        res = client.db.orders()

        assert res["result"][0]["order_id"]

    def test_okay_order_details(self, client):
        res = client.db.order(752)

        assert res["order_id"] == 752


class TestTransfers:
    def test_okay_list_transfers(self, client):
        res = client.db.transfers()

        assert res["result"][0]["transaction_id"]

    def test_okay_transfer_details(self, client):
        res = client.db.transfer(50314)

        assert res["transaction_id"] == 50314


class TestWithdrawals:
    def test_okay_list_withdrawals(self, client):
        res = client.db.withdrawals()
        print(res)
        # assert

    # def test_okay_withdrawal_details(self, client):
    #     res = client.db.withdrawal()

    #     assert res[""] ==

# TODO not working?
# class TestSnapshot:
#     def test_okay_snapshot(self, mainnet_client, gods_unchained_addr):
#         res = mainnet_client.db.snapshot(gods_unchained_addr)

#         print(res)

class TestTokens:
    def test_okay_list_tokens(self, client):
        res = client.db.tokens()

        assert res["result"][0]["name"]

    def test_okay_token_details(self, client):
        res = client.db.token("0x4c04c39fb6d2b356ae8b06c47843576e32a1963e")

        assert res["symbol"] == "GODS"
