import { Text, View } from 'react-native';

import { Card, Chip, Heading, Screen } from '@/components/ui';
import { useTheme } from '@/constants/theme';
import { profile, skillGroups } from '@/data/profile';

export default function Skills() {
  const t = useTheme();

  return (
    <Screen>
      <Heading sub="Core technologies and strengths behind the work I build and ship.">Skills</Heading>
      <Card accent>
          <Text style={{ color: t.text, fontWeight: '800', fontSize: 22, marginBottom: 16 }}>
            {profile.name}
          </Text>
          <Text style={{ color: t.muted, fontSize: 16, lineHeight: 26 }}>
            I build modern products with a practical focus on performance, clean architecture, and user value.
          </Text>
        </Card>

      {skillGroups.map((group, idx) => (
        <View key={group.title} style={{ marginBottom: idx === skillGroups.length - 1 ? 0 : 16 }}>
          <Text style={{ color: t.text, fontWeight: '800', fontSize: 18, marginBottom: 10 }}>{group.title}</Text>
          <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8 }}>
            {group.items.map((item) => (
              <Chip key={item} label={item} />
            ))}
          </View>
        </View>
      ))}
    </Screen>
  );
}
