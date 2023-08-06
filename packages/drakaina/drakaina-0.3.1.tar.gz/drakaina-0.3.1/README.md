# drakaina

❗ WIP

Module for simple RPC server implementation

![license: Apache License 2.0](https://img.shields.io/badge/license-Apache%202-blue) ![Python: >=3.7](https://img.shields.io/badge/python-%3E=3.7-blue) ![Code style: black](https://img.shields.io/badge/code%20style-black-black)

## Quick use

```python
from drakaina import remote_procedure
from drakaina.rpc_protocols import JsonRPCv2


@remote_procedure
def my_method():
    return "Hello Bro! ✋️"


JsonRPCv2().handle({"jsonrpc": "2.0", "method": "my_method", "id": 1})
```

## Installation

```shell
pip install drakaina
```
