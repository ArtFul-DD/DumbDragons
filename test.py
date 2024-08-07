import json
import random
import os
from PIL import Image

main_directory = r"C:\Users\AF.DD\Pictures\Dumb Dragon's\Layers"

Outline_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Outline"
Scale_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Scale"
Underbelly_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Underbelly"
Wings_Underbelly_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Wings_Underbelly"
Eye_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Eye"
Horn_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Horn"
Background_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Background"

Outline_paths = [os.path.join(Outline_directory, Outline) for Outline in os.listdir(Outline_directory)]
Scale_paths = [os.path.join(Scale_directory, file) for file in os.listdir(Scale_directory) if file.endswith('.png')]
Wings_Underbelly_paths = [os.path.join(Wings_Underbelly_directory, file) for file in os.listdir(Wings_Underbelly_directory) if file.endswith('.png')]
Eye_paths = [os.path.join(Eye_directory, file) for file in os.listdir(Eye_directory) if file.endswith('.png')]
Horn_paths = [os.path.join(Horn_directory, file) for file in os.listdir(Horn_directory) if file.endswith('.png')]
Background_paths = [os.path.join(Background_directory, file) for file in os.listdir(Background_directory) if file.endswith('.png')]

# Create output folders
png_output_folder = os.path.join(main_directory, "Output", "DumbDragons")
meta_output_folder = os.path.join(main_directory, "Output", "DumbDragons_Metadata")
os.makedirs(png_output_folder, exist_ok=True)
os.makedirs(meta_output_folder, exist_ok=True)

# Initialize the frequency of each component
component_types = ["scale", "wings_underbelly", "eyes", "horn", "background"]
component_paths_lists = [Scale_paths, Wings_Underbelly_paths, Eye_paths, Horn_paths, Background_paths]

component_frequencies = {component_type: {component_path: 0 for component_path in component_paths} for component_type, component_paths in zip(component_types, component_paths_lists)}

# Loop for generating images
num_images = 100
image_infos = []  # List to store image info dictionaries
for i in range(num_images):
    image_info = {"image_path": ""}

    base_image = Image.new("RGBA", (2600, 2600), (255, 255, 255, 255))

    # Shuffle the order of component paths within each category
    random.shuffle(Outline_paths)
    random.shuffle(Scale_paths)
    random.shuffle(Wings_Underbelly_paths)
    random.shuffle(Eye_paths)
    random.shuffle(Horn_paths)
    random.shuffle(Background_paths)

    # Add the background layer
    background_path = random.choice(Background_paths)
    background_layer = Image.open(background_path)
    base_image.paste(background_layer, (0, 0), background_layer)
    image_info["background"] = background_path  # Store the path of the used component

    # Add the selected layers to the base image (excluding outline and background)
    layer_types = ["scale", "wings_underbelly", "eyes", "horn"]
    layer_paths_lists = [Scale_paths, Wings_Underbelly_paths, Eye_paths, Horn_paths]
    for layer_type, layer_paths in zip(layer_types, layer_paths_lists):
        layer_path = random.choice(layer_paths)
        print(f"Adding {layer_type} layer from {layer_path}")
        layer = Image.open(layer_path)
        base_image.paste(layer, (0, 0), layer)
        image_info[layer_type] = layer_path  # Store the path of the used component

        # Update the frequency of the used component
        component_frequencies[layer_type][layer_path] += 1

    # Add the outline layer
    outline_layer = Image.open(Outline_paths[0])  # Assuming only one outline is selected
    base_image.paste(outline_layer, (0, 0), outline_layer)

    # Upscale the image
    upscaled_size = (2600, 2600)  # Define the new size
    upscaled_image = base_image.resize(upscaled_size, Image.LANCZOS)

    # Save the upscaled image
    image_path = os.path.join(png_output_folder, f"#{i}.png")
    upscaled_image.save(image_path)
    image_info["image_path"] = image_path

    image_infos.append(image_info)  # Add the image info dictionary to the list

# Calculate and store the rarity score for each layer after all images have been generated
for image_info in image_infos:
    for layer_type in component_types:
        usage_proportion = component_frequencies[layer_type][image_info[layer_type]] / num_images
        image_info[f"{layer_type}_rarity_score"] = 1 - usage_proportion

    # Save metadata
    metadata_file_path = os.path.join(meta_output_folder, f"#{image_infos.index(image_info)}_metadata.json")
    with open(metadata_file_path, "w") as metadata_file:
        json.dump(image_info, metadata_file, indent=4)


# Display generated image info
print("Generated image info:")
for i in range(num_images):
    print(f"Image #{i}:")
    print("Image Path:", image_infos[i]["image_path"])
    print("Rarity Scores:")
    for layer_type in component_types:
        print(f"{layer_type.capitalize()}: {image_infos[i][f'{layer_type}_rarity_score']}")
