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
import subprocess as sp

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# TODO fix the import stuff, that sucks like that
from imxpy.imx_db import IMXDB
from imxpy.imx_objects import *
from imxpy import utils
from imxpy.cmd_factory import CMDFactory


class IMXClient:
    def __init__(self, net, n_workers=32, pk=None):
        self.pk = pk
        self.net = net
        self.db = IMXDB(net)
        self.pool = ThreadPoolExecutor(n_workers)

    @utils.ensure_pk
    def sign_msg(self, params: SignMsgParams, max_retries: int = 1):
        return self._run_pool("sign_msg", params, max_retries)

    @utils.ensure_pk
    def register(self, max_retries: int = 1):
        return self._run_pool("register", None, max_retries)

    @utils.ensure_pk
    def create_project(self, params: CreateProjectParams, max_retries: int = 1):
        return self._run_pool("create_project", params, max_retries)

    @utils.ensure_pk
    def create_collection(self, params: CreateCollectionParams, max_retries: int = 1):
        return self._run_pool("create_collection", params, max_retries)

    @utils.ensure_pk
    def update_collection(self, params: UpdateCollectionParams, max_retries: int = 1):
        return self._run_pool("update_collection", params, max_retries)

    @utils.ensure_pk
    def create_metadata_schema(
        self, params: CreateMetadataSchemaParams, max_retries: int = 1
    ):
        return self._run_pool("create_metadata_schema", params, max_retries)

    @utils.ensure_pk
    def update_metadata_schema(
        self, params: UpdateMetadataSchemaParams, max_retries: int = 1
    ):
        return self._run_pool("update_metadata_schema", params, max_retries)

    @utils.ensure_pk
    def create_exchange(self, params: CreateExchangeParams, max_retries: int = 1):
        return self._run_pool("create_exchange", params, max_retries)

    @utils.ensure_pk
    def transfer(self, params: TransferParams, max_retries: int = 1):
        return self._run_pool("transfer", params, max_retries)

    @utils.ensure_pk
    def mint(self, params: MintParams, max_retries: int = 1):
        return self._run_pool("mint", params, max_retries)

    @utils.ensure_pk
    def burn(self, params: BurnParams, max_retries: int = 1):
        return self._run_pool("burn", params, max_retries)

    @utils.ensure_pk
    def prepare_withdrawal(self, params: PrepareWithdrawalParams, max_retries: int = 1):
        return self._run_pool("prepare_withdrawal", params, max_retries)

    @utils.ensure_pk
    def complete_withdrawal(
        self, params: CompleteWithdrawalParams, max_retries: int = 1
    ):
        return self._run_pool("complete_withdrawal", params, max_retries)

    @utils.ensure_pk
    def deposit(self, params: DepositParams, max_retries: int = 1):
        return self._run_pool("deposit", params, max_retries)

    @utils.ensure_pk
    def create_order(self, params: CreateOrderParams, max_retries: int = 1):
        return self._run_pool("create_order", params, max_retries)

    @utils.ensure_pk
    def cancel_order(self, params: CancelOrderParams, max_retries: int = 1):
        return self._run_pool("cancel_order", params, max_retries)

    @utils.ensure_pk
    def create_trade(self, params: CreateTradeParams, max_retries: int = 1):
        return self._run_pool("create_trade", params, max_retries)

    @utils.ensure_pk
    def approve_nft(self, params: ApproveNFTParams, max_retries: int = 1):
        return self._run_pool("approve_nft", params, max_retries)

    @utils.ensure_pk
    def approve_erc20(self, params: ApproveERC20Params, max_retries: int = 1):
        return self._run_pool("approve_erc20", params, max_retries)

    def wait(self):
        self.pool.shutdown()

    def _run_pool(self, function_name: str, params=None, max_retries: int = 1):
        def _run_cmd(function_name, cmd, max_retries):
            for _ in range(max_retries):
                res = sp.run(cmd, shell=True, capture_output=True)
                res = self._parse_result(res, function_name)
                if res["status"] != "error" or not max_retries:
                    break

            return res

        cmd = self._make_cmd(function_name, params)
        return self.pool.submit(_run_cmd, function_name, cmd, max_retries)

    def _make_cmd(self, function_name, params=None):
        base_params = BaseParams(
            pk=self.pk, network=self.net, function_name=function_name
        )

        cmd = CMDFactory.make(base_params, params)
        # DEBUG
        # print(cmd)

        return cmd

    def _parse_result(self, res, function_name):
        err = res.stderr.decode()
        if err:
            print(f"[ERROR] {function_name} failed.\n", err)

        res = res.stdout.decode()
        # DEBUG whole stdout output
        # print(res)
        try:
            res = json.loads(res)
        except Exception as e:
            print(f"[ERROR] {function_name}::parse_result failed\n", e)
            res = None

        return res
