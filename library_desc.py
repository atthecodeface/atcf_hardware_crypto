import cdl_desc
from cdl_desc import CdlModule, CdlSimVerilatedModule, CModel, CSrc

class Library(cdl_desc.Library):
    name="crypto"
    pass

class PrngiModules(cdl_desc.Modules):
    name = "prng"
    src_dir      = "cdl/prng"
    tb_src_dir   = "tb_cdl"
    libraries = {"std":True, "apb":True}
    cdl_include_dirs = ["cdl", "cdl/prng"]
    export_dirs = cdl_include_dirs + [ src_dir ]
    modules = []
    modules += [ CdlModule("prng_whiteness_monitor") ]
    modules += [ CdlModule("prng_entropy_mux_4") ]
    modules += [ CdlModule("prng") ]
    modules += [ CdlModule("apb_target_prng", constants={"cfg_disable_whiteness":0}) ]
    modules += [ CdlModule("tb_prng", src_dir=tb_src_dir) ]
    pass

class KasumiModules(cdl_desc.Modules):
    name = "kasumi"
    src_dir      = "cdl/kasumi"
    tb_src_dir   = "tb_cdl"
    libraries = {"std":True}
    cdl_include_dirs = ["cdl/kasumi"]
    export_dirs = cdl_include_dirs + [ src_dir ]
    modules = []
    modules += [ CdlModule("kasumi_fi") ]
    modules += [ CdlModule("kasumi_fo_cycles_3") ]
    modules += [ CdlModule("kasumi_sbox7") ]
    modules += [ CdlModule("kasumi_sbox9") ]
    modules += [ CdlModule("kasumi_cipher_3") ]
    modules += [ CdlModule("tb_kasumi_cipher", src_dir=tb_src_dir) ]
    pass

