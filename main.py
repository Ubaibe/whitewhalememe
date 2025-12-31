# main.py - White Whale Meme Generator
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import textwrap

app = FastAPI(title="White Whale Meme Generator 🐋")

templates = Jinja2Templates(directory="templates")

# ⚠️ REPLACE WITH YOUR OFFICIAL WHITE WHALE IMAGE URL
WHALE_IMAGE_URL = "data:image/jpeg;base64,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"  # Put your direct link

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "meme_url": None,
        "top_text": "",
        "bottom_text": ""
    })

@app.post("/", response_class=HTMLResponse)
async def generate_meme(
    request: Request,
    top_text: str = Form(""),
    bottom_text: str = Form("")
):
    top = top_text.strip().upper()
    bottom = bottom_text.strip().upper()

    # Build the meme URL using QuickMeme-style generator (free, reliable, supports custom image)
    # Alternative services: imgflip, memegen.link — this one is simple & fast
    base = "https://api.memegen.link/images/custom"
    url = f"{base}/{top}/{bottom}.png?background={WHALE_IMAGE_URL}"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "meme_url": url,
        "top_text": top_text,
        "bottom_text": bottom_text
    })

