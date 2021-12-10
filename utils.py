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
import sys
import datetime as dt
from pydantic import BaseModel, Field, validator
from typing import Union, Optional


def ensure_pk(func):
    def deco(self, *args, **kwargs):
        if self.pk is None:
            print("Aborting: Please provide a private_key to call this function.")
            sys.exit()

        return func(self, *args, **kwargs)

    return deco


def make_unique(iterable, key=None):
    keys = set()
    idxs_to_remove = []
    for idx, val in enumerate(iterable):
        k = key(val)
        if k not in keys:
            keys.add(k)
        else:
            idxs_to_remove.append(idx)

    for counter, idx in enumerate(idxs_to_remove):
        iterable.pop(idx - counter)

    return iterable


class IMXTime:
    format_ = "%Y-%m-%dT%H:%M:%S.%fZ"

    @staticmethod
    def from_str(timestamp_str):
        return dt.datetime.strptime(timestamp_str, IMXTime.format_)

    @staticmethod
    def to_str(timestamp):
        return timestamp.strftime(IMXTime.format_)

    @staticmethod
    def now():
        return dt.datetime.utcnow()


class SafeNumber:
    def __init__(self, number, decimals=None, as_wei=False):
        self.value = self.convert_to_safe(number, decimals, as_wei)

    def convert_to_safe(self, number, decimals, as_wei):
        if not isinstance(number, (int, str)):
            raise ValueError("SafeNumber: Only 'str' and 'int' numbers allowed.")

        if as_wei:
            # raises if there are fobidden chars in str
            return str(int(number))

        number = str(number)
        if "." not in number:
            before_comma, after_comma = number, ""
        else:
            before_comma, after_comma = number.split(".")

        if len(after_comma) > decimals:
            raise ValueError(
                f"More decimals present than allowed\n\tnumber: {number}\n\t:decimals: {decimals}"
            )

        len_padding = decimals - len(after_comma)
        padding = "".join("0" for _ in range(len_padding))

        safe_number = ""
        if int(before_comma):
            safe_number = before_comma + after_comma + padding
        # happens when a 0 is put in
        elif not safe_number:
            safe_number = "0"
        else:
            # remove leading zeros and append
            safe_number = str(int(after_comma)) + padding

        return safe_number
