from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import numpy as np
import pandas as pd
import argparse
import os

def classify_line_blocks(image, padding=10, brightness_threshold=180):
    grayscale = image.convert("L")
    width, height = grayscale.size

    # Get line-level data from Tesseract
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    n_boxes = len(data['text'])

    line_blocks = []
    for i in range(n_boxes):
        text = data['text'][i].strip()
        if text == "":
            continue

        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

        # Apply padding, while staying within image bounds
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(width, x + w + padding)
        y2 = min(height, y + h + padding)

        region = grayscale.crop((x1, y1, x2, y2))
        avg_brightness = np.mean(np.array(region))

        classification = "Prompt/Response" if avg_brightness < brightness_threshold else "Commentary"
        line_blocks.append((text, classification))

    return line_blocks

def process_pdf(pdf_path, output_path=None, padding=10, brightness_threshold=180):
    """
    Process a PDF file and classify its text content.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_path (str, optional): Path for the output CSV file. If None, uses the PDF filename with .csv extension
        padding (int, optional): Padding around text blocks. Defaults to 10
        brightness_threshold (int, optional): Brightness threshold for classification. Defaults to 180
    
    Returns:
        str: Path to the generated CSV file
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Convert PDF to images
    print(f"Converting PDF to images: {pdf_path}")
    pdf_images = convert_from_path(pdf_path)
    
    # Process each page
    print("Processing pages...")
    results = []
    for i, img in enumerate(pdf_images, 1):
        print(f"Processing page {i}/{len(pdf_images)}")
        results.extend(classify_line_blocks(img, padding, brightness_threshold))
    
    # Create output path if not provided
    if output_path is None:
        output_path = os.path.splitext(pdf_path)[0] + '.csv'
    
    # Save results to CSV
    print(f"Saving results to: {output_path}")
    df = pd.DataFrame(results, columns=["Text", "Classification"])
    df.to_csv(output_path, index=False)
    
    # Print the contents of the CSV
    print("\nCSV Contents:")
    print("=" * 80)
    print(df.to_string(index=False))
    print("=" * 80)
    
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Process a PDF file and classify its text content based on brightness.')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--output', '-o', help='Path for the output CSV file (optional)')
    parser.add_argument('--padding', '-p', type=int, default=10, help='Padding around text blocks (default: 10)')
    parser.add_argument('--threshold', '-t', type=int, default=180, 
                       help='Brightness threshold for classification (default: 180)')
    
    args = parser.parse_args()
    
    try:
        output_path = process_pdf(
            args.pdf_path,
            args.output,
            args.padding,
            args.threshold
        )
        print(f"Successfully processed PDF. Results saved to: {output_path}")
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
