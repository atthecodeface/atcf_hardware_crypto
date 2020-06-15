#a Copyright
#  
#  This file 'prng.py' copyright Gavin J Stark 2020
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
This file includes an operating model of the PRNG from the CDL to generate bitstreams to run through assess.
"""
from random import Random
from ..utils.lfsr import Lfsr

t_prng_whiteness_control = {"request":1, "control":16, "run_length":32}
t_prng_whiteness_result  = {"ack":1, "valid":1, "data":64}
t_prng_config = {"enable":1, "min_valid":3, "seed_request":1}
t_prng_data   = {"valid":1, "data":1}
t_prng_status = {"data":t_prng_data, "seed_complete":1}

class Prng(object):
    
    def __init__(self, min_valid):
        self.min_valid = min_valid
        l0 = Lfsr(nbits=47, poly=(1<<46)|1)
        l1 = Lfsr(nbits=53, poly=(1<<52)|(1<<51)|(1<<47)|1)
        l2 = Lfsr(nbits=59, poly=(1<<57)|(1<<55)|(1<<52)|1)
        l3 = Lfsr(nbits=61, poly=(1<<60)|(1<<59)|(1<<56)|1)
        self.lfsrs = (l0, l1, l2, l3)
        for l in self.lfsrs:
            l.set(1)
            pass
        pass
    #f seed
    def seed(self, seed):
        random = Random()
        random.seed(seed)
        for l in self.lfsrs:
            for i in range(4):
                l.set(l.get() ^ random.randrange(0,1<<16))
                l.clk(16)
                pass
            pass
        pass
    #f clock
    def clock(self, n):
        for l in self.lfsrs:
            l.clk(n)
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
        return (nv>=self.min_valid, v)
    pass

seed =  "It was the best of times"
seed =  "The quick brown fox jumps over the lazy dog"
def get_entropy(seed, min_valid=2, bits_per_line=32, attempts_per_line=64, nlines=10000):
    """
    From the discussion in prng.cdl, then min_valid should be 1 or 2 really
    """
    p = Prng(min_valid=min_valid)
    p.seed(seed)
    result = []
    for j in range(nlines):
        r = 0
        n = 0
        i = attempts_per_line
        while i>0:
            (nv,v) = p.get_value()
            i-=1
            p.clock(2)
            if nv:
                r=(r<<1)+v
                n+=1
                if (n==bits_per_line):
                    result.append(r)
                    break
                pass
            pass
        if i>0: p.clock(2*i)
        pass
    return result

import struct
entropy_data = {"one_per_four_32":    (1,4,32),
                "one_per_six_32":     (2,6,32),
                "one_per_sixteen_32": (2,16,32),
                }
entropy_data = {}
total_bits = 1000*1000
for (filename, (min_valid, cycles_per_bit, bits_per_line)) in entropy_data.items():                
    entropy = get_entropy(seed=seed, min_valid=min_valid, bits_per_line=bits_per_line, attempts_per_line=bits_per_line*cycles_per_bit//2, nlines = (total_bits+100*bits_per_line) // bits_per_line)
    with open(filename,"wb") as f:
        for r in entropy:
            f.write(struct.pack("I",r))
            pass
        pass
    pass


def test_sbox(sbox):
    # For a nonlinear sbox, we know that
    #   For any W, {f(W+x)-f(x) | x in S} = half of S
    f=[]
    for w in sbox:
        if w==0: continue
        set_x = set()
        for x in sbox:
            v = sbox[x^w] ^ sbox[x]
            # print("A",w,x,x^w,v,sbox[x],sbox[x^w])
            # if v in set_x:print(w,x,v)
            set_x.add(v)
            pass
        if len(set_x) != len(sbox)/2-1:
            #print(len(set_x),len(sbox))
            f.append(w)
            pass
        pass
    return len(f)

sbox_not = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
sbox_rijndael = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
            0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
            0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
            0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
            0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
            0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
            0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
            0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
            0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
            0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
            0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
            0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
            0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
            0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
            0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
            0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
sbox4 = [3,7,6,4,13,8,9,5,14,15,10,1,2,11,0,12]
sbox_in = sbox_not
sbox_in = sbox4
sbox = {}
for i in range(len(sbox_in)):
    sbox[i] = sbox_in[i]
    pass
for k in range(len(sbox)):
  break
  min=16
  for i in range(16):
    sbox_test = dict(sbox)
    (sbox_test[i], sbox_test[k]) = (sbox_test[k], sbox_test[i])
    l=test_sbox(sbox_test)
    if l<min:
        min=l
        min_i = i
        pass
    pass
  print(min,k,min_i,sbox[k],sbox[min_i])
#import sys
#sys.exit(0)

        

        
