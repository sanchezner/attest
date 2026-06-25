export type EvaluationStatus = 'ok' | 'violated' | 'missing'

export interface ArtifactStatus {
    artifact_id: string
    status: EvaluationStatus
    reason: string | null
    observed_at: string | null
}

export interface ProjectStatus {
    project_slug: string
    evaluated_at: string
    artifacts: ArtifactStatus[]
}