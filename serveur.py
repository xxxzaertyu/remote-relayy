import asyncio
import websockets

clients = set()


async def handler(websocket):
    clients.add(websocket)

    print("Client connecté")

    try:
        async for message in websocket:
            for client in clients:
                if client != websocket:
                    await client.send(message)

    except websockets.exceptions.ConnectionClosed:
        print("Client déconnecté")

    finally:
        clients.discard(websocket)


async def main():
    print("Serveur démarré sur le port 8765")

    async with websockets.serve(
        handler,
        "0.0.0.0",
        8765
    ):
        await asyncio.Future()


asyncio.run(main())