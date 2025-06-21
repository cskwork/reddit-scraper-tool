# Reddit 스마트 콘텐츠 스크래퍼

AI 기반 Reddit 콘텐츠 필터링 및 분석 도구

## 기능

- 키워드 기반 Reddit 게시물 검색
- Ollama LLM을 사용한 지능형 콘텐츠 필터링
- 관련성 점수 기반 품질 평가
- 검색 기록 및 결과 저장
- 아름다운 터미널 UI (Rich 라이브러리)
- AI 인사이트 추출

## 빠른 시작

### Windows

```powershell
# 1. 설치
setup.bat

# 2. 실행
run.bat

# 3. 설치 확인 (선택사항)
python test_install.py
```

### macOS/Linux

```bash
# 1. 설치
chmod +x setup.sh
./setup.sh

# 2. 실행
./run.sh

# 3. 설치 확인 (선택사항)
python test_install.py
```

## 상세 설치 가이드

### 사전 요구사항

1. **Python 3.8+**

   - Windows: [python.org](https://python.org)에서 다운로드
   - macOS: `brew install python3`
   - Linux: `sudo apt install python3 python3-pip python3-venv`

2. **Reddit API 자격증명**

   - [Reddit Apps](https://www.reddit.com/prefs/apps)에서 앱 생성
   - "script" 타입 선택
   - client_id와 client_secret 메모

3. **Ollama (선택사항, AI 필터링용)**
   - Windows/macOS/Linux: [ollama.ai](https://ollama.ai/download)에서 다운로드
   - 설치 후: `ollama pull gemma3:1b`

### 설치 과정

설치 스크립트(`setup.bat` 또는 `setup.sh`)가 자동으로:

- Python 가상환경 생성
- 필요한 패키지 설치
- `.env` 파일 생성
- 의존성 확인

### 설정

설치 후 `.env` 파일을 편집하여 Reddit API 자격증명 입력:

```
REDDIT_CLIENT_ID=your_actual_client_id
REDDIT_CLIENT_SECRET=your_actual_client_secret
```

## 사용법

### 대화형 모드 (권장)

```bash
# Windows
run.bat

# macOS/Linux
./run.sh
```

메뉴에서 선택:

1. 새로운 검색
2. 검색 기록 보기
3. 상위 게시물 보기
4. 설정
5. 종료

### CLI 모드

```bash
# 기본 검색
run.bat -k "python" "programming"
./run.sh -k "python" "programming"

# 특정 서브레딧에서 검색
run.bat -k "machine learning" -s "MachineLearning" -l 100
./run.sh -k "machine learning" -s "MachineLearning" -l 100
```

### CLI 옵션

- `-k, --keywords`: 검색할 키워드 (필수)
- `-s, --subreddits`: 검색할 서브레딧 (기본: all)
- `-l, --limit`: 가져올 게시물 수 (기본: 50)
- `-i, --interactive`: 대화형 모드 실행

## 문제 해결

### Python이 설치되어 있지 않음

- 각 플랫폼별 Python 설치 가이드 참조

### Reddit API 오류

- `.env` 파일의 자격증명 확인
- Reddit 앱이 활성화되어 있는지 확인

### Ollama 연결 실패

- Ollama가 실행 중인지 확인: `ollama list`
- 필요한 모델 다운로드: `ollama pull gemma3:1b`

## 데이터 저장

모든 데이터는 `reddit_scraper.db` SQLite 데이터베이스에 저장:

- 검색 기록
- 필터링된 게시물
- AI 분석 결과
- 관련성 점수

## 주요 컴포넌트

- `reddit_client.py`: Reddit API 통신
- `content_analyzer.py`: AI 기반 콘텐츠 분석
- `database.py`: SQLite 데이터베이스 관리
- `terminal_ui.py`: Rich 터미널 인터페이스
- `main.py`: 메인 애플리케이션
