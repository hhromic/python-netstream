# python-netstream
A NetStream implementation in Python for GraphStream

Example Usage
=============

```python
#!/usr/bin/env python

import netstream
import logging

logging.basicConfig(level=logging.DEBUG)

transport = netstream.BinaryNetStreamTransport("localhost", 2012)
sender = netstream.NetStreamSender(transport)
proxy = netstream.NetStreamProxyGraph(sender)

style = "node{fill-mode:plain;fill-color:gray;size:1px;}"
proxy.add_attribute("stylesheet", style)

proxy.add_attribute("ui.antialias", True)
proxy.add_attribute("layout.stabilization-limit", 0)

for i in range(0,500):
    proxy.add_node(str(i))
    if i > 0:
        proxy.add_edge(str(i) + "_" + str(i-1), str(i), str(i-1), False)
        proxy.add_edge(str(i) + "__" + str(i/2), str(i), str(i/2), False)
```
