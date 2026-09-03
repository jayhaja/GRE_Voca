@echo off
chcp 65001 >nul
setlocal
set "PYTHONIOENCODING=utf-8"
cd /d "%~dp0"

echo ========================================
echo  GRE Voca - DOWNLOAD
echo  GitHub -^> Anki
echo ========================================
echo.

call :findpython || goto :fail

echo [1/2] GitHub에서 최신 단어장을 받는 중...
git pull --ff-only || goto :fail

echo.
echo [2/2] Anki에 반영하는 중...
%PY% scripts\sync_to_anki.py || goto :fail

echo.
echo 완료: 최신 단어장이 Anki에 반영되었습니다.
echo 이 창은 닫아도 됩니다.
echo.
pause
exit /b 0

:findpython
set "PY="
where py >nul 2>nul
if not errorlevel 1 set "PY=py"
if defined PY exit /b 0
where python >nul 2>nul
if not errorlevel 1 set "PY=python"
if defined PY exit /b 0
echo Python을 찾을 수 없습니다. python.org에서 설치한 뒤 다시 실행하세요.
exit /b 1

:fail
echo.
echo 실패: 위 오류 메시지를 확인하세요. 변경사항은 적용되지 않았습니다.
echo.
pause
exit /b 1
