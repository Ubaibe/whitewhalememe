# main.py - White Whale Meme Generator
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import textwrap

app = FastAPI(title="White Whale Meme Generator 🐋")

templates = Jinja2Templates(directory="templates")

# ⚠️ REPLACE WITH YOUR OFFICIAL WHITE WHALE IMAGE URL
WHALE_IMAGE_URL = "https://pbs.twimg.com/media/G9OOx9jW8AAgN_O.jpg"
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




