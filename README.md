# AI Video Analyzer

A modular Python project for analyzing YouTube videos.
It fetches video metadata from YouTube channels, stores them in a persistent local cache, and uses an LLM (OpenAI) to generate factual German summaries or comments.

The project is intentionally built with a clean architecture, no hard-coded secrets, and a maintainable src/ layout.
## Features
- Fetch YouTube channel uploads via the YouTube Data API
- Persistent local cache to avoid re-fetching videos
- Automatic video summaries using OpenAI (Responses API)
- Clear separation of data, logic, and prompting
- No secrets committed to the repository
- Professional Python project structure (src/ layout)

## Project Structure
```pgsql
ai-video-analyzer/
│
├── src/
│   └── ai_video_analyzer/
│       ├── yt/                # YouTube API logic
│       │   ├── ChannelStorage.py
│       │   └── Videogetter.py
│       ├── llm/               # LLM / OpenAI logic
│       │   └── CommentGenerator.py
│       ├── config.py          # Central paths & configuration
│       └── __init__.py
│
├── scripts/
│   └── pipeline.py            # Entry point / orchestration
│
├── data/
│   └── cache/
│       └── videos.json        # Persistent video cache
│
├── secrets/                   # NOT committed
│   ├── openai_key.txt
│   ├── client_secret.json
│   └── template.txt
│
├── README.md
└── .gitignore
```
## Secrets and Configuration
All sensitive data is stored outside of src/ in the secrets/ directory.
### Required files
```pgsql
secrets/
├── openai_key.txt        # OpenAI API key
├── client_secret.json   # YouTube OAuth client secret
└── template.txt         # Prompt rules & style
```
### Important
The secrets/ directory is ignored via .gitignore and must never be committed.#

## Prompt Template (template.txt)
The template contains only rules, style, and structure — no variables.

## Installation

### 1️. Clone the repository
```bash
git clone https://github.com/FeixZeiss/ai-video-analyzer.git
cd ai-video-analyzer
```
### 2. Run setup script
```bash
./setup.sh
```
This will:
- create a virtual environment (.venv)
- install all required dependencies

## 3. Activate the environment
```bash
source .venv/bin/activate
```

## 4. Create secrets dictionary  
```bash
mkdir secrets
```
Add the following files:
- openai_key.txt
- client_secret.json
- template.txt

## Running the Project
### 1. Activate environment
```bash
conda activate youtube_api
export PYTHONPATH=src
export AIVA_SECRETS_DIR=secrets
```
### 2. Running the pipeline
```bash
python scripts/pipeline.py
```
## Cache Behavior
- Videos are fetched only once
- Already known videos are detected via data/cache/videos.json
- Only new videos are processed again
This results in:
   - fewer API calls
   - faster re-runs
   - reproducible results


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

## YouTube API Key (YouTube Data API v3)
### How to obtain the key

1. Go to the Google Cloud Console:
https://console.cloud.google.com/
2. Create a new project (or use an existing one)
3. Open the API Library
4. Enable YouTube Data API v3
5. Go to Credentials → Create credentials → API key
6. Copy the generated key

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