import { getPermalink, getBlogPermalink, getAsset } from './utils/permalinks';
import type { Translations } from './i18n/schema';

export function getHeaderData(t: Translations, locale: string) {
  const prefix = locale === 'en' ? '' : `/${locale}`;
  return {
    links: [
      {
        text: t.nav.product,
        links: [
          { text: t.nav.features, href: `${prefix}/#features` },
          { text: t.nav.howItWorks, href: `${prefix}/#how-it-works` },
          { text: t.nav.whatWeBuild, href: `${prefix}/services` },
          { text: t.nav.caseStudies, href: `${prefix}/case-studies` },
        ],
      },
      {
        text: t.nav.pricing,
        href: `${prefix}/pricing`,
      },
      {
        text: t.nav.resources,
        links: [
          { text: t.nav.blog, href: `${prefix}/blog` },
          { text: t.nav.about, href: `${prefix}/about` },
          { text: t.nav.contact, href: `${prefix}/contact` },
        ],
      },
    ],
    actions: [{ text: t.nav.getStarted, href: 'https://app.borchani.com/signup', target: '_blank' }],
  };
}

export function getFooterData(t: Translations, locale: string = 'en') {
  const prefix = locale === 'en' ? '' : `/${locale}`;
  return {
    links: [
      {
        title: t.footer.productTitle,
        links: [
          { text: t.footer.features, href: `${prefix}/#features` },
          { text: t.footer.howItWorks, href: `${prefix}/#how-it-works` },
          { text: t.footer.pricing, href: `${prefix}/pricing` },
          { text: t.footer.changelog, href: '#' },
          { text: t.footer.roadmap, href: '#' },
        ],
      },
      {
        title: t.footer.developersTitle,
        links: [
          { text: t.footer.documentation, href: '#' },
          { text: t.footer.apiReference, href: '#' },
          { text: t.footer.sdk, href: '#' },
          { text: t.footer.examples, href: '#' },
        ],
      },
      {
        title: t.footer.supportTitle,
        links: [
          { text: t.footer.helpCenter, href: '#' },
          { text: t.footer.community, href: '#' },
          { text: t.footer.status, href: '#' },
          { text: t.footer.contactUs, href: `${prefix}/contact` },
        ],
      },
      {
        title: t.footer.companyTitle,
        links: [
          { text: t.footer.about, href: `${prefix}/about` },
          { text: t.footer.blog, href: `${prefix}/blog` },
          { text: t.footer.careers, href: '#' },
          { text: t.footer.privacyPolicy, href: getPermalink('/privacy') },
          { text: t.footer.termsOfService, href: getPermalink('/terms') },
        ],
      },
    ],
    secondaryLinks: [
      { text: t.footer.terms, href: getPermalink('/terms') },
      { text: t.footer.privacyPolicy, href: getPermalink('/privacy') },
    ],
    socialLinks: [
      { ariaLabel: 'X / Twitter', icon: 'tabler:brand-x', href: 'https://x.com/borchani' },
      { ariaLabel: 'Discord', icon: 'tabler:brand-discord', href: '#' },
      { ariaLabel: 'RSS', icon: 'tabler:rss', href: getAsset('/rss.xml') },
    ],
    footNote: t.footer.copyright,
  };
}

// Backward-compatible English exports (used by any file that hasn't been updated yet)
import en from './i18n/en';
export const headerData = getHeaderData(en, 'en');
export const footerData = getFooterData(en, 'en');
