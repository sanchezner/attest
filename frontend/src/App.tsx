import { useCallback, useEffect, useState } from 'react';
import { fetchProjectStatus } from './api/client';
import { StatusTable } from './components/StatusTable';
import { Spinner } from './components/Spinner';
import type { ProjectStatus } from './types';
import './App.css'

const project_slug = import.meta.env.VITE_PROJECT_SLUG;
if (!project_slug) {
  throw new Error('Set VITE_PROJECT_SLUG in frontend/.env.local (see .env.example)');
}

function App() {
  const [status, setStatus] = useState<ProjectStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchProjectStatus(project_slug);
      setStatus(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <div className="app">
      <div className="header">
        <h1>
          <span className="brand">attest</span>
          <span className="title-context">
            for <span className='title-context-slug'>{status?.project_slug ?? project_slug}</span>
          </span>
        </h1>
        <button className="refresh-btn" onClick={load} disabled={loading}>
          {loading ? <Spinner size="sm" /> : 'Refresh'}
        </button>
      </div>

      {error && <p className="error">Error: {error}</p>}
      
      {loading && !status && (
        <div className="loading-state">
          <Spinner />
          <span>Loading status…</span>
        </div>
      )}

      {status && <StatusTable artifacts={status.artifacts} />}
    </div>
  );
}

export default App;