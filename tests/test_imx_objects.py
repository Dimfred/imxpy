import pytest
import json
from pprint import pprint
from pydantic import ValidationError
import itertools as it

from imx_objects import *


class TestCollectionParams:
    def test_okay_update_collection(self, acc1):
        expected = {
            "contractAddress": acc1.addr,
            "params": {
                "name": "test",
                "description": None,
                "icon_url": None,
                "metadata_api_url": None,
                "collection_image_url": None,
            },
        }
        params = UpdateCollectionParams(contract_addr=acc1.addr, name="test")

        assert params.dict() == expected


class TestTransferParams:
    def test_okay_eth(self, one_eth, acc1, acc2):
        expected = {
            "sender": acc1.addr,
            "receiver": acc2.addr,
            "token": {"type": "ETH", "data": {"decimals": 18}},
            "quantity": str(one_eth),
        }

        params = TransferParams(
            sender=acc1.addr, receiver=acc2.addr, token=ETH(quantity=1)
        )
        assert params.dict() == expected
        # it is okay if this test fails since it is dependent on the order of the dict
        # it is just here for me to check it at least once, that the same stuff comes out
        # of both and json() uses dict()
        assert params.json() == json.dumps(expected, separators=(",", ":"))

    def test_okay_erc721(self, acc1, acc2):
        expected = {
            "sender": acc1.addr,
            "receiver": acc2.addr,
            "token": {
                "type": "ERC721",
                "data": {"tokenAddress": acc1.addr, "tokenId": "1"},
            },
            "quantity": "1",
        }

        for quantity, token_id in it.product(("1", 1), ("1", 1)):
            params = TransferParams(
                sender=acc1.addr,
                receiver=acc2.addr,
                token=ERC721(token_id=token_id, contract_addr=acc1.addr),
            )
            assert params.dict() == expected

    # TODO test ERC20

    def test_fails_addr_wrong(self):
        with pytest.raises(ValidationError) as e:
            does_not_start_with_0x = "0"
            TransferParams(sender=does_not_start_with_0x)
        assert "has to start with 0x" in str(e.value)

        with pytest.raises(ValidationError) as e:
            too_short = "0x000"
            TransferParams(sender=too_short)
        assert "Len addr incorrect" in str(e.value)

        with pytest.raises(ValidationError) as e:
            too_long = "0x00000000000000000000000000000000000000000000000000"
            TransferParams(sender=too_long)
        assert "Len addr incorrect" in str(e.value)

    def test_fails_erc721_too_high_quantity(self, acc1, acc2):
        with pytest.raises(ValidationError) as e:
            TransferParams(
                sender=acc1.addr,
                receiver=acc2.addr,
                data=ERC721(quantity=2, token_id=1, contract_addr=acc1.addr),
            )
        assert "Quantity must be" in str(e.value)


class TestMintParams:
    def test_okay_royalty_float(self, acc1):
        expected = {"recipient": acc1.addr, "percentage": 1.0}

        r = Royalty(recipient=acc1.addr, percentage=1.0)
        assert r.dict() == expected

        r = Royalty(recipient=acc1.addr, percentage=1)
        assert r.dict() == expected

    def test_okay_mintable_without_royalties(self, acc1):
        expected = {
            "id": "1",
            "blueprint": "test",
        }

        m = MintableToken(id="1", blueprint="test")
        assert m.dict() == expected

    def test_okay_mintable_with_royalties(self, acc1):
        expected = {
            "id": "1",
            "blueprint": "test",
            "royalties": [{"recipient": acc1.addr, "percentage": 1.0}],
        }

        m = MintableToken(
            id="1",
            blueprint="test",
            royalties=[Royalty(recipient=acc1.addr, percentage=1.0)],
        )
        assert m.dict() == expected

    def test_okay_minttarget(self, acc1):
        expected = {
            "etherKey": acc1.addr,
            "tokens": [
                {
                    "id": "1",
                    "blueprint": "test",
                    "royalties": [{"recipient": acc1.addr, "percentage": 1.0}],
                }
            ],
        }

        m = MintTarget(
            addr=acc1.addr,
            tokens=[
                MintableToken(
                    id="1",
                    blueprint="test",
                    royalties=[Royalty(recipient=acc1.addr, percentage=1.0)],
                )
            ],
        )
        assert m.dict() == expected

    def test_okay_mintparams_without_royalties(self, acc1):
        expected = [
            {
                "contractAddress": acc1.addr,
                "users": [
                    {
                        "etherKey": acc1.addr,
                        "tokens": [
                            {
                                "id": "1",
                                "blueprint": "test",
                                "royalties": [
                                    {"recipient": acc1.addr, "percentage": 1.0}
                                ],
                            }
                        ],
                    }
                ],
            }
        ]

        m = MintParams(
            contract_addr=acc1.addr,
            targets=[
                MintTarget(
                    addr=acc1.addr,
                    tokens=[
                        MintableToken(
                            id="1",
                            blueprint="test",
                            royalties=[Royalty(recipient=acc1.addr, percentage=1.0)],
                        )
                    ],
                )
            ],
        )
        assert m.dict() == expected

    def test_okay_mintparams_with_royalties(self, acc1):
        expected = [
            {
                "contractAddress": acc1.addr,
                "users": [
                    {
                        "etherKey": acc1.addr,
                        "tokens": [
                            {
                                "id": "1",
                                "blueprint": "test",
                                "royalties": [
                                    {"recipient": acc1.addr, "percentage": 1.0}
                                ],
                            }
                        ],
                    }
                ],
                "royalties": [{"recipient": acc1.addr, "percentage": 1.0}],
            }
        ]

        m = MintParams(
            contract_addr=acc1.addr,
            royalties=[Royalty(recipient=acc1.addr, percentage=1.0)],
            targets=[
                MintTarget(
                    addr=acc1.addr,
                    tokens=[
                        MintableToken(
                            id="1",
                            blueprint="test",
                            royalties=[Royalty(recipient=acc1.addr, percentage=1.0)],
                        )
                    ],
                )
            ],
        )
        assert m.dict() == expected
