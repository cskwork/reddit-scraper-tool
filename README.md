# Reddit 스마트 콘텐츠 스크래퍼

AI 기반 Reddit 콘텐츠 필터링 및 분석 도구

## 기능

- 키워드 기반 Reddit 게시물 검색
- Ollama LLM을 사용한 지능형 콘텐츠 필터링
- 관련성 점수 기반 품질 평가
- 검색 기록 및 결과 저장
- 아름다운 터미널 UI (Rich 라이브러리)
- AI 인사이트 추출

## 설치

1. Python 가상환경 생성 및 활성화:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. 의존성 설치:

```powershell
pip install -r requirements.txt
```

3. Reddit API 설정:
   - https://www.reddit.com/prefs/apps 에서 앱 생성
   - `.env` 파일 생성:

```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
```

4. Ollama 설치 및 모델 다운로드:

```powershell
# Ollama 설치 후
ollama pull gemma3:1b
```

## 사용법

### 대화형 모드

```powershell
python main.py -i
```

### CLI 모드

```powershell
# 기본 검색
python main.py -k "python" "programming"

# 특정 서브레딧에서 검색
python main.py -k "machine learning" -s "MachineLearning" "learnmachinelearning" -l 100
```

## 주요 컴포넌트

- `reddit_client.py`: Reddit API 통신
- `content_analyzer.py`: AI 기반 콘텐츠 분석
- `database.py`: SQLite 데이터베이스 관리
- `terminal_ui.py`: Rich 터미널 인터페이스
- `main.py`: 메인 애플리케이션

## 데이터베이스

SQLite 데이터베이스 (`reddit_scraper.db`)에 다음 정보 저장:

- 검색 기록
- 필터링된 게시물
- AI 분석 결과
- 관련성 점수
