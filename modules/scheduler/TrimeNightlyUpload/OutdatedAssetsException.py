class OutdatedAssetsException(BaseException):
    """
    Assets 不是最新的
    """
    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message