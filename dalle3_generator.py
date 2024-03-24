#!/usr/bin/env python3

import os
import csv
import subprocess
import sys
import argparse

def main(csv_file, output_dir):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header
        for row in reader:
            number, message = row
            file_path = os.path.join(output_dir, f"{number}.png")
            subprocess.run(["python", "dalle3.py", "--prompt", message, "--output", file_path], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates images from the messages received in a CSV.')
    parser.add_argument('--csv', '-c', type=str, 
                        help='The full path of the CSV file.')
    parser.add_argument('--output', '-o', type=str, 
                        help='The path of the folder where the images will be saved.')

    args = parser.parse_args()

    main(args.csv, args.output)