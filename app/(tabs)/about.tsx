import { Image, Text, View } from 'react-native';

import { Card, Chip, FadeIn, Heading, Screen, Stat } from '@/components/ui';
import { useTheme } from '@/constants/theme';
import { profile, skillGroups } from '@/data/profile';

const focusAreas = [
  ['Product thinking', 'I turn ideas into clean, usable experiences with clear business value.'],
  ['Full-stack delivery', 'From UI to API to database, I build complete products end to end.'],
  ['Practical problem solving', 'I like learning fast, debugging clearly and shipping reliable features.'],
];

export default function About() {
  const t = useTheme();
  return (
    <Screen>
      <Heading sub="I build complete, thoughtful digital products with a focus on usability and real value.">About me</Heading>
      <Card accent>
          <View style={{ flexDirection: 'row', alignItems: 'center', gap: 18, flexWrap: 'wrap' }}>
            <Image
              source={require('@/assets/images/profile-photo.png')}
              style={{
                width: 120,
                height: 120,
                borderRadius: 30,
                borderWidth: 2,
                borderColor: 'rgba(255,255,255,0.5)',
              }}
            />
            <View style={{ flex: 1, minWidth: 180 }}>
              <Text style={{ color: t.text, fontSize: 26, fontWeight: '800' }}>{profile.name}</Text>
              <Text style={{ color: t.accent, fontWeight: '700', marginTop: 4, fontSize: 16 }}>
                {profile.title}
              </Text>
              <Text style={{ color: t.muted, marginTop: 12, fontWeight: '600' }}>{profile.location}</Text>
            </View>
          </View>
          <Text style={{ color: t.muted, fontSize: 16, lineHeight: 25, marginTop: 18 }}>
            {profile.summary}
          </Text>
        </Card>

      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginBottom: 8 }}>
        <Stat value="Full-stack" label="Design + frontend + backend" />
        <Stat value="Fast learner" label="Always building and iterating" />
        <Stat value="Launch-ready" label="API, app, and database together" />
      </View>

      <Heading sub="The way I work">How I build</Heading>
      <Card>
        {focusAreas.map(([title, body], index) => (
          <View
            key={title}
            style={{
              paddingVertical: 12,
              borderTopWidth: index === 0 ? 0 : 1,
              borderTopColor: t.border,
            }}>
            <Text style={{ color: t.text, fontWeight: '800', fontSize: 16, marginBottom: 4 }}>{title}</Text>
            <Text style={{ color: t.muted, fontSize: 15, lineHeight: 22 }}>{body}</Text>
          </View>
        ))}
      </Card>

      <Heading sub="Core tools and technologies I use for production work">Skills</Heading>
      <Card>
        {skillGroups.map((g, idx) => (
          <View key={g.title} style={{ marginBottom: idx === skillGroups.length - 1 ? 0 : 16 }}>
            <Text style={{ color: t.text, fontWeight: '800', marginBottom: 8 }}>{g.title}</Text>
            <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8 }}>
              {g.items.map((s) => (
                <Chip key={s} label={s} />
              ))}
            </View>
          </View>
        ))}
      </Card>
    </Screen>
  );
}
