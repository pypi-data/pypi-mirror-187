import sys
import json
import traceback
from datetime import datetime as DateTime
from typing import Coroutine, Any
from threading import Thread
import asyncio
from asyncio import (
    AbstractEventLoop
)
from aiohttp import ClientSession, ClientWebSocketResponse


class WebSocketClient():
    """
    """

    def __init__(self, url: str, proxy_host: str = "", proxy_port: int = 0, headers: dict = None, ping_interval: int = 60) -> None:
        """
        Constructor
        """
        self._url = url
        self._ping_interval = ping_interval
        self._headers = headers if headers else {}
        self._proxy = f"http://{proxy_host}:{proxy_port}" if proxy_host and proxy_port else ""         
        self._is_active: bool = False
        self._session: ClientSession = None
        self._response: ClientWebSocketResponse = None
        self._event_loop: AbstractEventLoop = None
        self._last_sent_message: str = ""
        self._last_received_message: str = ""

    def open(self):
        """
        Open connection
        """
        self._is_active = True

        try:
            self._event_loop = asyncio.get_running_loop()

        except RuntimeError:
            self._event_loop = asyncio.new_event_loop()

        self._start_event_loop(self._event_loop)
        asyncio.run_coroutine_threadsafe(self._run(), self._event_loop)

    def close(self):
        """
        Close connection
        """
        self._is_active = False

        if self._response:
            coro = self._response.close()
            asyncio.run_coroutine_threadsafe(coro, self._event_loop)

        if self._event_loop and self._event_loop.is_running():
            self._event_loop.stop()

    def join(self):
        """
        等待后台线程退出。
        """
        pass

    def send(self, packet: dict):
        """
        Send message to server.
        """
        if self._response:
            text: str = json.dumps(packet)
            self._record_last_sent_text(text)
            coro: Coroutine[Any, Any, None] = self._response.send_str(text)
            asyncio.run_coroutine_threadsafe(coro, self._event_loop)

    def parse_data(self, data: str):
        """
        Parse data from server.
        """
        return json.loads(data)

    def on_connected(self):
        """
        连接成功回调
        """
        pass

    def on_disconnected(self):
        """
        连接断开回调
        """
        pass

    def on_data_received(self, packet: dict):
        """
        收到数据回调
        """
        pass

    def on_error(self, exception_type: type, exception: Exception, tb) -> None:
        """
        触发异常回调
        """
        try:
            print("WebsocketClient on error" + "-" * 10)
            print(self._format_exception(exception_type, exception, tb))
        except Exception:
            traceback.print_exc()

    def _format_exception(self, exception_type: type, exception_value: Exception, tb) -> str:
        """
        Format exception message
        """
        message = "[{}]: Unhandled WebSocket Error:{}\n".format(
            DateTime.now().isoformat(), exception_type
        )
        message += "LastSentText:\n{}\n".format(self._last_sent_message)
        message += "LastReceivedText:\n{}\n".format(self._last_received_message)
        message += "Exception trace: \n"
        message += "".join(
            traceback.format_exception(exception_type, exception_value, tb)
        )
        return message

    async def _run(self):
        """
        在事件循环中运行的主协程
        """
        self._session = ClientSession()

        while self._is_active:
            try:
                # 发起Websocket连接
                self._response = await self._session.ws_connect(
                    self._url,
                    proxy=self._proxy,
                    verify_ssl=False
                )
                self.on_connected()

                async for msg in self._response:
                    text: str = msg.data
                    self._record_last_received_text(text)
                    data: dict = self.parse_data(text)
                    self.on_data_received(data)

                self._response = None
                self.on_disconnected()

            except Exception:
                et, ev, tb = sys.exc_info()
                self.on_error(et, ev, tb)

    def _record_last_sent_text(self, text: str):
        """记录最近发出的数据字符串"""
        self._last_sent_message = text[:1000]

    def _record_last_received_text(self, text: str):
        """记录最近收到的数据字符串"""
        self._last_received_message = text[:1000]


    def _start_event_loop(self, event_loop: AbstractEventLoop) -> None:
        """启动事件循环"""
        if not event_loop.is_running():
            thread = Thread(target=self._run_event_loop, args=(event_loop,))
            thread.daemon = True
            thread.start()

    def _run_event_loop(self, event_loop: AbstractEventLoop) -> None:
        """运行事件循环"""
        asyncio.set_event_loop(event_loop)
        event_loop.run_forever()



