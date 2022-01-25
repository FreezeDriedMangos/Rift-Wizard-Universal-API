from typing import Callable, TypeVar

T = TypeVar('T')

def patch_init(cls: T, init: Callable[[T], None]):
    old_init = cls.__init__
    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        init(self, *args, **kwargs)
    cls.__init__ = new_init
