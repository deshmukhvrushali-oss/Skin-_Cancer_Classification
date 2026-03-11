import os
from PIL import Image

dataset_path = "dataset"

def remove_corrupted_images(folder):
    removed = 0

    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                img = Image.open(file_path)
                img.verify()  # verify image
            except Exception:
                print("Removing corrupted:", file_path)
                os.remove(file_path)
                removed += 1

    print("Total corrupted images removed:", removed)

remove_corrupted_images(dataset_path)
print("Cleaning complete!")