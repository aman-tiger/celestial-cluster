# Borchani — celestial-cluster (Astro Site)

## Stack
- **Framework**: Astro 5 (static output)
- **Styling**: Tailwind CSS (no base styles)
- **Content**: MDX + Markdown in `src/data/post/`
- **Icons**: astro-icon (tabler)
- **SEO**: @astrolib/seo

## CRITICAL: All blog content MUST use Astro + MDX only
- Never suggest React/Next.js/WordPress for content pages
- All articles go in `src/data/post/` as `.mdx` files
- Use Astro content collections (defined in `src/content/config.ts`)
- Follow the exact frontmatter schema below

---

## Frontmatter Schema (required for every article)

```yaml
---
publishDate: 2025-01-01T00:00:00Z   # ISO date, required
updateDate: 2025-06-01T00:00:00Z    # Update date (important for freshness signals)
title: "Article Title"               # 50-60 chars, include primary keyword
excerpt: "Meta description text"     # 140-160 chars, include keyword + value prop
image: https://images.unsplash.com/... # 1200x630, always include
category: "Comparisons"              # One of: Comparisons, Guides, Tools, FAQ, Templates, Use Cases, Blog
tags:
  - primary keyword
  - secondary keyword
  - brand keyword (borchani)
author: "Zhassulan Baigozha"
metadata:
  canonical: https://borchani.com/slug
  robots:
    index: true
    follow: true
  description: "..."                 # Overrides excerpt if different
  openGraph:
    type: article
    images:
      - url: https://...
        width: 1200
        height: 630
---
```

---

## Author
- All articles: `author: "Zhassulan Baigozha"` — never change this

## Related Articles (Internal Linking)
- Every article MUST have 5 related article links at the bottom
- Add a `## Related Articles` section at the end with 5 manual links to other relevant posts
- Format: `- [Article Title](/slug)` — pick articles from the same block or adjacent blocks
- Also include 2-3 inline contextual links inside the body text
- Use descriptive anchor text, never "click here" or "read more"

---

## SEO Best Practices (50+ rules — follow always)

### On-Page SEO
1. **H1 = exactly one per page** — contains primary keyword naturally
2. **Title tag 50-60 chars** — keyword first, brand last: "Cursor Alternative | Borchani"
3. **Meta description 140-160 chars** — includes keyword + CTA verb ("Discover", "Compare", "Build")
4. **URL slugs** — lowercase, hyphens, keyword-first: `/cursor-alternative` not `/alternative-to-cursor`
5. **H2s every 300-500 words** — descriptive, include secondary keywords
6. **H3s for sub-sections** — never skip levels (H2 → H4 is wrong)
7. **First paragraph contains H1 keyword** — within first 100 words
8. **Image alt text** — REQUIRED on every image: descriptive + keyword where natural, never keyword-stuffed, never empty
9. **Internal links** — minimum 5 per article (use `<RelatedArticles />` component at bottom + inline links in body), use descriptive anchor text
10. **External links** — link to authoritative sources (GitHub, official docs), opens in new tab
11. **Canonical URL** — always set to avoid duplicate content
12. **robots: index: true** — always explicit
13. **Word count** — minimum: FAQ 800w, Guides 2000w, Comparisons 2500w, Glossary 1500w
14. **Reading time** — auto-calculated via remark plugin, target 5-15 min
15. **Keyword density** — 1-2% for primary, mention naturally not forcibly

### Content Structure (AEO — Answer Engine Optimization)
16. **Answer the H1 question in first 2 sentences** — for featured snippets
17. **TL;DR box after H1** — 2-3 bullet summary for AI answers (Perplexity, ChatGPT)
18. **FAQ section at end** — minimum 4 Q&A pairs, use FAQPage schema
19. **Comparison tables** — use markdown tables for vs/comparison articles
20. **Step-by-step numbered lists** — for how-to content (helps Google rich results)
21. **Definition boxes** — for glossary/dictionary terms (blockquote or callout)
22. **Scannable structure** — every section must have clear H2/H3 header
23. **Short intro** — 2-3 sentences max before first H2
24. **Conclusion with CTA** — last section always links to Borchani signup
25. **Code blocks** — for technical articles, use fenced code blocks with language tag

### Schema Markup (in MDX using JSON-LD)
26. **Article schema** — every blog post (author, datePublished, dateModified)
27. **FAQPage schema** — every article with FAQ section
28. **HowTo schema** — for step-by-step guides
29. **Product schema** — for template/tool pages
30. **BreadcrumbList schema** — for category hierarchy

### GEO (Generative Engine Optimization — for AI search)
31. **llms.txt file** — keep updated with key pages summary
32. **Clear brand mentions** — "Borchani" in first paragraph of every article
33. **Entity consistency** — always spell "Borchani" the same way
34. **Structured facts** — pricing, features as scannable lists (AI loves bullet points)
35. **Comparison tables** — AI engines extract these for comparisons
36. **Direct answers** — state conclusions clearly: "Borchani is better for X because..."
37. **Date signals** — updateDate field keeps content fresh in AI indexes
38. **Author entity** — consistent author name improves E-E-A-T
39. **Cite sources** — link to official docs increases trust score for AI
40. **Use exact keywords users type** — "how to build app without coding" not "application development methodology"

### Technical SEO
41. **Sitemap** — auto-generated by @astrojs/sitemap, ensure all posts included
42. **No orphan pages** — every article linked from at least one category/index page
43. **Image optimization** — always use Astro Image component or external CDN URL
44. **Page speed** — Astro static = fast by default, never add client-side JS to blog posts
45. **Mobile-first** — Tailwind responsive classes, test on mobile viewport
46. **OG tags** — every post needs og:image (1200x630), og:type=article
47. **Twitter card** — summary_large_image for all posts
48. **RSS feed** — exists at /rss.xml, keep updated
49. **robots.txt** — allow all crawlers for blog posts
50. **Hreflang** — when adding i18n, add hreflang tags per locale

---

## Article Categories & URL Patterns

| Block | Category | URL Pattern | Min Words |
|-------|----------|-------------|-----------|
| 01_alternatives | Comparisons | `/[tool]-alternative` | 2500 |
| 02_vs | Comparisons | `/[tool-a]-vs-[tool-b]` | 2500 |
| 03_solutions | Guides | `/best-[tool]-for-[use-case]` | 2000 |
| 04_build | Guides | `/how-to-build-[thing]` | 2000 |
| 05_for | Guides | `/best-app-for-[use-case]` | 1500 |
| 06_use-cases | Use Cases | `/[tool]-use-cases` | 1500 |
| 07_guides | Guides | `/guide-[topic]` | 2000 |
| 08_templates | Templates | `/[type]-template` | 1500 |
| 09_prompts | Guides | `/[topic]-prompts` | 1500 |
| 10_blog | Blog | `/blog/[topic]` | 1500 |
| 11_faq | FAQ | `/what-is-[term]` | 800 |
| 12_dictionary | FAQ | `/[term]-definition` | 1000 |
| 14_tools | Tools | `/[tool-name]-generator` | 1000 |
| 16_paywall | Guides | `/how-to-add-paywall` | 1500 |
| 17_landing | Templates | `/landing-page-[topic]` | 1500 |
| 18_pricing | Guides | `/saas-pricing-[topic]` | 2000 |
| 19_auth | Guides | `/[topic]-authentication` | 1500 |
| 21_affiliate | Blog | `/affiliate-[topic]` | 1500 |

---

## Content Files Location
- Blog posts: `src/data/post/`
- SEO keyword data: `/Users/amanyessen/NEW/SEO Borchani/` (outside this repo)
- Prompts: `/Users/amanyessen/NEW/SEO Borchani/_prompts/`
- Competitor examples: `/Users/amanyessen/NEW/competitors with expamles site /`

## Brand Voice
- Direct, technical, developer-first tone
- No fluff, no "In today's fast-paced world..."
- Use "you" not "users"
- Mention Borchani naturally, not as forced ads
- Always end with concrete CTA: "Build it with Borchani → borchani.com"
