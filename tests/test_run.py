#!/usr/bin/env python
# pushstore_parser.py
# Copyright 2016 Jake Valletta (@jake_valletta)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Simple test to execute pushstore_parser.py on a .pushstore"""

from pushstore_parser import pushstore_parser
import sys


def test_run():

    """Simply execute and parse a .pushstore"""

    sys.argv.append("com.e4bf058461-1-42.pushstore")
    rtn = pushstore_parser.main()

    assert(rtn == 0)
