@echo off
cd /d "C:\Users\marco\Documents\analisador-etico"
call .\venv\Scripts\activate.bat
echo ============================================
echo   PsicologIA - Iniciando...
echo ============================================
echo.
streamlit run app.py
pause
