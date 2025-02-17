from zf_pf_geometry.pipeline import do_all

import logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    nuc_path="/home/max/Documents/02_Data/structured_data/structured_vinita/Nuclei"
    mask_path="/home/max/Documents/02_Data/structured_data/structured_vinita/Mask"
    res_geometry_path="/home/max/Documents/02_Data/structured_data/structured_vinita/Geometry"
    do_all([nuc_path],"Image_Nuclei",mask_path,"Image_Mask",res_geometry_path,check_surfaces=True)