# Allow running with python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

import os
import sys
import subprocess
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Query, File, UploadFile
import tempfile


app = FastAPI()

# Store last OCR result
last_ocr_result = {"output": None, "error": None}

# Direct image upload endpoint
@app.post("/ocr/upload")
async def upload_ocr(file: UploadFile = File(...)):
    # Save uploaded file to a temporary location
    suffix = os.path.splitext(file.filename)[-1] or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    # Run OCR as before
    python_exe = sys.executable
    cli_path = os.path.join(os.path.dirname(__file__),
                            '..', 'receipt_ocr', 'cli.py')
    cli_path = os.path.abspath(cli_path)
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'))
    cmd = [python_exe, cli_path, tmp_file_path]
    try:
        result = subprocess.run(cmd, capture_output=True,
                                text=True, env=env, check=True)
        last_ocr_result["output"] = result.stdout.strip()
        last_ocr_result["error"] = None
        return {"output": last_ocr_result["output"]}
    except subprocess.CalledProcessError as e:
        last_ocr_result["output"] = None
        last_ocr_result["error"] = e.stderr.strip()
        return {"error": last_ocr_result["error"]}

# Root endpoint with health status
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Receipt OCR backend is running."}

# Endpoint to get last OCR result/content
@app.get("/ocr/result")
def get_last_ocr_result():
    return last_ocr_result
