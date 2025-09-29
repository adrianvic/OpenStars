#!/bin/bash

PKG="com.classicbrawl.client"
SERVER_CMD="python3 Main.py"

echo "[*] Killing app $PKG..."
adb shell am force-stop "$PKG"

echo "[*] Starting app $PKG..."
adb shell monkey -p "$PKG" -c android.intent.category.LAUNCHER 1

echo "[*] Starting server..."
$SERVER_CMD
