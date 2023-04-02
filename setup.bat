@echo off
docker-compose up -d 
python src/misc/setup.py
start "" python src/generate_comment_data.py
start "" python src/generate_trading_data.py
timeout /t 2 /nobreak
python src/merge.py
pause