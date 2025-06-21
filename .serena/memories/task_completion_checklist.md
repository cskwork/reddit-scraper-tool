# Task Completion Checklist

When completing a coding task, ensure the following:

1. **Code Quality**
   - Run linting: `flake8 .` and `pylint *.py`
   - Format code: `black .`
   - Type checking: `mypy .`

2. **Testing**
   - Write unit tests for new functionality
   - Run all tests: `pytest`
   - Ensure all tests pass

3. **Documentation**
   - Update docstrings (in Korean)
   - Update README if functionality changed
   - Add comments for complex logic

4. **Dependencies**
   - Update requirements.txt if new packages added
   - Ensure virtual environment is clean

5. **Manual Testing**
   - Test main functionality with various inputs
   - Check error handling
   - Verify database operations work correctly

6. **Git**
   - Commit with descriptive message
   - Push changes to repository