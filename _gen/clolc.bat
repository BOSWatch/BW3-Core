@echo off

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
echo Run count lines of code ...
echo.
cd ..
_bin\win\cloc_1_72\cloc-1.72.exe . --exclude-lang=HTML,JavaScript,CSS --exclude-dir=_docu,_config,_info
echo.
echo.
pause