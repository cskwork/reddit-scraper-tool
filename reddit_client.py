"""
Reddit API 클라이언트 - PRAW를 사용한 Reddit 데이터 수집
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

import praw

from config import REDDIT_CONFIG

logger = logging.getLogger(__name__)


class RedditClient:
    """Reddit API 클라이언트"""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        """
        Reddit 클라이언트 초기화

        Args:
            client_id: Reddit API 클라이언트 ID
            client_secret: Reddit API 클라이언트 시크릿
            user_agent: User Agent 문자열
        """
        self.reddit = praw.Reddit(
            client_id=client_id or REDDIT_CONFIG["client_id"],
            client_secret=client_secret or REDDIT_CONFIG["client_secret"],
            user_agent=user_agent or REDDIT_CONFIG["user_agent"],
        )

    def search_posts(
        self, keywords: List[str], subreddits: List[str], limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        키워드로 Reddit 게시물 검색

        Args:
            keywords: 검색할 키워드 리스트
            subreddits: 검색할 서브레딧 리스트
            limit: 가져올 게시물 수

        Returns:
            게시물 정보 딕셔너리 리스트
        """
        posts = []
        query = " OR ".join(keywords)

        for subreddit_name in subreddits:
            try:
                if subreddit_name.lower() == "all":
                    subreddit = self.reddit.subreddit("all")
                else:
                    subreddit = self.reddit.subreddit(subreddit_name)

                # 검색 수행
                for submission in subreddit.search(query, limit=limit):
                    post_data = {
                        "id": submission.id,
                        "title": submission.title,
                        "author": (
                            str(submission.author) if submission.author else "[deleted]"
                        ),
                        "subreddit": submission.subreddit.display_name,
                        "text": submission.selftext,
                        "url": submission.url,
                        "score": submission.score,
                        "num_comments": submission.num_comments,
                        "created_utc": datetime.fromtimestamp(submission.created_utc),
                        "permalink": f"https://reddit.com{submission.permalink}",
                        "keywords_matched": [
                            kw
                            for kw in keywords
                            if kw.lower() in submission.title.lower()
                            or kw.lower() in submission.selftext.lower()
                        ],
                    }
                    posts.append(post_data)

            except Exception as e:
                logger.error(f"서브레딧 {subreddit_name} 검색 중 오류: {e}")

        return posts

    def get_post_comments(self, post_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        게시물의 댓글 가져오기

        Args:
            post_id: Reddit 게시물 ID
            limit: 가져올 댓글 수

        Returns:
            댓글 정보 딕셔너리 리스트
        """
        comments = []

        try:
            submission = self.reddit.submission(id=post_id)
            submission.comments.replace_more(limit=0)  # 더보기 제거

            for comment in submission.comments.list()[:limit]:
                comment_data = {
                    "id": comment.id,
                    "author": str(comment.author) if comment.author else "[deleted]",
                    "body": comment.body,
                    "score": comment.score,
                    "created_utc": datetime.fromtimestamp(comment.created_utc),
                }
                comments.append(comment_data)

        except Exception as e:
            logger.error(f"댓글 가져오기 오류: {e}")

        return comments
