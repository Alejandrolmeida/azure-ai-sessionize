#!/usr/bin/env python3

import subprocess
import os
import time
import json

def load_paths():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Load paths from a JSON file
    with open(os.path.join(script_dir, 'settings.json'), 'r') as f:
        paths = json.load(f)

    # Add script_dir prefix to all paths
    for category in paths:
        for key in paths[category]:
            paths[category][key] = os.path.join(script_dir, paths[category][key])

    # Definition of the metadata file paths
    tweets_csv_path = paths['metadata']['tweets_csv_path']
    imagedescription_table_path = paths['metadata']['imagedescription_table_path']
    pictures_path = paths['metadata']['pictures_path']

    # Definition of the metaprompt file paths
    create_imagedescription_path = paths['metaprompt']['create_imagedescription_path']

    return create_imagedescription_path, tweets_csv_path, imagedescription_table_path, pictures_path

def main():
    create_imagedescription_path, tweets_csv_path, imagedescription_table_path, pictures_path = load_paths()

    global_start_time = time.time()

    if not os.path.isfile(imagedescription_table_path):
        start_time = time.time()
        print("Creating table with image descriptions...", end="")
        subprocess.run(["python", "gpt4.py", "--max_tokens", "4000", "--files", create_imagedescription_path, tweets_csv_path], stdout=open(imagedescription_table_path, "w"))
        print(f"done! {time.time() - start_time} seconds")
 
    start_time = time.time()
    print("Processing records and adding image descriptions to the CSV table...")
    subprocess.run(["python", "dalle3_generator.py", "--csv", imagedescription_table_path, "--output", pictures_path])
    print(f"done! {time.time() - start_time} seconds")

    elapsed_time = time.time() - global_start_time
    minutes = int(elapsed_time / 60)
    seconds = int(elapsed_time % 60)
    print(f"Process completed in: {minutes} minutes {seconds} seconds")

if __name__ == "__main__":
    main()