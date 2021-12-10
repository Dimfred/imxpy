from pathlib import Path
import sys

# add parent dir of imxpy
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


from easydict import EasyDict as edict
import pytest

from imx_client import IMXClient
from imx_objects import *


@pytest.fixture
def acc1():
    acc = edict()
    acc.pk = "4c4b2554e43b374f4cafdd5adaeea5e9aff9b3be54d329bc939752bb747294b9"
    acc.addr = "0x77406103701907051070fc029e0a90d5be82f76c"

    return acc


@pytest.fixture
def acc2():
    acc = edict()
    acc.pk = "ac5d52cc7f75e293ecf2a95f3fafef23c9f5345b4a434ed5bacffccbdbe944fd"
    acc.addr = "0xea047d1919b732a4b9b12337a60876536f4f2659"

    return acc

@pytest.fixture
def acc3():
    acc = edict()
    acc.pk = "bfde975ea5aa3779c7e2f2aade7c2a594b53e32ee23a2ae395927ec5fce4aa4b"
    acc.addr = "0xd5f5ad7968147c2e198ddbc40868cb1c6f059c6d"

    return acc


@pytest.fixture
def one_eth():
    return 1_000_000_000_000_000_000


@pytest.fixture
def half_eth(one_eth):
    return one_eth // 2


@pytest.fixture(scope="function")
def client(acc1):
    return IMXClient("test", pk=acc1.pk)


@pytest.fixture(scope="function")
def client2(acc2):
    return IMXClient("test", pk=acc2.pk)


@pytest.fixture(scope="function")
def project_id(client, acc1):
    params = CreateProjectParams(
        name="test_proj", company_name="test_company", contact_email="test@test.com"
    )

    res = client.create_project(params)
    res = res.result()

    return res["result"]["id"]


@pytest.fixture(scope="function")
def random_addr():
    import random

    allowed = "abcdef0123456789"
    addr = f"0x{''.join(random.choice(allowed) for _ in range(40))}"

    return addr


@pytest.fixture
def contract_addr():
    return "0xb72d1aa092cf5b3b50dabb55bdab0f33dfab37b7"

@pytest.fixture
def unregistered_contract_addr():
    return "0xb55016be31047c16c951612f3b0f7c5f92f1faf5"


@pytest.fixture(scope="function")
def token_id(client2, acc1, acc2, contract_addr):
    _token_id = 0
    yield _token_id

    params = TransferParams(
        sender=acc2.addr,
        receiver=acc1.addr,
        token=ERC721(token_id=_token_id, contract_addr=contract_addr),
    )
    client2.transfer(params)

@pytest.fixture(scope="function")
def minted_nft_id(client, acc1, contract_addr):
    import random

    id_ = random.randint(0, 100000000000000000000000000000000000)
    params = MintParams(
        contract_addr=contract_addr,
        targets=[
            MintTarget(
                addr=acc1.addr,
                tokens=[
                    MintableToken(
                        id=id_,
                        blueprint=str(id_),
                    ),
                ]
            ),
        ],
    )
    res = client.mint(params, max_retries=1)
    res = res.result()

    assert res["status"] == "success"

    return id_
