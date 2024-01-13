from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from chat_model.google import make_chat_with_google_model
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def add_chat(query, data):
    with open("chats.json", "r") as chat_file:
        chats = json.load(chat_file)    
    chats[query] = data
    with open("chats.json", "w") as chat_file:
        json.dump(chats, chat_file, indent=2)
    return chats


@app.get("/")
async def home(request: Request):
    with open("chats.json", "r") as chat_file:
        results = json.load(chat_file)
    return templates.TemplateResponse(
        request=request, name="index.html", context={"chats": dict(reversed(list(results.items())))}
    )

@app.post("/chats")
async def make_chat(request:Request):
    user_input = await request.form()
    query = user_input["prompt"]
    response = make_chat_with_google_model(query)
    results=add_chat(query, f"{response.content}")
    return results[query]


@app.delete("/chats/{chat_id}")
async def delete_chat(request: Request, chat_id: str):

    with open("chats.json", "r") as chat_file:
        chats = json.load(chat_file)

    if chat_id in chats:
        del chats[chat_id]

        with open("chats.json", "w") as chat_file:
            json.dump(chats, chat_file)

        return {"message": f"Chat with ID {chat_id} deleted successfully"}

    else:
        return {"error": f"Chat with ID {chat_id} not found"}
