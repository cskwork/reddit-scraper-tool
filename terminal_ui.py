"""
터미널 UI - Rich를 사용한 아름다운 터미널 인터페이스
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.text import Text
from rich import box
from typing import List, Dict, Any
from config import SEARCH_CONFIG


class TerminalUI:
    """Rich 기반 터미널 UI"""

    def __init__(self):
        """터미널 UI 초기화"""
        self.console = Console()

    def display_header(self) -> None:
        """애플리케이션 헤더 표시"""
        header = Panel(
            "[bold cyan]Reddit 스마트 콘텐츠 스크래퍼[/bold cyan]\n"
            "[dim]AI 기반 키워드 필터링 도구[/dim]",
            style="bold blue",
            box=box.DOUBLE,
        )
        self.console.print(header)
        self.console.print()

    def display_search_params(
        self, keywords: List[str], subreddits: List[str], limit: int
    ) -> None:
        """검색 파라미터 표시"""
        params_table = Table(title="검색 설정", box=box.ROUNDED)
        params_table.add_column("항목", style="cyan")
        params_table.add_column("값", style="green")

        params_table.add_row("키워드", ", ".join(keywords))
        params_table.add_row("서브레딧", ", ".join(subreddits))
        params_table.add_row("게시물 수", str(limit))

        self.console.print(params_table)
        self.console.print()

    def display_posts(
        self, posts: List[Dict[str, Any]], title: str = "검색 결과"
    ) -> None:
        """게시물 목록 표시"""
        if not posts:
            self.console.print("[yellow]검색 결과가 없습니다.[/yellow]")
            return

        table = Table(title=title, box=box.ROUNDED, show_lines=True)
        table.add_column("#", style="dim", width=3)
        table.add_column("제목", style="cyan", width=50)
        table.add_column("서브레딧", style="magenta", width=15)
        table.add_column("점수", justify="right", style="yellow", width=6)
        table.add_column("관련성", justify="right", style="green", width=8)

        for idx, post in enumerate(posts[:20], 1):  # 상위 20개만 표시
            relevance = post.get("relevance_score", 0)
            relevance_color = (
                "green" if relevance > 0.7 else "yellow" if relevance > 0.4 else "red"
            )

            table.add_row(
                str(idx),
                Text(
                    post["title"][:50] + "..."
                    if len(post["title"]) > 50
                    else post["title"]
                ),
                f"r/{post['subreddit']}",
                str(post["score"]),
                f"[{relevance_color}]{relevance:.2f}[/{relevance_color}]",
            )

        self.console.print(table)

    def display_insights(self, insights: Dict[str, Any]) -> None:
        """AI 인사이트 표시"""
        insights_panel = Panel(
            f"[bold]요약:[/bold] {insights.get('summary', 'N/A')}\n\n"
            f"[bold]트렌드:[/bold] {', '.join(insights.get('trends', []))}\n\n"
            f"[bold]주요 토픽:[/bold] {', '.join(insights.get('topics', []))}",
            title="[bold magenta]AI 인사이트[/bold magenta]",
            box=box.ROUNDED,
        )
        self.console.print(insights_panel)

    def display_post_detail(self, post: Dict[str, Any]) -> None:
        """게시물 상세 정보 표시"""
        detail_panel = Panel(
            f"[bold cyan]{post['title']}[/bold cyan]\n\n"
            f"[dim]작성자: {post['author']} | 서브레딧: r/{post['subreddit']}[/dim]\n"
            f"[dim]점수: {post['score']} | 댓글: {post['num_comments']}[/dim]\n\n"
            f"{post['text'][:500]}{'...' if len(post['text']) > 500 else ''}\n\n"
            f"[bold]분석:[/bold] {post.get('analysis_reason', 'N/A')}\n"
            f"[bold]URL:[/bold] [link]{post['permalink']}[/link]",
            title="게시물 상세",
            box=box.DOUBLE,
        )
        self.console.print(detail_panel)

    def display_search_history(self, searches: List[Dict[str, Any]]) -> None:
        """검색 기록 표시"""
        if not searches:
            self.console.print("[yellow]검색 기록이 없습니다.[/yellow]")
            return

        history_table = Table(title="최근 검색 기록", box=box.ROUNDED)
        history_table.add_column("ID", style="dim", width=10)
        history_table.add_column("키워드", style="cyan", width=30)
        history_table.add_column("서브레딧", style="magenta", width=20)
        history_table.add_column("결과", justify="right", style="green", width=10)
        history_table.add_column("날짜", style="dim", width=20)

        for search in searches:
            history_table.add_row(
                search["search_id"][:8],
                ", ".join(search["keywords"]),
                ", ".join(search["subreddits"]),
                f"{search['filtered_count']}/{search['post_count']}",
                search["created_at"][:16],
            )

        self.console.print(history_table)

    def show_progress(self, description: str = "Processing...") -> Progress:
        """진행 상황 표시"""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console,
        )

    def prompt_menu(self) -> str:
        """메인 메뉴 표시"""
        self.console.print("\n[bold cyan]메뉴:[/bold cyan]")
        self.console.print("1. 새로운 검색")
        self.console.print("2. 검색 기록 보기")
        self.console.print("3. 상위 게시물 보기")
        self.console.print("4. 설정")
        self.console.print("5. 종료")

        choice = Prompt.ask("\n선택", choices=["1", "2", "3", "4", "5"])
        return choice

    def prompt_keywords(self) -> List[str]:
        """키워드 입력 받기"""
        keywords_str = Prompt.ask("[cyan]검색할 키워드 (쉼표로 구분)[/cyan]")
        return [k.strip() for k in keywords_str.split(",") if k.strip()]

    def prompt_subreddits(self) -> List[str]:
        """서브레딧 입력 받기"""
        subreddits_str = Prompt.ask(
            "[magenta]검색할 서브레딧 (쉼표로 구분, 기본값: all)[/magenta]",
            default="all",
        )
        return [s.strip() for s in subreddits_str.split(",") if s.strip()]

    def prompt_limit(self) -> int:
        """게시물 수 입력 받기"""
        self.console.print(f"\n[cyan]게시물 수 설정[/cyan]")
        self.console.print(f"기본값: {SEARCH_CONFIG['default_limit']}")
        self.console.print(f"범위: {SEARCH_CONFIG['min_limit']} ~ {SEARCH_CONFIG['max_limit']}")
        self.console.print(f"추천 옵션: {', '.join(map(str, SEARCH_CONFIG['limit_options']))}")
        
        limit = IntPrompt.ask(
            "[cyan]가져올 게시물 수[/cyan]",
            default=SEARCH_CONFIG['default_limit'],
            show_default=True
        )
        
        if limit < SEARCH_CONFIG['min_limit'] or limit > SEARCH_CONFIG['max_limit']:
            self.display_error(f"게시물 수는 {SEARCH_CONFIG['min_limit']}개 이상 {SEARCH_CONFIG['max_limit']}개 이하여야 합니다.")
            return self.prompt_limit()
        
        return limit

    def confirm_action(self, message: str) -> bool:
        """확인 프롬프트"""
        return Confirm.ask(message)

    def display_error(self, error_message: str) -> None:
        """에러 메시지 표시"""
        self.console.print(f"[bold red]오류:[/bold red] {error_message}")

    def display_success(self, message: str) -> None:
        """성공 메시지 표시"""
        self.console.print(f"[bold green]성공:[/bold green] {message}")

    def clear_screen(self) -> None:
        """화면 지우기"""
        self.console.clear()
