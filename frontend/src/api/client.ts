export async function fetchProjectStatus(projectSlug: string){
    const res = await fetch(`/api/v1/projects/${encodeURIComponent(projectSlug)}/dashboard/status`);

    if (!res.ok) {
        throw new Error(`Failed to load status: ${res.status}`)
    };

    return res.json();
}