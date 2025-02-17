from zf_pf_diffeo.pipeline import do_referenceGeometries

import logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    # Define folder paths
    maps_dir = "/home/max/Documents/02_Data/structured_data/structured_vinita/Maps"
    proj_dir = "/home/max/Documents/02_Data/structured_data/structured_vinita/Projected"

    # Run processing
    do_referenceGeometries(proj_dir,["experimentalist","genotype","condition","time in hpf"],maps_dir,"projected_data","Projected Surface file name")