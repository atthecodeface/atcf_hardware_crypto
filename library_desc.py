import cdl_desc
from cdl_desc import CdlModule, CdlSimVerilatedModule, CModel, CSrc

class Library(cdl_desc.Library):
    name="crypto"
    pass

class KasumiModules(cdl_desc.Modules):
    name = "kasumi"
    src_dir      = "cdl/kasumi"
    tb_src_dir   = "tb_cdl"
    libraries = {"std":True}
    cdl_include_dirs = ["cdl"]
    export_dirs = cdl_include_dirs + [ src_dir ]
    modules = []
    modules += [ CdlModule("kasumi_fi") ]
    modules += [ CdlModule("kasumi_fo") ]
    modules += [ CdlModule("kasumi_sbox7") ]
    modules += [ CdlModule("kasumi_sbox9") ]
    modules += [ CdlModule("kasumi_cipher_3") ]
    modules += [ CdlModule("tb_kasumi_cipher", src_dir=tb_src_dir) ]
    pass

