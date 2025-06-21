#!/bin/bash

echo "==================================="
echo "Reddit Scraper Tool Setup - macOS/Linux"
echo "==================================="
echo

# Python 버전 확인
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3이 설치되어 있지 않습니다!"
    echo "Python 3.8+ 버전을 설치하세요:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo
    exit 1
fi

echo "[1/5] Python 가상환경 생성 중..."
if [ -d ".venv" ]; then
    read -p "가상환경이 이미 존재합니다. 재생성하시겠습니까? (y/n): " recreate
    if [[ $recreate =~ ^[Yy]$ ]]; then
        rm -rf .venv
        python3 -m venv .venv
    fi
else
    python3 -m venv .venv
fi

echo "[2/5] 가상환경 활성화 중..."
source .venv/bin/activate

echo "[3/5] 패키지 설치 중..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "[4/5] 환경 설정 파일 생성 중..."
if [ ! -f .env ]; then
    cat > .env << EOF
# Reddit API 설정
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here

# Ollama 설정 (선택사항)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:1b
EOF
    echo
    echo "[주의] .env 파일이 생성되었습니다."
    echo "Reddit API 자격증명을 설정하려면:"
    echo "1. https://www.reddit.com/prefs/apps 에서 앱 생성"
    echo "2. .env 파일에 client_id와 client_secret 입력"
    echo
fi

echo "[5/5] Ollama 설치 확인 중..."
if ! command -v ollama &> /dev/null; then
    echo
    echo "[주의] Ollama가 설치되어 있지 않습니다!"
    echo "AI 기반 필터링을 사용하려면 Ollama를 설치하세요:"
    echo
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS: curl -fsSL https://ollama.ai/install.sh | sh"
    else
        echo "Linux: curl -fsSL https://ollama.ai/install.sh | sh"
    fi
    echo
    echo "설치 후 다음 명령어로 모델을 다운로드하세요:"
    echo "ollama pull gemma3:1b"
    echo
fi

# 실행 권한 설정
chmod +x run.sh

echo "==================================="
echo "설치 완료!"
echo
echo "실행 방법:"
echo "  ./run.sh           - 대화형 모드 실행"
echo "  ./run.sh -k 키워드 - CLI 모드 실행"
echo "===================================" 