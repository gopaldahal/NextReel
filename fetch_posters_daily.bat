@echo off
cd /d "e:\Projects\Manoj\NextReel"
call venv\Scripts\activate.bat
python manage.py fetch_posters_omdb --api-key 12a0641e --limit 1000 >> e:\Projects\Manoj\NextReel\poster_fetch.log 2>&1
