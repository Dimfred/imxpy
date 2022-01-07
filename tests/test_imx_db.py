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


# TODO
# class TestIMXDB:
#     def test_return_min_max_timestamp(client):
#         min_timestamp = utils.timestamp_from_str("2021-10-23T07:53:32.496377Z")
#         max_timestamp = utils.timestamp_from_str("2021-10-23T07:53:47.15727Z")

#         transfers = client.transfers(
#             config.user_addr, min_timestamp=min_timestamp, max_timestamp=max_timestamp
#         )
#         transfers = transfers["result"]

#         assert len(transfers) == 2


#     def test_balances(config):
#         client = IMXClient("test")
#         res = client.balances(config.user_addr)

#         assert res["result"][0]["balance"]


#     def test_assets(config):
#         client = IMXClient("test")
#         res = client.assets(config.user_addr, config.token_addr)
#         pprint(res)

#         assert res


#     def test_all_assets(config):
#         client = IMXClient("test")
#         res = client.all_pages(client.assets, config.user_addr, config.token_addr)

#         assert res


#     def test_all_asset_unique(config):
#         client = IMXClient("test")
#         res = client.all_pages(
#             client.assets, config.user_addr, config.token_addr, key=lambda x: x["token_id"]
#         )

#         unique = {r["token_id"] for r in res}
#         assert len(res) == len(unique)


#     def test_all_transfers(config):
#         client = IMXClient("test")

#         res = client.all_pages(
#             client.transfers,
#             receiver=config.user_addr,
#             min_timestamp=config.min_timestamp,
#             page_size=1,
#         )

#         assert len(res) > 1


#     def test_all_transfers_unique(config):
#         client = IMXClient("test")

#         res = client.all_pages(
#             client.transfers,
#             receiver=config.user_addr,
#             min_timestamp=config.min_timestamp,
#             page_size=1,
#         )

#         unique = {r["transaction_id"] for r in res}
#         pprint(res)

#         assert len(res) == len(unique)
