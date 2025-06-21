# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Reddit 스마트 콘텐츠 스크래퍼 (Reddit Smart Content Scraper) - An AI-powered Reddit content filtering and analysis tool written in Python. The application uses PRAW for Reddit API access, Ollama LLM for intelligent content filtering, SQLite for storage, and Rich for terminal UI.

## Development Setup

1. Create and activate Python virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .\.venv\Scripts\Activate.ps1  # Windows PowerShell
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables by copying `.env.example` to `.env` and filling in:
   - `REDDIT_CLIENT_ID` - Get from https://www.reddit.com/prefs/apps
   - `REDDIT_CLIENT_SECRET` - Get from Reddit app creation
   - `OLLAMA_URL` (optional) - Default: http://localhost:11434
   - `OLLAMA_MODEL` (optional) - Default: gemma3:1b

4. Install and configure Ollama:
```bash
# Install Ollama then pull the model
ollama pull gemma3:1b
```

## Running the Application

### Interactive Mode
```bash
python main.py -i
```

### CLI Mode
```bash
# Basic search
python main.py -k "python" "programming"

# Search specific subreddits with limit
python main.py -k "machine learning" -s "MachineLearning" "learnmachinelearning" -l 100
```

## Architecture

The application follows a modular architecture with clear separation of concerns:

- **main.py**: Entry point handling CLI arguments and orchestrating the search/analysis workflow
- **reddit_client.py**: Reddit API wrapper using PRAW for data collection
- **content_analyzer.py**: AI-powered content analysis using Ollama LLM API
- **database.py**: SQLAlchemy-based SQLite database management with SearchRecord and PostRecord models
- **terminal_ui.py**: Rich library-based terminal interface for interactive display
- **config.py**: Centralized configuration management with environment variable loading

### Key Data Flow
1. User provides keywords via CLI or interactive prompts
2. RedditClient searches Reddit using PRAW
3. ContentAnalyzer evaluates each post using Ollama LLM for relevance scoring
4. Posts with relevance_score >= 0.5 are filtered and stored
5. Database saves search records and filtered posts
6. TerminalUI displays results with insights

### Database Schema
- `search_records`: Search metadata, keywords, subreddits, insights
- `post_records`: Individual Reddit posts with relevance scores and analysis

## Configuration

All configuration is centralized in `config.py` with categories:
- `REDDIT_CONFIG`: API credentials and user agent
- `OLLAMA_CONFIG`: LLM model settings and API URL
- `FILTER_CRITERIA`: Content filtering thresholds and quality indicators
- `DATABASE_CONFIG`: SQLite database path and settings
- `UI_CONFIG`: Display limits and formatting
- `SEARCH_CONFIG`: Default search parameters

## Dependencies

Core dependencies:
- `praw==7.8.1`: Reddit API client
- `rich==13.9.4`: Terminal UI framework
- `sqlalchemy==2.0.36`: Database ORM
- `requests==2.32.3`: HTTP client for Ollama API
- `python-dotenv==1.0.1`: Environment variable management
- `click==8.1.8`: CLI framework