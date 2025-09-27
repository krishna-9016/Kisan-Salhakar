import os
import re
import pandas as pd
import torch
from torch.utils.data import Dataset
from PIL import Image


class PlantVillageDataset(Dataset):
    """Custom PyTorch Dataset for loading plant village images."""

    def __init__(self, dataframe, class_to_idx_map, transform=None):
        self.df = dataframe
        self.transform = transform
        self.class_to_idx_map = class_to_idx_map

    def __len__(self):
        """Returns the total number of samples in the dataset."""
        return len(self.df)

    def __getitem__(self, idx):
        """Fetches and returns one sample from the dataset at the given index."""
        image_path = self.df.iloc[idx]['filepath']
        label_str = self.df.iloc[idx]['label']

        image = Image.open(image_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        label_idx = self.class_to_idx_map[label_str]

        return image, label_idx


def create_dataframe_from_folders(directory):
    """
    Scans a directory with class-based subfolders (like train/valid)
    and returns a DataFrame of filepaths and labels.
    """
    filepaths = []
    labels = []
    for dirpath, _, filenames in os.walk(directory):
        # Ensure we are in a subdirectory, not the root
        if dirpath != directory:
            label = os.path.basename(dirpath)
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                filepaths.append(filepath)
                labels.append(label)
    return pd.DataFrame({'filepath': filepaths, 'label': labels})


def create_dataframe_from_filenames(directory, train_labels_map):
    """
    Parses a flat directory of test images where the label is in the filename
    (e.g., "AppleScab1.jpg" -> label "Apple___Apple_scab").
    """
    filepaths = []
    labels = []

    # Create a mapping from simple name (e.g., 'potatosca') to full name
    simple_name_map = {
        label.replace('___', '').replace('_', '').lower(): label
        for label in train_labels_map
    }

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(directory, filename)

            # Extract label part from filename (e.g., "PotatoScab1" -> "potatosca")
            base_name = os.path.splitext(filename)[0]
            label_part = re.sub(
                r'\d+$', '', base_name).replace('_', '').lower()

            # Find the corresponding full label name
            full_label = simple_name_map.get(label_part)

            if full_label:
                filepaths.append(filepath)
                labels.append(full_label)

    return pd.DataFrame({'filepath': filepaths, 'label': labels})
