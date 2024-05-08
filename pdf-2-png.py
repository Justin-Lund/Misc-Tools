"""
Script Name: pdf-2-png.py
Author: Justin Lund
Last modified: 04/16/24
Date created: 12/05/23
Version: 1.0

Purpose: Convert PDF to series of PNG images

Dependencies: poppler
- On MacOS: brew install poppler
- On Ubuntu: apt-get install poppler-utis

Paramaters:
-i / --input <filename>
-o / --output <output folder name>
-r / --dpi <number> (Resolution / DPI quality - defaults to 600)

Usage:
python3 pdf-2-png.py -i filename.pdf -o pdf_images
python3 pdf-2-png.py -i filename.pdf -o pdf_images -r 800
"""

import argparse
import os
import subprocess

def convert_pdf_to_pngs(pdf_path, output_folder, dpi=600):
    # Make sure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create a full output path pattern
    output_path_pattern = os.path.join(output_folder, "")

    # Run the pdftoppm command to convert each page to a PNG
    command = ["pdftoppm", "-png", "-r", str(dpi), pdf_path, output_path_pattern]
    subprocess.run(command)

    # Rename the files
    for filename in os.listdir(output_folder):
        if filename.endswith('.png'):
            os.rename(
                os.path.join(output_folder, filename),
                os.path.join(output_folder, filename.replace('-', ''))
            )

if __name__ == "__main__":
    # Initialize argument parser
    parser = argparse.ArgumentParser(description='Convert a PDF into PNG images.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input PDF file.')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output folder for PNGs.')
    parser.add_argument('-r', '--dpi', type=int, default=600, help='DPI for the output images.')

    # Parse the arguments
    args = parser.parse_args()

    # Run the conversion
    convert_pdf_to_pngs(args.input, args.output, args.dpi)
