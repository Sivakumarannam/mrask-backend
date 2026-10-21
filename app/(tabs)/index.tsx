import { useRouter } from 'expo-router';
import { Text, View } from 'react-native';

import { ProjectCard } from '@/components/ProjectCard';
import { Button, Chip, Heading, Screen, openLink } from '@/components/ui';
import { useTheme } from '@/constants/theme';
import { profile, skillGroups } from '@/data/profile';
import { projects } from '@/data/projects';

export default function Home() {
  const t = useTheme();
  const router = useRouter();

  return (
    <Screen>
      <View style={{ paddingTop: 32 }}>
        <View
          style={{
            alignSelf: 'flex-start',
            backgroundColor: t.chip,
            paddingHorizontal: 12,
            paddingVertical: 6,
            borderRadius: 999,
          }}>
          <Text style={{ color: t.chipText, fontWeight: '700', fontSize: 13 }}>
            {'\u25CF  ' + profile.openTo}
          </Text>
        </View>

        <Text style={{ color: t.text, fontSize: 40, fontWeight: '800', marginTop: 16 }}>
          {"Hi, I'm " + profile.name}
        </Text>
        <Text style={{ color: t.accent, fontSize: 22, fontWeight: '700', marginTop: 6 }}>
          {profile.title}
        </Text>
        <Text style={{ color: t.muted, fontSize: 17, lineHeight: 26, marginTop: 14 }}>
          {profile.summary}
        </Text>

        <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginTop: 20 }}>
          <Button
            label="Email me"
            onPress={() => openLink('mailto:' + profile.email)}
          />
          <Button
            label="View projects"
            variant="secondary"
            onPress={() => router.push('/projects')}
          />
          <Button label="GitHub" variant="secondary" onPress={() => openLink(profile.github)} />
        </View>
      </View>

      <Heading sub="Technologies I have worked with">Skills</Heading>
      {skillGroups.map((g) => (
        <View key={g.title} style={{ marginBottom: 14 }}>
          <Text style={{ color: t.text, fontWeight: '700', marginBottom: 8 }}>{g.title}</Text>
          <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8 }}>
            {g.items.map((s) => (
              <Chip key={s} label={s} />
            ))}
          </View>
        </View>
      ))}

      <Heading sub="Built end to end by me">Featured projects</Heading>
      {projects.map((p) => (
        <ProjectCard key={p.id} p={p} />
      ))}
    </Screen>
  );
}
