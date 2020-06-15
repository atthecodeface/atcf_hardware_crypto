#a Copyright
#  
#  This file 'test_prng_entropy.py' copyright Gavin J Stark 2020
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
from regress.utils.lfsr import Lfsr
from regress.crypto.prng import t_prng_config, t_prng_status, t_prng_whiteness_control, t_prng_whiteness_result
from cdl.sim     import ThExecFile, LogEventParser
from cdl.sim     import HardwareThDut
from cdl.sim     import TestCase

from typing import List, Tuple, Dict, Optional

#a Log classes
#c EntropyLogParser - log event parser for tx gmii
class EntropyLogParser(LogEventParser):
    def filter_module(self, module_name:str) -> bool : return True
    def map_log_type(self, log_type:str) -> Optional[str] :
        if log_type in self.attr_map: return log_type
        return None
    attr_map = {"entropy_out":{"active":1,"count":2,"entropy":3}}
    pass

#a PrngEntropyMux Test classes
#c PrngEntropyMux4_Base
class PrngEntropyMux4_Base(ThExecFile):
    """
    """
    l5 = Lfsr(nbits=5, poly=0x9)
    l6 = Lfsr(nbits=6, poly=0x9)
    l7 = Lfsr(nbits=7, poly=0x41)
    l8 = Lfsr(nbits=8, poly=0x71)
    lfsrs = (l8,l7,l6,l5)
    prng_module = "dut"

    #f clock_lfsrs
    def clock_lfsrs(self, deltas=0):
        for i in range(4):
            l = self.lfsrs[i]
            l.clk_once()
            l.set(l.get() ^ ((deltas>>i)&1))
            pass
        pass
    #f get_entropy
    def get_entropy(self):
        v=0
        for l in self.lfsrs:
            v ^= l.get()
            pass
        return v&1
    #f drive_entropy
    def drive_entropy(self, b):
        b = b & 0xf
        d = b ^ self.last_entropy_in
        self.entropy_in.drive(b)
        self.bfm_wait(1)
        self.last_entropy_in = b
        if self.burst is None: self.burst = [self.get_entropy()]
        self.clock_lfsrs(d)
        self.burst.append(self.get_entropy())
        pass
    #f finish_burst
    def finish_burst(self):
        count = 0
        if self.get_entropy()==0: count+=1
        active = True
        while count<16:
            self.clock_lfsrs(0)
            if self.get_entropy()==0: count+=1
            self.burst.append(self.get_entropy())
            self.bfm_wait(1)
            pass
        self.bfm_wait(1)
        self.clock_lfsrs(0)
        self.bursts.append(self.burst)
        self.burst = None
        pass
    #f validate_burst
    def validate_burst(self, burst):
        last_cycle = None
        tpc = self.ticks_per_cycle()
        while (self.log_entropy.num_events()!=0) and (burst!=[]):
            l = self.log_entropy_parser.parse_log_event(self.log_entropy.event_pop())
            if last_cycle is not None:
                self.compare_expected("Entropy back-to-back",last_cycle+tpc,l.global_cycle)
                pass
            last_cycle = l.global_cycle
            e = burst.pop(0)
            self.compare_expected("Entropy out %s"%(str(l)),e,l.entropy)
            pass
        pass
    #f run__init - invoked by submodules
    def run__init(self):
        self.log_entropy         = self.log_recorder(self.prng_module)
        self.log_entropy_parser  = EntropyLogParser()
        self.l5.set(0)
        self.l6.set(0)
        self.l7.set(0)
        self.l8.set(0)
        self.last_entropy_in = 0
        self.burst = None
        self.bursts = []
        self.bfm_wait(10)
        pass
    #f run
    def run(self):
        pass
    #f run__finalize
    def run__finalize(self):
        for b in self.bursts:
            self.validate_burst(b)
            pass
        # self.verbose.error("%s"%(self.global_cycle()))
        self.bfm_wait_until_test_done(1000)
        self.passtest("Test completed")
        pass
    #f All done
    pass

#c PrngEntropyMux4_0
class PrngEntropyMux4_0(PrngEntropyMux4_Base):
    #f run
    def run(self):
        self.bfm_wait(20)
        self.drive_entropy(1)
        self.drive_entropy(0)
        self.finish_burst()
        self.bfm_wait(200)
        pass
    pass

#c PrngEntropyMux4_1
class PrngEntropyMux4_1(PrngEntropyMux4_Base):
    #f run
    def run(self):
        self.bfm_wait(20)
        self.drive_entropy(2)
        self.drive_entropy(0)
        self.finish_burst()
        self.bfm_wait(200)
        pass
    pass

#c PrngEntropyMux4_2
class PrngEntropyMux4_2(PrngEntropyMux4_Base):
    #f run
    def run(self):
        self.bfm_wait(20)
        self.drive_entropy(4)
        self.drive_entropy(0)
        self.finish_burst()
        self.bfm_wait(200)
        pass
    pass

#c PrngEntropyMux4_3
class PrngEntropyMux4_3(PrngEntropyMux4_Base):
    #f run
    def run(self):
        self.bfm_wait(20)
        self.drive_entropy(8)
        self.drive_entropy(0)
        self.finish_burst()
        self.bfm_wait(200)
        pass
    pass

#c PrngEntropyMux4_4
class PrngEntropyMux4_4(PrngEntropyMux4_Base):
    #f run
    def run(self):
        self.bfm_wait(20)
        for i in range(4):
            self.drive_entropy(1<<i)
            self.drive_entropy(0)
            self.finish_burst()
            pass
        self.bfm_wait(200)
        pass
    pass

#c PrngEntropyMux4_5
class PrngEntropyMux4_5(PrngEntropyMux4_Base):
    #f run
    def run(self):
        self.bfm_wait(20)
        random = Random()
        random.seed("PrngEntropyMux4_5")
        for b in range(10):
            for i in range(32):
                self.drive_entropy(random.randrange(16))
                pass
            self.finish_burst()
            self.bfm_wait(200)
            pass
        pass
    pass

#a Prng Test classes
#c Prng_Base
class Prng_Base(ThExecFile):
    """
    """
    prng_module = "dut"

    l0 = Lfsr(nbits=47, poly=(1<<46)|1)
    l1 = Lfsr(nbits=53, poly=(1<<52)|(1<<51)|(1<<47)|1)
    l2 = Lfsr(nbits=59, poly=(1<<57)|(1<<55)|(1<<52)|1)
    l3 = Lfsr(nbits=61, poly=(1<<60)|(1<<59)|(1<<56)|1)
    # min_valid of 4 will yield 1/16  = 0.0625
    # min_valid of 3 will yield 5/16  = 0.3125
    # min_valid of 2 will yield 10/16 = 0.625
    prng_config = {"min_valid":2}
    lfsrs = (l0, l1, l2, l3)
    #f clock_lfsrs
    def clock_lfsrs(self):
        for i in range(4):
            l = self.lfsrs[i]
            l.clk_once()
            if l.get()==0: l.set(1)
            pass
        pass
    #f get_value
    def get_value(self):
        v=0
        nv = 0
        for l in self.lfsrs:
            lv = l.get(3)
            if lv in [1,2]:
                v ^= lv & 1
                nv = nv + 1
                pass
            pass
        return (nv, v)
    #f drive_entropy
    def drive_entropy(self, entropy, seed_request=0):
        self.prng_config__seed_request.drive(seed_request)
        for e in entropy:
            self.entropy_in.drive(e)
            self.bfm_wait(1)
            self.clock_lfsrs()
            self.prng_config__seed_request.drive(0)
            pass
        self.entropy_in.drive(0)
        pass
    #f run__init - invoked by submodules
    def run__init(self):
        self.log_entropy         = self.log_recorder(self.prng_module)
        self.log_entropy_parser  = EntropyLogParser()
        for l in self.lfsrs: l.set(1)
        self.bfm_wait(10)
        self.prng_config__enable.drive(1)
        self.prng_config__min_valid.drive(self.prng_config["min_valid"])
        self.bfm_wait(10)
        pass
    #f run
    def run(self):
        pass
    #f run__finalize
    def run__finalize(self):
        # self.verbose.error("%s"%(self.global_cycle()))
        self.bfm_wait_until_test_done(1000)
        self.passtest("Test completed")
        pass
    #f All done
    pass

#c Prng_0
class Prng_0(Prng_Base):
    #f run
    def run(self):
        random = Random()
        self.bfm_wait(20)
        self.drive_entropy([1,0,0])
        for j in range(10):
            self.drive_entropy([0],seed_request=1)
            self.bfm_wait(200)
            entropy = []
            for i in range(24):
                entropy.append(random.randrange(2))
                pass
            self.drive_entropy(entropy)
            self.bfm_wait(200)
            pass
        pass
    pass

#a TbPrng Test classes
#c TbPrng_Base
class TbPrng_Base(ThExecFile):
    """
    """
    prng_module = "dut"

    prng_config = {"min_valid":2}
    whiteness_control={ "mode":2, # 0-> count bits, 1 => run_length, 2 => template match, 3=>max excursions
                        "subtype":0, # count ones if 0, toggle if 1; ignored for run length; overlapping if 0; max excursions if 0, number >=N if 1
                        "only_valid":1, # run length counts down only if valid
                        "data":0xc6, # ctr0=#(run length) ctr1=#(>run length), ctr2=max run of zeros, ctr3=max run of ones
                        }
    # For mode 0, either subtype (e.g. 0,0 or 0,1)
    # In subtype 1, Runs test:
    #   Number of runs = K
    #   P(K | random) = erfc( |K-(2.n.p(1-p))| / 2sqrt(2).n.p.(1-p) )
    # ctr[0] = run_length * bits_per_clock
    # ctr[1] = run_length * bits_per_clock * 0.5
    
    # For mode 1 (e.g. 1, 0, 6)
    # Run many times N for M bits each time.
    # Accumulate number of occurrences for max run length = K
    # Bucket appropriately (bucket B):
    #  M=8,     N=16, K <=1,2,3,>=4
    #  M=128,   N=49, K <=4,5,6,7,8,>=9
    #  M=10000, N=75, K <=10,11,12,13,14,15,>=16
    #  Calculate Chi^2 = Sum(B)((count(B)-N.p(B))^2/N.p(B))
    #  where p(B) is given by tables
    # ctr[0] = E(run_length==data)
    # ctr[1] = E(run_length>data)
    # ctr[2] = (max run of zeros)-1
    # ctr[3] = (max run of ones)-1

    # For mode 2 (e.g. 2, 0, 0xc6)
    # Expectation of these is complex; ctrs 1 to 3 are invalid for subtype 1
    # Template T for non-overlapping should have last bit the NOT of the first bit
    #   and should not be splittable in to substring A such that T=AA or AAA or ...
    #   which means that a substream cannot match T in more than one way
    # For subtype 0, the aim is to run M times and accumulate the number of times
    #   out of M that K occurrences happen (K=0,1,2,3,4,>=5).
    #   Depending on M and m there are probabilities that can be derived for the
    #   distribution of K
    #   Apply Chi^2 test on observations
    # ctr[0] = #(6b110000)
    # ctr[1] = #(6b110001)
    # ctr[2] = #(6b110010)
    # ctr[3] = #(6b110011)

    # For mode 3 max excursions (e.g. 3, 0)
    # ctr[0] = #excursions
    # ctr[2] = #max +ve excursion
    # ctr[3] = #max -ve excursion

    # For mode 3 number of excursions (e.g. 3, 1, N)
    # ctr[0] = #excursions
    # ctr[2] = #+ve excursion of N
    # ctr[3] = #-ve excursion of N

    #f drive_entropy
    def drive_entropy(self, entropy, seed_request=0):
        self.prng_config__seed_request.drive(seed_request)
        for e in entropy:
            self.entropy_in.drive(e)
            self.bfm_wait(1)
            self.prng_config__seed_request.drive(0)
            pass
        self.entropy_in.drive(0)
        pass
    #f run__init - invoked by submodules
    def run__init(self):
        self.bfm_wait(10)
        self.prng_config__enable.drive(1)
        self.prng_config__min_valid.drive(self.prng_config["min_valid"])
        self.bfm_wait(10)
        pass
    #f run
    def run(self):
        pass
    #f run__finalize
    def run__finalize(self):
        # self.verbose.error("%s"%(self.global_cycle()))
        self.bfm_wait_until_test_done(1000)
        self.passtest("Test completed")
        pass
    #f All done
    pass

#c TbPrng_0
class TbPrng_0(TbPrng_Base):
    #f run
    def run(self):
        random = Random()
        self.bfm_wait(20)
        self.drive_entropy([1,0,0])
        self.whiteness_control__control.drive((self.whiteness_control["mode"]<<14) |
                                              (self.whiteness_control["subtype"]<<13) |
                                              (self.whiteness_control["only_valid"]<<12) |
                                              (self.whiteness_control["data"]<<0)
                                              
        )
        self.whiteness_control__run_length.drive(5000)
        self.whiteness_control__request.drive(1)
        self.bfm_wait(2)
        self.whiteness_control__request.drive(0)
        self.whiteness_result__valid.wait_for_value(1)
        r = self.whiteness_result__data.value()
        print("%016x"%r)
        pass
    pass

#a Hardware classes
#c PrngEntropyMux4Hw
class PrngEntropyMux4Hw(HardwareThDut):
    clock_desc = [("clk",(0,1,1)),
    ]
    reset_desc   = {"name":"reset_n", "init_value":0, "wait":5}
    module_name  = "prng_entropy_mux_4"
    dut_inputs   = {"entropy_in":4,
    }
    dut_outputs  = {"entropy_out":1
    }
    pass

#c PrngHw
class PrngHw(HardwareThDut):
    clock_desc = [("clk",(0,1,1)),
    ]
    reset_desc   = {"name":"reset_n", "init_value":0, "wait":5}
    module_name  = "prng"
    dut_inputs   = {"entropy_in":1,
                    "prng_config":t_prng_config,
    }
    dut_outputs  = {"prng_status":t_prng_status,
    }
    pass

#c TbPrngHw
class TbPrngHw(HardwareThDut):
    clock_desc = [("clk",(0,1,1)),
    ]
    reset_desc   = {"name":"reset_n", "init_value":0, "wait":5}
    module_name  = "tb_prng"
    dut_inputs   = {"entropy_in":8,
                    "prng_config":t_prng_config,
                    "whiteness_control":t_prng_whiteness_control,
    }
    dut_outputs  = {"prng_status":t_prng_status,
                    "whiteness_result":t_prng_whiteness_result,
    }
    pass

#a Simulation test classes
#c PrngEntropyMux4
class PrngEntropyMux4(TestCase):
    hw = PrngEntropyMux4Hw
    kwargs = {
        # "verbosity":0,
        "th_args":{
        },
    }
    _tests = {
        "mux4_0"  :  (PrngEntropyMux4_0,1*1000,  kwargs),
        "mux4_1"  :  (PrngEntropyMux4_1,1*1000,  kwargs),
        "mux4_2"  :  (PrngEntropyMux4_2,1*1000,  kwargs),
        "mux4_3"  :  (PrngEntropyMux4_3,1*1000,  kwargs),
        "mux4_4"  :  (PrngEntropyMux4_4,1*1000,  kwargs),
        "mux4_5"  :  (PrngEntropyMux4_5,6*1000,  kwargs),
    }
    pass

#c Prng
class Prng(TestCase):
    hw = PrngHw
    kwargs = {
        # "verbosity":0,
        "th_args":{
        },
    }
    _tests = {
        "smoke"  :  (Prng_0,40*1000,  kwargs),
    }
    pass

#c TbPrng
class TbPrng(TestCase):
    hw = TbPrngHw
    kwargs = {
        # "verbosity":0,
        "th_args":{
        },
    }
    _tests = {
        "smoke"  :  (TbPrng_0,40*1000,  kwargs),
    }
    pass

