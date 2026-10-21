import { Text } from 'react-native';

import { Card, Chip, Heading, Screen } from '@/components/ui';
import { useTheme } from '@/constants/theme';
import { education, experience, profile, skillGroups } from '@/data/profile';

export default function About() {
  const t = useTheme();
  return (
    <Screen>
      <Heading>About me</Heading>
      <Card>
        <Text style={{ color: t.text, fontSize: 20, fontWeight: '800' }}>{profile.name}</Text>
        <Text style={{ color: t.accent, fontWeight: '700', marginTop: 4 }}>{profile.title}</Text>
        <Text style={{ color: t.muted, fontSize: 16, lineHeight: 24, marginTop: 10 }}>
          {profile.summary}
        </Text>
        <Text style={{ color: t.muted, marginTop: 10 }}>{profile.location}</Text>
      </Card>

      <Heading>Experience</Heading>
      {experience.map((e) => (
        <Card key={e.role}>
          <Text style={{ color: t.text, fontSize: 18, fontWeight: '800' }}>{e.role}</Text>
          <Text style={{ color: t.accent, fontWeight: '600', marginTop: 4 }}>{e.org}</Text>
          <Text style={{ color: t.muted, marginTop: 8 }}>{e.note}</Text>
        </Card>
      ))}

      <Heading>Education</Heading>
      <Card>
        <Text style={{ color: t.text, fontSize: 18, fontWeight: '800' }}>{education.degree}</Text>
        <Text style={{ color: t.muted, marginTop: 6 }}>{education.school}</Text>
      </Card>

      <Heading>Skills</Heading>
      <Card>
        {skillGroups.map((g) => (
          <Text key={g.title} style={{ color: t.muted, marginBottom: 6, lineHeight: 22 }}>
            <Text style={{ color: t.text, fontWeight: '700' }}>{g.title}: </Text>
            {g.items.join(', ')}
          </Text>
        ))}
      </Card>

      <Heading>How I work</Heading>
      <Card>
        <Chip label="Solo builder" />
        <Text style={{ color: t.muted, fontSize: 15, lineHeight: 22, marginTop: 10 }}>
          I plan, code, debug and document my projects myself, from the first idea to a working
          result.
        </Text>
      </Card>
    </Screen>
  );
}
