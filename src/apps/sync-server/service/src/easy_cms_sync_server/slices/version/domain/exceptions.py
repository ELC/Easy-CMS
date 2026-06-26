from dataclasses import dataclass


@dataclass
class VersionUnavailable(Exception):
    detail: str = "Sync Server version could not be reported."

    def __post_init__(self) -> None:
        super().__init__(self.detail)
