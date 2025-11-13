"""Verify dataset structure for YOLO project.

Usage (cmd.exe):
    python scripts\verify_dataset.py --data data\placas.yaml

It checks data/images/{train,val,test} and data/labels/{train,val,test}.
Prints counts and lists mismatches (images without .txt and labels without image).
Returns exit code 1 if mismatches found, 0 otherwise.
"""
import argparse
import os
from pathlib import Path
import sys
import yaml

IMG_EXTS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}


def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def list_files(directory, exts):
    p = Path(directory)
    if not p.exists():
        return []
    files = [x for x in p.rglob('*') if x.suffix.lower() in exts]
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/placas.yaml', help='path to dataset yaml')
    args = parser.parse_args()

    data_yaml = args.data
    if not Path(data_yaml).exists():
        print(f"Data yaml not found: {data_yaml}")
        sys.exit(2)

    data = load_yaml(data_yaml)

    # Expect train/val/test to point to image directories
    splits = ['train', 'val', 'test']
    total_images = 0
    total_labels = 0
    errors = False

    for s in splits:
        path = data.get(s)
        if not path:
            print(f"Split '{s}' not defined in {data_yaml}")
            continue
        p = Path(path)
        if not p.is_absolute():
            p = (Path.cwd() / p).resolve()

        images_dir = p
        labels_dir = Path(str(p).replace(os.sep + 'images' + os.sep, os.sep + 'labels' + os.sep))
        # Fallback: if data.yaml was configured with data/images/* we expect labels in data/labels/*
        if 'images' in str(p):
            labels_dir = Path(str(p).replace('images', 'labels'))

        imgs = list_files(images_dir, IMG_EXTS)
        labs = list_files(labels_dir, {'.txt'})

        img_stems = {x.stem for x in imgs}
        lab_stems = {x.stem for x in labs}

        only_images = sorted(img_stems - lab_stems)
        only_labels = sorted(lab_stems - img_stems)

        print(f"\nSplit: {s}")
        print(f" Images dir: {images_dir}")
        print(f" Labels dir: {labels_dir}")
        print(f" {len(imgs)} images, {len(labs)} labels")

        if only_images:
            errors = True
            print(f" Images without label ({len(only_images)}): {only_images[:20]}")
        if only_labels:
            errors = True
            print(f" Labels without image ({len(only_labels)}): {only_labels[:20]}")

        total_images += len(imgs)
        total_labels += len(labs)

    print(f"\nTotal images: {total_images}, total labels: {total_labels}")
    if errors:
        print("\nDataset verification failed: mismatches found.")
        sys.exit(1)
    else:
        print("\nDataset verification passed: images and labels match.")
        sys.exit(0)


if __name__ == '__main__':
    main()
