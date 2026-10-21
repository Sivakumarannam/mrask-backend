import { LinearGradient } from 'expo-linear-gradient';
import { Text, View } from 'react-native';

import { gradient, useTheme } from '@/constants/theme';

/** Numbered vertical flow that shows how a project works step by step. */
export function Pipeline({ steps }: { steps: string[] }) {
  const t = useTheme();
  return (
    <View>
      {steps.map((s, i) => (
        <View key={s + i} style={{ flexDirection: 'row' }}>
          <View style={{ alignItems: 'center', marginRight: 14 }}>
            <LinearGradient
              colors={gradient}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
              style={{
                width: 32,
                height: 32,
                borderRadius: 16,
                alignItems: 'center',
                justifyContent: 'center',
              }}>
              <Text style={{ color: '#FFFFFF', fontWeight: '800' }}>{i + 1}</Text>
            </LinearGradient>
            {i < steps.length - 1 ? (
              <View style={{ width: 2, flex: 1, minHeight: 18, backgroundColor: t.border }} />
            ) : null}
          </View>
          <Text
            style={{
              color: t.text,
              fontSize: 16,
              fontWeight: '600',
              paddingTop: 5,
              paddingBottom: 16,
              flex: 1,
            }}>
            {s}
          </Text>
        </View>
      ))}
    </View>
  );
}
