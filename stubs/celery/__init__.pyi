from typing import Any, List

class Task: ...

class Celery(object):
    conf = None  # type: Any
    def __init__(self, *args, **kwargs): ...
    def autodiscover_tasks(
        self,
        packages: List[str] = None,
        related_name: str = "tasks",
        force: bool = False,
    ) -> Any: ...
    def task(self, *args, **opts): ...
    def config_from_object(self, *args, **opts): ...

def signature(*args, **kwargs) -> Any: ...

current_app = Celery()
signals = None  # type: Any
