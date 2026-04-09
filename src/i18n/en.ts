import type { Translations } from './schema';

const en: Translations = {
  meta: {
    title: 'Borchani — Build Full-Stack Apps with AI',
    description:
      'Borchani turns your ideas into production-ready web applications. Describe what you want to build, and AI generates clean React + TypeScript + Tailwind code with live preview and one-click deployment.',
  },
  nav: {
    product: 'Product',
    features: 'Features',
    howItWorks: 'How it works',
    whatWeBuild: 'What we build',
    caseStudies: 'Case Studies',
    pricing: 'Pricing',
    resources: 'Resources',
    blog: 'Blog',
    about: 'About',
    contact: 'Contact',
    getStarted: 'Get Started Free',
  },
  footer: {
    productTitle: 'Product',
    developersTitle: 'Developers',
    supportTitle: 'Support',
    companyTitle: 'Company',
    features: 'Features',
    howItWorks: 'How it works',
    pricing: 'Pricing',
    changelog: 'Changelog',
    roadmap: 'Roadmap',
    documentation: 'Documentation',
    apiReference: 'API Reference',
    sdk: 'SDK',
    examples: 'Examples',
    helpCenter: 'Help Center',
    community: 'Community',
    status: 'Status',
    contactUs: 'Contact Us',
    about: 'About',
    blog: 'Blog',
    careers: 'Careers',
    privacyPolicy: 'Privacy Policy',
    termsOfService: 'Terms of Service',
    terms: 'Terms',
    copyright: '&copy; 2025 Borchani. All rights reserved.',
  },
  hero: {
    titleLine1: 'Turn any idea into a',
    titleHighlight: 'deployed web app',
    titleLine3: 'in minutes',
    subtitleDesktop:
      '<strong>Borchani</strong> uses AI to generate production-quality full-stack applications from a plain English description. No boilerplate, no config hell — just code that works.',
    subtitleMobile: 'AI-powered app builder. Describe it. Ship it.',
    ctaPrimary: 'Start Building Free',
    ctaSecondary: 'See a Demo',
    signInGoogle: 'Sign in with Google',
    signInComingSoon: 'Coming soon',
  },
  note: {
    trusted: 'Trusted by developers:',
    stats: '10,000+ apps built &nbsp;·&nbsp; 50+ UI components &nbsp;·&nbsp; React 19 + TypeScript + Tailwind',
  },
  features: {
    tagline: 'Why Borchani',
    title: 'Everything you need to ship faster',
    subtitle: 'From first idea to live URL — Borchani handles the heavy lifting so you can focus on what matters.',
    aiCode: {
      title: 'AI Code Generation',
      description:
        'Describe your app in plain English. Borchani writes clean, idiomatic React + TypeScript with automatic error detection and self-correction.',
    },
    livePreview: {
      title: 'Live Preview Sandbox',
      description:
        'Every build runs instantly in an isolated sandbox. See the real app — not a mockup — as the AI generates each component.',
    },
    iteration: {
      title: 'Conversational Iteration',
      description:
        'Refine your app through chat. "Make the sidebar collapsible", "Add dark mode", "Swap the chart library" — Borchani keeps full context across turns.',
    },
    stack: {
      title: 'Production-Grade Stack',
      description:
        'React 19, TypeScript, Vite, Tailwind CSS, and shadcn/ui out of the box. Every generated project follows best practices from day one.',
    },
    deploy: {
      title: 'One-Click Deploy',
      description:
        'Push to the cloud or export directly to GitHub with a single click. Your generated code is yours — no lock-in, no surprises.',
    },
    security: {
      title: 'Enterprise-Grade Security',
      description:
        'End-to-end encryption for API keys, isolated execution containers, rate limiting, and SOC 2-ready infrastructure.',
    },
  },
  steps: {
    title: 'From idea to deployed app in 3 steps',
    step1: {
      title: 'Step 1: <span class="font-medium">Describe your app</span>',
      description:
        'Type what you want to build in plain English. "A task manager with drag-and-drop, tags, and a dark mode toggle." No wireframes required.',
    },
    step2: {
      title: 'Step 2: <span class="font-medium">Watch AI build it</span>',
      description:
        'Borchani generates the full codebase phase by phase, showing a live preview as each component comes to life. Spot issues early and steer the build through chat.',
    },
    step3: {
      title: 'Step 3: <span class="font-medium">Refine and deploy</span>',
      description:
        'Iterate with follow-up messages, then deploy to the cloud or export clean code to your GitHub repo — ready for production.',
    },
    done: 'Done!',
  },
  techStack: {
    tagline: 'Technology',
    title: 'A stack built for 2025',
    contentTitle: 'Production-ready from line one',
    contentSubtitle:
      'No legacy patterns, no outdated dependencies — every app Borchani generates is built on the same stack top engineers use today.',
    modern: {
      title: 'Modern frontend',
      description:
        'React 19, TypeScript, Vite, Tailwind CSS v4, React Router v7, and the full shadcn/ui component library — latest stable versions, every time.',
    },
    edge: {
      title: 'Edge-ready backend',
      description:
        'Generated APIs run on a globally distributed, serverless edge network. Sub-50 ms cold starts, unlimited scale, zero DevOps.',
    },
    realtime: {
      title: 'Real-time by default',
      description:
        'WebSocket support baked in. Build collaborative tools, live dashboards, and chat apps without writing a single line of socket code manually.',
    },
  },
  sdk: {
    contentTitle: 'Build programmatically with the SDK',
    typed: {
      title: 'Fully typed SDK',
      description:
        'First-class TypeScript support with autocompletion, inline docs, and strict type safety across every method.',
    },
    session: {
      title: 'Session management',
      description:
        'Start a build, wait for the deployable state, stream logs, and query app state — all from a single fluent API.',
    },
    cicd: {
      title: 'CI/CD ready',
      description:
        'Integrate Borchani into your existing pipelines. Generate apps programmatically, run tests, and deploy automatically.',
    },
  },
  useCases: {
    tagline: 'Use cases',
    title: 'What you can build with Borchani',
    subtitle: 'If you can describe it, Borchani can build it. Here are some popular starting points.',
    tasks: {
      title: 'Task & Project Tools',
      description: 'Kanban boards, to-do lists, project trackers — with drag-and-drop, labels, and due dates.',
    },
    dashboards: {
      title: 'Dashboards & Analytics',
      description: 'Interactive charts, filterable tables, KPI cards, and real-time data feeds.',
    },
    ecommerce: {
      title: 'E-Commerce Interfaces',
      description: 'Product catalogs, shopping carts, checkout flows, and order management UIs.',
    },
    internal: {
      title: 'Internal Tools',
      description: 'Admin panels, CRUD interfaces, approval workflows, and data entry forms.',
    },
    ai: {
      title: 'AI-Powered Apps',
      description: 'Chat interfaces, image generators, prompt playgrounds, and AI assistant UIs.',
    },
    saas: {
      title: 'SaaS Prototypes',
      description: 'Turn an idea into a clickable, working MVP in hours — not weeks.',
    },
    social: {
      title: 'Social & Community',
      description: 'Feed UIs, comment threads, messaging apps, and real-time collaboration tools.',
    },
    content: {
      title: 'Content Platforms',
      description: 'Blog engines, portfolio sites, documentation hubs, and CMS-connected frontends.',
    },
    productivity: {
      title: 'Productivity Apps',
      description: 'Habit trackers, timers, note-takers, and personal finance managers.',
    },
  },
  stats: {
    appsBuilt: 'Apps Built',
    developers: 'Developers',
    components: 'UI Components',
    deployTime: 'Avg. Time to Deploy',
    appsAmount: '10K+',
    devsAmount: '3K+',
    componentsAmount: '50+',
    deployAmount: '< 5 min',
  },
  faq: {
    tagline: 'FAQ',
    title: 'Frequently Asked Questions',
    subtitle: 'Everything you need to know about Borchani before you start building.',
    q1: {
      title: 'What is Borchani?',
      description:
        'Borchani is an AI-powered app builder. You describe what you want to create in plain English, and Borchani generates a complete, production-ready full-stack application — React frontend, TypeScript, Tailwind CSS — with a live preview and one-click deployment.',
    },
    q2: {
      title: 'Do I need to know how to code?',
      description:
        'No. Borchani is designed for both developers who want to move faster and non-technical users who want to build without learning to code. You can use Borchani entirely through natural language conversation.',
    },
    q3: {
      title: 'What tech stack do generated apps use?',
      description:
        'All apps are built with React 19, TypeScript, Vite, Tailwind CSS, and shadcn/ui components. The stack is modern, well-documented, and widely adopted — so if you want to extend or customize the code yourself, you can.',
    },
    q4: {
      title: 'Can I export and own the code?',
      description:
        'Yes. Every app you build belongs to you. Export the full source code to GitHub at any time, or download it as a ZIP. There are no platform fees on the code itself — it is yours to deploy anywhere.',
    },
    q5: {
      title: 'How secure is Borchani?',
      description:
        'We take security seriously. API keys are encrypted end-to-end, code runs in isolated containers that are torn down after each session, and our infrastructure is built on SOC 2-ready cloud services. We never store your API keys in plaintext.',
    },
    q6: {
      title: 'What happens if the AI makes a mistake?',
      description:
        'Borchani includes automatic error detection and self-correction. If the generated code has a bug, the AI identifies it, explains what went wrong, and fixes it — all without you having to intervene. You can also guide corrections through the chat.',
    },
    q7: {
      title: 'Is there a free plan?',
      description:
        'Yes. You can start building for free with a generous monthly quota. Paid plans unlock higher limits, priority queue access, team collaboration features, and advanced deployment options.',
    },
    q8: {
      title: 'Can I use Borchani for commercial projects?',
      description:
        'Absolutely. All plans — including the free tier — allow you to use generated applications for commercial purposes. The code is yours and carries no restrictions on how you use or distribute it.',
    },
  },
  pricing: {
    title: 'Simple, transparent pricing',
    subtitle: 'Start free. Scale when you\'re ready. No hidden fees.',
    starterTitle: 'Starter',
    starterSubtitle: 'For solo builders and side projects',
    starterCta: 'Get Starter',
    proTitle: 'Pro',
    proSubtitle: 'For developers who ship every week',
    proCta: 'Get Pro',
    proRibbon: 'Most Popular',
    businessTitle: 'Business',
    businessSubtitle: 'For teams building products together',
    businessCta: 'Get Business',
    perMonth: '/ month',
  },
  contact: {
    title: 'Have questions? We\'re here.',
    subtitle: 'Our team is ready to help you get started or answer any questions before you sign up.',
    cta: 'Contact us',
    email: 'Email us',
    emailHandle: 'hello@borchani.com',
    follow: 'Follow us',
    followHandle: '@borchani',
    discord: 'Join Discord',
    discordHandle: 'discord.gg/borchani',
  },
  blog: {
    title: 'From the Borchani blog',
    subtitle:
      'Tips, tutorials, and deep dives on AI-powered development, prompt engineering, and shipping faster with Borchani.',
  },
  cta: {
    titleLine1: 'Ready to build your next app',
    titleHighlight: '10× faster?',
    subtitle:
      'Join thousands of developers and founders who ship with Borchani.<br class="hidden md:inline" />No credit card required to get started.',
    primary: 'Start Building Free',
    secondary: 'View Pricing',
  },
  languageSwitcher: {
    label: 'Language',
  },
};

export default en;
