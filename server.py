from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess, tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run")
async def run(req: Request):
    code = await req.body()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".m", delete=False) as f:
        f.write(code.decode())
        path = f.name

    try:
        result = subprocess.check_output(
            ["python3", "may.py", path],
            stderr=subprocess.STDOUT,
            timeout=3
        ).decode()
    except subprocess.CalledProcessError as e:
        result = e.output.decode()

    return {"output": result}