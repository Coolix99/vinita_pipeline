from zf_pf_diffeo.plot_static import plot_all_reference_meshes,plot_all_reference_data
import numpy as np
def data_to_value_function(hist_data):
        print("Keys in .npz file:", hist_data.files)
        
        totalcc = np.array([np.median(cc) for cc in hist_data['BRE_max_intensity']])
        
        mean_value = np.nanmean(totalcc)

        # Replace NaN values with the computed mean
        totalcc[np.isnan(totalcc)] = mean_value
        #print(totalcc)
        return totalcc

if __name__ == "__main__":
    # Define folder paths
    maps_dir = "/home/max/Documents/02_Data/structured_data/structured_vinita/Maps"
    proj_dir = "/home/max/Documents/02_Data/structured_data/structured_vinita/Projected"
    
    plot_all_reference_meshes(maps_dir, scale_unit="µm")
    plot_all_reference_data(maps_dir, data_to_value_function, scale_unit="µm")