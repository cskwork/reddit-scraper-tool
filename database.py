"""
데이터베이스 모듈 - SQLAlchemy를 사용한 스크래핑 기록 저장
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    JSON,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class SearchRecord(Base):
    """검색 기록 테이블"""

    __tablename__ = "search_records"

    id = Column(Integer, primary_key=True)
    search_id = Column(String(50), unique=True)
    keywords = Column(JSON)  # 검색 키워드 리스트
    subreddits = Column(JSON)  # 검색한 서브레딧 리스트
    created_at = Column(DateTime, default=datetime.utcnow)
    post_count = Column(Integer)
    filtered_count = Column(Integer)  # 필터링 후 게시물 수
    insights = Column(JSON)  # AI가 추출한 인사이트


class PostRecord(Base):
    """게시물 기록 테이블"""

    __tablename__ = "post_records"

    id = Column(Integer, primary_key=True)
    search_id = Column(String(50))  # 검색 기록 참조
    reddit_id = Column(String(20), unique=True)
    title = Column(Text)
    author = Column(String(100))
    subreddit = Column(String(100))
    content = Column(Text)
    url = Column(Text)
    score = Column(Integer)
    num_comments = Column(Integer)
    created_utc = Column(DateTime)
    permalink = Column(Text)
    relevance_score = Column(Float)  # AI 분석 점수
    analysis_reason = Column(Text)  # AI 분석 이유
    keywords_matched = Column(JSON)
    saved_at = Column(DateTime, default=datetime.utcnow)


class Database:
    """데이터베이스 관리 클래스"""

    def __init__(self, db_path: str = "reddit_scraper.db"):
        """
        데이터베이스 초기화

        Args:
            db_path: SQLite 데이터베이스 파일 경로
        """
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        Base.metadata.create_all(self.engine)
        self.session_local = sessionmaker(bind=self.engine)

    def save_search(
        self,
        search_id: str,
        keywords: List[str],
        subreddits: List[str],
        post_count: int,
        filtered_count: int,
        insights: Dict[str, Any],
    ) -> None:
        """
        검색 기록 저장

        Args:
            search_id: 고유 검색 ID
            keywords: 검색 키워드
            subreddits: 검색한 서브레딧
            post_count: 전체 게시물 수
            filtered_count: 필터링된 게시물 수
            insights: AI 인사이트
        """
        with self.session_local() as session:
            record = SearchRecord(
                search_id=search_id,
                keywords=keywords,
                subreddits=subreddits,
                post_count=post_count,
                filtered_count=filtered_count,
                insights=insights,
            )
            session.add(record)
            session.commit()

    def save_posts(self, search_id: str, posts: List[Dict[str, Any]]) -> None:
        """
        게시물 목록 저장

        Args:
            search_id: 검색 ID
            posts: 저장할 게시물 리스트
        """
        with self.session_local() as session:
            for post in posts:
                # 중복 확인
                existing = (
                    session.query(PostRecord).filter_by(reddit_id=post["id"]).first()
                )

                if not existing:
                    record = PostRecord(
                        search_id=search_id,
                        reddit_id=post["id"],
                        title=post["title"],
                        author=post["author"],
                        subreddit=post["subreddit"],
                        content=post["text"],
                        url=post["url"],
                        score=post["score"],
                        num_comments=post["num_comments"],
                        created_utc=post["created_utc"],
                        permalink=post["permalink"],
                        relevance_score=post.get("relevance_score", 0.0),
                        analysis_reason=post.get("analysis_reason", ""),
                        keywords_matched=post.get("keywords_matched", []),
                    )
                    session.add(record)
            session.commit()

    def get_recent_searches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        최근 검색 기록 조회

        Args:
            limit: 조회할 기록 수

        Returns:
            검색 기록 리스트
        """
        with self.session_local() as session:
            searches = (
                session.query(SearchRecord)
                .order_by(SearchRecord.created_at.desc())
                .limit(limit)
                .all()
            )

            return [
                {
                    "search_id": s.search_id,
                    "keywords": s.keywords,
                    "subreddits": s.subreddits,
                    "created_at": s.created_at.isoformat(),
                    "post_count": s.post_count,
                    "filtered_count": s.filtered_count,
                    "insights": s.insights,
                }
                for s in searches
            ]

    def get_posts_by_search(self, search_id: str) -> List[Dict[str, Any]]:
        """
        특정 검색의 게시물 조회

        Args:
            search_id: 검색 ID

        Returns:
            게시물 리스트
        """
        with self.session_local() as session:
            posts = (
                session.query(PostRecord)
                .filter_by(search_id=search_id)
                .order_by(PostRecord.relevance_score.desc())
                .all()
            )

            return [
                {
                    "reddit_id": p.reddit_id,
                    "title": p.title,
                    "author": p.author,
                    "subreddit": p.subreddit,
                    "score": p.score,
                    "relevance_score": p.relevance_score,
                    "analysis_reason": p.analysis_reason,
                    "permalink": p.permalink,
                    "saved_at": p.saved_at.isoformat(),
                }
                for p in posts
            ]

    def get_top_posts(self, days: int = 7, limit: int = 20) -> List[Dict[str, Any]]:
        """
        최근 N일간 상위 게시물 조회

        Args:
            days: 조회 기간 (일)
            limit: 조회할 게시물 수

        Returns:
            상위 게시물 리스트
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        with self.session_local() as session:
            posts = (
                session.query(PostRecord)
                .filter(PostRecord.saved_at >= cutoff_date)
                .order_by(PostRecord.relevance_score.desc())
                .limit(limit)
                .all()
            )

            return [
                {
                    "title": p.title,
                    "subreddit": p.subreddit,
                    "score": p.score,
                    "relevance_score": p.relevance_score,
                    "permalink": p.permalink,
                    "keywords_matched": p.keywords_matched,
                }
                for p in posts
            ]
