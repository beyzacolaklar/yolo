@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
title DeskDetect - YOLOv8 Nesne Tespiti
color 0F

echo.
echo   ============================================================
echo     DeskDetect - YOLOv8 Nesne Tespiti
echo   ============================================================
echo.

REM ---------------------------------------------------------------
REM 1) Model dosyasi var mi
REM ---------------------------------------------------------------

if not exist "best.pt" goto NO_MODEL
if not exist "app.py" goto NO_APP

REM ---------------------------------------------------------------
REM 2) Python bul  (once "py -3", sonra "python")
REM ---------------------------------------------------------------

set "PY="

py -3 -c "import sys" >nul 2>&1
if not errorlevel 1 set "PY=py -3"

if defined PY goto PY_FOUND

python -c "import sys" >nul 2>&1
if not errorlevel 1 set "PY=python"

if defined PY goto PY_FOUND
goto NO_PYTHON

:PY_FOUND
for /f "tokens=*" %%v in ('%PY% --version 2^>^&1') do set "PYVER=%%v"
echo   [1/3] Python bulundu: %PYVER%

REM ---------------------------------------------------------------
REM 3) Sanal ortam
REM ---------------------------------------------------------------

if exist ".venv\Scripts\python.exe" goto VENV_OK

echo   [2/3] Ilk kurulum - sanal ortam olusturuluyor...
%PY% -m venv .venv
if errorlevel 1 goto VENV_FAIL
if not exist ".venv\Scripts\python.exe" goto VENV_FAIL
goto VENV_OK

:VENV_OK
set "VPY=.venv\Scripts\python.exe"

REM ---------------------------------------------------------------
REM 4) Kutuphaneler
REM ---------------------------------------------------------------

"%VPY%" -c "import ultralytics, gradio" >nul 2>&1
if not errorlevel 1 goto DEPS_OK

echo   [2/3] Kutuphaneler kuruluyor...
echo.
echo   ------------------------------------------------------------
echo     Bu adim 5-10 DAKIKA surebilir. PyTorch buyuk bir paket.
echo     Ekranda cok sayida satir akacak - bu normaldir.
echo     Pencereyi KAPATMAYIN.
echo.
echo     Bu islem sadece ilk calistirmada yapilir.
echo   ------------------------------------------------------------
echo.

"%VPY%" -m pip install --upgrade pip --quiet
"%VPY%" -m pip install -r requirements.txt
if errorlevel 1 goto PIP_FAIL

"%VPY%" -c "import ultralytics, gradio" >nul 2>&1
if errorlevel 1 goto PIP_FAIL

echo.
echo   Kurulum tamamlandi.
echo.

:DEPS_OK
echo   [3/3] Uygulama baslatiliyor...
echo.
echo   ------------------------------------------------------------
echo     Tarayici birazdan kendiliginden acilacak.
echo     Acilmazsa su adrese gidin:  http://127.0.0.1:7860
echo.
echo     Kapatmak icin: bu pencerede Ctrl + C
echo   ------------------------------------------------------------
echo.

"%VPY%" app.py
if errorlevel 1 goto APP_FAIL

echo.
echo   Uygulama kapatildi.
pause
exit /b 0


REM ===============================================================
REM Hata durumlari
REM ===============================================================

:NO_MODEL
echo   HATA: best.pt dosyasi bulunamadi.
echo.
echo   best.pt dosyasi bu dosyayla ayni klasorde olmali.
echo   Zip'i cikarirken tum dosyalar cikti mi kontrol edin.
echo.
pause
exit /b 1

:NO_APP
echo   HATA: app.py dosyasi bulunamadi.
echo.
echo   Bu baslatici, app.py ile ayni klasorde olmali.
echo   Zip'i cikarirken tum dosyalar cikti mi kontrol edin.
echo.
pause
exit /b 1

:NO_PYTHON
echo   HATA: Python bulunamadi.
echo.
echo   Yapilacaklar:
echo     1. https://www.python.org/downloads/  adresine gidin
echo     2. Sari "Download Python" butonuna basin
echo     3. Kurulumu baslatin
echo     4. ONEMLI: Ilk ekranda "Add python.exe to PATH" kutusunu
echo        MUTLAKA isaretleyin, sonra "Install Now" deyin
echo     5. Kurulum bitince bu dosyaya tekrar cift tiklayin
echo.
echo   Tarayicida indirme sayfasi aciliyor...
start https://www.python.org/downloads/
echo.
pause
exit /b 1

:VENV_FAIL
echo.
echo   HATA: Sanal ortam olusturulamadi.
echo.
echo   Muhtemel sebep: klasor OneDrive icinde ya da yazma izni yok.
echo   Klasoru Masaustune tasiyip tekrar deneyin.
echo.
pause
exit /b 1

:PIP_FAIL
echo.
echo   HATA: Kutuphaneler kurulamadi.
echo.
echo   Muhtemel sebepler:
echo     - Internet baglantisi koptu
echo     - Disk alani yetersiz (yaklasik 3 GB gerekiyor)
echo     - Guvenlik duvari pip'i engelledi
echo.
echo   Yukaridaki kirmizi satirlari okuyup tekrar deneyin.
echo.
pause
exit /b 1

:APP_FAIL
echo.
echo   HATA: Uygulama beklenmedik sekilde kapandi.
echo   Yukaridaki hata mesajini okuyun.
echo.
echo   Sik gorulen: 7860 portu baska bir program tarafindan kullaniliyor.
echo   Bu durumda app.py icindeki server_port degerini 7861 yapin.
echo.
pause
exit /b 1
