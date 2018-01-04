@echo off

cd ..
if not exist "logs/" mkdir logs

echo " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
echo "     ____  ____  ______       __      __       __       _____ "
echo "    / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  / "
echo "   / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <  "
echo "  / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /  "
echo " /_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/   "
echo "                German BOS Information Script                 "
echo "                     by Bastian Schroll                       "
echo " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
echo.
echo BOSWatch 3 Unittest framework
echo.
echo Which test? [ENTER] for all
echo Or name a specific test test_[###].py
echo.

set /p test=Testcase: 
if "%test%" == "" (
	goto start
) else (
	goto start_spec
)

:start
echo.
python -m pytest -c "_config/pytest.ini" -v --pep8 --cov --cov-report=term-missing
echo.
echo --- Hit any key to repeat ---
pause
cls
goto start

:start_spec
echo.
python -m pytest test/test_%test%.py -c "_config/pytest.ini" -v --pep8 --cov --cov-report=term-missing
echo.
echo --- Hit any key to repeat ---
pause
cls
goto start_spec
