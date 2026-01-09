@echo off
REM Format code with black
REM Usage: format_code.bat

echo Formatting code with black...
python -m black --line-length 100 my_rdbms\ tests\
echo Code formatting complete!
pause
