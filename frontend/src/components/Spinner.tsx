interface SpinnerProps {
    size?: 'sm' | 'md';
}

export function Spinner({ size = 'md' }: SpinnerProps) {
    return <span className={`spinner spinner-${size}`} aria-label='Loading' />;
}