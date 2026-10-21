import { Linking, Platform } from 'react-native';

import { profile } from '@/data/profile';

/** Opens a web link in a new tab on web, or the system handler on phones. */
export function openLink(url: string) {
  if (Platform.OS === 'web') {
    window.open(url, '_blank', 'noopener,noreferrer');
  } else {
    Linking.openURL(url).catch(() => {});
  }
}

/** Opens Gmail compose directly when possible, with a web fallback. */
export function openGmail(
  subject = 'Hello Siva, I saw your portfolio',
  body = ''
) {
  const recipient = encodeURIComponent(profile.email);
  const subjectText = encodeURIComponent(subject);
  const bodyText = encodeURIComponent(body);
  const gmailUrl = `googlegmail://co?to=${recipient}&subject=${subjectText}&body=${bodyText}`;
  const webUrl = `https://mail.google.com/mail/?view=cm&fs=1&to=${recipient}&su=${subjectText}&body=${bodyText}`;

  if (Platform.OS === 'web') {
    openLink(webUrl);
    return;
  }

  Linking.canOpenURL(gmailUrl)
    .then((supported) => {
      if (supported) {
        return Linking.openURL(gmailUrl);
      }
      return Linking.openURL(webUrl);
    })
    .catch(() => {
      openLink(webUrl);
    });
}
