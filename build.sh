#!/usr/bin/env bash
set -e

# 1) Clean old builds
rm -rf build/ dist/ FlightBooking.spec

# 2) Build in one‑dir mode
pyinstaller \
  --onedir \
  --noconsole \
  --name FlightBooking \
  --add-data "assets;assets" \
  --add-data "data;data" \
  main.py

echo "✅ Build finished! Check dist/FlightBooking/FlightBooking.exe"
