import { useColorScheme } from 'react-native';

const light = {
  bg: '#F6F7FB',
  card: '#FFFFFF',
  text: '#0F172A',
  muted: '#475569',
  border: '#E2E8F0',
  accent: '#4F46E5',
  accentText: '#FFFFFF',
  chip: '#EEF2FF',
  chipText: '#3730A3',
};

const dark = {
  bg: '#0B1020',
  card: '#141B2E',
  text: '#F1F5F9',
  muted: '#94A3B8',
  border: '#243049',
  accent: '#818CF8',
  accentText: '#0B1020',
  chip: '#1E2742',
  chipText: '#C7D2FE',
};

export type Theme = typeof light;

/** Returns the dark or light palette based on the device / browser setting. */
export function useTheme(): Theme {
  return useColorScheme() === 'dark' ? dark : light;
}
