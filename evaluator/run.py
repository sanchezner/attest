from datetime import datetime, timezone
from db.queries import (
    get_latest_evaluation_status,
    get_latest_observation,
    insert_evaluation,
    insert_alert_log,
    list_all_contracts,
)
from evaluator.contract import evaluate_contract
from evaluator.transitions import should_alert
from notifier.ntfy import NtfyConfig, send_alert


def run_evaluations(session, *, now: datetime | None = None, dry_run: bool = False):
    if now is None:
        now = datetime.now(timezone.utc)

    ntfy_config = None if dry_run else NtfyConfig.from_env()
    alerts = []

    for project_slug, contract in list_all_contracts(session):
        latest = get_latest_observation(session, project_slug, contract.artifact_id)
        result = evaluate_contract(contract, latest, now=now)

        previous = get_latest_evaluation_status(
            session, project_slug, contract.artifact_id,
        )

        if should_alert(previous, result.status):
            alert = {
                'project_slug': project_slug,
                'artifact_id': contract.artifact_id,
                'previous': previous.value if previous else None,
                'current': result.status.value,
                'reason': result.reason,
            }
            
            alerts.append(alert)

            if ntfy_config is not None:
                http_status = send_alert(ntfy_config, alert)
                insert_alert_log(
                    session=session,
                    project_slug=project_slug,
                    artifact_id=contract.artifact_id,
                    previous_status=alert['previous'],
                    current_status=alert['current'],
                    reason=alert['reason'],
                    ntfy_topic=ntfy_config.topic,
                    http_status=http_status,
                    sent_at=now,
                )

        insert_evaluation(session, project_slug, contract.artifact_id, result, evaluated_at=now)
    
    return alerts