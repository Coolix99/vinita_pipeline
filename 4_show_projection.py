import os
import numpy as np
import pyvista as pv
import napari
import matplotlib.pyplot as plt

def visualize_and_analyze(output_dir):
    """
    Loops through all projected surfaces, visualizes them using Napari, and 
    creates a histogram of the pixel count data.
    
    Args:
        output_dir (str): Directory containing processed `.vtk` files.
    """
    # Collect pixel count data for histogram
    all_pixel_counts = []

    # Find all subdirectories in output_dir
    dataset_folders = [d for d in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, d))]

    for dataset_name in dataset_folders:
        dataset_path = os.path.join(output_dir, dataset_name)
        vtk_file = os.path.join(dataset_path, dataset_name + ".vtk")

        if not os.path.exists(vtk_file):
            print(f"Skipping {dataset_name}: No .vtk file found.")
            continue
        
        print(f"Loading and visualizing: {vtk_file}")

        # Load surface
        surface = pv.read(vtk_file)
        for name in ["BRE","Smoc"]:
            # Check if required data exists
            if name+"_max_intensity" not in surface.point_data or name+"_pixel_count" not in surface.point_data:
                print(f"Skipping {dataset_name}: Missing projected data.")
                continue

            print(surface.point_data)
            # Extract data
            max_intensity = surface[name+"_max_intensity"]
            pixel_count = surface[name+"_pixel_count"]

            # Store pixel count data for histogram
            all_pixel_counts.extend(pixel_count)

            # Open Napari viewer
            viewer = napari.Viewer(title=f"Projection Visualization - {dataset_name}",ndisplay=3)

            # Convert PyVista mesh to a format Napari can handle
            faces = surface.faces.reshape(-1, 4)[:, 1:4]  # Extract triangle indices
            viewer.add_surface((surface.points, faces,pixel_count), colormap="hsv", opacity=0.7, name="Surface count "+name)
            viewer.add_surface((surface.points, faces,max_intensity), colormap="hsv", opacity=0.7, name="Surface max "+name)
            

            napari.run()  # Keep viewer open until user closes it

    # Plot histogram of pixel counts
    if all_pixel_counts:
        plt.figure(figsize=(8, 5))
        plt.hist(np.log(np.array(all_pixel_counts)+1), bins=100, color="blue", alpha=0.7)
        plt.xlabel("Number of pixels mapped to surface")
        plt.ylabel("Frequency")
        plt.title("Histogram of Pixel Counts")
        plt.grid(True)
        plt.show()
    else:
        print("No valid pixel count data available for histogram.")

if __name__ == "__main__":
    output_dir = "/home/max/Documents/02_Data/structured_data/structured_vinita/Projected"
    visualize_and_analyze(output_dir)
