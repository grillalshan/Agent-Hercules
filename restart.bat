@echo off
echo ==========================================
echo Gym Subscription Manager - Agent Hercules
echo ==========================================
echo.
echo Checking for running instances...
taskkill /F /IM streamlit.exe 2>NUL
timeout /t 2 /nobreak >NUL
echo.
echo Starting app...
python -m streamlit run 🏠_Home.py
