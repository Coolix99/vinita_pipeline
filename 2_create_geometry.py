from zf_pf_geometry.pipeline import do_all

if __name__ == "__main__":
    nuc_path="/home/max/Documents/02_Data/structured_data/structured_vinita/Nuclei"
    mask_path="/home/max/Documents/02_Data/structured_data/structured_vinita/Mask"
    res_geometry_path="/home/max/Documents/02_Data/structured_data/structured_vinita/Geometry"
    do_all([nuc_path],"Image",mask_path,"Image",res_geometry_path,check_surfaces=True)