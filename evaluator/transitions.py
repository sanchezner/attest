from db.schemas import EvaluationStatus


def should_alert(
    previous: EvaluationStatus | None,
    current: EvaluationStatus, 
):
    if current == EvaluationStatus.OK:
        return previous is not None and previous != EvaluationStatus.OK

    if previous is None:
        return True

    return previous != current