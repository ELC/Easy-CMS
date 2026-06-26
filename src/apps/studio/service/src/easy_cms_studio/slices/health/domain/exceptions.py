from dataclasses import dataclass


@dataclass
class HealthUnavailable(Exception):
    detail: str

    def __post_init__(self) -> None:
        super().__init__(self.detail)
