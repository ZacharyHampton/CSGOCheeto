from fastapi import FastAPI, WebSocket
import uvicorn
from client.cheeto.models.packet import Packet


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, packet: Packet):
        for connection in self.active_connections:
            await connection.send_json(packet.json())


manager = ConnectionManager()

from client.internal.wss.route import router
app = FastAPI()
app.include_router(router)


def start():
    uvicorn.run(app, port=8000)
