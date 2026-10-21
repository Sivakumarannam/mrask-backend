import { useEffect, useState } from 'react';

import { projects as localProjects, type Project } from '@/data/projects';
import { getProjects } from '@/lib/api';

export function useProjects() {
  const [projects, setProjects] = useState<Project[]>(localProjects);
  const [loading, setLoading] = useState(true);
  const [source, setSource] = useState<'api' | 'local'>('local');

  useEffect(() => {
    let alive = true;
    getProjects().then((r) => {
      if (!alive) return;
      setProjects(r.projects);
      setSource(r.source);
      setLoading(false);
    });
    return () => {
      alive = false;
    };
  }, []);

  return { projects, loading, source };
}
