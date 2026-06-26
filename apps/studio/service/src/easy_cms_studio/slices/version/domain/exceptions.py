class VersionUnavailable(Exception):
    default_detail = "CMS Studio sidecar version could not be reported."

    def __init__(self, detail: str = default_detail) -> None:
        super().__init__(detail)
        self.detail = detail
