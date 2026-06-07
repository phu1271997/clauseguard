# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *


class Contract(gl.Contract):
    value: u256
    store: TreeMap[str, u256]

    def __init__(self):
        self.value = u256(0)
        # Note: self.store is NOT reassigned here, satisfying Rule 2.

    @gl.public.write
    def set_val(self, val: u256) -> None:
        self.value = val
        self.store["key"] = val

    @gl.public.view
    def get_val(self) -> u256:
        return self.value

    @gl.public.view
    def get_store_val(self) -> u256:
        return self.store.get("key", u256(0))
