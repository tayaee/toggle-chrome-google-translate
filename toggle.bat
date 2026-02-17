@echo off
title Google Translate Automation (uv)
cd /d "%~dp0"
:: Install uv => iwr -useb https://astral.sh/uv/install.ps1 | iex)
uv run toggle.py
