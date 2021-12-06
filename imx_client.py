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
import subprocess as sp

from urlpath import URL
from concurrent.futures import ThreadPoolExecutor

import utils
from .imx_cmd_factory import CmdFactory


class IMXClient:
    def __init__(self, net, n_workers=32, pk=None):
        self.pk = pk
        self.net = net
        self._init_urls(net)

        self.pool = ThreadPoolExecutor(n_workers)

    @utils.ensure_pk
    def mint(self, mint_to_addr, tokens, contract_addr, royalties=None, max_retries=10):
        cmd = CmdFactory.make_mint(
            self.pk, self.net, mint_to_addr, tokens, contract_addr, royalties
        )
        return self.pool.submit(self._run_cmd, cmd, max_retries, "mint")

    @utils.ensure_pk
    def register(self, max_retries=1):
        cmd = CmdFactory.make_register(self.pk, self.net)
        return self.pool.submit(self._run_cmd, cmd, max_retries, "register")

    @utils.ensure_pk
    def transfer_eth(self, sender, receiver, amount, as_wei=False, max_retries=10):
        cmd = CmdFactory.make_transfer_eth(
            self.pk, self.net, sender, receiver, amount, as_wei
        )
        return self.pool.submit(self._run_cmd, cmd, max_retries, "transfer_eth")

    @utils.ensure_pk
    def transfer_nft(self, sender, receiver, token_id, contract_addr, max_retries=10):
        cmd = CmdFactory.make_transfer_nft(
            self.pk, self.net, sender, receiver, token_id, contract_addr
        )
        return self.pool.submit(self._run_cmd, cmd, max_retries, "transfer_nft")

    @utils.ensure_pk
    def order(self, user_addr, token_id, contract_addr, price, side, max_retries=10):
        # TODO
        if side == "BUY":
            raise NotImplementedError("BUY is broke.")

        cmd = CmdFactory.make_order(
            self.pk, self.net, user_addr, token_id, contract_addr, price, side
        )
        return self.pool.submit(self._run_cmd, cmd, max_retries, "order")

    def sell(self, user_addr, token_id, contract_addr, price, max_retries=10):
        return self.order(
            user_addr, token_id, contract_addr, price, "SELL", max_retries
        )

    def buy(self, user_addr, token_id, contract_addr, price, max_retries=10):
        return self.order(user_addr, token_id, contract_addr, price, "BUY", max_retries)

    @utils.ensure_pk
    def create_project(self, name, company_name, contact_email, max_retries=10):
        cmd = CmdFactory.make_create_project(
            self.pk, self.net, name, company_name, contact_email
        )
        return self.pool.submit(self._run_cmd, cmd, max_retries, "create_project")

    @utils.ensure_pk
    def create_collection(
        self,
        name,
        contract_addr,
        owner_public_key,
        project_id,
        description,
        icon_url,
        metadata_api_url,
        collection_image_url,
        max_retries=10,
    ):
        cmd = CmdFactory.make_create_collection(
            self.pk,
            self.net,
            name,
            contract_addr,
            owner_public_key,
            project_id,
            description,
            icon_url,
            metadata_api_url,
            collection_image_url,
        )
        return self.pool.submit(self._run_cmd, cmd, max_retries, "create_collection")

    @utils.ensure_pk
    def create_metadata_schema(self, contract_addr, metadata_schema, max_retries=10):
        cmd = CmdFactory.make_create_metadata_schema(
            self.pk, self.net, contract_addr, metadata_schema
        )
        return self.pool.submit(
            self._run_cmd, cmd, max_retries, "create_metadata_schema"
        )

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

    def wait(self):
        self.pool.shutdown()

    def _get(self, url, params=None):
        res = req.get(url, params=params)
        res = json.loads(res.text)

        if "message" in res:
            res["status"] = "error"

        return res

    def _run_cmd(self, cmd, max_retries, function_name):
        for try_ in range(max_retries):
            res = sp.run(cmd, shell=True, capture_output=True)
            res = self._parse_result(res, function_name)
            if res["status"] != "error" or not max_retries:
                break

        return res

    def _parse_result(self, res, function_name):
        err = res.stderr.decode()
        if err:
            print(f"[ERROR] {function_name} failed.\n", err)

        res = res.stdout.decode()
        # print(res)
        try:
            res = json.loads(res)
        except Exception as e:
            print(f"[ERROR] {function_name}::parse_result failed\n", e)
            res = None

        return res

    def _init_urls(self, net):
        if net == "test":
            self.base = URL("https://api.uat.x.immutable.com")
        elif net == "main":
            self.base = URL("https://api.x.immutable.com")
        else:
            raise ValueError(f"Unknown net: '{net}")

        urlv1 = self.base / "v1"
        urlv2 = self.base / "v2"

        self.transfer_url = urlv1 / "transfers"
        self.balances_url = urlv2 / "balances"
        self.assets_url = urlv1 / "assets"
