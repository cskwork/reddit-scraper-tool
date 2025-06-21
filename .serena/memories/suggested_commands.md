# Suggested Commands

## Development Environment Setup
```bash
# Create Python virtual environment
python -m venv .venv

# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Running the Application
```bash
# Basic usage
python main.py -k "keyword1" "keyword2" 

# With specific subreddits
python main.py -k "python" "programming" -s "learnpython" "programming" -l 100
```

## Development Commands
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .

# Lint code
flake8 .
pylint *.py

# Type checking
mypy .
```

## Git Commands (Windows)
```bash
git status
git add .
git commit -m "메시지"
git push
```

## Utility Commands (Windows PowerShell)
```bash
# List files
ls or dir

# Change directory
cd directory_name

# View file content
cat filename or type filename

# Search in files
Select-String -Pattern "pattern" -Path "*.py"
```