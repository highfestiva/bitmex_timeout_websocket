# bitmex_timeout_websocket.py

Problems arise when a bitmex-ws websocket goes stale. This simple wrapper helps you fix that. Use like so:

```python
from bitmex_timeout_websocket import BitMEXTimeoutWebsocket
from time import sleep

ws = BitMEXTimeoutWebsocket(endpoint='https://testnet.bitmex.com/api/v1', symbol='XBTUSD')
while not ws.exit_on_timeout():
    sleep(5.0)
```


## Licence

MIT
