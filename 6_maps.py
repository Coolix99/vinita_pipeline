from zf_pf_diffeo.plot_static import plot_all_reference_meshes,plot_all_reference_data

def data_to_value_function(hist_data):
        print("Keys in .npz file:", hist_data.files)
        #print(len(hist_data['cell_count']))
        #print(hist_data['cell_count'])
        #print(len(hist_data['geminin_count']))
        totalcc = np.array([np.sum(cc) for cc in hist_data['cell_count']])
        print(np.sum(totalcc))
        totalgc = np.array([np.sum(gc) for gc in hist_data['geminin_count']])
        rate=totalgc/totalcc
        print(np.max(rate))
        return rate

if __name__ == "__main__":
    # Define folder paths
    maps_dir = "/home/max/Documents/02_Data/structured_data/structured_vinita/Maps"
    proj_dir = "/home/max/Documents/02_Data/structured_data/structured_vinita/Projected"
    from zf_pf_diffeo.pipeline import do_HistPointData

    do_HistPointData(proj_dir,maps_dir,["experimentalist","genotype","condition","time in hpf"],maps_dir,"projected_data","Projected Surface file name")
    #plot_all_reference_data(maps_dir, data_to_value_function, scale_unit="µm")