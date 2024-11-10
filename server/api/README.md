## Activating the virtual environment

cd api

# Windows

python -m venv fast
.\fast\Scripts\activate

# macOS/Linux

python -m venv fast
source fast/bin/activate

### Install dependencies

pip install -r requirements.txt

## starting local server

uvicorn main:app --reload
