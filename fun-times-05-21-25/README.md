# Line Classification with Brightness

This Python script analyzes text in images or PDFs and classifies lines as either "Prompt/Response" or "Commentary" based on their brightness levels. It's particularly useful for processing documents with different text styles or backgrounds.

## Features

- Processes both images and PDF files
- Uses OCR (Optical Character Recognition) to extract text
- Classifies text based on brightness analysis
- Supports custom padding and brightness thresholds
- Outputs results to CSV format with console preview
- Command-line interface for easy usage

## Prerequisites

Before running this script, you'll need to install Poppler, which is used by the pdf2image package to convert PDFs to images:

### macOS
```bash
brew install poppler
```

### Ubuntu/Debian
```bash
sudo apt-get install poppler-utils
```

## Installation

1. Clone this repository
2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

The script can be run directly from the command line:

```bash
# Basic usage (output will be input.pdf.csv)
python line_classification_with_brightness.py input.pdf

# Specify output file
python line_classification_with_brightness.py input.pdf --output results.csv

# Customize padding and threshold
python line_classification_with_brightness.py input.pdf --padding 15 --threshold 200

# Using short options
python line_classification_with_brightness.py input.pdf -o results.csv -p 15 -t 200
```

### Command Line Options

- `pdf_path`: Path to the PDF file (required)
- `--output`, `-o`: Path for the output CSV file (optional)
- `--padding`, `-p`: Padding around text blocks (default: 10)
- `--threshold`, `-t`: Brightness threshold for classification (default: 180)

### Output

The script will:
1. Process the PDF file page by page
2. Show progress updates during processing
3. Save results to a CSV file
4. Display the contents of the CSV in the console

Example output:
```
Converting PDF to images: input.pdf
Processing pages...
Processing page 1/3
Processing page 2/3
Processing page 3/3
Saving results to: input.pdf.csv

CSV Contents:
================================================================================
Text                    Classification
This is some text      Prompt/Response
A comment here         Commentary
More text              Prompt/Response
================================================================================
```

## Parameters

The `classify_line_blocks` function accepts the following parameters:

- `image`: PIL Image object to process
- `padding`: Number of pixels to add around each text block (default: 10)
- `brightness_threshold`: Threshold for classification (default: 180)
  - Text with average brightness below this value is classified as "Prompt/Response"
  - Text with average brightness above this value is classified as "Commentary"

## License

This project is open source and available under the MIT License. 