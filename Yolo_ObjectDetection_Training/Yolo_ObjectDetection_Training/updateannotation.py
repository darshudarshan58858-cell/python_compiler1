import os
import glob

def update_annotation_files(dataset_path):
    """
    Update class indices in YOLO annotation files
    """
    # Mapping from old indices to new indices
    class_mapping = {
        '3': '0',  # EarlyBlight: 3 -> 0
        '4': '1',  # virus: 4 -> 1
        '5': '2',  # Healthy: 5 -> 2
        '8': '3',  # Powdery: 8 -> 3
        '9': '4'   # Rust: 9 -> 4
    }
    
    # Find all .txt files in train/labels, val/labels, and test/labels directories
    for split in ['train', 'val', 'test']:
        labels_path = os.path.join(dataset_path, split, 'labels')
        if os.path.exists(labels_path):
            txt_files = glob.glob(os.path.join(labels_path, '*.txt'))
            
            for txt_file in txt_files:
                try:
                    # Read the file
                    with open(txt_file, 'r') as f:
                        lines = f.readlines()
                    
                    # Update class indices
                    updated_lines = []
                    for line in lines:
                        if line.strip():  # Skip empty lines
                            parts = line.strip().split()
                            if len(parts) >= 5:  # Valid YOLO format: class x y w h
                                old_class = parts[0]
                                if old_class in class_mapping:
                                    parts[0] = class_mapping[old_class]
                                    print(f"Updated {txt_file}: class {old_class} -> {parts[0]}")
                                updated_lines.append(' '.join(parts) + '\n')
                            else:
                                updated_lines.append(line)  # Keep as is if invalid format
                    
                    # Write back the updated content
                    with open(txt_file, 'w') as f:
                        f.writelines(updated_lines)
                        
                except Exception as e:
                    print(f"Error processing {txt_file}: {e}")

# Usage
dataset_path = r"C:\Users\ADMIN\Desktop\Train_Model\Yolo_ObjectDetection_Training\dataset"
update_annotation_files(dataset_path)
print("Annotation files updated successfully!")



# import os
# import glob
# from collections import Counter

# def diagnose_dataset(dataset_path):
#     """
#     Diagnose YOLO dataset to find class index issues
#     """
#     print("=== YOLO Dataset Diagnostic ===\n")
    
#     # Check data.yaml file
#     yaml_path = os.path.join(dataset_path, r"C:\Users\ADMIN\Desktop\Train_Model\Yolo_ObjectDetection_Training\data.yaml")
#     if os.path.exists(yaml_path):
#         print("✓ data.yaml found")
#         print("Content of data.yaml:")
#         with open(yaml_path, 'r') as f:
#             print(f.read())
#         print("-" * 50)
#     else:
#         print("✗ data.yaml not found!")
#         return
    
#     # Check each split directory
#     all_classes = set()
    
#     for split in ['train', 'val', 'test']:
#         labels_path = os.path.join(dataset_path, split, 'labels')
#         images_path = os.path.join(dataset_path, split, 'images')
        
#         print(f"\n=== {split.upper()} SET ===")
        
#         if not os.path.exists(labels_path):
#             print(f"✗ {labels_path} not found!")
#             continue
            
#         if not os.path.exists(images_path):
#             print(f"✗ {images_path} not found!")
#             continue
            
#         # Count files
#         txt_files = glob.glob(os.path.join(labels_path, '*.txt'))
#         img_files = glob.glob(os.path.join(images_path, '*.*'))
        
#         print(f"✓ Labels folder: {len(txt_files)} files")
#         print(f"✓ Images folder: {len(img_files)} files")
        
#         # Check class indices in annotation files
#         split_classes = []
#         sample_files = []
        
#         for txt_file in txt_files[:10]:  # Check first 10 files
#             try:
#                 with open(txt_file, 'r') as f:
#                     lines = f.readlines()
#                     for line_num, line in enumerate(lines, 1):
#                         if line.strip():
#                             parts = line.strip().split()
#                             if len(parts) >= 5:
#                                 class_id = parts[0]
#                                 split_classes.append(class_id)
#                                 all_classes.add(class_id)
                                
#                                 # Store sample for debugging
#                                 if len(sample_files) < 3:
#                                     sample_files.append({
#                                         'file': os.path.basename(txt_file),
#                                         'line': line_num,
#                                         'content': line.strip()
#                                     })
#             except Exception as e:
#                 print(f"Error reading {txt_file}: {e}")
        
#         # Show class distribution for this split
#         if split_classes:
#             class_counts = Counter(split_classes)
#             print(f"Class indices found: {sorted(class_counts.keys())}")
#             print(f"Class distribution: {dict(class_counts)}")
            
#             # Show sample annotations
#             print("Sample annotations:")
#             for sample in sample_files:
#                 print(f"  {sample['file']} (line {sample['line']}): {sample['content']}")
#         else:
#             print("No valid annotations found!")
    
#     print(f"\n=== SUMMARY ===")
#     print(f"All class indices found across dataset: {sorted(all_classes)}")
    
#     # Check if indices are valid (should be 0, 1, 2, 3, 4 for 5 classes)
#     expected_classes = set(str(i) for i in range(len(all_classes)))
#     if all_classes == expected_classes:
#         print("✓ Class indices are valid and consecutive starting from 0")
#     else:
#         print("✗ PROBLEM FOUND!")
#         print(f"Expected class indices: {sorted(expected_classes)}")
#         print(f"Actual class indices: {sorted(all_classes)}")
#         print("You need to fix the annotation files!")

# # Usage
# dataset_path = r"C:\Users\ADMIN\Desktop\Train_Model\Yolo_ObjectDetection_Training\dataset"
# diagnose_dataset(dataset_path)