from bitmex_websocket import BitMEXWebsocket
from time import time, sleep


class BitMEXTimeoutWebsocket(BitMEXWebsocket):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_timeout = 10.0

    def _BitMEXWebsocket__on_message(self, message):
        super()._BitMEXWebsocket__on_message(message)
        self.last_update_t = time()

    def _BitMEXWebsocket__on_close(self):
        super()._BitMEXWebsocket__on_close()
        self.exited = True

    def exit_if_overdue(self, ensure_updated_after_t, max_wait=2.0):
        end_t = time() + max_wait
        while time() < end_t:
            if self.last_update_t > ensure_updated_after_t:
                return self.exit_on_timeout()
            sleep(0.1)
        self.exit()
        return True

    def exit_on_timeout(self, timeout=None):
        timeout = timeout or self.default_timeout
        if self.exited or not self.wst.is_alive() or time()-self.last_update_t > timeout:
            self.logger.error('Timeout or disconnected!')
            self.exit()
        return self.exited


def refresh(ws, timeout=None):
    if ws.exit_on_timeout(timeout):
        print('WARNING: BitMEX websocket done, creating a new one')
        return BitMEXTimeoutWebsocket(ws.endpoint, ws.symbol, ws.api_key, ws.api_secret)
    return ws
