@echo off
call "C:\Users\Kishan Shetty\anaconda3\Scripts\activate.bat"
cd "C:\Users\Kishan Shetty\Downloads\DTLEL (1)\DTLEL\backend"
uvicorn main:app --reload --port 8005
