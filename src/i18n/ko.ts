import type { Translations } from './schema';

const ko: Translations = {
  meta: {
    title: 'Borchani — AI로 풀스택 앱을 구축하세요',
    description:
      'Borchani는 아이디어를 프로덕션 준비 완료 웹 애플리케이션으로 전환합니다. 만들고 싶은 것을 설명하면 AI가 라이브 프리뷰와 원클릭 배포가 포함된 깔끔한 React + TypeScript + Tailwind 코드를 생성합니다.',
  },
  nav: {
    product: '제품',
    features: '기능',
    howItWorks: '작동 방식',
    whatWeBuild: '구축 가능한 것',
    caseStudies: '사례 연구',
    pricing: '요금',
    resources: '리소스',
    blog: '블로그',
    about: '소개',
    contact: '문의',
    getStarted: '무료로 시작하기',
  },
  footer: {
    productTitle: '제품',
    developersTitle: '개발자',
    supportTitle: '지원',
    companyTitle: '회사',
    features: '기능',
    howItWorks: '작동 방식',
    pricing: '요금',
    changelog: '변경 기록',
    roadmap: '로드맵',
    documentation: '문서',
    apiReference: 'API 레퍼런스',
    sdk: 'SDK',
    examples: '예제',
    helpCenter: '도움말 센터',
    community: '커뮤니티',
    status: '상태',
    contactUs: '문의하기',
    about: '소개',
    blog: '블로그',
    careers: '채용',
    privacyPolicy: '개인정보 처리방침',
    termsOfService: '이용 약관',
    terms: '약관',
    copyright: '&copy; 2026 Borchani. All rights reserved.',
  },
  hero: {
    titleLine1: '어떤 아이디어든',
    titleHighlight: '배포된 웹 앱',
    titleLine3: '으로 몇 분 만에',
    subtitleDesktop:
      '<strong>Borchani</strong>는 AI를 사용해 일반 텍스트 설명에서 프로덕션 품질의 풀스택 애플리케이션을 생성합니다. 보일러플레이트 없음, 설정 지옥 없음 — 작동하는 코드만.',
    subtitleMobile: 'AI 기반 앱 빌더. 설명하세요. 배포하세요.',
    ctaPrimary: '무료로 구축 시작',
    ctaSecondary: '데모 보기',
    signInGoogle: 'Google로 로그인',
    signInComingSoon: '출시 예정',
  },
  note: {
    trusted: '개발자들이 신뢰합니다:',
    stats: '10,000개 이상의 앱 구축 &nbsp;·&nbsp; 50개 이상의 UI 컴포넌트 &nbsp;·&nbsp; React 19 + TypeScript + Tailwind',
  },
  features: {
    tagline: 'Borchani를 선택하는 이유',
    title: '더 빠르게 배포하는 데 필요한 모든 것',
    subtitle: '첫 아이디어부터 라이브 URL까지 — Borchani가 힘든 작업을 처리하므로 중요한 것에 집중할 수 있습니다.',
    aiCode: {
      title: 'AI 코드 생성',
      description:
        '일반 언어로 앱을 설명하세요. Borchani가 자동 오류 감지 및 자가 수정 기능이 포함된 깔끔하고 관용적인 React + TypeScript를 작성합니다.',
    },
    livePreview: {
      title: '라이브 프리뷰 샌드박스',
      description:
        '모든 빌드는 격리된 샌드박스에서 즉시 실행됩니다. AI가 각 컴포넌트를 생성하는 동안 목업이 아닌 실제 앱을 확인하세요.',
    },
    iteration: {
      title: '대화형 반복',
      description:
        '채팅을 통해 앱을 개선하세요. "사이드바를 접을 수 있게 해줘", "다크 모드 추가해줘", "차트 라이브러리 바꿔줘" — Borchani가 전체 대화에 걸쳐 완전한 컨텍스트를 유지합니다.',
    },
    stack: {
      title: '프로덕션 수준 스택',
      description:
        'React 19, TypeScript, Vite, Tailwind CSS, shadcn/ui가 바로 사용 가능합니다. 생성되는 모든 프로젝트는 첫날부터 모범 사례를 따릅니다.',
    },
    deploy: {
      title: '원클릭 배포',
      description:
        '클릭 한 번으로 클라우드에 푸시하거나 GitHub에 직접 내보낼 수 있습니다. 생성된 코드는 여러분의 것 — 잠금 없음, 놀라움 없음.',
    },
    security: {
      title: '엔터프라이즈급 보안',
      description:
        'API 키의 엔드투엔드 암호화, 격리된 실행 컨테이너, 속도 제한, SOC 2 준비 인프라.',
    },
  },
  steps: {
    title: '3단계로 아이디어에서 배포된 앱으로',
    step1: {
      title: '1단계: <span class="font-medium">앱을 설명하세요</span>',
      description:
        '만들고 싶은 것을 일반 언어로 입력하세요. "드래그 앤 드롭, 태그, 다크 모드 토글이 있는 작업 관리자." 와이어프레임이 필요 없습니다.',
    },
    step2: {
      title: '2단계: <span class="font-medium">AI가 구축하는 것을 보세요</span>',
      description:
        'Borchani가 각 컴포넌트가 완성될 때마다 라이브 프리뷰를 보여주면서 전체 코드베이스를 단계별로 생성합니다. 문제를 조기에 발견하고 채팅을 통해 빌드를 이끌어 가세요.',
    },
    step3: {
      title: '3단계: <span class="font-medium">개선하고 배포하세요</span>',
      description:
        '후속 메시지로 반복하고, 클라우드에 배포하거나 GitHub 저장소로 깔끔한 코드를 내보내세요 — 프로덕션 준비 완료.',
    },
    done: '완료!',
  },
  techStack: {
    tagline: '기술',
    title: '2025년을 위해 구축된 스택',
    contentTitle: '첫 번째 줄부터 프로덕션 준비 완료',
    contentSubtitle:
      '레거시 패턴 없음, 오래된 의존성 없음 — Borchani가 생성하는 모든 앱은 오늘날 최고의 엔지니어들이 사용하는 동일한 스택으로 구축됩니다.',
    modern: {
      title: '모던 프론트엔드',
      description:
        'React 19, TypeScript, Vite, Tailwind CSS v4, React Router v7, 전체 shadcn/ui 컴포넌트 라이브러리 — 항상 최신 안정 버전.',
    },
    edge: {
      title: '엣지 준비 백엔드',
      description:
        '생성된 API는 전 세계적으로 분산된 서버리스 엣지 네트워크에서 실행됩니다. 콜드 스타트 50ms 미만, 무제한 확장, DevOps 제로.',
    },
    realtime: {
      title: '기본으로 실시간',
      description:
        'WebSocket 지원이 내장되어 있습니다. 소켓 코드를 한 줄도 수동으로 작성하지 않고 협업 도구, 라이브 대시보드, 채팅 앱을 구축하세요.',
    },
  },
  sdk: {
    contentTitle: 'SDK로 프로그래밍 방식으로 구축',
    typed: {
      title: '완전히 타입화된 SDK',
      description:
        '자동 완성, 인라인 문서, 모든 메서드에 걸친 엄격한 타입 안전성을 갖춘 최고 수준의 TypeScript 지원.',
    },
    session: {
      title: '세션 관리',
      description:
        '빌드 시작, 배포 가능 상태 대기, 로그 스트리밍, 앱 상태 쿼리 — 단일 fluent API에서 모두 가능.',
    },
    cicd: {
      title: 'CI/CD 준비 완료',
      description:
        'Borchani를 기존 파이프라인에 통합하세요. 프로그래밍 방식으로 앱을 생성하고, 테스트를 실행하고, 자동으로 배포하세요.',
    },
  },
  useCases: {
    tagline: '사용 사례',
    title: 'Borchani로 구축할 수 있는 것',
    subtitle: '설명할 수 있다면 Borchani가 구축할 수 있습니다. 인기 있는 시작점 몇 가지를 소개합니다.',
    tasks: {
      title: '작업 및 프로젝트 도구',
      description: '칸반 보드, 할 일 목록, 프로젝트 트래커 — 드래그 앤 드롭, 레이블, 마감일 포함.',
    },
    dashboards: {
      title: '대시보드 및 분석',
      description: '인터랙티브 차트, 필터링 가능한 테이블, KPI 카드, 실시간 데이터 피드.',
    },
    ecommerce: {
      title: '이커머스 인터페이스',
      description: '상품 카탈로그, 장바구니, 결제 플로우, 주문 관리 UI.',
    },
    internal: {
      title: '내부 도구',
      description: '관리 패널, CRUD 인터페이스, 승인 워크플로우, 데이터 입력 양식.',
    },
    ai: {
      title: 'AI 기반 앱',
      description: '채팅 인터페이스, 이미지 생성기, 프롬프트 플레이그라운드, AI 어시스턴트 UI.',
    },
    saas: {
      title: 'SaaS 프로토타입',
      description: '몇 주가 아닌 몇 시간 만에 아이디어를 클릭 가능한 작동하는 MVP로 전환하세요.',
    },
    social: {
      title: '소셜 및 커뮤니티',
      description: '피드 UI, 댓글 스레드, 메시징 앱, 실시간 협업 도구.',
    },
    content: {
      title: '콘텐츠 플랫폼',
      description: '블로그 엔진, 포트폴리오 사이트, 문서 허브, CMS 연결 프론트엔드.',
    },
    productivity: {
      title: '생산성 앱',
      description: '습관 트래커, 타이머, 노트 앱, 개인 재무 관리 앱.',
    },
  },
  stats: {
    appsBuilt: '구축된 앱',
    developers: '개발자',
    components: 'UI 컴포넌트',
    deployTime: '평균 배포 시간',
    appsAmount: '10K+',
    devsAmount: '3K+',
    componentsAmount: '50+',
    deployAmount: '5분 미만',
  },
  faq: {
    tagline: 'FAQ',
    title: '자주 묻는 질문',
    subtitle: '구축을 시작하기 전에 Borchani에 대해 알아야 할 모든 것.',
    q1: {
      title: 'Borchani란 무엇인가요?',
      description:
        'Borchani는 AI 기반 앱 빌더입니다. 만들고 싶은 것을 일반 언어로 설명하면, Borchani가 라이브 프리뷰와 원클릭 배포가 포함된 완전한 프로덕션 준비 완료 풀스택 애플리케이션 — React 프론트엔드, TypeScript, Tailwind CSS — 을 생성합니다.',
    },
    q2: {
      title: '코딩을 알아야 하나요?',
      description:
        '아니요. Borchani는 더 빠르게 움직이고 싶은 개발자와 코딩을 배우지 않고 구축하고 싶은 비기술 사용자 모두를 위해 설계되었습니다. Borchani는 완전히 자연어 대화를 통해 사용할 수 있습니다.',
    },
    q3: {
      title: '생성된 앱은 어떤 기술 스택을 사용하나요?',
      description:
        '모든 앱은 React 19, TypeScript, Vite, Tailwind CSS, shadcn/ui 컴포넌트로 구축됩니다. 스택은 현대적이고, 잘 문서화되어 있으며, 널리 채택되어 있습니다 — 코드를 직접 확장하거나 커스터마이즈하고 싶다면 언제든지 가능합니다.',
    },
    q4: {
      title: '코드를 내보내고 소유할 수 있나요?',
      description:
        '네. 구축한 모든 앱은 여러분의 것입니다. 언제든지 전체 소스 코드를 GitHub로 내보내거나 ZIP으로 다운로드하세요. 코드 자체에 대한 플랫폼 수수료는 없습니다 — 어디서든 배포할 수 있습니다.',
    },
    q5: {
      title: 'Borchani는 얼마나 안전한가요?',
      description:
        '보안을 진지하게 생각합니다. API 키는 엔드투엔드로 암호화되고, 코드는 각 세션 후 폐기되는 격리된 컨테이너에서 실행되며, 인프라는 SOC 2 준비 클라우드 서비스로 구축됩니다. API 키를 평문으로 저장하지 않습니다.',
    },
    q6: {
      title: 'AI가 실수를 하면 어떻게 되나요?',
      description:
        'Borchani에는 자동 오류 감지 및 자가 수정이 포함되어 있습니다. 생성된 코드에 버그가 있으면 AI가 이를 식별하고, 무엇이 잘못되었는지 설명하고, 수정합니다 — 여러분이 개입할 필요 없이. 채팅을 통해 수정을 안내할 수도 있습니다.',
    },
    q7: {
      title: '무료 플랜이 있나요?',
      description:
        '네. 넉넉한 월별 할당량으로 무료로 구축을 시작할 수 있습니다. 유료 플랜은 더 높은 한도, 우선 대기열 접근, 팀 협업 기능, 고급 배포 옵션을 제공합니다.',
    },
    q8: {
      title: 'Borchani를 상업 프로젝트에 사용할 수 있나요?',
      description:
        '물론입니다. 무료 티어를 포함한 모든 플랜에서 생성된 애플리케이션을 상업 목적으로 사용할 수 있습니다. 코드는 여러분의 것이며 사용 또는 배포 방법에 제한이 없습니다.',
    },
  },
  pricing: {
    title: '간단하고 투명한 요금',
    subtitle: '무료로 시작하세요. 준비되면 확장하세요. 숨겨진 수수료 없음.',
    starterTitle: 'Starter',
    starterSubtitle: '개인 빌더와 사이드 프로젝트용',
    starterCta: 'Starter 시작하기',
    proTitle: 'Pro',
    proSubtitle: '매주 배포하는 개발자용',
    proCta: 'Pro 시작하기',
    proRibbon: '가장 인기',
    businessTitle: 'Business',
    businessSubtitle: '함께 제품을 구축하는 팀용',
    businessCta: 'Business 시작하기',
    perMonth: '/ 월',
  },
  contact: {
    title: '질문이 있으신가요? 여기 있습니다.',
    subtitle: '저희 팀이 시작을 돕거나 가입 전 궁금한 점에 답변할 준비가 되어 있습니다.',
    cta: '문의하기',
    email: '이메일 보내기',
    emailHandle: 'hello@borchani.com',
    follow: '팔로우하기',
    followHandle: '@borchani',
    discord: 'Discord 참여',
    discordHandle: 'discord.gg/borchani',
  },
  blog: {
    title: 'Borchani 블로그에서',
    subtitle:
      'AI 기반 개발, 프롬프트 엔지니어링, Borchani로 더 빠르게 배포하는 팁, 튜토리얼, 심층 분석.',
  },
  cta: {
    titleLine1: '다음 앱을',
    titleHighlight: '10배 빠르게',
    subtitle:
      'Borchani로 배포하는 수천 명의 개발자와 창업자들과 함께하세요.<br class="hidden md:inline" />시작하는 데 신용카드가 필요 없습니다.',
    primary: '무료로 구축 시작',
    secondary: '요금 보기',
  },
  languageSwitcher: {
    label: '언어',
  },
};

export default ko;
