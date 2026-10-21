import { useColorScheme } from 'react-native';

const light = {
  bg: '#05070A',
  card: '#0D1116',
  cardAlt: '#121920',
  text: '#F5F7FA',
  muted: '#AAB7C4',
  border: '#1D2731',
  accent: '#7DB9FF',
  accent2: '#9CC9FF',
  accent3: '#D9E9FF',
  chip: '#101922',
  chipText: '#ECF5FF',
  glow: 'rgba(125, 185, 255, 0.08)',
  glow2: 'rgba(125, 185, 255, 0.05)',
};

const dark = { ...light };

export type Theme = typeof light;

/** Blue gradient matching the old portfolio reference. */
export const gradient = ['#149DDD', '#37B3ED', '#0EA5E9'] as const;

/** Keep the app in the dark black-blue style matching the old portfolio reference. */
export function useTheme(): Theme {
  return dark;
}
