from fastapi import FastAPI, Form, UploadFile, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
from pathlib import Path
import pandas as pd

from agent import agent

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = BASE_DIR / "prompts"
PROMPTS_DIR.mkdir(exist_ok=True)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


# 工具函数：列出 prompts
def list_prompts():
    return [p.name for p in PROMPTS_DIR.glob("*.yaml")]


# ---------- 单条对话 ----------
@app.get("/", response_class=HTMLResponse)
async def single_page(request: Request):
    return templates.TemplateResponse("single.html", {"request": request, "prompts": list_prompts(), "result": None})

@app.post("/run_single", response_class=HTMLResponse)
async def run_single(request: Request, system_prompt: str = Form(...), user_prompt: str = Form(...)):
    # agent_name = Path(system_prompt).stem.replace("_", "-")
    # result = agent(agent_name, user_prompt)
    result = agent(system_prompt, user_prompt)
    return templates.TemplateResponse("single.html", {"request": request, "prompts": list_prompts(), "result": result})


# ---------- 批处理 ----------
@app.get("/batch", response_class=HTMLResponse)
async def batch_page(request: Request):
    return templates.TemplateResponse("batch.html", {"request": request, "prompts": list_prompts(), "download": None})

@app.post("/run_batch", response_class=HTMLResponse)
async def run_batch(request: Request, system_prompt: str = Form(...), file: UploadFile = None, output_name: str = Form("result.csv")):
    if file is None:
        return RedirectResponse("/batch", status_code=303)

    df = pd.read_csv(file.file)
    results = []
    for _, row in df.iterrows():
        # agent_name = Path(system_prompt).stem.replace("_", "-")
        # result = agent(agent_name, row["user_prompt"])
        result = agent(system_prompt, row["user_prompt"])
        results.append({"id": row["id"], "user_prompt": row["user_prompt"], "result": result})

    out_df = pd.DataFrame(results)
    output_path = BASE_DIR / output_name
    out_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    return templates.TemplateResponse("batch.html", {"request": request, "prompts": list_prompts(), "download": f"/download/{output_name}"})


@app.get("/download/{filename}")
async def download_file(filename: str):
    return FileResponse(BASE_DIR / filename, filename=filename)


# ---------- Prompt 管理 ----------
@app.get("/prompts", response_class=HTMLResponse)
async def prompts_page(request: Request):
    return templates.TemplateResponse("prompts.html", {"request": request, "files": list_prompts()})

@app.post("/upload_prompt")
async def upload_prompt(file: UploadFile):
    dest = PROMPTS_DIR / file.filename
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return RedirectResponse("/prompts", status_code=303)

@app.get("/delete_prompt/{filename}")
async def delete_prompt(filename: str):
    (PROMPTS_DIR / filename).unlink(missing_ok=True)
    return RedirectResponse("/prompts", status_code=303)


