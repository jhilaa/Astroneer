from fastapi import FastAPI, Request
import subprocess
import os
import datetime
import sys

app = FastAPI()

# ==== chemins de base ====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_DIR = os.path.join(BASE_DIR, "python")
LOG_FILE = os.path.join(BASE_DIR, "load.log")

# ==== scopes autorisés → module Python ====
ALLOWED_SCOPES = {
    "RESOURCES": "scraping.main_scrape_RESOURCES_page",
    "PLANETS": "scraping.main_scrape_PLANETS_page"
    
    # "ATMO_RES": "scraping.main_scrape_ATMO_RES_page",
    # "NAT_RES": "scraping.main_scrape_NAT_RES_page",
    # etc. 
}


@app.post("/load")
async def run_load(req: Request):
    data = await req.json()
    scope = data.get("scope")

    if not scope:
        return {"status": "error", "output": "Missing 'scope' in request body"}

    module_name = ALLOWED_SCOPES.get(scope)
    if module_name is None:
        return {"status": "error", "output": f"Invalid scope '{scope}'"}

    try:
        result = subprocess.run(
            [sys.executable, "-m", module_name],
            cwd=PYTHON_DIR,          # On exécute depuis projet/python
            capture_output=True,
            text=True,
            check=True,
            timeout=300,             # 5 minutes max
        )
        return {"status": "success", "scope": scope, "output": result.stdout}

    except subprocess.CalledProcessError as e:
        return {"status": "error", "scope": scope, "output": e.stderr}
