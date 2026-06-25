import type { EvaluationStatus } from "../types";

const styles: Record<EvaluationStatus, { label: string; className: string}> = {
    ok: { label: 'OK', className: 'badge badge-ok' },
    violated: { label: 'Violated', className: 'badge badge-violated' },
    missing: { label: 'Missing', className: 'badge badge-missing' },
};

interface StatusBadgeProps {
    status: EvaluationStatus;
}

export function StatusBadge({ status }: StatusBadgeProps) {
    const { label, className } = styles[status];

    return <span className={className}>{label}</span>;
}