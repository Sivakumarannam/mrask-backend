import { useRouter } from 'expo-router';
import { Text, View } from 'react-native';

import { Button, Card, Heading, Screen } from '@/components/ui';
import { useTheme } from '@/constants/theme';

export default function Contact() {
  const t = useTheme();
  const router = useRouter();

  return (
    <Screen>
      <Heading sub="Get in touch when the contact details are ready and I will share the direct links here.">
        Contact
      </Heading>

      <Card accent>
        <Text style={{ color: t.text, fontSize: 20, fontWeight: '800', marginBottom: 8 }}>
          Contact details aren’t listed yet.
        </Text>
        <Text style={{ color: t.muted, fontSize: 16, lineHeight: 26 }}>
          For now, explore the project pages for details about each tool. This page will link to direct
          contact options once they’re provided.
        </Text>

        <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginTop: 18 }}>
          <Button label="Explore projects" onPress={() => router.push('/projects')} />
          <Button label="Back to home" variant="secondary" onPress={() => router.push('/')} />
        </View>
      </Card>
    </Screen>
  );
}
