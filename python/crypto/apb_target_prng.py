#a Copyright
#  
#  This file 'apb_target_prng.py' copyright Gavin J Stark 2020
#  
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#a Imports
from cdl.utils.csr   import Csr, CsrField, CsrFieldZero, Map, MapCsr, CsrFieldResvd

#a CSRs
class DataCsr(Csr):
    _fields = { 0:   CsrField(width=32, name="data", brief="data", doc="Random data; if not valid, then zero is returned"),
              }

class WhitenessDataCsr(Csr):
    _fields = { 0:   CsrField(width=32, name="data", brief="len", doc="Data from whiteness monitor"),
              }

class WhitenessRunLengthCsr(Csr):
    _fields = { 0:   CsrField(width=32, name="length", brief="len", doc="Number of cycles/valid bits to run monitor for"),
              }

class WhitenessControlCsr(Csr):
    _fields = { 0:   CsrField(width=1, name="enable", brief="en", doc="If asserted then whiteness monitor is enabled"),
                1:   CsrField(width=1, name="continuous", brief="cont", doc="If asserted then run whiteness continuously"),
                2:   CsrFieldResvd(width=2),
                4:   CsrField(width=1, name="source", brief="src", doc="If asserted then monitor entropy in; else monitor PRNG"),
                16:   CsrField(width=16, name="control", brief="ctl", doc="Control register value, including type and data for whiteness monitor type"),
              }

class PrngConfigCsr(Csr):
    _fields = { 0:   CsrField(width=1, name="enable", brief="en", doc="If asserted then PRNG is enabled; must be set for random data"),
                1:   CsrFieldResvd(width=3),
                4:   CsrField(width=3, name="min_valid", brief="mv", doc="Minimum number of bits valid out of 4 LFSRs for valid data"),
                7:  CsrFieldResvd(width=25),
              }

class StatusCsr(Csr):
    _fields = { 0: CsrFieldZero(width=32),
                # locked config
                # whiteness data ready
                # whiteness requested
              }

class ConfigCsr(Csr):
    _fields = { 0: CsrFieldZero(width=32),
              }

class PrngAddressMap(Map):
    _map = [ MapCsr(reg=0,  name="config",       brief="cfg",    csr=ConfigCsr, doc=""),
             MapCsr(reg=1,  name="status",       brief="sts",    csr=StatusCsr, doc=""),
             MapCsr(reg=2,  name="prng_config",  brief="prng",   csr=PrngConfigCsr, doc="Configuration of PRNG"),
             MapCsr(reg=3,  name="prng_data",    brief="data",   csr=DataCsr,       doc="Data from PRNG"),
             MapCsr(reg=4,  name="whiteness_control",  brief="wctrl",   csr=WhitenessControlCsr, doc="Control of whiteness monitor"),
             MapCsr(reg=5,  name="whiteness_run_length",  brief="wlen",   csr=WhitenessRunLengthCsr, doc="Run length of whiteness monitoring"),
             MapCsr(reg=6,  name="whiteness_data_0",  brief="wd0",   csr=WhitenessDataCsr, doc="Data from whiteness monitor"),
             MapCsr(reg=7,  name="whiteness_data_1",  brief="wd0",   csr=WhitenessDataCsr, doc="Data from whiteness monitor"),
             ]
