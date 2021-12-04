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


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def timestamp_from_str(timestamp_str):
    return dt.datetime.strptime(timestamp_str, TIMESTAMP_FORMAT)


def timestamp_to_str(timestamp):
    return timestamp.strftime(TIMESTAMP_FORMAT)


def timestamp_now():
    return dt.datetime.utcnow()
