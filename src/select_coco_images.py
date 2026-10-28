#!/usr/bin/env python3
"""Select COCO 2017 validation images for a manually labeled VLM test set.

Reads instances_val2017.json and writes:
  * a CSV inventory of selected images and their annotated categories/counts
  * a JSONL template with one blank question/answer record per selected image

Example:
 cd "D:\Obsidian Vault\PARA\Projects\LLM\多模态\Mllm_learning"

python .\src\select_coco_images.py `
  --annotations ".\data\annotations\instances_val2017.json" `
  --images ".\data\val2017" `
  --out ".\data\my_vlm_test_set" `
  --categories "person,bicycle" `
  --mode all `
  --count 30 `
  --seed 42
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Filter COCO 2017 validation images by annotated object categories."
    )
    parser.add_argument("--annotations", required=True, type=Path,
                        help="Path to instances_val2017.json")
    parser.add_argument("--images", required=True, type=Path,
                        help="Path to the extracted val2017 image directory")
    parser.add_argument("--out", required=True, type=Path,
                        help="Output directory for selected manifest and JSONL template")
    parser.add_argument("--categories", required=True,
                        help="Comma-separated COCO category names, e.g. person,bicycle")
    parser.add_argument("--mode", choices=("any", "all"), default="any",
                        help="any: image contains at least one requested class; "
                             "all: image contains every requested class (default: any)")
    parser.add_argument("--count", type=int, default=100,
                        help="Maximum number of images to sample (default: 100)")
    parser.add_argument("--min-instances", type=int, default=1,
                        help="Minimum number of annotated instances across requested "
                             "categories (default: 1)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducible sampling (default: 42)")
    parser.add_argument("--questions-per-image", type=int, default=1,
                        help="Blank annotation records to create per image (default: 1)")
    parser.add_argument("--copy-images", action="store_true",
                        help="Copy selected images into OUT/images (otherwise only write paths)")
    return parser.parse_args()


def load_coco(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Annotation JSON not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    args = parse_args()
    requested = [name.strip() for name in args.categories.split(",") if name.strip()]
    if not requested:
        print("Error: --categories must contain at least one category name.", file=sys.stderr)
        return 2
    if args.count < 1 or args.min_instances < 1 or args.questions_per_image < 1:
        print("Error: --count, --min-instances, and --questions-per-image must be >= 1.",
              file=sys.stderr)
        return 2

    coco = load_coco(args.annotations)
    category_id_to_name = {c["id"]: c["name"] for c in coco["categories"]}
    available = set(category_id_to_name.values())
    unknown = sorted(set(requested) - available)
    if unknown:
        print("Unknown COCO categories: " + ", ".join(unknown), file=sys.stderr)
        print("Available categories: " + ", ".join(sorted(available)), file=sys.stderr)
        return 2

    image_by_id = {im["id"]: im for im in coco["images"]}
    counts_by_image: dict[int, Counter[str]] = defaultdict(Counter)
    for ann in coco["annotations"]:
        name = category_id_to_name.get(ann["category_id"])
        if name is not None:
            counts_by_image[ann["image_id"]][name] += 1

    requested_set = set(requested)
    candidates = []
    missing_files = 0
    for image_id, image_info in image_by_id.items():
        image_path = args.images / image_info["file_name"]
        if not image_path.is_file():
            missing_files += 1
            continue
        counts = counts_by_image[image_id]
        present = set(counts) & requested_set
        category_match = (requested_set.issubset(present) if args.mode == "all"
                          else bool(present))
        instance_total = sum(counts.get(name, 0) for name in requested)
        if category_match and instance_total >= args.min_instances:
            candidates.append((image_info, counts, image_path))

    random.Random(args.seed).shuffle(candidates)
    selected = candidates[:args.count]
    args.out.mkdir(parents=True, exist_ok=True)
    copied_images_dir = args.out / "images"
    if args.copy_images:
        import shutil
        copied_images_dir.mkdir(parents=True, exist_ok=True)

    csv_path = args.out / "selected_images.csv"
    jsonl_path = args.out / "annotation_template.jsonl"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "image_id", "file_name", "image_path", "matched_categories",
            "requested_category_counts", "all_annotated_categories",
        ])
        writer.writeheader()
        with jsonl_path.open("w", encoding="utf-8") as jf:
            for image_info, counts, source_path in selected:
                image_id = image_info["id"]
                matched_counts = {name: counts[name] for name in requested if counts.get(name, 0)}
                all_categories = {name: n for name, n in sorted(counts.items())}
                if args.copy_images:
                    import shutil
                    destination = copied_images_dir / source_path.name
                    if not destination.exists():
                        shutil.copy2(source_path, destination)
                    display_path = str(Path("images") / source_path.name)
                else:
                    display_path = str(source_path.resolve())

                writer.writerow({
                    "image_id": image_id,
                    "file_name": image_info["file_name"],
                    "image_path": display_path,
                    "matched_categories": ",".join(matched_counts),
                    "requested_category_counts": json.dumps(matched_counts, ensure_ascii=False),
                    "all_annotated_categories": json.dumps(all_categories, ensure_ascii=False),
                })
                for q_num in range(1, args.questions_per_image + 1):
                    record = {
                        "id": f"coco_{image_id}_q{q_num}",
                        "image": display_path,
                        "coco_image_id": image_id,
                        "question": "",
                        "reference_answer": "",
                        "category": "",
                        "scoring_criteria": "",
                        "annotator_notes": "",
                    }
                    jf.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Matching images found: {len(candidates)}")
    print(f"Selected images: {len(selected)} (seed={args.seed})")
    if missing_files:
        print(f"Images missing from --images directory: {missing_files}")
    print(f"Image list: {csv_path}")
    print(f"Annotation template: {jsonl_path}")
    if args.copy_images:
        print(f"Copied images: {copied_images_dir}")
    if len(selected) < args.count:
        print("Note: fewer images matched than requested; consider --mode any, "
              "a different category set, or a smaller --min-instances.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
