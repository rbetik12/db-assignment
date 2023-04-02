@echo off
docker-compose up -d 
python setup.py
start "" python generate_data.py
start "" python generate_comments.py
timeout /t 2 /nobreak
python merge_data.py
python print_migrated_data.py
docker-compose down
pause