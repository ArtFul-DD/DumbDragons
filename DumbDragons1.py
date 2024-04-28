import json
import random
import os
from PIL import Image

main_directory = r"C:\Users\AF.DD\Pictures\Dumb Dragon's\Layers"

Outline_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Outline"
Scale_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Scale"
Underbelly_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Underbelly"
Wing_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Wing"
Horn_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Horn"
Eye_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Eye"
Background_directory = r"c:\Users\AF.DD\Pictures\Dumb Dragon's\Layers\Background"

Outline_paths = [os.path.join(Outline_directory, Outline) for Outline in os.listdir(Outline_directory)]
Scale_paths = [os.path.join(Scale_directory, f"#{i}.png") for i in range(9)]
Underbelly_paths = [os.path.join(Underbelly_directory, f"#{i}.png") for i in range(9)]
Wing_paths = [os.path.join(Wing_directory, f"#{i}.png") for i in range(9)]
Horn_paths = [os.path.join(Horn_directory, f"#{i}.png") for i in range(8)]
Eye_paths = [os.path.join(Eye_directory, f"#{i}.png") for i in range(6)]
Background_paths = [os.path.join(Background_directory, f"#{i}.png") for i in range(14)]

# Create output folders
png_output_folder = os.path.join(main_directory, "Output", "DumbDragons")
meta_output_folder = os.path.join(main_directory, "Output", "DumbDragons_Metadata")
os.makedirs(png_output_folder, exist_ok=True)
os.makedirs(meta_output_folder, exist_ok=True)

# Loop for generating images
num_images = 100
for i in range(num_images):
    image_info = {"image_path": ""}

    base_image = Image.new("RGBA", (480, 480), (255, 255, 255, 255))

    # Shuffle the order of component paths within each category
    random.shuffle(Outline_paths)
    random.shuffle(Scale_paths)
    random.shuffle(Underbelly_paths)
    random.shuffle(Wing_paths)
    random.shuffle(Horn_paths)
    random.shuffle(Eye_paths)
    random.shuffle(Background_paths)

    # Add the background layer
    background_layer = Image.open(random.choice(Background_paths))
    base_image.paste(background_layer, (0, 0), background_layer)

    # Add the selected layers to the base image (excluding outline and background)
    layer_types = ["scale", "underbelly", "wing", "horn", "eyes"]
    layer_paths_lists = [Scale_paths, Underbelly_paths, Wing_paths, Horn_paths, Eye_paths]
    for layer_type, layer_paths in zip(layer_types, layer_paths_lists):
        layer_path = random.choice(layer_paths)
        print(f"Adding {layer_type} layer from {layer_path}")
        layer = Image.open(layer_path)
        base_image.paste(layer, (0, 0), layer)

    # Add the outline layer
    outline_layer = Image.open(Outline_paths[0])  # Assuming only one outline is selected
    base_image.paste(outline_layer, (0, 0), outline_layer)

    # Save the image
    image_path = os.path.join(png_output_folder, f"DumbDragons_{i}.png")
    base_image.save(image_path)
    image_info["image_path"] = image_path

    # Save metadata
    metadata_file_path = os.path.join(meta_output_folder, f"DumbDragons_{i}_metadata.json")
    with open(metadata_file_path, "w") as metadata_file:
        json.dump(image_info, metadata_file, indent=4)

# Display generated image info
print("Generated image info:")
for i in range(num_images):
    print(f"Image #{i}:")
    print("Image Path:", image_info["image_path"])
