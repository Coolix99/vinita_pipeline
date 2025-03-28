import os
import logging
import napari
import numpy as np
import git
from imaris_ims_file_reader.ims import ims
from zf_pf_geometry.metadata_manager import write_JSON
from tifffile import imwrite
from skimage import measure
from simple_file_checksum import get_checksum
import pyclesperanto_prototype as cle
from skimage.morphology import remove_small_holes

def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger("ImageAnalysisPipeline")

def load_ims(file):
    """Load IMS file and extract image and resolution."""
    image_data = ims(file, ResolutionLevelLock=0)
    return image_data[0], image_data.resolution

def largest_connected_component(mask):
    # Label connected components
    labeled_mask, num_labels = measure.label(mask, background=0, return_num=True)
    
    # Count pixels in each connected component
    component_sizes = np.bincount(labeled_mask.ravel())
    
    # Get the index of the largest connected component
    largest_component_index = np.argmax(component_sizes[1:]) + 1
    
    # Create a mask with only the largest connected component
    largest_component_mask = (labeled_mask == largest_component_index)
    
    return largest_component_mask

def getMask(raw_mask,scales):
    disk_size_opening = int(18/scales[1])
    padded_mask = np.pad(raw_mask, ((0, 0), (disk_size_opening, disk_size_opening), (disk_size_opening, disk_size_opening)), mode='constant', constant_values=0)
    #print(padded_mask.shape)

    closed_mask = cle.closing_sphere(padded_mask,radius_x=disk_size_opening,radius_y=disk_size_opening,radius_z=0)

    closed_mask = closed_mask[:, disk_size_opening:closed_mask.shape[1]-disk_size_opening, disk_size_opening:closed_mask.shape[2]-disk_size_opening]
    processed_mask = np.zeros_like(raw_mask,dtype=bool)
    for z in range(raw_mask.shape[0]):
        opened_slice=np.array(closed_mask[z],dtype=bool)
        filled_slice = remove_small_holes(opened_slice, area_threshold=1000/scales[1]/scales[2]) 
        processed_mask[z] = filled_slice
    original_shape = raw_mask.shape
    return largest_connected_component(processed_mask[:original_shape[0], :original_shape[1], :original_shape[2]])
    

def register_images(vinita_root_dir, result_root_dir):
    logger = setup_logger()
    conditions = ["Development", "Regeneration"]
    repo = git.Repo('.', search_parent_directories=True)
    git_hash = repo.head.object.hexsha
    
    for condition in conditions:
        condition_path = os.path.join(vinita_root_dir, condition)
        if not os.path.exists(condition_path):
            logger.warning(f"Skipping missing directory: {condition_path}")
            continue
        
        for time_folder in os.listdir(condition_path):
            if not time_folder.endswith("hpf"):
                continue  # Skip non-time folders
            
            time_path = os.path.join(condition_path, time_folder)
            time_hpf = int(time_folder.replace("hpf", ""))
            
            for file in os.listdir(time_path):
                if not file.endswith(".ims"):
                    continue  # Skip non-image files
                
                file_path = os.path.join(time_path, file)
                logger.info(f"Processing {file} from {condition} at {time_hpf} hpf")
                
                # Load image
                image, resolution = load_ims(file_path)
                smoc_img=image[3,:,:,:]
                nuclei_img=image[4,:,:,:]
                BRE_img=image[5,:,:,:]
                mask=getMask((smoc_img+nuclei_img+BRE_img)>0,resolution)

                channels={
                    "Smoc": smoc_img,
                    "Nuclei": nuclei_img.astype(np.float64),
                    "BRE": BRE_img,
                    "Mask": mask
                }

                # Split channels and save
                for key in channels:
                   
                    # Napari visualization (for debugging)
                    # viewer = napari.Viewer()
                    # viewer.add_image(channels[key], name=f"Channel {key}")
                    # napari.run()
                    
                    # Create output paths
                    channel_dir = os.path.join(result_root_dir, key)
                    os.makedirs(channel_dir, exist_ok=True)
                    
                    data_name=f"{time_hpf}hpf_{condition}_{file.replace('.ims', '')}"
                    image_folder_dir=os.path.join(channel_dir,data_name)
                    os.makedirs(image_folder_dir, exist_ok=True)

                    image_name = data_name+".tif"
                    save_path = os.path.join(image_folder_dir, image_name)
                    
                    # Save as TIFF
                    imwrite(save_path, channels[key])
                    
                    # Compute checksum
                    checksum = get_checksum(save_path, algorithm="SHA1")
                    
                    # Generate metadata
                    metadata = {
                        "git hash": git_hash,
                        "git repo": "vinita_pipeline",
                        "image file": image_name,
                        "condition": condition,
                        "time in hpf": time_hpf,
                        "experimentalist": "Vinita",
                        "genotype": "WT",
                        "scale": resolution,
                        "image checksum": checksum
                    }
                    
                    # Write metadata
                    write_JSON(image_folder_dir, "Image_"+key, metadata)
                    logger.info(f"Saved metadata for {image_name}")

if __name__ == "__main__":
    #register_images("/media/max_kotz/share_vinita/from_vinita", "/media/max_kotz/share_vinita/structured_vinita")
    register_images("/home/max/Documents/02_Data/structured_data/from_vinita", "/home/max/Documents/02_Data/structured_data/structured_vinita")