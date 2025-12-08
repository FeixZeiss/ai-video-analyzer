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

## API Configuration

To run the AI Video Analyzer, you need two API keys:

1. An **OpenAI API Key** (for ChatGPT-based analysis)
2. A **YouTube Data API v3 Key** (for fetching video metadata)

Below is a short guide on how to obtain both keys and where to place them in the project.

---

## OpenAI API Key (ChatGPT)

### How to obtain the key

1. Log in to your OpenAI account:  
   https://platform.openai.com/

2. Go to **User Menu → View API Keys**  
3. Click **Create new secret key**  
4. Copy the generated key (it starts with `sk-`)

### Where to store it

Do **NOT** put the key inside the repository.

Instead, set it as an **environment variable**:

```bash
export OPENAI_API_KEY="your-key-here"


## YouTube API Key (YouTube Data API v3)
How to obtain the key

Go to the Google Cloud Console:
https://console.cloud.google.com/

Create a new project (or use an existing one)

Open the API Library

Enable YouTube Data API v3

Go to Credentials → Create credentials → API key

Copy the generated key

Where to store it

Set it as an environment variable:

export YOUTUBE_API_KEY="your-key-here"


To link it with the YouTube request logic, update the constructor in:

YT/Videogetter.py:

import os
self.youtube = build(
    "youtube",
    "v3",
    developerKey=os.getenv("YOUTUBE_API_KEY")
)

Important Note

Do not store API keys or OAuth tokens in the repository.
Make sure .gitignore includes:

ChatGPT/key.txt
YT/token/
.env

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
