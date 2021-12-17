import asyncio
import websockets

USERS = set()
useres = {}


async def addUser(websocket):
    useres[websocket] = "polzowatel"
    USERS.add(websocket)


async def removeUser(websocket):
    await asyncio.wait([user.send(str(useres[websocket]) + " left") for user in USERS])
    useres.pop(websocket)
    USERS.remove(websocket)


async def socket(websocket, path):
    await addUser(websocket)
    try:
        while True:
            message = await websocket.recv()
            a = message[0:7]
            if useres[websocket] == "polzowatel" or useres[websocket] == "":
                useres[websocket] = message
                await asyncio.wait([user.send(message + " joined the chat") for user in USERS])
            elif a == "private":
                us = message.split(":")[1]
                b = []
                for i in useres:
                    if useres[i] == us:
                        b.append(i)
                if len(b) == 0:
                    await websocket.send("Error user not find")
                else:
                    await asyncio.wait(
                        [user.send(str("privat message from " + useres[websocket]) + ": " + message.split(":")[2]) for
                         user in b])
                    await websocket.send("privat message to " + useres[websocket] + ": " + message.split(":")[2])
            else:
                await asyncio.wait([user.send(str(useres[websocket]) + ": " + message) for user in USERS])
    finally:
        await removeUser(websocket)


start_server = websockets.serve(socket, '192.168.230.32', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
