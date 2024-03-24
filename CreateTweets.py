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


    # Definition of the metadata file paths [INPUT]
    speaker_list_path = paths['metadata']['speaker_list_path']
    sessions_table_01_path = paths['metadata']['sessions_table_01_path']
    sessions_table_02_path = paths['metadata']['sessions_table_02_path']

    # Definition of the metadata file paths [OUTPUT]
    handle_table_path = paths['metadata']['handle_table_path']
    tweets_csv_path = paths['metadata']['tweets_csv_path']
    schedule_tweets_path = paths['metadata']['schedule_tweets_path']

    # Definition of the metaprompt file paths [PROCESSING]
    create_handle_table_path = paths['metaprompt']['create_handle_table_path']
    create_tweets_path = paths['metaprompt']['create_tweets_path']
    create_schedule_tweets_path = paths['metaprompt']['create_schedule_tweets_path']

    return speaker_list_path, handle_table_path, tweets_csv_path, sessions_table_01_path, sessions_table_02_path, schedule_tweets_path, create_handle_table_path, create_tweets_path, create_schedule_tweets_path

def main():
    speaker_list_path, handle_table_path, tweets_csv_path, sessions_table_01_path, sessions_table_02_path, schedule_tweets_path, create_handle_table_path, create_tweets_path, create_schedule_tweets_path = load_paths()

    global_start_time = time.time()

    if not os.path.isfile(handle_table_path):
        start_time = time.time()
        print("Creating Table with X (Twitter) Handles...", end="")
        subprocess.run(["python", "gpt4.py", "--files", create_handle_table_path , speaker_list_path], stdout=open(handle_table_path, "w"))
        print(f"done! {time.time() - start_time} seconds")

    if not os.path.isfile(tweets_csv_path):
        start_time = time.time()
        print("Creating CSV table header for tweets...", end="")
        with open(tweets_csv_path, 'w') as f:
            f.write("Numero;Mensaje\n")
        print(f"done! {time.time() - start_time} seconds")

        start_time = time.time()
        print("Processing records up to 20 and adding tweets to the CSV table...", end="")
        subprocess.run(["python", "gpt4.py", "--files", create_tweets_path, handle_table_path, sessions_table_01_path], stdout=open(tweets_csv_path, "a"))
        print(f"done! {time.time() - start_time} seconds")

        start_time = time.time()
        print("Processing records from 21 onwards and adding tweets to the CSV table...", end="")        
        subprocess.run(["python", "gpt4.py", "--files", create_tweets_path, handle_table_path, sessions_table_02_path], stdout=open(tweets_csv_path, "a"))
        print(f"done! {time.time() - start_time} seconds")

    if not os.path.isfile(schedule_tweets_path):   
        print("Scheduling tweets...", end="")
        subprocess.run(["python", "gpt4.py", "--max_tokens", "4000", "--files", create_schedule_tweets_path, tweets_csv_path], stdout=open(schedule_tweets_path, "w"))
        print(f"done! {time.time() - start_time} seconds")

    elapsed_time = time.time() - global_start_time
    minutes = int(elapsed_time / 60)
    seconds = int(elapsed_time % 60)
    print(f"Process completed in: {minutes} minutes {seconds} seconds")
    
if __name__ == "__main__":
    main()