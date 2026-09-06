#!/usr/bin/env bash
# DeskDetect baslatici - macOS / Linux
# macOS'ta ilk kullanimdan once terminalde bir kez:  chmod +x BASLAT-mac-linux.command

cd "$(dirname "$0")" || exit 1

echo
echo "  ============================================================"
echo "    DeskDetect - YOLOv8 Nesne Tespiti"
echo "  ============================================================"
echo

fail() {
    echo
    echo "  HATA: $1"
    echo
    read -r -p "  Kapatmak icin Enter'a basin..."
    exit 1
}

[ -f best.pt ] || fail "best.pt bulunamadi. Bu dosyayla ayni klasorde olmali."
[ -f app.py ]  || fail "app.py bulunamadi. Bu baslatici app.py ile ayni klasorde olmali."

# --- Python bul ---------------------------------------------------

PY=""
for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c "import sys" >/dev/null 2>&1; then
        PY="$candidate"
        break
    fi
done

if [ -z "$PY" ]; then
    echo "  Python bulunamadi."
    echo
    echo "  macOS : brew install python   (ya da python.org/downloads)"
    echo "  Ubuntu: sudo apt install python3 python3-venv"
    echo
    read -r -p "  Kapatmak icin Enter'a basin..."
    exit 1
fi

echo "  [1/3] Python bulundu: $($PY --version 2>&1)"

# --- Sanal ortam --------------------------------------------------

if [ ! -x .venv/bin/python ]; then
    echo "  [2/3] Ilk kurulum - sanal ortam olusturuluyor..."
    "$PY" -m venv .venv || fail "Sanal ortam olusturulamadi."
fi

VPY=".venv/bin/python"

# --- Kutuphaneler -------------------------------------------------

if ! "$VPY" -c "import ultralytics, gradio" >/dev/null 2>&1; then
    echo "  [2/3] Kutuphaneler kuruluyor..."
    echo
    echo "  ------------------------------------------------------------"
    echo "    Bu adim 5-10 DAKIKA surebilir. PyTorch buyuk bir paket."
    echo "    Pencereyi kapatmayin."
    echo
    echo "    Bu islem sadece ilk calistirmada yapilir."
    echo "  ------------------------------------------------------------"
    echo

    "$VPY" -m pip install --upgrade pip --quiet
    "$VPY" -m pip install -r requirements.txt || fail "Kutuphaneler kurulamadi."
    "$VPY" -c "import ultralytics, gradio" >/dev/null 2>&1 || fail "Kutuphaneler kurulamadi."

    echo
    echo "  Kurulum tamamlandi."
    echo
fi

# --- Calistir -----------------------------------------------------

echo "  [3/3] Uygulama baslatiliyor..."
echo
echo "  ------------------------------------------------------------"
echo "    Tarayici birazdan kendiliginden acilacak."
echo "    Acilmazsa:  http://127.0.0.1:7860"
echo
echo "    Kapatmak icin: Ctrl + C"
echo "  ------------------------------------------------------------"
echo

"$VPY" app.py

echo
read -r -p "  Uygulama kapatildi. Enter'a basin..."
