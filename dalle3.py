#!/usr/bin/env python3

import os
import json
import argparse
import requests
import azureoai
from dotenv import load_dotenv
from PIL import Image

def load_variables():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    path=os.path.join(os.curdir, script_dir + ".env")
    load_dotenv(path)

def generate_dalle3(client, prompt):
    return generate_image(client, prompt, 
                        model="dalle3", 
                        size="1792x1024", 
                        quality="hd", 
                        style="natural", 
                        n=1)

def generate_image(client, prompt, model, size, quality, style, n):
    result = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        style=style,
        n=1
    )    
    return json.loads(result.model_dump_json())

def save_image_folder(json_response):
    image_dir = os.path.join(os.curdir, "images")
    os.makedirs(image_dir, exist_ok=True)

    for item in json_response["data"]:
        image_url = item["url"]
        generated_image = requests.get(image_url).content

        base_filename = f"generated_image.png"
        filename, file_extension = os.path.splitext(base_filename)
        count = 1    
        while os.path.exists(os.path.join(image_dir, f"{filename}_{count:0{3}}{file_extension}")):
            count += 1

        final_filename = os.path.join(image_dir, f"{filename}_{count:0{3}}{file_extension}")

        try:
            with open(final_filename, "wb") as image_file:
                image_file.write(generated_image)
        except Exception as e:
            print(f"Error: {e}")
            return None

    return final_filename

def save_image(json_response, output_path):
    try:
        for item in json_response["data"]:
            image_url = item["url"]
            generated_image = requests.get(image_url).content

            with open(output_path, "wb") as image_file:
                image_file.write(generated_image)
                
    except Exception as e:
        print(f"Error: {e}")
        return None

    return output_path

def main(prompt, output_path):
    client = azureoai.setup_client()
    json_response = generate_dalle3(client, prompt)
    final_filename = save_image(json_response, output_path)

    if final_filename:
        text = f"""The image has been generated: {final_filename}"""
        print(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates an image from a text.')
    parser.add_argument('--prompt', '-p', type=str, 
                        help='The text from which the image will be generated.')
    parser.add_argument('--output', '-o', type=str, 
                        help='The full path of the image file to be generated.')
    
    args = parser.parse_args()
    
    load_variables()
    
    main(args.prompt, args.output)        