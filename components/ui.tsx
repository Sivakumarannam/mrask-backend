import type { ReactNode } from 'react';
import { Linking, Pressable, ScrollView, Text, View } from 'react-native';

import { useTheme } from '@/constants/theme';

export const openLink = (url: string) => {
  Linking.openURL(url).catch(() => {});
};

export function Screen({ children }: { children: ReactNode }) {
  const t = useTheme();
  return (
    <ScrollView
      style={{ flex: 1, backgroundColor: t.bg }}
      contentContainerStyle={{ alignItems: 'center', padding: 20, paddingBottom: 48 }}>
      <View style={{ width: '100%', maxWidth: 880 }}>{children}</View>
    </ScrollView>
  );
}

export function Heading({ children, sub }: { children: ReactNode; sub?: string }) {
  const t = useTheme();
  return (
    <View style={{ marginTop: 28, marginBottom: 12 }}>
      <Text style={{ color: t.text, fontSize: 24, fontWeight: '800' }}>{children}</Text>
      {sub ? <Text style={{ color: t.muted, fontSize: 15, marginTop: 4 }}>{sub}</Text> : null}
    </View>
  );
}

export function Chip({ label }: { label: string }) {
  const t = useTheme();
  return (
    <View
      style={{
        backgroundColor: t.chip,
        paddingHorizontal: 10,
        paddingVertical: 5,
        borderRadius: 999,
      }}>
      <Text style={{ color: t.chipText, fontSize: 13, fontWeight: '600' }}>{label}</Text>
    </View>
  );
}

export function Button({
  label,
  onPress,
  variant = 'primary',
}: {
  label: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary';
}) {
  const t = useTheme();
  const primary = variant === 'primary';
  return (
    <Pressable
      onPress={onPress}
      style={({ pressed }) => ({
        backgroundColor: primary ? t.accent : 'transparent',
        borderColor: primary ? t.accent : t.border,
        borderWidth: 1,
        paddingHorizontal: 18,
        paddingVertical: 11,
        borderRadius: 10,
        opacity: pressed ? 0.7 : 1,
      })}>
      <Text style={{ color: primary ? t.accentText : t.text, fontWeight: '700', fontSize: 15 }}>
        {label}
      </Text>
    </Pressable>
  );
}

export function Card({ children }: { children: ReactNode }) {
  const t = useTheme();
  return (
    <View
      style={{
        backgroundColor: t.card,
        borderColor: t.border,
        borderWidth: 1,
        borderRadius: 16,
        padding: 18,
        marginBottom: 14,
      }}>
      {children}
    </View>
  );
}
