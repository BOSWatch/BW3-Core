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
echo Build Doxygen Documentation
echo.
cd ..
_bin\win\doxygen\doxygen.exe "_config\doxygen.ini"
echo.
echo.
pause