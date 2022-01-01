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

from types import new_class
from typing import Optional, Union, Generator, Callable, Any, List, cast
from typingx import isinstancex

from enum import Enum

from pydantic import BaseModel, Field, validator
from pydantic.generics import Generic, TypeVar

from imxpy import utils


########################################################################################
# UTILS
########################################################################################
class Utils:
    @staticmethod
    def exclude(param, kwargs):
        if "exclude" not in kwargs or not kwargs["exclude"]:
            kwargs["exclude"] = set()

        if isinstance(param, (list, tuple, set)):
            kwargs["exclude"].update(param)
        else:
            kwargs["exclude"].add(param)

        return kwargs


T = TypeVar("T")


def _display_type(v: Any) -> str:
    try:
        return v.__name__
    except AttributeError:
        # happens with typing objects
        return str(v).replace("typing.", "")


# taken from https://github.com/samuelcolvin/pydantic/issues/2079
# that is some sick shit!
class Strict(Generic[T]):
    __typelike__: T

    @classmethod
    def __class_getitem__(cls, typelike: T) -> T:
        new_cls = new_class(
            f"Strict[{_display_type(typelike)}]",
            (cls,),
            {},
            lambda ns: ns.update({"__typelike__": typelike}),
        )
        return cast(T, new_cls)

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> T:
        if not isinstancex(value, cls.__typelike__):
            raise TypeError(f"{value!r} is not of valid type")
        return value


########################################################################################
# VALIDATION
########################################################################################
class Validator:
    @staticmethod
    def validate_addr(addr):
        if not addr.startswith("0x"):
            raise ValueError(f"Addr has to start with 0x got: {addr}")

        l = len(addr)
        if l != 42:
            raise ValueError(f"Len addr incorrect: {l} / 42")

        return addr.lower()

    @staticmethod
    def validate_token(token):
        if token.type in ("ETH", "ERC20"):
            safe_number = utils.SafeNumber(
                number=token.quantity, decimals=token.decimals, as_wei=token.as_wei
            )
        else:  # ERC721
            safe_number = utils.SafeNumber(number=token.quantity, as_wei=True)

        token.quantity = safe_number.value
        return token

########################################################################################
# Base
########################################################################################
class Base(BaseModel):
    def json(self):
        return json.dumps(self.dict(), separators=(',', ':'))



########################################################################################
# TOKENS
########################################################################################
class TokenType(Enum):
    ETH = 0
    ERC20 = 1
    ERC721 = 2
    MINTABLE_ERC721 = 3

    def __str__(self):
        return self.name


class ETH(Base):
    quantity: Union[str, int] = 0
    type: str = str(TokenType.ETH)
    decimals: int = 18
    as_wei: bool = False

    @validator("quantity")
    def check_empty(cls, quantity):
        return quantity if quantity else 0

    def dict(self, *args, **kwargs):
        Utils.exclude("as_wei", kwargs)
        d = super().dict(*args, **kwargs)
        new_d = {"type": d.pop("type"), "data": d}

        return new_d


class ERC20(Base):
    symbol: str
    tokenAddress: str = Field(alias="contract_addr")
    decimals: int = 18
    quantity: Union[str, int] = 0
    type: str = str(TokenType.ERC20)
    as_wei: bool = False

    @validator("tokenAddress")
    def validate_addr(cls, addr):
        return Validator.validate_addr(addr)

    def dict(self, *args, **kwargs):
        Utils.exclude("as_wei", kwargs)
        d = super().dict(*args, **kwargs)
        new_d = {"type": d.pop("type"), "data": d}

        return new_d


class ERC721(Base):
    tokenAddress: str = Field(alias="contract_addr")
    tokenId: Union[str, int] = Field(alias="token_id")
    quantity: Union[str, int] = 1
    type: str = str(TokenType.ERC721)

    @validator("quantity")
    def ensure_one(cls, quantity):
        if quantity != 1:
            raise ValueError("Quantity must be '1'.")

        return quantity

    @validator("tokenAddress")
    def validate_addr(cls, addr):
        return Validator.validate_addr(addr)

    @validator("tokenId")
    def as_str(cls, token_id):
        return str(token_id)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        new_d = {"type": d.pop("type"), "data": d}

        return new_d


########################################################################################
# BASE
########################################################################################
class BaseParams(Base):
    pk: str
    network: str
    function_name: str
    # TODO bother later with types and bla
    gas_limit: Optional[str]
    gas_price: Optional[str]


########################################################################################
# REGISTRATION & PROJECT & COLLECTION
########################################################################################
class CreateProjectParams(Base):
    name: str
    company_name: str
    contact_email: str


class CreateCollectionParams(Base):
    name: str
    contract_address: str = Field(alias="contract_addr")
    owner_public_key: str
    project_id: int
    metadata_api_url: Optional[str]
    description: Optional[str]
    icon_url: Optional[str]
    collection_image_url: Optional[str]

    @validator("contract_address")
    def validate_addr(cls, addr):
        return Validator.validate_addr(addr)


class UpdateCollectionParams(Base):
    contractAddress: str = Field(alias="contract_addr")
    name: Optional[str]
    description: Optional[str]
    icon_url: Optional[str]
    metadata_api_url: Optional[str]
    collection_image_url: Optional[str]

    @validator("contractAddress")
    def validate_addr(cls, addr):
        return Validator.validate_addr(addr)

    def dict(self, *args, **kwargs):
        new_d = {}
        d = super().dict(*args, **kwargs)

        new_d["contractAddress"] = d.pop("contractAddress")
        new_d["params"] = d

        return new_d


class CreateMetadataSchemaParams(Base):
    contractAddress: str = Field(alias="contract_addr")
    # TODO could also define the whole schema as a model
    metadata: dict


########################################################################################
# TRANSFER
########################################################################################
class TransferParams(Base):
    sender: str
    receiver: str
    token: Strict[Union[ETH, ERC721, ERC20]]

    @validator("sender", "receiver")
    def validate_addr(cls, addr):
        return Validator.validate_addr(addr)

    @validator("token")
    def validate_token(cls, token):
        return Validator.validate_token(token)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["quantity"] = d["token"]["data"].pop("quantity")

        return d


########################################################################################
# MINT
########################################################################################
class Royalty(Base):
    recipient: str
    percentage: Union[float, int]

    @validator("recipient")
    def validate_addr(cls, addr):
        return Validator.validate_addr(addr)


class MintableToken(Base):
    id: str
    blueprint: str
    # local royalties for this token, overrides global royalty config
    royalties: Optional[List[Royalty]]

    def dict(self, *args, **kwargs):
        if self.royalties is None:
            Utils.exclude("royalties", kwargs)

        return super().dict(*args, **kwargs)


class MintTarget(Base):
    etherKey: str = Field(alias="addr")
    tokens: List[MintableToken]


class MintParams(Base):
    contractAddress: str = Field(alias="contract_addr")
    users: List[MintTarget] = Field(alias="targets")
    # global royalty config, will get overridden by MintableToken royalties
    royalties: Optional[List[Royalty]]

    def dict(self, *args, **kwargs):
        if self.royalties is None:
            Utils.exclude("royalties", kwargs)

        return [super().dict(*args, **kwargs)]


########################################################################################
# BURN
########################################################################################
class BurnParams(Base):
    sender: str
    token: Strict[Union[ETH, ERC20, ERC721]]

    @validator("sender")
    def validate_addr(cls, addr):
        return Validator.validate_addr(addr)

    @validator("token")
    def validate_token(cls, token):
        return Validator.validate_token(token)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["quantity"] = d["token"]["data"].pop("quantity")

        return d


########################################################################################
# WITHDRAW & DEPOSIT
########################################################################################
class PrepareWithdrawalParams(Base):
    user: str = Field(alias="sender")
    token: Strict[Union[ETH, ERC20, ERC721]]

    @validator("user")
    def validate_addr(cls, addr):
        return Validator.validate_addr(addr)

    @validator("token")
    def validate_token(cls, token):
        return Validator.validate_token(token)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["quantity"] = d["token"]["data"].pop("quantity")

        return d


class CompleteWithdrawalParams(Base):
    token: Strict[Union[ETH, ERC20, ERC721]]

    @validator("token")
    def validate_token(cls, token):
        return Validator.validate_token(token)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["token"]["data"].pop("quantity")

        return d


class DepositParams(Base):
    user: str = Field(alias="sender")
    token: Strict[Union[ETH, ERC20, ERC721]]

    @validator("token")
    def validate_token(cls, token):
        return Validator.validate_token(token)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["quantity"] = d["token"]["data"].pop("quantity")

        return d


########################################################################################
# TRADING
########################################################################################
class CreateOrderParams(Base):
    user: str = Field(alias="sender")
    tokenSell: Strict[Union[ETH, ERC20, ERC721]] = Field(alias="token_sell")
    tokenBuy: Strict[Union[ETH, ERC20, ERC721]] = Field(alias="token_buy")

    @validator("user")
    def validate_addr(cls, addr):
        return Validator.validate_addr(addr)

    @validator("tokenSell", "tokenBuy")
    def validate_token(cls, token):
        return Validator.validate_token(token)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["amountSell"] = d["tokenSell"]["data"].pop("quantity")
        d["amountBuy"] = d["tokenBuy"]["data"].pop("quantity")

        return d


class CancelOrderParams(Base):
    order_id: Union[str, int]

    @validator("order_id")
    def to_int(cls, sn):
        return int(sn)


class CreateTradeParams(Base):
    orderId: int = Field(alias="order_id")
    user: str = Field(alias="sender")
    tokenSell: Strict[Union[ETH, ERC20, ERC721]] = Field(alias="token_sell")
    tokenBuy: Strict[Union[ETH, ERC20, ERC721]] = Field(alias="token_buy")

    @validator("user")
    def validate_addr(cls, addr):
        return Validator.validate_addr(addr)

    @validator("tokenSell", "tokenBuy")
    def validate_token(cls, token):
        return Validator.validate_token(token)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["amountSell"] = d["tokenSell"]["data"].pop("quantity")
        d["amountBuy"] = d["tokenBuy"]["data"].pop("quantity")

        return d
