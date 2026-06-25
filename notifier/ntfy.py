import os
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class NtfyConfig:
    topic: str
    server: str = 'https://ntfy.sh'

    @classmethod
    def from_env(cls):
        topic = os.getenv('NTFY_TOPIC')
        if not topic:
            return None
        server = os.getenv('NTFY_SERVER', 'https://ntfy.sh').rstrip('/')
        return cls(topic=topic, server=server)

    
def format_alert_message(alert: dict):
    project = alert['project_slug']
    artifact = alert['artifact_id']
    previous = alert['previous']
    current = alert['current']
    reason = alert.get('reason') or ''

    title = f': {project} / {artifact}'
    body = f'{previous} -> {current}'
    if reason:
        body = f'{body}: {reason}'
    return title, body


def send_alert(config: NtfyConfig, alert: dict):
    title, body = format_alert_message(alert)
    url = f'{config.server}/{config.topic}'

    request = Request(
        url,
        data=body.encode('utf-8'),
        method='POST',
        headers={
            'Title': title,
            'Tags': 'warning',
            'Priority': '4',
        },
    )

    try:
        with urlopen(request, timeout=10) as response:
            return response.status
    except HTTPError as exc:
        return exc.code
    except URLError:
        return None