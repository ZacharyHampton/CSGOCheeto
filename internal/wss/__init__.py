from fastapi import FastAPI, WebSocket
import uvicorn


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

from internal.wss.route import router
app = FastAPI()
app.include_router(router)


def start():
    uvicorn.run(app, port=8000)
