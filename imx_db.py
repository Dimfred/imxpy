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

    def application(self, id):
        return self._get(self.urlv1 / "applications" / id)

    def applications(self, order_by="name", direction="asc", page_size=100, cursor=""):
        params = self._make_params(locals())
        return self._get(self.urlv1 / "applications", params=params)

    def asset(self, token_id, contract_addr, include_fees=True):
        params = {"include_fees": True}

        return self._get(
            self.urlv1 / "assets" / contract_addr / str(token_id), params=params
        )

    def assets(
        self,
        user="",
        collection="",
        name="",
        metadata="",
        sell_orders=True,
        buy_orders=True,
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
        return self._get(self.urlv1 / "assets", params=params)

    def transfers(
        self,
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
        return self._get(self.urlv1 / "transfers", params=params)

    def balances(self, owner, token_addr=None):
        url = self.urlv2 / "balances" / owner
        if token_addr is not None:
            url = url / token_addr

        return self._get(url)

    def mintable_token(self, imx_token_id=None, token_id=None, contract_addr=None):
        if imx_token_id is not None:
            return self._get(self.urlv1 / "mintable-token" / imx_token_id)

        return self._get(self.urlv1 / "mintable-token" / contract_addr / str(token_id))

    def mints(self, imx_token_id):
        return self._get(self.urlv1 / "mints" / imx_token_id)

    def claims(self, addr):
        return self._get(self.urlv1 / "rewards" / addr)

    def stark_key(self, addr):
        return self._get(self.urlv1 / "users" / addr)

    def is_registered(self, addr):
        res = self.stark_key(addr)
        return "accounts" in res

    def orders(
        self,
        sell_token_addr="",
        sell_token_name="",
        sell_token_type="ERC721",
        buy_token_addr="",
        buy_token_type="",
        include_fees=True,
        # asc / desc
        direction="asc",
        # timestamp, buy_quantity
        order_by="timestamp",
        status="active",
        page_size=100,
        cursor="",
    ):
        params = self._make_params(locals())
        return self._get(self.urlv1 / "orders", params=params)

    def trades(
        self,
        party_a_token_type="",
        party_a_token_addr="",
        party_a_token_id="",
        party_b_token_type="",
        party_b_token_addr="",
        party_b_token_id="",
        min_timestamp="",
        max_timestamp="",
        direction="asc",
        order_by="timestamp",
        page_size=100,
        cursor="",
    ):
        params = self._make_params(locals())
        return self._get(self.urlv1 / "trades", params=params)

    def all_pages(self, func, *args, key=None, **kwargs):
        results = []

        cursor = ""
        while True:
            res = func(*args, **kwargs, cursor=cursor)
            cursor = res["cursor"]
            res = res["result"]
            if res is None:
                break

            results.extend(res)

            if not cursor:
                break

        if key is not None:
            results = utils.make_unique(results, key=key)

        return results

    def _make_params(self, locals_):
        del locals_["self"]

        for k, v in list(locals_.items()):
            if k.endswith("addr"):
                del locals_[k]
                new_k = k.replace("addr", "address")
                locals_[new_k] = v
            elif k == "sender":
                del locals_[k]
                new_k = "user"
                locals_[new_k] = v
            elif not isinstance(v, bool) and not v:
                del locals_[k]
            elif k.endswith("timestamp") and isinstance(v, dt.datetime):
                locals_[k] = IMXTime.to_str(v)

        return locals_

    def _get(self, url, params=None):
        res = req.get(url, params=params)
        res = json.loads(res.text)

        if "message" in res:
            res["status"] = "error"

        return res
