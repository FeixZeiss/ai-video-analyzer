# AI Video Analyzer

A lightweight Python-based tool for analyzing YouTube videos using only their public metadata (title, description, tags).  
The project demonstrates how Large Language Models (LLMs) can extract structured insights from unstructured video metadata.

The tool is simple, modular, and easy to extend. It is ideal for experimenting with video analysis workflows or showcasing AI-assisted automation in software engineering portfolios.

## Features

### Metadata extraction
- Video title
- publishing Date 
- tags
- Description

### AI-powered analysis
Using only metadata, the analyzer can generate:
- Summaries

### Local test data support
Supports reading JSON files such as `videos.json` for offline testing.

### Modular design
Clear separation of concerns:
- YouTube API interaction
- LLM-based processing
- File storage utilities
- Test scripts and loaders

## Tech Stack

- Python 3.12
- YouTube Data API v3
- Google API Client
- OpenAI GPT models
- JSON-based storage

## Installation

```bash
git clone https://github.com/<yourname>/ai-video-analyzer
cd ai-video-analyzer

conda env create -f environment.yml
conda activate youtube_api

## Usage
### Insert your YouTube API key

Edit YT/Videogetter.py:
```Python
self.youtube = build("youtube", "v3", developerKey=YOUR_API_KEY)

### Run the example script
'''bash
python TestVideoloader.py

This fetches metadata, and stores the results locally.


##Project Structure#
"""pgsql
ai-video-analyzer/
│
├── YT/
│   ├── Videogetter.py
│
├── ChatGPT/
│   ├── Chatgpt.py
│
├── TestVideoloader.py
├── TestFieStorage.py
├── videos.json
├── videos1.json
├── environment.yml
└── README.md

## Planned Extensions
Possible additions:
 - SEO title suggestions
 - Hashtag recommendations
 - Audience personas
 - Sentiment and tone analysis
 - Topic modeling
 - Social-media post generation

## Contact
Feel free to open an issue or fork the project for improvements.