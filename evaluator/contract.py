from datetime import datetime
from db.schemas import Contract, Observation, EvaluationResult, EvaluationStatus
from evaluator.evaluate import evaluate


def _requires_observation(contract: Contract):
    return (
        contract.must_exist 
        or contract.min_row_count is not None 
        or contract.max_age_hours
    )


def evaluate_contract(
    contract: Contract,
    latest: Observation | None,
    *,
    now: datetime,
):
    if latest is None:
        if _requires_observation(contract):
            return EvaluationResult(
                status=EvaluationStatus.MISSING,
                reason='no observation recieved',
            )
        return EvaluationResult(
            status=EvaluationStatus.OK,
        )

    return evaluate(contract, latest, now=now)