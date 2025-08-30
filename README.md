# Video REST API + Minimal Test Client

A tiny Flask REST API backed by SQLite, with a basic web page to test CRUD on videos.

## Run It (Essentials)

Windows PowerShell:
```powershell
python -m pip install -r requirements.txt
python main.py
```

macOS/Linux:
```bash
pip3 install -r requirements.txt
python3 main.py
```

Then open:
```
http://127.0.0.1:5000/
```

Notes:
- Use the page buttons (CREATE, UPDATE, GET, DELETE, CLEAR DB) to test the API.
- Data is stored locally in `database.db`. The CLEAR DB button wipes it.
