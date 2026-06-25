export function formatRelative(iso: string | null) {
    if (!iso) return '-';

    const then = new Date(iso).getTime();
    const now = Date.now();
    const diffSec = Math.round((then - now) / 1000);
    const abs = Math.abs(diffSec);

    const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });

    if (abs < 60) return rtf.format(diffSec, 'second');
    if (abs < 3600) return rtf.format(Math.round(diffSec / 60), 'minute');
    if (abs < 86400) return rtf.format(Math.round(diffSec / 86400), 'hour');
    return rtf.format(Math.round(diffSec / 86400), 'day');
}