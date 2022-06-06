import asyncio
import logging
import json
import random
from typing import Any

import aiohttp.web as aiohttp
import lz4.frame as lz4

async def send(ws: aiohttp.WebSocketResponse, data: Any, event_name: str):
    as_json: str = json.dumps(
        {
            'event': event_name,
            'data': data,
            'service': 'venera.com',
        }
    )
    ready = lz4.compress(as_json.encode())
    await ws.send_bytes(ready)

async def handle_message(data: dict):
    type = data['type']

    if type == 'PULL':
        # Pull or Get data
        ...
    elif type == 'AUTHORIZE':
        # Get a User Token
        ...
    elif type == '':
        ...

async def recv(ws: aiohttp.WebSocketResponse):
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.CLOSE:
            break
        elif msg.type == aiohttp.WSMsgType.TEXT:
            data = msg.json()
            loop = asyncio.get_running_loop()
            loop.create_task(handle_message(data=data))
        else:
            # TODO: Handle?
            ...

# NOTE: for the actual version, I'll need to think up of a
# anti-DDOS system.
async def ws_handler(request: aiohttp.Request):
    timeout = random.randint(40.0, 49.0)
    ws = aiohttp.WebSocketResponse(timeout=timeout)
    await ws.prepare(request=request)
    ws.enable_chunked_encoding(1024)

    await send(
        ws=ws,
        data={
            'timeout': timeout,
        },
        event_name='HELLO',
    )
    loop = asyncio.get_running_loop()

    loop.create_task(recv(ws=ws))

def binder():
    app = aiohttp.Application()
    return app

async def gunicorn_binder():
    app = binder()
    return app

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = binder()
    aiohttp.run_app(app=app, port=5000)
