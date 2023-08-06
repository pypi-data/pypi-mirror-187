import _toori

import socket
import asyncio
import socketio
from concurrent.futures import ThreadPoolExecutor

# Increase the packet buffer
from engineio.payload import Payload

Payload.max_decode_packets = 2500000

_executor = ThreadPoolExecutor(1)

sio = socketio.AsyncClient()

loop = asyncio.get_event_loop()


def resolve_address(address):
    hostname = address.split("//")[-1:][0]
    ip = socket.gethostbyname(hostname)

    return ip


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip


@sio.on("connect")
async def on_connect():
    print("connected to server")


@sio.on("in")
async def handle_incoming(data):
    # await loop.run_in_executor(_executor, _toori.inj, data)
    _toori.inj(data)
    # await asyncio.sleep(0.0)


async def start_client(address):

    await sio.connect(f"{address}")

    _toori.init(
        f"outbound && !loopback && ip && ip.DstAddr != {resolve_address(address)}",
        get_local_ip(),
    )

    while True:
        data = await loop.run_in_executor(_executor, _toori.get)
        # data = _toori.get()
        if len(data) > 0:
            try:
                await sio.emit(event="out", data=data)
            except Exception:
                pass

        # await asyncio.sleep(0.0001)

def start(address):
    loop.run_until_complete(start_client(address))
