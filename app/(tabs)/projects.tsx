import { ProjectCard } from '@/components/ProjectCard';
import { Heading, Screen } from '@/components/ui';
import { projects } from '@/data/projects';

export default function Projects() {
  return (
    <Screen>
      <Heading sub="Every project here was designed, built and tested by me alone">Projects</Heading>
      {projects.map((p) => (
        <ProjectCard key={p.id} p={p} />
      ))}
    </Screen>
  );
}
