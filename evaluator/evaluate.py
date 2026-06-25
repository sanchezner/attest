from datetime import datetime
from db.schemas import Contract, Observation, EvaluationResult, EvaluationStatus

def evaluate(
    contract: Contract,
    observation: Observation,
    *,
    now: datetime,
):
    if observation.artifact_id != contract.artifact_id:
        return EvaluationResult(
            status=EvaluationStatus.VIOLATED, 
            reason=f'artifact mismatch: observation={observation.artifact_id}, contract={contract.artifact_id}',
        )
    
    if contract.expected_reporter is not None:
        if observation.reporter != contract.expected_reporter:
            return EvaluationResult(
                status=EvaluationStatus.VIOLATED,
                reason=f'unexpected reporter: got {observation.reporter}, expected {contract.expected_reporter}',
            )

    if contract.min_row_count is not None:
        if observation.row_count is None:
            return EvaluationResult(
                status=EvaluationStatus.VIOLATED,
                reason='row_count missing but contract requires min_row_count',
            )
        if observation.row_count < contract.min_row_count:
            return EvaluationResult(
                status=EvaluationStatus.VIOLATED,
                reason=f'row_count {observation.row_count} < min {contract.min_row_count}',
            )

    if contract.max_age_hours is not None:
        age_hours = (now - observation.observed_at).total_seconds() / 3600
        if age_hours > contract.max_age_hours:
            return EvaluationResult(
                status=EvaluationStatus.VIOLATED,
                reason=f'stale: age {age_hours:.1f}h > max {contract.max_age_hours}h',
            )
        
    return EvaluationResult(
        status=EvaluationStatus.OK,
    )