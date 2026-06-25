class ContractViolation(Exception):
    def __init__(self, artifact_id: str, status:str, reason: str | None):
        self.artifact_id = artifact_id
        self.status = status
        self.reason = reason
        super().__init__(
            f'{artifact_id}: {status}' + (f' ({reason})' if reason else '')
        )