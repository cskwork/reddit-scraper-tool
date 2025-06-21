#!/usr/bin/env python3
"""
Reddit 콘텐츠 스크래퍼 - 키워드 기반 스마트 필터링 도구
"""

import argparse
import uuid
import logging
from reddit_client import RedditClient
from content_analyzer import ContentAnalyzer
from database import Database
from terminal_ui import TerminalUI


def main():
    """메인 실행 함수"""
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # 컴포넌트 초기화
    ui = TerminalUI()
    db = Database()

    # 헤더 표시
    ui.display_header()

    # CLI 모드 처리
    parser = argparse.ArgumentParser(description="Reddit 콘텐츠 스크래퍼")
    parser.add_argument("--keywords", "-k", nargs="+", help="검색할 키워드들")
    parser.add_argument(
        "--subreddits", "-s", nargs="+", help="검색할 서브레딧들", default=["all"]
    )
    parser.add_argument("--limit", "-l", type=int, help="가져올 게시물 수", default=50)
    parser.add_argument("--interactive", "-i", action="store_true", help="대화형 모드")

    args = parser.parse_args()

    # 대화형 모드
    if args.interactive or not args.keywords:
        while True:
            choice = ui.prompt_menu()

            if choice == "1":  # 새로운 검색
                keywords = ui.prompt_keywords()
                subreddits = ui.prompt_subreddits()
                limit = 50

                # 검색 수행
                search_and_analyze(ui, db, keywords, subreddits, limit)

            elif choice == "2":  # 검색 기록
                searches = db.get_recent_searches()
                ui.display_search_history(searches)

                if searches and ui.confirm_action("특정 검색 결과를 보시겠습니까?"):
                    search_id = input("검색 ID (처음 8자리): ")
                    posts = db.get_posts_by_search(search_id)
                    ui.display_posts(posts, f"검색 ID: {search_id}")

            elif choice == "3":  # 상위 게시물
                days = int(input("며칠간의 데이터? (기본: 7): ") or "7")
                posts = db.get_top_posts(days=days)
                ui.display_posts(posts, f"최근 {days}일 상위 게시물")

            elif choice == "4":  # 설정
                ui.display_error("설정 기능은 아직 구현되지 않았습니다.")

            elif choice == "5":  # 종료
                ui.display_success("프로그램을 종료합니다.")
                break

    else:
        # CLI 모드로 단일 검색 수행
        search_and_analyze(ui, db, args.keywords, args.subreddits, args.limit)


def search_and_analyze(ui, db, keywords, subreddits, limit):
    """검색 및 분석 수행"""
    try:
        # 검색 ID 생성
        search_id = str(uuid.uuid4())

        # 파라미터 표시
        ui.display_search_params(keywords, subreddits, limit)

        # Reddit 클라이언트 초기화
        ui.display_success("Reddit API 연결 중...")
        reddit_client = RedditClient()

        # 콘텐츠 분석기 초기화
        analyzer = ContentAnalyzer()

        # 진행 상황 표시
        with ui.show_progress("Reddit 검색 중...") as progress:
            task = progress.add_task("검색 중...", total=100)

            # Reddit에서 게시물 가져오기
            progress.update(task, advance=20, description="게시물 수집 중...")
            posts = reddit_client.search_posts(keywords, subreddits, limit)

            # AI 분석 수행
            progress.update(task, advance=30, description="AI 분석 중...")
            filtered_posts = []

            for post in posts:
                relevance_score, reason = analyzer.analyze_relevance(post, keywords)
                post["relevance_score"] = relevance_score
                post["analysis_reason"] = reason

                # 관련성 점수가 0.5 이상인 게시물만 필터링
                if relevance_score >= 0.5:
                    filtered_posts.append(post)

                # 진행률 업데이트
                progress.update(task, advance=40 / len(posts) if posts else 0)

            # 인사이트 추출
            progress.update(task, advance=10, description="인사이트 추출 중...")
            insights = analyzer.extract_insights(filtered_posts)

            # 데이터베이스 저장
            progress.update(task, description="데이터 저장 중...")
            db.save_search(
                search_id,
                keywords,
                subreddits,
                len(posts),
                len(filtered_posts),
                insights,
            )
            db.save_posts(search_id, filtered_posts)

            progress.update(task, advance=100, description="완료!")

        # 결과 표시
        ui.console.print()
        ui.display_success(
            f"총 {len(posts)}개 중 {len(filtered_posts)}개 게시물 필터링됨"
        )

        # 필터링된 게시물 표시
        ui.display_posts(filtered_posts, "필터링된 게시물")

        # 인사이트 표시
        ui.console.print()
        ui.display_insights(insights)

        # 상세 보기 옵션
        if filtered_posts and ui.confirm_action(
            "\n특정 게시물의 상세 정보를 보시겠습니까?"
        ):
            post_num = int(input("게시물 번호 (1-20): ")) - 1
            if 0 <= post_num < len(filtered_posts):
                ui.display_post_detail(filtered_posts[post_num])

    except Exception as e:
        ui.display_error(f"검색 중 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
