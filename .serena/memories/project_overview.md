# Reddit Scraper Tool Overview

## Purpose
Terminal-based tool that scrapes Reddit content based on user-defined keywords, uses AI/LLM to filter and identify relevant quality information, and stores records of input/output.

## Tech Stack
- **Language**: Python 3.12
- **Environment**: Windows (PowerShell)
- **Key Libraries**: 
  - PRAW (Python Reddit API Wrapper) - for Reddit API access
  - SQLite - for record keeping
  - Rich/Textual - for terminal UI
  - Ollama API - for content analysis ([using gemma3:1b by default][[memory:6915601622667373233]])
  
## Project Structure
- `main.py` - Entry point with CLI argument parsing
- Components to be built:
  - Reddit API integration module
  - Content analyzer with LLM integration
  - Database handler for records
  - Terminal UI for interaction
  - Configuration management