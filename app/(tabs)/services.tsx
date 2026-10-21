import { Text, View } from 'react-native';

import { Card, Heading, Screen } from '@/components/ui';
import { useTheme } from '@/constants/theme';

const services = [
  {
    title: 'Front-end development',
    body: 'I craft high-performance interfaces that feel modern, responsive, and conversion-focused.',
  },
  {
    title: 'Web design',
    body: 'I design fast, clean, user-friendly experiences tailored to product goals and audience behavior.',
  },
  {
    title: 'UX design',
    body: 'I think through product experience, clarity, flow, and usability to support better decisions.',
  },
  {
    title: 'Maintenance',
    body: 'I help maintain and improve existing products, fix issues, and ship incremental product upgrades.',
  },
  {
    title: 'Time management',
    body: 'I organize work efficiently and keep projects moving with a clear delivery mindset.',
  },
];

export default function Services() {
  const t = useTheme();

  return (
    <Screen>
      <Heading sub="The kinds of product and engineering work I can help deliver.">Services</Heading>
      {services.map((service) => (
        <Card key={service.title}>
          <Text style={{ color: t.text, fontWeight: '800', fontSize: 20, marginBottom: 8 }}>{service.title}</Text>
          <Text style={{ color: t.muted, fontSize: 15, lineHeight: 24 }}>{service.body}</Text>
        </Card>
      ))}
    </Screen>
  );
}
