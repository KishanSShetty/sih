
import uvicorn
import os
import sys

# Ensure the project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"


if __name__ == "__main__":
    print(f"Starting server v3 from {PROJECT_ROOT} on port 8005")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8005, reload=False)

