import type { ArtifactStatus } from "../types";
import { formatRelative } from "../utils/time";
import { StatusBadge } from "./StatusBadge";

interface StatusTableProps {
    artifacts: ArtifactStatus[];
}

export function StatusTable({ artifacts }: StatusTableProps) {
    if (artifacts.length === 0) {
        return <p className='empty'>No contracts registered for this project.</p>
    }

    return (
        <table className='status-table'>
            <thead>
                <tr>
                    <th>Artifact</th>
                    <th>Status</th>
                    <th>Reason</th>
                    <th>Last observed</th>
                </tr>
            </thead>
            <tbody>
                {artifacts.map((artifact) => (
                    <tr key={artifact.artifact_id}>
                        <td className='artifact-id'>{artifact.artifact_id}</td>
                        <td><StatusBadge status={artifact.status} /></td>
                        <td className='reason'>{artifact.reason ?? '-'}</td>
                        <td className='timestamp' title={artifact.observed_at ?? undefined}>{formatRelative(artifact.observed_at)}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    )
}