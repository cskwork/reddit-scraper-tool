#!/usr/bin/env python3
"""
설치 테스트 스크립트
"""

import sys
import os
from pathlib import Path


def test_python_version():
    """Python 버전 확인"""
    print("1. Python 버전 확인...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} - Python 3.8+ 필요")
        return False


def test_imports():
    """필수 패키지 import 테스트"""
    print("\n2. 필수 패키지 확인...")
    packages = {
        "praw": "Reddit API",
        "rich": "터미널 UI",
        "sqlalchemy": "데이터베이스",
        "requests": "HTTP 요청",
        "dotenv": "환경 변수",
        "click": "CLI 인터페이스"
    }
    
    all_ok = True
    for package, desc in packages.items():
        try:
            if package == "dotenv":
                __import__("dotenv")
            else:
                __import__(package)
            print(f"   ✓ {package} ({desc}) - OK")
        except ImportError:
            print(f"   ✗ {package} ({desc}) - 설치 필요")
            all_ok = False
    
    return all_ok


def test_env_file():
    """환경 설정 파일 확인"""
    print("\n3. 환경 설정 확인...")
    env_path = Path(".env")
    
    if env_path.exists():
        print("   ✓ .env 파일 존재 - OK")
        
        # .env 파일 내용 확인
        from dotenv import load_dotenv
        load_dotenv()
        
        client_id = os.getenv("REDDIT_CLIENT_ID", "")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET", "")
        
        if client_id and client_id != "your_client_id_here":
            print("   ✓ Reddit Client ID 설정됨")
        else:
            print("   ! Reddit Client ID 설정 필요")
            
        if client_secret and client_secret != "your_client_secret_here":
            print("   ✓ Reddit Client Secret 설정됨")
        else:
            print("   ! Reddit Client Secret 설정 필요")
            
        return True
    else:
        print("   ✗ .env 파일 없음 - 생성 필요")
        return False


def test_ollama():
    """Ollama 설치 확인 (선택사항)"""
    print("\n4. Ollama 확인 (선택사항)...")
    
    try:
        import subprocess
        result = subprocess.run(
            ["ollama", "--version"], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("   ✓ Ollama 설치됨 - AI 필터링 사용 가능")
            
            # 모델 확인
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if "gemma3:1b" in result.stdout:
                print("   ✓ gemma3:1b 모델 설치됨")
            else:
                print("   ! gemma3:1b 모델 미설치 - 'ollama pull gemma3:1b' 실행 필요")
            
            return True
        else:
            print("   ! Ollama 미설치 - AI 필터링 사용 불가 (기본 필터링은 작동)")
            return True  # 선택사항이므로 True 반환
            
    except Exception:
        print("   ! Ollama 미설치 - AI 필터링 사용 불가 (기본 필터링은 작동)")
        return True  # 선택사항이므로 True 반환


def main():
    """메인 테스트 실행"""
    print("=== Reddit Scraper 설치 테스트 ===\n")
    
    results = [
        test_python_version(),
        test_imports(),
        test_env_file(),
        test_ollama()
    ]
    
    print("\n=== 테스트 결과 ===")
    if all(results[:3]):  # 처음 3개는 필수
        print("✓ 설치가 정상적으로 완료되었습니다!")
        print("\n실행 방법:")
        if sys.platform.startswith('win'):
            print("  run.bat        - 대화형 모드")
            print("  run.bat -k 키워드  - CLI 모드")
        else:
            print("  ./run.sh       - 대화형 모드")
            print("  ./run.sh -k 키워드 - CLI 모드")
    else:
        print("✗ 일부 구성 요소가 누락되었습니다.")
        print("\n해결 방법:")
        if sys.platform.startswith('win'):
            print("  setup.bat 실행")
        else:
            print("  ./setup.sh 실행")


if __name__ == "__main__":
    main() 