#!/bin/bash
# Reddit Scraper Tool 실행 스크립트 - macOS/Linux

# 가상환경 확인
if [ ! -d ".venv" ]; then
    echo "[ERROR] 가상환경이 없습니다. 먼저 ./setup.sh를 실행하세요."
    exit 1
fi

# 가상환경 활성화
source .venv/bin/activate

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo "[ERROR] .env 파일이 없습니다. 먼저 ./setup.sh를 실행하세요."
    exit 1
fi

# Ollama 상태 확인 (선택사항)
if ! ollama list &> /dev/null; then
    echo "[주의] Ollama가 실행되고 있지 않습니다."
    echo "AI 필터링은 사용할 수 없습니다."
    echo
    read -p "계속하시겠습니까? (y/n): " continue
    if [[ ! $continue =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# 인자가 없으면 대화형 모드, 있으면 CLI 모드
if [ $# -eq 0 ]; then
    python main.py -i
else
    python main.py "$@"
fi 