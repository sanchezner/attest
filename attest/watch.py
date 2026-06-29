import json
from contextlib import contextmanager
from datetime import datetime, timezone
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from sdk.config import WatchConfig
from sdk.exceptions import ContractViolation


class Watch:
    def __init__(self, config: WatchConfig):
        self.config = config
        self._token = config.resolve_token()
        self._base = config.api_url.rstrip('/')

    @classmethod
    def from_config(cls, path: str = 'attest.yaml'):
        return cls(WatchConfig.from_yaml(path))

    def _request(self, method: str, path: str, body: dict | None = None):
        url = f'{self._base}{path}'
        data = None
        headers = {
            'Authorization': f'Bearer {self._token}',
            'Accept': 'application/json',
        }
        if body is not None:
            data = json.dumps(body).encode('utf-8')
            headers['Content-Type'] = 'application/json'

        request = Request(url, data=data, method=method, headers=headers)
        try:
            with urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except HTTPError as exc:
            detail = exc.read().decode('utf-8')
            raise RuntimeError(f'{method} {path} failed ({exc.code}): {detail}') from exc

    def report(
        self,
        artifact_id: str,
        *,
        row_count: int | None = None,
        observed_at: datetime | None = None,
    ):
        if observed_at is None:
            observed_at = datetime.now(timezone.utc)

        body = {
            'artifact_id': artifact_id,
            'reporter': self.config.reporter,
            'observed_at': observed_at.isoformat(),
            'row_count': row_count,
        }
        return self._request(
            method='POST',
            path=f'/api/v1/projects/{self.config.project}/observations',
            body=body,
        )

    def verify(self, artifact_id: str):
        result = self._request(
            method='GET',
            path=f'/api/v1/projects/{self.config.project}/status?artifact_id={artifact_id}',
        )
        artifacts = result.get('artifacts', [])
        if not artifacts:
            raise ContractViolation(artifact_id, 'unknown', 'contract not found')

        artifact = artifacts[0]
        if artifact['status'] != 'ok':
            raise ContractViolation(
                artifact_id=artifact_id,
                status=artifact['status'],
                reason=artifact.get('reason'),
            )

    @contextmanager
    def stage(
        self,
        artifact_id: str,
        *,
        row_count: int | None = None
    ):
        try:
            yield
        except Exception:
            raise
        else:
            self.report(artifact_id, row_count=row_count)