import os
import random
import shutil
import pandas as pd
from pathlib import Path

def setup_flakycat():
    base_dir = os.getcwd()
    repo_url = "https://github.com/serval-uni-lu/FlakyCat.git"
    repo_name = "FlakyCat"
    temp_repo_path = os.path.join(base_dir, repo_name)
    samples_dir = os.path.join(base_dir, "../dataset/FlakyCat/20Samples")
    output_csv = os.path.join(base_dir, "../dataset/FlakyCat/flakycat_input.csv")

    if not os.path.exists(temp_repo_path):
        print("Cloning FlakyCat repository...")
        os.system(f"git clone {repo_url}")
    
    source_dir = os.path.join(temp_repo_path, "data", "test_files_v0")
    
    if not os.path.exists(source_dir):
        print(f"Error: Could not find source directory at {source_dir}")
        return

    all_files = [f for f in os.listdir(source_dir) if f.endswith('.txt')]
    count = min(20, len(all_files))
    selected_files = random.sample(all_files, count)

    print(f"Processing {count} files into CSV...")
    data = []
    
    if not os.path.exists(samples_dir):
        os.makedirs(samples_dir)

    for file_name in selected_files:
        shutil.copy2(os.path.join(source_dir, file_name), os.path.join(samples_dir, file_name))
        
        try:
            parts = file_name.split('@')[0].split('.')
            project = parts[0]
            test_name = parts[-1]
            class_name = parts[-2] if len(parts) > 2 else "Unknown"
            
            with open(os.path.join(source_dir, file_name), 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            data.append({
                'project': 'FlakyCat',
                'class_name': class_name,
                'test_name': test_name,
                'final_code': code,
                'flaky': 1
            })
        except Exception as e:
            print(f"Skipping {file_name} due to parsing error: {e}")

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    
    print("-" * 30)
    print(f"SUCCESS!")
    print(f"1. 20 raw files copied to: {samples_dir}")
    print(f"2. Predictor input created: {output_csv}")
    print("-" * 30)

if __name__ == "__main__":
    setup_flakycat()