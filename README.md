# PDF Image to Text Pipeline

A robust image processing and OCR pipeline that successfully extracted and processed over **1 million rows** of data from image-based PDFs into a set of structured JSON files for MongoDB database using Google Cloud Vision API.

## 🚀 Key Features

- Processes image-based PDFs at scale
- Intelligent image slicing for optimal OCR accuracy
- Parallel processing with thread pooling
- Built-in caching to prevent redundant processing
- Successfully processed 1M+ rows with high accuracy

## 📋 Prerequisites

- Python 3.7+
- Google Cloud SDK
- Active Google Cloud Vision API credentials
- PIL (Python Imaging Library)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/hamadrehman/gcloud-ocr-sample
cd gcloud-ocr-sample
```

2. Install required packages:
```bash
pip install Pillow google-cloud-vision
```

3. Set up Google Cloud credentials:
```bash
gcloud auth application-default login
```

## 💻 Usage

Run the script by providing the base folder containing your images:

```bash
python process_images.py /path/to/images
```

The script will:
1. Recursively find all JPG images in the specified directory
2. Slice each image into horizontal segments
3. Process each slice with Google Cloud Vision OCR
4. Store results in JSON format

## 📁 Directory Structure

```
base_folder/
├── image1.jpg
├── image1_slices/
│   ├── image1_row_1.jpg
│   ├── image1_row_2.jpg
│   └── output/
│       ├── output_image1_row_1.json
│       └── output_image1_row_2.json
└── image2.jpg
```

## ⚙️ Configuration

- Default number of slices per image: 17
- Maximum concurrent OCR operations: 5
- Supported image format: JPG

## 🏆 Performance

- Successfully processed 1,000,000+ rows
- Parallel processing enables efficient batch operations
- Built-in caching prevents redundant API calls
- Intelligent error handling ensures pipeline continuity

## 📈 Scaling Considerations

- Adjust `max_workers` in ThreadPoolExecutor based on API quotas
- Monitor Google Cloud Vision API usage
- Implement appropriate rate limiting

## ⚠️ Known Limitations

- Currently only processes JPG files
- Fixed slice count may need adjustment for different image sizes
- Requires Google Cloud Vision API access
- Memory usage scales with image size

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Cloud Vision API for reliable OCR processing
- The open source community for various supporting libraries

## 📧 Contact

For questions and feedback, please open an issue on this repository.
