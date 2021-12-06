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
from pathlib import Path
import json


class CmdHelper:
    @staticmethod
    def export(var, value):
        return f"export {var}='{value}'; "

    @staticmethod
    def cd(dir):
        return f"cd {dir}; "

    @staticmethod
    def node(bin):
        return f"node {bin}; "

    @staticmethod
    def base(pk, network):
        working_dir = Path(__file__).parent
        cmd = CmdHelper.cd(working_dir)
        cmd += CmdHelper.export("PRIVATE_KEY", pk)
        cmd += CmdHelper.export("NETWORK", network)

        return cmd


class CmdFactory:
    @staticmethod
    def make_mint(pk, network, mint_to_addr, tokens, contract_addr, royalties=None):
        binary = "./build/minting.js"

        tokens = [
            {"id": str(token), "blueprint": str(blueprint)}
            for token, blueprint in tokens
        ]
        tokens = json.dumps(tokens)

        cmd = CmdHelper.base(pk, network)
        cmd += CmdHelper.export("TOKENS", tokens)
        cmd += CmdHelper.export("MINT_TO_ADDR", mint_to_addr)
        cmd += CmdHelper.export("CONTRACT_ADDR", contract_addr)
        if royalties is not None:
            royalties = json.dumps(royalties)
            cmd += CmdHelper.export("ROYALTIES", royalties)

        cmd += CmdHelper.node(binary)

        print(cmd)
        import sys
        sys.exit()

        return cmd

    @staticmethod
    def make_register(pk, network):
        binary = "./build/register.js"

        cmd = CmdHelper.base(pk, network)
        cmd += CmdHelper.node(binary)

        return cmd

    @staticmethod
    def make_transfer_eth(pk, network, sender, receiver, amount, as_wei):
        assert isinstance(amount, (int, str)), "Amount must be a string"

        binary = "./build/transfer_eth.js"

        cmd = CmdHelper.base(pk, network)
        cmd += CmdHelper.export("SENDER_ADDR", sender)
        cmd += CmdHelper.export("RECEIVER_ADDR", receiver)
        cmd += CmdHelper.export("AMOUNT", amount)
        cmd += CmdHelper.export("AS_WEI", as_wei)
        cmd += CmdHelper.node(binary)

        return cmd

    @staticmethod
    def make_transfer_nft(pk, network, sender, receiver, token_id, contract_addr):
        binary = "./build/transfer_nft.js"

        cmd = CmdHelper.base(pk, network)
        cmd += CmdHelper.export("SENDER_ADDR", sender)
        cmd += CmdHelper.export("RECEIVER_ADDR", receiver)
        cmd += CmdHelper.export("TOKEN_ID", token_id)
        cmd += CmdHelper.export("CONTRACT_ADDR", contract_addr)
        cmd += CmdHelper.node(binary)

        return cmd

    @staticmethod
    def make_order(pk, network, user_addr, token_id, token_addr, price, side):
        binary = "./build/order.js"

        cmd = CmdHelper.base(pk, network)
        cmd += CmdHelper.export("USER_ADDR", user_addr)
        cmd += CmdHelper.export("TOKEN_ID", token_id)
        cmd += CmdHelper.export("TOKEN_ADDR", token_addr)
        cmd += CmdHelper.export("ETH_AMOUNT", price)
        cmd += CmdHelper.export("SIDE", side)
        cmd += CmdHelper.node(binary)

        return cmd

    @staticmethod
    def make_create_project(pk, network, name, company_name, contact_email):
        binary = "./build/create_project.js"

        cmd = CmdHelper.base(pk, network)
        cmd += CmdHelper.export("NAME", name)
        cmd += CmdHelper.export("COMPANY_NAME", company_name)
        cmd += CmdHelper.export("CONTACT_EMAIL", contact_email)
        cmd += CmdHelper.node(binary)

        return cmd

    @staticmethod
    def make_create_collection(
        pk,
        network,
        name,
        contract_addr,
        owner_public_key,
        project_id,
        description,
        icon_url,
        metadata_api_url,
        collection_image_url,
    ):
        binary = "./build/create_collection.js"

        cmd = CmdHelper.base(pk, network)
        cmd += CmdHelper.export("NAME", name)
        cmd += CmdHelper.export("CONTRACT_ADDR", contract_addr)
        cmd += CmdHelper.export("OWNER_PUBLIC_KEY", owner_public_key)
        cmd += CmdHelper.export("PROJECT_ID", project_id)
        cmd += CmdHelper.export("DESCRIPTION", description)
        cmd += CmdHelper.export("ICON_URL", icon_url)
        cmd += CmdHelper.export("METADATA_API_URL", metadata_api_url)
        cmd += CmdHelper.export("COLLECTION_IMAGE_URL", collection_image_url)
        cmd += CmdHelper.node(binary)

        return cmd

    @staticmethod
    def make_create_metadata_schema(pk, network, contract_addr, metadata_schema):
        binary = "./build/create_metadata_schema.js"

        cmd = CmdHelper.base(pk, network)
        cmd += CmdHelper.export("CONTRACT_ADDR", contract_addr)
        cmd += CmdHelper.export("METADATA_SCHEMA", metadata_schema)
        cmd += CmdHelper.node(binary)

        return cmd
