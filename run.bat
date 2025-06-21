@echo off
REM Reddit Scraper Tool 실행 스크립트 - Windows

REM 가상환경 확인
if not exist .venv (
    echo [ERROR] 가상환경이 없습니다. 먼저 setup.bat을 실행하세요.
    pause
    exit /b 1
)

REM 가상환경 활성화
call .venv\Scripts\activate.bat

REM .env 파일 확인
if not exist .env (
    echo [ERROR] .env 파일이 없습니다. 먼저 setup.bat을 실행하세요.
    pause
    exit /b 1
)

REM Ollama 상태 확인 (선택사항)
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo [주의] Ollama가 실행되고 있지 않습니다.
    echo AI 필터링은 사용할 수 없습니다.
    echo.
    set /p continue="계속하시겠습니까? (Y/N): "
    if /i not "%continue%"=="Y" exit /b 0
)

REM 인자가 없으면 대화형 모드, 있으면 CLI 모드
if "%~1"=="" (
    python main.py -i
) else (
    python main.py %*
) 