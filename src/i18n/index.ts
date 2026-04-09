import type { Translations } from './schema';
import en from './en';
import es from './es';
import ru from './ru';
import ja from './ja';
import ko from './ko';

const translations: Record<string, Translations> = { en, es, ru, ja, ko };

export function useTranslations(locale: string | undefined): Translations {
  return translations[locale ?? 'en'] ?? translations['en'];
}

export const SUPPORTED_LOCALES = ['en', 'es', 'ru', 'ja', 'ko'] as const;
export type SupportedLocale = typeof SUPPORTED_LOCALES[number];

export const LOCALE_LABELS: Record<SupportedLocale, string> = {
  en: 'English',
  es: 'Español',
  ru: 'Русский',
  ja: '日本語',
  ko: '한국어',
};
