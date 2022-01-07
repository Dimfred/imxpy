from pathlib import Path
import sys
import time

# add parent dir of imxpy
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


from easydict import EasyDict as edict
import pytest

from imx_client import IMXClient
from imx_objects import *


def random_number():
    import random

    return random.randint(0, 100000000000000000000000000000000000)


@pytest.fixture
def random_str():
    return str(random_number())


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
def mainnet_client():
    return IMXClient("main")


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


def mint_params(contract_addr, id_, addr):
    params = MintParams(
        contract_addr=contract_addr,
        targets=[
            MintTarget(
                addr=addr,
                tokens=[
                    MintableToken(
                        id=id_,
                        blueprint=str(id_),
                    ),
                ],
            ),
        ],
    )

    return params


@pytest.fixture(scope="function")
def minted_nft_id(client, acc1, contract_addr):
    token_id = random_number()
    params = mint_params(contract_addr, token_id, acc1.addr)
    res = client.mint(params)
    res = res.result()

    # wait until the database has applied the state
    time.sleep(2)

    return token_id


@pytest.fixture(scope="function")
def valid_order_params(client, client2, acc2, contract_addr):
    # client1 is in control of the sc therefore he mints to acc2
    token_id = random_number()
    params = mint_params(contract_addr, token_id, acc2.addr)
    res = client.mint(params)
    time.sleep(2)

    # client2 now has the nft and can create the order which client1 will buy
    params = CreateOrderParams(
        sender=acc2.addr,
        token_sell=ERC721(token_id=token_id, contract_addr=contract_addr),
        token_buy=ETH(quantity="0.000001"),
    )
    res = client2.create_order(params)
    res = res.result()

    time.sleep(2)

    return (res["result"]["order_id"], token_id)


@pytest.fixture
def unregistered_addr():
    return "0xd2Bf8229D98716abEA9D22453C5C5613078B2c46"


@pytest.fixture
def erc20_contract_addr():
    return "0x4c04c39fb6d2b356ae8b06c47843576e32a1963e"


@pytest.fixture
def gods_unchained_addr():
    return "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c"
