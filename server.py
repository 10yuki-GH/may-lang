from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import subprocess
import tempfile
import os

app = FastAPI()

# ✅ 允许浏览器跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 执行 May 代码（后端调用 may.py）
@app.post("/run")
async def run_code(request: Request):
    code = await request.body()

    # 把用户输入的代码写成临时 .m 文件
    with tempfile.NamedTemporaryFile(mode="w", suffix=".m", delete=False) as f:
        f.write(code.decode())
        tmp_path = f.name

    try:
        result = subprocess.check_output(
            ["python3", "may.py", tmp_path],
            stderr=subprocess.STDOUT,
            timeout=5
        ).decode(errors="replace")
    except subprocess.CalledProcessError as e:
        result = e.output.decode(errors="replace")
    finally:
        os.remove(tmp_path)

    return {"output": result}


# ✅ 托管前端页面（index.html）
app.mount(
    "/",
    StaticFiles(directory="web", html=True),
    name="frontend"
)