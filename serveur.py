import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

clients = set()


@app.get("/")
async def home():
    return {"status": "Relay OK"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)

    print("Client connecté")

    try:
        while True:
            message = await websocket.receive_text()

            for client in clients.copy():
                if client != websocket:
                    try:
                        await client.send_text(message)
                    except Exception:
                        clients.discard(client)

    except WebSocketDisconnect:
        print("Client déconnecté")

    finally:
        clients.discard(websocket)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
