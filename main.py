import asyncio
import websockets

USERS = set()
useres = {}

async def addUser(websocket):
    i = len(useres)
    useres[websocket] = i
    USERS.add(websocket)


async def removeUser(websocket):
    useres.pop(websocket)
    USERS.remove(websocket)


async def socket(websocket, path):
    await addUser(websocket)

    try:
        while True:
            message = await websocket.recv()
            print(type(message))
            await asyncio.wait([user.send(str(useres[websocket])+" " + message) for user in USERS])
    finally:
        await removeUser(websocket)


start_server = websockets.serve(socket, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()