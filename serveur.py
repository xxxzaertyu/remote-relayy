import asyncio
import os

import websockets


clients = set()


async def handler(websocket):
    clients.add(websocket)

    print("Client connecté")

    try:
        async for message in websocket:

            # Relayer le message aux autres clients
            for client in clients.copy():

                if client != websocket:

                    try:
                        await client.send(message)

                    except websockets.exceptions.ConnectionClosed:
                        clients.discard(client)

    except websockets.exceptions.ConnectionClosed:
        print("Client déconnecté")

    finally:
        clients.discard(websocket)


async def main():

    # Render fournit automatiquement le port
    port = int(os.environ.get("PORT", 10000))

    print(f"Serveur démarré sur le port {port}")

    async with websockets.serve(
        handler,
        "0.0.0.0",
        port
    ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
