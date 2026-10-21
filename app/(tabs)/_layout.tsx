import { SymbolView } from 'expo-symbols';
import { Tabs, useRouter } from 'expo-router';
import { Image, Pressable, Text, View } from 'react-native';

import { useTheme } from '@/constants/theme';
import { profile } from '@/data/profile';
import { openGmail, openLink } from '@/lib/links';

const navItems: any[] = [
  { label: 'Home', path: '/', icon: { ios: 'house', android: 'home', web: 'home' } },
  { label: 'About', path: '/about', icon: { ios: 'person', android: 'person', web: 'person' } },
  { label: 'Portfolio', path: '/projects', icon: { ios: 'folder', android: 'folder', web: 'folder' } },
  { label: 'Skills', path: '/skills', icon: { ios: 'star', android: 'star', web: 'star' } },
  { label: 'Services', path: '/services', icon: { ios: 'briefcase', android: 'work', web: 'briefcase' } },
  { label: 'Contact', path: '/contact', icon: { ios: 'envelope', android: 'mail', web: 'mail' } },
];

export default function TabLayout() {
  const t = useTheme();
  const router = useRouter();

  return (
    <View style={{ flex: 1, flexDirection: 'row', backgroundColor: t.bg }}>
      <View
        style={{
          width: 300,
          backgroundColor: '#050A0F',
          paddingTop: 36,
          paddingHorizontal: 18,
          paddingBottom: 18,
          borderRightWidth: 1,
          borderRightColor: 'rgba(255,255,255,0.08)',
        }}>
        <View style={{ alignItems: 'center', marginBottom: 12 }}>
          <Image
            source={require('@/assets/images/profile-photo.png')}
            style={{
              width: 120,
              height: 120,
              borderRadius: 60,
              borderWidth: 1,
              borderColor: 'rgba(255,255,255,0.14)',
              backgroundColor: '#101922',
            }}
          />
        </View>

        <Text style={{ color: '#F5F7FA', fontSize: 24, fontWeight: '800', marginBottom: 16 }}>
          {profile.displayName}
        </Text>

        <View style={{ flexDirection: 'row', marginBottom: 22, gap: 8 }}>
          <Pressable
            onPress={() => openGmail()}
            style={{
              width: 30,
              height: 30,
              borderRadius: 15,
              backgroundColor: 'rgba(255,255,255,0.04)',
              alignItems: 'center',
              justifyContent: 'center',
              borderWidth: 1,
              borderColor: 'rgba(255,255,255,0.1)',
            }}>
            <Text style={{ color: '#F1F5F9', fontWeight: '800', fontSize: 12 }}>✉</Text>
          </Pressable>

          <Pressable
            onPress={() => openLink(profile.github)}
            style={{
              width: 30,
              height: 30,
              borderRadius: 15,
              backgroundColor: 'rgba(255,255,255,0.04)',
              alignItems: 'center',
              justifyContent: 'center',
              borderWidth: 1,
              borderColor: 'rgba(255,255,255,0.1)',
            }}>
            <Text style={{ color: '#F1F5F9', fontWeight: '800', fontSize: 11 }}>GH</Text>
          </Pressable>

          <Pressable
            onPress={() => openLink(profile.linkedin)}
            style={{
              width: 30,
              height: 30,
              borderRadius: 15,
              backgroundColor: 'rgba(255,255,255,0.04)',
              alignItems: 'center',
              justifyContent: 'center',
              borderWidth: 1,
              borderColor: 'rgba(255,255,255,0.1)',
            }}>
            <Text style={{ color: '#F1F5F9', fontWeight: '800', fontSize: 11 }}>in</Text>
          </Pressable>
        </View>

        <View style={{ gap: 6 }}>
          {navItems.map((item) => (
            <Pressable
              key={item.label}
              onPress={() => router.push(item.path as never)}
              style={({ pressed }) => ({
                opacity: pressed ? 0.8 : 1,
                flexDirection: 'row',
                alignItems: 'center',
                paddingVertical: 12,
                paddingHorizontal: 12,
                borderRadius: 10,
                backgroundColor: item.path === '/' ? 'rgba(125,185,255,0.08)' : 'transparent',
              })}>
              <SymbolView
                name={item.icon}
                tintColor={item.path === '/' ? '#A9D2FF' : '#DDDFE4'}
                size={18}
              />
              <Text
                style={{
                  color: item.path === '/' ? '#A9D2FF' : '#E4E9F0',
                  fontSize: 16,
                  fontWeight: item.path === '/' ? '700' : '500',
                  marginLeft: 10,
                }}>
                {item.label}
              </Text>
            </Pressable>
          ))}
        </View>

        <View style={{ marginTop: 'auto', paddingTop: 18, borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.08)' }}>
          <Text style={{ color: '#D9E1EA', fontSize: 12, fontWeight: '600' }}>
            © {profile.displayName}
          </Text>
        </View>
      </View>

      <View style={{ flex: 1, backgroundColor: '#0B0F13' }}>
        <Tabs
          screenOptions={{
            headerShown: false,
            tabBarStyle: { display: 'none' },
            tabBarShowLabel: false,
            tabBarButton: () => null,
          }}
        >
          <Tabs.Screen name="index" options={{ title: 'Home' }} />
          <Tabs.Screen name="projects" options={{ title: 'Projects' }} />
          <Tabs.Screen name="about" options={{ title: 'About' }} />
          <Tabs.Screen name="skills" options={{ title: 'Skills' }} />
          <Tabs.Screen name="services" options={{ title: 'Services' }} />
          <Tabs.Screen name="contact" options={{ title: 'Contact' }} />
        </Tabs>
      </View>
    </View>
  );
}
