# Copyright 2021 dimfred.1337@web.de
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import json
from pydantic.typing import new_type_supertype
import requests as req
import datetime as dt
from urlpath import URL

from imxpy.utils import IMXTime
from imxpy import utils


class IMXDB:
    def __init__(self, net):
        if net == "test":
            self.base = URL("https://api.ropsten.x.immutable.com")
        elif net == "main":
            self.base = URL("https://api.x.immutable.com")
        else:
            raise ValueError(f"Unknown net: '{net}")

        self.urlv1 = self.base / "v1"
        self.urlv2 = self.base / "v2"

        self.applications_url = self.urlv1 / "applications"
        self.orders_url = self.urlv1 / "orders"
        self.assets_url = self.urlv1 / "assets"
        self.balances_url = self.urlv2 / "balances"
        self.collections_url = self.urlv1 / "collections"
        self.deposits_url = self.urlv1 / "deposits"
        self.mintable_token_url = self.urlv1 / "mintable-token"
        self.mints_url = self.urlv1 / "mints"
        self.claims_url = self.urlv1 / "rewards"
        self.users_url = self.urlv1 / "users"
        self.transfers_url = self.urlv1 / "transfers"
        self.withdrawals_url = self.urlv1 / "withdrawals"
        self.snapshot_url = self.urlv1 / "snapshot" / "balances"
        self.tokens_url = self.urlv1 / "tokens"
        self.trades_url = self.urlv1 / "trades"

    def application(self, id):
        return self._get(self.applications_url / id)

    def applications(
        self, *, order_by="name", direction="asc", page_size=100, cursor=""
    ):
        params = self._make_params(locals())
        return self._get(self.applications_url, params=params)

    def asset(self, token_id, contract_addr, include_fees=True):
        params = {"include_fees": True}

        return self._get(self.assets_url / contract_addr / str(token_id), params=params)

    def assets(
        self,
        *,
        user="",
        collection="",
        name="",
        metadata="",
        sell_orders=False,
        buy_orders=False,
        include_fees=True,
        updated_min_timestamp="",
        updated_max_timestamp="",
        status="imx",
        order_by="name",
        direction="asc",
        page_size=100,
        cursor="",
    ):
        params = self._make_params(locals())
        return self._get(self.assets_url, params=params)

    def balances(self, owner, token_addr=""):
        url = self.balances_url / owner
        if token_addr:
            return self._get(url / token_addr)

        return self._get(url)

    def collection(self, contract_addr):
        return self._get(self.collections_url / contract_addr)

    def collections(
        self,
        *,
        blacklist="",
        order_by="name",
        direction="asc",
        page_size=100,
        cursor="",
    ):
        params = self._make_params(locals())
        return self._get(self.collections_url, params=params)

    def collection_filters(self, contract_addr, *, page_size=100, next_page_token=""):
        params = {"page_size": page_size, "next_page_token": next_page_token}
        return self._get(
            self.collections_url / contract_addr / "filters", params=params
        )

    def collection_metadata_schema(self, contract_addr):
        return self._get(self.collections_url / contract_addr / "metadata-schema")

    def deposit(self, id):
        return self._get(self.deposits_url / str(id))

    def deposits(
        self,
        *,
        user="",
        status="",
        token_type="",
        token_id="",
        asset_id="",
        token_address="",
        token_name="",
        min_quantity="",
        max_quantity="",
        metadata="",
        order_by="",
        direction="asc",
        min_timestamp="",
        max_timestamp="",
        page_size=100,
        cursor="",
    ):
        params = self._make_params(locals())
        return self._get(self.deposits_url, params=params)

    def mintable_token(self, imx_token_id=None, token_id=None, contract_addr=None):
        if imx_token_id is not None:
            return self._get(self.urlv1 / "mintable-token" / imx_token_id)

        return self._get(self.mintable_token_url / contract_addr / str(token_id))

    def mints(self, imx_token_id):
        return self._get(self.mints_url / imx_token_id)

    def order(self, order_id):
        return self._get(self.urlv1 / "orders" / str(order_id))

    def orders(
        self,
        *,
        user="",
        sell_token_addr="",
        sell_token_type="",
        sell_token_name="",
        sell_token_id="",
        sell_asset_id="",
        sell_min_quantity="",
        sell_max_quantity="",
        sell_metadata="",
        buy_token_addr="",
        buy_token_type="",
        buy_token_name="",
        buy_token_id="",
        buy_asset_id="",
        buy_min_quantity="",
        buy_max_quantity="",
        buy_metadata="",
        include_fees=True,
        # asc / desc
        direction="asc",
        updated_min_timestamp="",
        updated_max_timestamp="",
        min_timestamp="",
        max_timestamp="",
        order_by="timestamp",
        status="active",
        page_size=100,
        cursor="",
    ):
        params = self._make_params(locals())
        return self._get(self.orders_url, params=params)

    def claims(self, addr):
        return self._get(self.claims_url / addr)

    def stark_key(self, addr):
        return self._get(self.users_url / addr)

    def is_registered(self, addr):
        res = self.stark_key(addr)
        return "accounts" in res

    def transfer(self, id):
        return self._get(self.transfers_url / str(id))

    def transfers(
        self,
        *,
        sender="",
        receiver="",
        # order_by="timestamp",
        direction="asc",
        token_type="ETH",
        token_id="",
        token_addr="",
        min_timestamp="",
        max_timestamp="",
        page_size=100,
        cursor="",
    ):
        params = self._make_params(locals())
        return self._get(self.transfers_url, params=params)

    def withdrawal(self, id):
        return self._get(self.withdrawals_url / str(id))

    # def withdrawals(self, *)

    def snapshot(self, contract_addr, page_size=100, cursor=""):
        params = {"page_size": page_size, "cursor": cursor}
        return self._get(self.snapshot_url / contract_addr, params=params)

    def token(self, token_addr=""):
        return self._get(self.tokens_url / token_addr)

    def tokens(self, addr="", symbols=""):
        params = self._make_params(locals())
        return self._get(self.tokens_url, params=params)

    def trades(
        self,
        *,
        party_a_token_type="",
        party_a_token_addr="",
        party_a_token_id="",
        party_b_token_type="",
        party_b_token_addr="",
        party_b_token_id="",
        min_timestamp="",
        max_timestamp="",
        direction="asc",
        order_by="",
        page_size=100,
        cursor="",
    ):
        params = self._make_params(locals())
        return self._get(self.trades_url, params=params)

    def _make_params(self, locals_):
        del locals_["self"]
        for k, v in list(locals_.items()):
            if not isinstance(v, bool) and not v:
                del locals_[k]
            elif k.endswith("addr"):
                del locals_[k]
                new_k = k.replace("addr", "address")
                locals_[new_k] = v
            elif k == "sender":
                del locals_[k]
                new_k = "user"
                locals_[new_k] = v
            elif k.endswith("timestamp") and isinstance(v, dt.datetime):
                locals_[k] = IMXTime.to_str(v)

        return locals_

    def _get(self, url, params=None):
        res = req.get(url, params=params)
        res = json.loads(res.text)

        if "message" in res:
            res["status"] = "error"

        return res
