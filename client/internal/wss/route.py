from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from client.internal.wss import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
