import { Text, View } from 'react-native';

import { Button, Card, Heading, Screen, openLink } from '@/components/ui';
import { useTheme } from '@/constants/theme';
import { profile } from '@/data/profile';

export default function Contact() {
  const t = useTheme();
  const mailto =
    'mailto:' +
    profile.email +
    '?subject=' +
    encodeURIComponent('Hello Siva, I saw your portfolio');

  return (
    <Screen>
      <Heading sub="Interested in working together or want to talk about a project? Reach out.">
        Get in touch
      </Heading>

      <Card>
        <Text style={{ color: t.muted, fontSize: 14 }}>Email</Text>
        <Text style={{ color: t.text, fontSize: 18, fontWeight: '700', marginTop: 4 }}>
          {profile.email}
        </Text>
        <View style={{ flexDirection: 'row', marginTop: 14 }}>
          <Button label="Send an email" onPress={() => openLink(mailto)} />
        </View>
      </Card>

      <Card>
        <Text style={{ color: t.muted, fontSize: 14, marginBottom: 12 }}>Find me online</Text>
        <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 10 }}>
          <Button label="LinkedIn" variant="secondary" onPress={() => openLink(profile.linkedin)} />
          <Button label="GitHub" variant="secondary" onPress={() => openLink(profile.github)} />
        </View>
      </Card>
    </Screen>
  );
}
