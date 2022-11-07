import datetime
from typing import List
from fastapi import (FastAPI, WebSocket, WebSocketDisconnect, Request, Response, Body)
from fastapi.templating import Jinja2Templates
import models
import db

templates = Jinja2Templates(directory="template")
app = FastAPI()


class ConnectRepository():
    def __init__(self):
        self.activeConnectons: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, user: str):
        await websocket.accept()
        self.activeConnectons.append((websocket, user))

    def disconnect(self, websocket: WebSocket, user: str):
        self.activeConnectons.remove((websocket, user))

    async def broadcast(self, data: models.Info):
        for connection in self.activeConnectons:
            await connection[0].send_json(data)
            db.create(data)
            print(data)




connectRepository = ConnectRepository()


@app.websocket("/api/chat")
async def chat(websocket: WebSocket):
    sender = websocket.cookies.get("X-Authorization")
    if sender:
        await connectRepository.connect(websocket, sender)
        response = {
            "sender": sender,
            "message": "got connected",
            "time":str(datetime.datetime.now())
        }
        await connectRepository.broadcast(response)
        try:
            while True:
                data = await websocket.receive_json()
                await connectRepository.broadcast(data)
        except WebSocketDisconnect:
            connectRepository.disconnect(websocket, sender)
            response['message'] = "left"
            await connectRepository.broadcast(response)


@app.get("/api/current_user")
def get_user(request: Request):
    # return {"user" : request.cookies.get("X-Authorization") }
    return request.cookies.get("X-Authorization")

@app.get("/")
def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/api/register")
def api_register(response: Response, data=Body()):
    name = data["name"]
    response.set_cookie(key="X-Authorization", value=name, httponly=True)

@app.get("/chat")
def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})
