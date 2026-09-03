@echo off
chcp 65001 >nul
setlocal
set "PYTHONIOENCODING=utf-8"
cd /d "%~dp0"

echo ========================================
echo  GRE Voca - UPLOAD
echo  Anki -^> GitHub
echo ========================================
echo.

call :findpython || goto :fail

echo [1/4] GitHub 변경사항 확인 중...
git fetch origin main || goto :fail

for /f %%i in ('git rev-parse HEAD') do set "LOCAL=%%i"
for /f %%i in ('git rev-parse origin/main') do set "REMOTE=%%i"
for /f %%i in ('git merge-base HEAD origin/main') do set "BASE=%%i"

if not "%LOCAL%"=="%REMOTE%" if "%LOCAL%"=="%BASE%" (
  echo.
  echo 업로드 중단: GitHub에 내가 아직 받지 않은 변경사항이 있습니다.
  echo 먼저 download.bat 를 실행한 뒤 다시 업로드하세요.
  echo.
  pause
  exit /b 1
)

echo [2/4] Anki에서 현재 단어장을 내보내는 중...
%PY% scripts\export_from_anki.py || goto :fail

echo [3/4] 변경사항 저장 중...
git add data/vocabulary.csv || goto :fail

git diff --cached --quiet
if not errorlevel 1 (
  echo.
  echo 업로드할 변경사항이 없습니다.
  echo.
  pause
  exit /b 0
)

git commit -m "Update vocabulary" || goto :fail

echo [4/4] GitHub에 업로드 중...
git push origin main || goto :fail

echo.
echo 완료: Anki 변경사항이 GitHub에 업로드되었습니다.
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
echo 실패: 위 오류 메시지를 확인하세요.
echo.
pause
exit /b 1
