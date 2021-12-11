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
from urlpath import URL

from imxpy import utils


class IMXDB:
    def __init__(self, net):
        self._init_urls(net)

    def transfers(
        self,
        sender=None,
        receiver=None,
        page_size=10000000000,
        # order_by="timestamp",
        direction="asc",
        token_type="ETH",
        token_id=None,
        token_address=None,
        min_timestamp=None,
        max_timestamp=None,
        cursor=None,
    ):
        params = {
            "page_size": page_size,
            # "order_by": order_by,
            "direction": direction,
            "token_type": token_type,
        }
        if sender is not None:
            params["user"] = sender

        if receiver is not None:
            params["receiver"] = receiver

        if token_id is not None:
            params["token_id"] = token_id

        if token_address is not None:
            params["token_address"] = token_address

        if min_timestamp is not None:
            params["min_timestamp"] = utils.timestamp_to_str(min_timestamp)

        if max_timestamp is not None:
            params["max_timestamp"] = utils.timestamp_to_str(max_timestamp)

        if cursor is not None:
            params["cursor"] = cursor

        return self._get(self.transfer_url, params=params)

    def balances(self, owner, token_addr=None):
        url = self.balances_url / owner
        if token_addr is not None:
            url = url / token_addr

        return self._get(url)

    def asset(self, token_id, contract_addr, include_fees=True):
        params = {"include_fees": True}

        return self._get(self.assets_url / contract_addr / str(token_id), params=params)

    def mintable_token(self, imx_token_id=None, token_id=None, contract_addr=None):
        if imx_token_id is not None:
            return self._get(self.mintable_token_url / imx_token_id)

        return self._get(self.mintable_token_url / contract_addr / str(token_id))

    def mints(self, imx_token_id):
        return self._get(self.mints_url / imx_token_id)

    def claims(self, addr):
        return self._get(self.rewards_url / addr)

    def assets(
        self,
        user,
        collection,
        cursor=None,
        order_by="name",
        direction="asc",
        page_size=100,
        status="imx",
    ):
        params = {
            "user": user,
            "collection": collection,
            "order_by": order_by,
            "direction": direction,
            "page_size": page_size,
            "status": status,
        }

        if cursor is not None:
            params["cursor"] = cursor

        return self._get(self.assets_url, params)

    def all_pages(self, func, *args, key=None, **kwargs):
        results = []

        cursor = None
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

    def _init_urls(self, net):
        if net == "test":
            self.base = URL("https://api.ropsten.x.immutable.com")
        elif net == "main":
            self.base = URL("https://api.x.immutable.com")
        else:
            raise ValueError(f"Unknown net: '{net}")

        urlv1 = self.base / "v1"
        urlv2 = self.base / "v2"

        self.transfer_url = urlv1 / "transfers"
        self.balances_url = urlv2 / "balances"
        self.assets_url = urlv1 / "assets"
        self.mintable_token_url = urlv1 / "mintable-token"
        self.mints_url = urlv1 / "mints"
        self.rewards_url = urlv1 / "rewards"

    def _get(self, url, params=None):
        res = req.get(url, params=params)
        res = json.loads(res.text)

        if "message" in res:
            res["status"] = "error"

        return res
