import os
from pathlib import Path
import argparse
from PIL import Image
from tqdm import tqdm

def prepare_dataset(raw_dir, processed_dir, size):
    """
    Processes a directory of raw images into a clean, resized dataset.

    Args:
        raw_dir (str or Path): Directory containing the original images.
        processed_dir (str or Path): Directory to save the processed images.
        size (tuple): A tuple of (width, height) for resizing.
    """
    raw_path = Path(raw_dir)
    processed_path = Path(processed_dir)

    if not raw_path.exists():
        print(f"Error: Raw data directory not found at '{raw_path}'")
        return

    processed_path.mkdir(parents=True, exist_ok=True)
    print(f"Processing images from: {raw_path}")
    print(f"Saving processed images to: {processed_path}")

    image_files = list(raw_path.glob('*.*'))

    for img_file in tqdm(image_files, desc="Processing Images"):
        try:
            with Image.open(img_file) as img:
                # Convert to grayscale, resize, and save
                processed_img = img.convert('L').resize(size, Image.LANCZOS)
                
                # Save with the same name in the new directory
                processed_img.save(processed_path / img_file.name)
        except Exception as e:
            print(f"Could not process file {img_file}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prepare an image dataset by resizing and converting to grayscale."
    )
    parser.add_argument(
        "--raw_dir",
        type=str,
        required=True,
        help="Path to the directory with raw images."
    )
    parser.add_argument(
        "--processed_dir",
        type=str,
        required=True,
        help="Path to the directory to save processed images."
    )
    parser.add_argument(
        "--img_size",
        type=int,
        default=128,
        help="The target size (width and height) for the processed images."
    )
    args = parser.parse_args()

    prepare_dataset(args.raw_dir, args.processed_dir, (args.img_size, args.img_size))
    print("Dataset preparation complete.")


# python prepare_dataset.py --raw_dir raw_crack_images --processed_dir processed_images --img_size 256