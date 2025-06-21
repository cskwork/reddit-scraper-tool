"""
콘텐츠 분석기 - Ollama를 사용한 지능형 콘텐츠 필터링
"""

import json
import subprocess
import logging
from typing import List, Dict, Any, Optional, Tuple
import requests
from config import OLLAMA_CONFIG

logger = logging.getLogger(__name__)


class ContentAnalyzer:
    """Ollama API를 사용한 콘텐츠 분석기"""

    def __init__(
        self, model: str = None, ollama_url: str = None
    ):
        """
        콘텐츠 분석기 초기화

        Args:
            model: 사용할 Ollama 모델 (None이면 config에서 가져옴)
            ollama_url: Ollama API URL (None이면 config에서 가져옴)
        """
        self.model = model or OLLAMA_CONFIG["default_model"]
        self.ollama_url = ollama_url or OLLAMA_CONFIG["url"]
        self._check_and_suggest_model()

    def _check_and_suggest_model(self) -> None:
        """사용 가능한 모델 확인 및 제안"""
        try:
            # ollama list 명령으로 설치된 모델 확인
            result = subprocess.run(
                ["ollama", "list"], capture_output=True, text=True, check=True
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                if len(lines) > 1:  # 헤더 제외
                    models = [line.split()[0] for line in lines[1:] if line.strip()]

                    if models:
                        logger.info("설치된 Ollama 모델: %s", ", ".join(models))

                        # 기본 모델이 없으면 첫 번째 모델 사용
                        if self.model not in models:
                            self.model = models[0]
                            logger.info("기본 모델 '%s'로 변경", self.model)
                    else:
                        logger.warning(
                            "설치된 Ollama 모델이 없습니다. 'ollama pull gemma3:1b' 실행 필요"
                        )

        except Exception as e:
            logger.error("Ollama 모델 확인 실패: %s", e)

    def analyze_relevance(
        self,
        post: Dict[str, Any],
        keywords: List[str],
        criteria: Optional[Dict[str, Any]] = None,
    ) -> Tuple[float, str]:
        """
        게시물의 관련성 분석

        Args:
            post: Reddit 게시물 데이터
            keywords: 관심 키워드 리스트
            criteria: 추가 평가 기준

        Returns:
            (관련성 점수 0-1, 분석 이유)
        """
        # 기본 평가 기준
        default_criteria = {
            "quality_indicators": [
                "detailed",
                "informative",
                "technical",
                "educational",
            ],
            "negative_indicators": ["spam", "promotional", "low effort", "off-topic"],
            "min_score": 10,
            "min_comments": 5,
        }

        if criteria:
            default_criteria.update(criteria)

        # LLM 프롬프트 구성
        prompt = f"""
        Analyze this Reddit post for relevance and quality.
        
        Keywords of interest: {', '.join(keywords)}
        
        Post Title: {post['title']}
        Post Content: {post['text'][:500]}...
        Score: {post['score']}
        Comments: {post['num_comments']}
        
        Evaluate based on:
        1. Relevance to keywords
        2. Content quality (informative, educational value)
        3. Community engagement (score, comments)
        4. Not spam or low-effort content
        
        Respond with JSON:
        {{
            "relevance_score": 0.0-1.0,
            "quality_score": 0.0-1.0,
            "reason": "brief explanation",
            "key_insights": ["insight1", "insight2"]
        }}
        """

        try:
            # Ollama API 호출
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                },
                timeout=10,
            )

            if response.status_code == 200:
                result = response.json()
                analysis = json.loads(result.get("response", "{}"))

                # 종합 점수 계산
                relevance = analysis.get("relevance_score", 0.5)
                quality = analysis.get("quality_score", 0.5)
                combined_score = relevance * 0.7 + quality * 0.3

                # 커뮤니티 참여도 고려
                if post["score"] >= default_criteria["min_score"]:
                    combined_score += 0.1
                if post["num_comments"] >= default_criteria["min_comments"]:
                    combined_score += 0.1

                combined_score = min(combined_score, 1.0)

                return combined_score, analysis.get("reason", "분석 완료")

        except Exception as e:
            logger.error("LLM 분석 실패: %s", e)

        # 폴백: 간단한 규칙 기반 평가
        score = 0.5
        matched_keywords = len(post.get("keywords_matched", []))

        if matched_keywords > 0:
            score += 0.2 * matched_keywords
        if post["score"] >= default_criteria["min_score"]:
            score += 0.1
        if post["num_comments"] >= default_criteria["min_comments"]:
            score += 0.1

        return min(score, 1.0), f"키워드 {matched_keywords}개 일치"

    def extract_insights(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        게시물 목록에서 주요 인사이트 추출

        Args:
            posts: 분석할 게시물 리스트

        Returns:
            추출된 인사이트
        """
        if not posts:
            return {"summary": "분석할 게시물이 없습니다.", "trends": [], "topics": []}

        # 상위 5개 게시물로 요약 생성
        top_posts = sorted(
            posts, key=lambda x: x.get("relevance_score", 0), reverse=True
        )[:5]

        titles = [p["title"] for p in top_posts]
        prompt = f"""
        Analyze these Reddit post titles and extract key insights:
        
        {chr(10).join(f"{i+1}. {title}" for i, title in enumerate(titles))}
        
        Provide:
        1. Main trends or patterns
        2. Common topics discussed
        3. Brief summary of community interest
        
        Respond in JSON format.
        """

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=10,
            )

            if response.status_code == 200:
                result = response.json()
                return json.loads(result.get("response", "{}"))

        except Exception as e:
            logger.error("인사이트 추출 실패: %s", e)

        return {
            "summary": "상위 게시물 분석 완료",
            "trends": [f"{len(posts)}개 게시물 발견"],
            "topics": list(
                set(kw for p in posts for kw in p.get("keywords_matched", []))
            ),
        }
