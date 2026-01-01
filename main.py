# main.py - White Whale Meme Generator with Multiple Templates
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="White Whale Meme Generator 🐋")

templates = Jinja2Templates(directory="templates")

# Add as many White Whale images as you want! (direct links)
WHALE_TEMPLATES = {
    "Armored Warrior": "https://pbs.twimg.com/media/G9OOx9jW8AAgN_O.jpg",  # Example official
    "Epic Charge": "https://pbs.twimg.com/media/G9dHoXxWwAU_qKU.jpg",
    "Built Different": "https://pbs.twimg.com/media/G9cuPMyWgAABykF.jpg",
    "Cheers Whale": "https://pbs.twimg.com/media/G9jSVCUWYAAwJWC.jpg",
    # Add your own uploaded ones here:
    "Custom Pose 1": "https://i.ibb.co/TMk1RNBc/image.png",
    "Custom Pose 2": "https://pbs.twimg.com/media/G9jSVCUWYAAwJWC.jpg",
    "Custom Pose 3": "https://pbs.twimg.com/media/G9b1RknWAAA1iyD.jpg",
    "Custom Pose 4": "https://pbs.twimg.com/media/G9bbp3BWwAIiBwM.jpg",
    "Custom Pose 5": "https://pbs.twimg.com/media/G9Xuf5uXgAAWfSW.jpg",
    "Custom Pose 6": "https://pbs.twimg.com/media/G9WjI4IXkAEr9U0.jpg",
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    default_template = list(WHALE_TEMPLATES.keys())[0]
    return templates.TemplateResponse("index.html", {
        "request": request,
        "templates": WHALE_TEMPLATES,
        "selected_template":default_template,
        "meme_url": None,
        "top_text": "",
        "bottom_text": ""
    })

@app.post("/", response_class=HTMLResponse)
async def generate_meme(
    request: Request,
    template: str = Form(...),
    top_text: str = Form(""),
    bottom_text: str = Form("")
):
    background_url = WHALE_TEMPLATES.get(template, list(WHALE_TEMPLATES.values())[0])
    top = top_text.strip().upper()
    bottom = bottom_text.strip().upper()

    meme_url = f"https://api.memegen.link/images/custom/{top}/{bottom}.png?background={background_url}"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "templates": WHALE_TEMPLATES,
        "selected_template": template,
        "meme_url": meme_url,
        "top_text": top_text,
        "bottom_text": bottom_text
    })



