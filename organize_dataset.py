import os
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split

# =========================
# PATHS
# =========================
metadata_path = "HAM10000_metadata.csv"
image_dir1 = "HAM10000_images_part_1"
image_dir2 = "HAM10000_images_part_2"
base_output_dir = "dataset"

# =========================
# READ METADATA
# =========================
print("Reading metadata...")
df = pd.read_csv(metadata_path)

# Keep only required 3 classes
df = df[df['dx'].isin(['bkl', 'mel', 'nv'])]

# Map labels
label_map = {
    'bkl': 'bkl',
    'mel': 'melanoma',
    'nv': 'nevus'
}

df['label'] = df['dx'].map(label_map)

print("Total selected images:", len(df))

# =========================
# TRAIN TEST SPLIT
# =========================
train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    stratify=df['label'],
    random_state=42
)

print("Train images:", len(train_df))
print("Test images:", len(test_df))

# =========================
# CREATE FOLDER STRUCTURE
# =========================
for split in ["train", "test"]:
    for label in ["bkl", "melanoma", "nevus"]:
        folder_path = os.path.join(base_output_dir, split, label)
        os.makedirs(folder_path, exist_ok=True)

print("Folders created successfully!")

# =========================
# MOVE IMAGES FUNCTION
# =========================
def move_images(dataframe, split_type):
    count = 0

    for _, row in dataframe.iterrows():
        image_id = row['image_id'] + ".jpg"
        label = row['label']

        # Check both image folders
        src_path1 = os.path.join(image_dir1, image_id)
        src_path2 = os.path.join(image_dir2, image_id)

        if os.path.exists(src_path1):
            src_path = src_path1
        elif os.path.exists(src_path2):
            src_path = src_path2
        else:
            continue  # skip if image not found

        dest_path = os.path.join(base_output_dir, split_type, label, image_id)

        try:
            shutil.move(src_path, dest_path)   # MOVE (not copy)
            count += 1
        except Exception as e:
            print("Error moving:", image_id, e)

    print(f"{split_type.upper()} images moved:", count)

# =========================
# ORGANIZE DATASET
# =========================
print("Moving train images...")
move_images(train_df, "train")

print("Moving test images...")
move_images(test_df, "test")

print("Dataset organized successfully!")