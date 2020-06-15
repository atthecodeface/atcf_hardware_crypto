#a Copyright
#  
#  This file 'test_apb_target_prng.py' copyright Gavin J Stark 2020
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

#a Documentation
"""
"""

#a Imports
from random import Random
from regress.apb.structs import t_apb_request, t_apb_response
from regress.apb.bfm     import ApbMaster
from regress.crypto      import apb_target_prng
from cdl.sim     import ThExecFile, LogEventParser
from cdl.sim     import HardwareThDut
from cdl.sim     import TestCase
from cdl.utils   import csr

from typing import List, Tuple, Dict, Optional

#a Test classes
#c ApbAddressMap
class ApbAddressMap(csr.Map):
    _width=32
    _select=0
    _address=0
    _shift=0
    _address_size=0
    _map=[csr.MapMap(offset=0, name="prng", map=apb_target_prng.PrngAddressMap),
         ]
    pass
#c PrngTestBase
class PrngTestBase(ThExecFile):
    """
    """
    #f run__init - invoked by submodules
    def run__init(self):
        self.bfm_wait(10)
        self.apb = ApbMaster(self, "apb_request",  "apb_response")
        self.apb_map = ApbAddressMap()
        self.prng_map  = self.apb_map.prng # This is an ApbAddressMap()
        pass

    #f run
    def run(self):
        pass
    #f run__finalize
    def run__finalize(self):
        self.bfm_wait_until_test_done(1000)
        self.passtest("Test completed")
        # self.verbose.error("%s"%(self.global_cycle()))
        pass
    #f All done
    pass

#c PrngTest_0
class PrngTest_0(PrngTestBase):
    #f run
    def run(self):
        self.apb.write(address=self.prng_map.prng_config.Address(),data=0x21)
        self.apb.write(address=self.prng_map.config.Address(),data=0x2)
        self.apb.write(address=self.prng_map.whiteness_run_length.Address(),data=0x1000)
        self.apb.write(address=self.prng_map.whiteness_control.Address(),data=0x20000003)
        self.apb.read(address=self.prng_map.status.Address())
        for i in range(20):
            self.bfm_wait(1000)
            data=self.apb.read(address=self.prng_map.data.Address())
            self.verbose.info("random data %08x"%data)
            w0=self.apb.read(address=self.prng_map.whiteness_data_0.Address())
            w1=self.apb.read(address=self.prng_map.whiteness_data_1.Address())
            self.verbose.info("whiteness %08x%08x"%(w1,w0))
            pass
        pass
    pass

#a Hardware classes
#c ApbTargetPrngHw
class ApbTargetPrngHw(HardwareThDut):
    clock_desc = [("clk",(0,1,1)),
    ]
    reset_desc = {"name":"reset_n", "init_value":0, "wait":5}
    module_name = "apb_target_prng"
    dut_inputs  = {"apb_request":t_apb_request,
                   "entropy_in":1,
    }
    dut_outputs = {"apb_response":t_apb_response,
    }
    pass

#a Simulation test classes
#c ApbTargetPrng
class ApbTargetPrng(TestCase):
    hw = ApbTargetPrngHw
    kwargs = {
        #"verbosity":0,
        "th_args":{
        },
    }
    _tests = {
        "smoke"  :  (PrngTest_0,50*1000,  kwargs),
    }
    pass

