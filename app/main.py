import asyncio
import socket
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.log_utils import get_daily_logger
from app.hw_utils import init_hw_status, hw_worker_loop

from app.routers import download, hw


class _CoalescingTransport:
    __slots__ = ("_real", "_buf", "_flushed")

    def __init__(self, real):
        self._real = real
        self._buf = bytearray()
        self._flushed = False

    def buffer_only(self, data):
        self._buf.extend(data)

    def write(self, data):
        if not self._flushed:
            self._flushed = True
            sock = self._real.get_extra_info("socket")
            if sock is not None:
                try:
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                except Exception:
                    pass
            self._real.write(bytes(self._buf) + bytes(data))
            self._buf.clear()
        else:
            self._real.write(data)

    def flush_if_needed(self):
        if not self._flushed and self._buf:
            self._flushed = True
            self._real.write(bytes(self._buf))
            self._buf.clear()

    def __getattr__(self, name):
        return getattr(self._real, name)


class _HeaderBufferTransport:
    __slots__ = ("_real", "_buf")

    def __init__(self, real):
        self._real = real
        self._buf = bytearray()

    def write(self, data):
        self._buf.extend(data)

    def __getattr__(self, name):
        return getattr(self._real, name)


def _install_single_packet_http_send():
    """
    Coalesce ASGI http.response.start (headers) and the first http.response.body
    chunk into a single socket write with TCP_NODELAY enabled, so HTTP 200 OK
    responses are transmitted in 1 single TCP packet instead of 2 segments.
    """
    for mod_name in (
        "uvicorn.protocols.http.httptools_impl",
        "uvicorn.protocols.http.h11_impl",
    ):
        try:
            mod = __import__(mod_name, fromlist=["RequestResponseCycle"])
            cls = mod.RequestResponseCycle
            if getattr(cls, "_coalesced_patch_installed", False):
                continue
            orig_send = cls.send

            async def coalesced_send(self, message, _orig=orig_send):
                msg_type = message.get("type")
                if msg_type == "http.response.start":
                    real_transport = getattr(self, "_real_transport", None) or self.transport
                    self._real_transport = real_transport
                    hb = _HeaderBufferTransport(real_transport)
                    self._header_buf_transport = hb
                    self.transport = hb
                    try:
                        return await _orig(self, message)
                    except Exception:
                        self.transport = real_transport
                        self._header_buf_transport = None
                        raise
                elif msg_type == "http.response.body" and getattr(self, "_header_buf_transport", None) is not None:
                    real_transport = self._real_transport
                    hb = self._header_buf_transport
                    self._header_buf_transport = None
                    ct = _CoalescingTransport(real_transport)
                    ct._buf = hb._buf
                    self.transport = ct
                    try:
                        res = await _orig(self, message)
                        ct.flush_if_needed()
                        return res
                    finally:
                        self.transport = real_transport
                else:
                    return await _orig(self, message)

            cls.send = coalesced_send
            cls._coalesced_patch_installed = True
        except Exception:
            pass


_install_single_packet_http_send()

app = FastAPI(
    title="Microservicio comunicacion con dispositivos de domotica",
    version="1.0.0"
)

logger = get_daily_logger()

@app.on_event("startup")
async def startup_event():
    await asyncio.to_thread(init_hw_status)
    asyncio.create_task(hw_worker_loop())

# Routers existentes
app.include_router(download.router)
app.include_router(hw.router)

@app.get("/health")
def health():
    return {"status": "ok"}
