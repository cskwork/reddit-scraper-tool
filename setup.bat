@echo off
echo ===================================
echo Reddit Scraper Tool Setup - Windows
echo ===================================
echo.

REM Python 버전 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python이 설치되어 있지 않습니다!
    echo Python 3.8+ 버전을 https://python.org 에서 다운로드하세요.
    echo.
    pause
    exit /b 1
)

echo [1/5] Python 가상환경 생성 중...
if exist .venv (
    echo 가상환경이 이미 존재합니다. 재생성하시겠습니까? (Y/N)
    set /p recreate=
    if /i "%recreate%"=="Y" (
        echo Removing existing virtual environment...
        rmdir /s /q .venv
        echo Creating new virtual environment...
        python -m venv .venv
        echo Virtual environment created successfully.
    ) else (
        echo Using existing virtual environment.
    )
) else (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created successfully.
)

echo [2/5] 가상환경 활성화 중...
call .venv\Scripts\activate.bat

echo [3/5] 패키지 설치 중...
echo Upgrading pip...
python -m pip install --upgrade pip
echo Installing requirements...
pip install -r requirements.txt
echo Package installation completed.

echo [4/5] 환경 설정 파일 생성 중...
if not exist .env (
    echo # Reddit API 설정 > .env
    echo REDDIT_CLIENT_ID=your_client_id_here >> .env
    echo REDDIT_CLIENT_SECRET=your_client_secret_here >> .env
    echo. >> .env
    echo # Ollama 설정 (선택사항) >> .env
    echo OLLAMA_URL=http://localhost:11434 >> .env
    echo OLLAMA_MODEL=gemma3:1b >> .env
    echo.
    echo [주의] .env 파일이 생성되었습니다.
    echo Reddit API 자격증명을 설정하려면:
    echo 1. https://www.reddit.com/prefs/apps 에서 앱 생성
    echo 2. .env 파일에 client_id와 client_secret 입력
    echo.
)

echo [5/5] Ollama 설치 확인 중...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [주의] Ollama가 설치되어 있지 않습니다!
    echo AI 기반 필터링을 사용하려면 Ollama를 설치하세요:
    echo https://ollama.ai/download
    echo.
    echo 설치 후 다음 명령어로 모델을 다운로드하세요:
    echo ollama pull gemma3:1b
    echo.
)

echo ===================================
echo 설치 완료!
echo.
echo 실행 방법:
echo   run.bat           - 대화형 모드 실행
echo   run.bat -k 키워드 - CLI 모드 실행
echo ===================================
pause 