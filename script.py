#!/usr/bin/env python3

import argparse
import os
import random
import string
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def generate_prefix():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(12))

def create_watermark_pdf(watermark_text, watermark_pdf, pagesize=A4):
    """Creates a watermark PDF with repeated text."""
    c = canvas.Canvas(watermark_pdf, pagesize=pagesize)
    width, height = pagesize
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.2, 0.2, 0.2, alpha=0.5)  # Light gray with transparency

    # Define the step for repeated watermark placement
    step_x, step_y = 300, 120  # Adjust these values as needed

    # Loop to create a tiled watermark
    for x in range(0, int(width), step_x):
        for y in range(0, int(height), step_y):
            c.saveState()
            c.translate(x, y)
            c.rotate(30)  # Rotate watermark
            c.drawString(0, 0, watermark_text)
            c.restoreState()

    c.save()

def apply_watermark(input_pdf, watermark_pdf, output_pdf):
    """Overlays watermark onto each page of the input PDF."""
    pdf_reader = PdfReader(input_pdf)
    watermark_reader = PdfReader(watermark_pdf)
    pdf_writer = PdfWriter()
    watermark_page = watermark_reader.pages[0]

    for page in pdf_reader.pages:
        page.merge_page(watermark_page)  # Overlay watermark
        pdf_writer.add_page(page)

    with open(output_pdf, "wb") as output_file:
        pdf_writer.write(output_file)

def convert_pdf_to_images(pdf_path):
    """Converts a PDF to images for permanent watermarking."""
    return convert_from_path(pdf_path)

def save_images_as_pdf(image_list, output_pdf):
    """Saves images as a new PDF, making the watermark permanent."""
    image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:])

def add_permanent_watermark(input_pdf, watermark_text):
    """Applies a non-removable watermark by converting PDF -> Image -> PDF."""
    temp_pre = f"/tmp/{generate_prefix()}"
    temp_watermark_pdf = f"{temp_pre}_watermark.pdf"
    temp_watermarked_pdf = f"{temp_pre}_watermarked.pdf"
    final_output_pdf = os.path.splitext(input_pdf)[0] + "_watermarked.pdf"

    # Step 1: Create watermark PDF
    create_watermark_pdf(watermark_text, temp_watermark_pdf)

    # Step 2: Apply watermark using merge_page
    apply_watermark(input_pdf, temp_watermark_pdf, temp_watermarked_pdf)

    # Step 3: Convert watermarked PDF to images
    images = convert_pdf_to_images(temp_watermarked_pdf)

    # Step 4: Convert images back to a final PDF (making watermark non-removable)
    save_images_as_pdf(images, final_output_pdf)

    # Cleanup temporary files
    os.remove(temp_watermark_pdf)
    os.remove(temp_watermarked_pdf)

    print(f"✅ Watermarked PDF saved as: {final_output_pdf}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a watermark to a PDF file.")

    parser.add_argument("-i", "--input", nargs="+", required=True, help="paths to the input PDF files")
    parser.add_argument("-t", "--text", required=True, help="text to be used as the watermark")

    args = parser.parse_args()

    for pdf in args.input:
        add_permanent_watermark(pdf, args.text)

