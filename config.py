"""
설정 파일 - 기본 설정값 관리
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Reddit API 설정
REDDIT_CONFIG = {
    "client_id": os.getenv("REDDIT_CLIENT_ID", "your_client_id"),
    "client_secret": os.getenv("REDDIT_CLIENT_SECRET", "your_client_secret"),
    "user_agent": "RedditScraper/1.0 by YourUsername",
}

# Ollama 설정
OLLAMA_CONFIG = {
    "url": os.getenv("OLLAMA_URL", "http://localhost:11434"),
    "default_model": os.getenv("OLLAMA_MODEL", "gemma3:1b"),
    "timeout": 30,
}

# 필터링 기준
FILTER_CRITERIA = {
    "min_relevance_score": 0.5,
    "quality_indicators": [
        "detailed",
        "informative",
        "technical",
        "educational",
        "insightful",
    ],
    "negative_indicators": [
        "spam",
        "promotional",
        "low effort",
        "off-topic",
        "clickbait",
    ],
    "min_post_score": 10,
    "min_comments": 5,
}

# 데이터베이스 설정
DATABASE_CONFIG = {"path": "reddit_scraper.db", "echo": False}

# UI 설정
UI_CONFIG = {"max_posts_display": 20, "max_title_length": 50, "theme": "default"}

# 검색 설정
SEARCH_CONFIG = {"default_limit": 50, "default_subreddits": ["all"], "max_limit": 1000}
