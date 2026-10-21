import { Text, View } from 'react-native';

import { Button, Card, Chip, openLink } from '@/components/ui';
import { useTheme } from '@/constants/theme';
import type { Project } from '@/data/projects';

export function ProjectCard({ p }: { p: Project }) {
  const t = useTheme();
  return (
    <Card>
      <View style={{ flexDirection: 'row', alignItems: 'center', flexWrap: 'wrap', gap: 10 }}>
        <Text style={{ color: t.text, fontSize: 22, fontWeight: '800' }}>{p.title}</Text>
        <Chip label={p.role} />
      </View>
      <Text style={{ color: t.accent, fontSize: 15, fontWeight: '600', marginTop: 4 }}>
        {p.tagline}
      </Text>
      <Text style={{ color: t.muted, fontSize: 15, lineHeight: 22, marginTop: 10 }}>{p.summary}</Text>

      <Text style={{ color: t.text, fontWeight: '700', marginTop: 14, marginBottom: 6 }}>
        What I built
      </Text>
      {p.highlights.map((h) => (
        <Text key={h} style={{ color: t.muted, fontSize: 15, lineHeight: 22 }}>
          {'\u2022  '}
          {h}
        </Text>
      ))}

      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 14 }}>
        {p.stack.map((s) => (
          <Chip key={s} label={s} />
        ))}
      </View>

      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginTop: 16 }}>
        <Button label="View code on GitHub" onPress={() => openLink(p.github)} />
        {p.demo ? (
          <Button label="Live demo" variant="secondary" onPress={() => openLink(p.demo!)} />
        ) : null}
      </View>
    </Card>
  );
}
