import React, { useEffect } from 'react';

const assetBase = '/X-Space';

const productImages = {
  hero: `${assetBase}/landing-page-lp_img_1_hero-1x1%20(3).png`,
  closeup: `${assetBase}/landing-page-lp_img_4_detail-1x1%20(1).png`,
  lifestyle: `${assetBase}/landing-page-lp_img_3_lifestyle-1x1%20(2).png`,
  product: `${assetBase}/landing-page-lp_img_2_feature-1x1%20(4).png`,
  duo: `${assetBase}/%E6%9C%AA%E5%91%BD%E5%90%8D-5(1).jpg`,
  traveler: `${assetBase}/%E7%89%B9%E5%AF%AB-1776818624440.png`,
  cta: `${assetBase}/landing-page-lp_img_6_cta-1x1.png`,
};

const coreFeatures = [
  {
    eyebrow: '科技支撐',
    title: '高效率環抱支撐，穩住長途移動中的脖頸壓力',
    copy:
      'Horizon X-Space 透過立體支撐弧線與高回彈包覆，讓頸部在飛機、高鐵、巴士與候機室都能維持更穩定角度，減少頭部左右傾倒造成的痠痛與僵硬。',
    image: productImages.product,
    alt: 'Horizon X-Space 太空漂浮安眠脖枕細節特寫',
  },
  {
    eyebrow: '固定扣設計',
    title: '調節式固定扣，讓姿勢不良改善更有感',
    copy:
      '前側固定扣可以依照使用者習慣調整鬆緊，讓下巴與頸側支撐更貼合，降低睡著後頭部前傾、歪斜與突然驚醒的機率。',
    image: productImages.closeup,
    alt: 'Horizon X-Space 固定扣與布料近拍',
  },
  {
    eyebrow: '多場景探索',
    title: '從候機、辦公到轉乘休息，改善旅行睡眠品質',
    copy:
      '不只是機上休息，Horizon X-Space 也適合用在咖啡館遠端工作、機場候機、跨城移動與短暫補眠時刻，讓每段旅程都更接近真正的恢復。',
    image: productImages.lifestyle,
    alt: '使用者在都市空間佩戴脖枕工作',
  },
];

const benefitChips = [
  '告別長途旅行頸部痠痛',
  '改善旅行睡眠與補眠效率',
  '穩定頭頸姿勢，降低前傾歪斜',
  '耐用包覆，適合反覆出行使用',
];

const comparisonPoints = [
  {
    label: '一般旅行頸枕',
    value: '容易鬆垮、支撐點分散，睡著後頭部仍可能往前掉。',
  },
  {
    label: 'Horizon X-Space',
    value: '立體包覆加上調節式固定扣，讓支撐更集中、貼合度更高。',
  },
  {
    label: '探索者體感',
    value: '減少醒來後的肩頸壓迫感，讓落地後還有餘裕繼續行程。',
  },
];

const seo = {
  title: '旅行頸枕推薦｜Horizon X-Space 太空漂浮安眠脖枕，改善長途旅行頸部痠痛',
  description:
    '探索者輕奢啟航。Horizon X-Space 太空漂浮安眠脖枕專為改善長途旅行頸部痠痛、姿勢不良與難以入睡而設計，以調節式固定扣與高效率支撐，幫助消除旅行疲勞。',
  keywords:
    '旅行頸枕,長途旅行頸部痠痛,頸枕選購指南,改善旅行睡眠,脖枕推薦品牌,姿勢不良改善,消除旅行疲勞',
  canonical: 'https://tw.elitefasion.com/x-space/horizon-x-space',
  ogImage: productImages.traveler,
};

function ensureMeta(selector, attributes) {
  let tag = document.head.querySelector(selector);
  if (!tag) {
    tag = document.createElement('meta');
    document.head.appendChild(tag);
  }

  Object.entries(attributes).forEach(([key, value]) => {
    tag.setAttribute(key, value);
  });
}

function ensureLink(rel, href) {
  let tag = document.head.querySelector(`link[rel="${rel}"]`);
  if (!tag) {
    tag = document.createElement('link');
    tag.setAttribute('rel', rel);
    document.head.appendChild(tag);
  }
  tag.setAttribute('href', href);
}

export default function HorizonXSpaceLanding() {
  useEffect(() => {
    document.title = seo.title;

    ensureMeta('meta[name="description"]', {
      name: 'description',
      content: seo.description,
    });
    ensureMeta('meta[name="keywords"]', {
      name: 'keywords',
      content: seo.keywords,
    });
    ensureMeta('meta[property="og:title"]', {
      property: 'og:title',
      content: seo.title,
    });
    ensureMeta('meta[property="og:description"]', {
      property: 'og:description',
      content: seo.description,
    });
    ensureMeta('meta[property="og:type"]', {
      property: 'og:type',
      content: 'website',
    });
    ensureMeta('meta[property="og:url"]', {
      property: 'og:url',
      content: seo.canonical,
    });
    ensureMeta('meta[property="og:image"]', {
      property: 'og:image',
      content: seo.ogImage,
    });
    ensureMeta('meta[name="twitter:card"]', {
      name: 'twitter:card',
      content: 'summary_large_image',
    });
    ensureMeta('meta[name="twitter:title"]', {
      name: 'twitter:title',
      content: seo.title,
    });
    ensureMeta('meta[name="twitter:description"]', {
      name: 'twitter:description',
      content: seo.description,
    });
    ensureMeta('meta[name="twitter:image"]', {
      name: 'twitter:image',
      content: seo.ogImage,
    });
    ensureLink('canonical', seo.canonical);

    const structuredData = {
      '@context': 'https://schema.org',
      '@type': 'Product',
      name: 'Horizon X-Space 太空漂浮安眠脖枕',
      description: seo.description,
      image: [productImages.hero, productImages.traveler, productImages.closeup],
      brand: {
        '@type': 'Brand',
        name: 'Horizon',
      },
      category: '旅行頸枕',
      keywords: seo.keywords,
      url: seo.canonical,
    };

    let scriptTag = document.head.querySelector('#horizon-x-space-jsonld');
    if (!scriptTag) {
      scriptTag = document.createElement('script');
      scriptTag.id = 'horizon-x-space-jsonld';
      scriptTag.type = 'application/ld+json';
      document.head.appendChild(scriptTag);
    }
    scriptTag.textContent = JSON.stringify(structuredData);
  }, []);

  return (
    <>
      <style>{`
        :root {
          color-scheme: dark;
          --bg: #07111f;
          --bg-soft: #0d1b30;
          --ink: #f8fbff;
          --muted: rgba(232, 242, 255, 0.78);
          --line: rgba(145, 187, 255, 0.16);
          --panel: rgba(9, 19, 37, 0.72);
          --panel-strong: rgba(11, 24, 46, 0.92);
          --aqua: #71f0ff;
          --gold: #ffc872;
          --violet: #8d7dff;
          --cta: #7af2ff;
          --cta-ink: #06131f;
          --shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
        }

        * {
          box-sizing: border-box;
        }

        html {
          scroll-behavior: smooth;
        }

        body {
          margin: 0;
          font-family: Inter, "Noto Sans TC", "PingFang TC", sans-serif;
          background:
            radial-gradient(circle at top left, rgba(122, 242, 255, 0.12), transparent 28%),
            radial-gradient(circle at top right, rgba(255, 200, 114, 0.16), transparent 26%),
            radial-gradient(circle at 50% 20%, rgba(141, 125, 255, 0.16), transparent 22%),
            linear-gradient(180deg, #04101c 0%, #081524 32%, #0a1320 100%);
          color: var(--ink);
        }

        a {
          color: inherit;
          text-decoration: none;
        }

        img {
          display: block;
          max-width: 100%;
        }

        .xspace-page {
          overflow: hidden;
        }

        .xspace-shell {
          width: min(1200px, calc(100% - 32px));
          margin: 0 auto;
        }

        .eyebrow {
          display: inline-flex;
          align-items: center;
          gap: 10px;
          padding: 10px 16px;
          border-radius: 999px;
          border: 1px solid rgba(122, 242, 255, 0.22);
          background: rgba(7, 24, 41, 0.58);
          backdrop-filter: blur(14px);
          color: var(--aqua);
          font-size: 0.82rem;
          letter-spacing: 0.12em;
          text-transform: uppercase;
        }

        .eyebrow::before {
          content: "";
          width: 9px;
          height: 9px;
          border-radius: 999px;
          background: linear-gradient(135deg, var(--gold), var(--aqua));
          box-shadow: 0 0 18px rgba(122, 242, 255, 0.72);
        }

        .hero {
          position: relative;
          padding: 24px 0 88px;
        }

        .hero::before {
          content: "";
          position: absolute;
          inset: 0 auto auto 50%;
          width: 760px;
          height: 760px;
          background: radial-gradient(circle, rgba(122, 242, 255, 0.14), transparent 62%);
          transform: translateX(-50%);
          pointer-events: none;
        }

        .hero-grid {
          display: grid;
          gap: 24px;
          align-items: center;
        }

        .hero-copy {
          position: relative;
          z-index: 1;
          padding-top: 40px;
        }

        .hero-kicker {
          margin: 18px 0 12px;
          color: var(--gold);
          font-weight: 700;
          letter-spacing: 0.06em;
          text-transform: uppercase;
          font-size: 0.9rem;
        }

        .hero-title {
          margin: 0;
          font-size: clamp(2.5rem, 8vw, 5.8rem);
          line-height: 0.96;
          letter-spacing: -0.04em;
        }

        .hero-title span {
          display: block;
          color: var(--aqua);
          text-shadow: 0 0 34px rgba(122, 242, 255, 0.22);
        }

        .hero-text {
          margin: 22px 0 0;
          max-width: 640px;
          color: var(--muted);
          font-size: 1rem;
          line-height: 1.9;
        }

        .hero-actions {
          display: flex;
          flex-wrap: wrap;
          gap: 14px;
          margin-top: 28px;
        }

        .button-primary,
        .button-secondary {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          min-height: 52px;
          padding: 0 22px;
          border-radius: 999px;
          font-weight: 800;
          transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        }

        .button-primary {
          background: linear-gradient(135deg, var(--aqua), #96fbff);
          color: var(--cta-ink);
          box-shadow: 0 14px 40px rgba(122, 242, 255, 0.24);
        }

        .button-secondary {
          border: 1px solid rgba(255, 255, 255, 0.16);
          background: rgba(255, 255, 255, 0.04);
          color: var(--ink);
        }

        .button-primary:hover,
        .button-secondary:hover,
        .feature-card:hover,
        .media-card:hover,
        .benefit-card:hover {
          transform: translateY(-3px);
        }

        .hero-meta {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 12px;
          margin-top: 26px;
        }

        .metric {
          padding: 14px 16px;
          border-radius: 20px;
          background: rgba(8, 21, 41, 0.7);
          border: 1px solid var(--line);
          box-shadow: var(--shadow);
        }

        .metric strong {
          display: block;
          color: var(--gold);
          font-size: 1.1rem;
          margin-bottom: 6px;
        }

        .metric span {
          color: var(--muted);
          line-height: 1.6;
          font-size: 0.92rem;
        }

        .hero-visual {
          position: relative;
        }

        .visual-frame {
          position: relative;
          padding: 18px;
          border-radius: 32px;
          background: linear-gradient(180deg, rgba(16, 33, 62, 0.92), rgba(8, 18, 33, 0.92));
          border: 1px solid rgba(122, 242, 255, 0.18);
          box-shadow: var(--shadow);
        }

        .visual-frame::before {
          content: "";
          position: absolute;
          inset: -1px;
          border-radius: inherit;
          padding: 1px;
          background: linear-gradient(135deg, rgba(122, 242, 255, 0.5), rgba(255, 200, 114, 0.28), transparent);
          -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
          -webkit-mask-composite: xor;
          mask-composite: exclude;
          pointer-events: none;
        }

        .visual-main {
          aspect-ratio: 1 / 1;
          border-radius: 26px;
          overflow: hidden;
        }

        .visual-main img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .floating-card,
        .floating-badge {
          position: absolute;
          z-index: 2;
          border: 1px solid rgba(255, 255, 255, 0.12);
          background: rgba(8, 19, 35, 0.74);
          backdrop-filter: blur(16px);
          box-shadow: var(--shadow);
        }

        .floating-card {
          right: -8px;
          bottom: -16px;
          width: 46%;
          padding: 12px;
          border-radius: 24px;
        }

        .floating-card img {
          width: 100%;
          border-radius: 16px;
          aspect-ratio: 1 / 1;
          object-fit: cover;
        }

        .floating-badge {
          top: -8px;
          left: -8px;
          padding: 14px 16px;
          border-radius: 20px;
          max-width: 220px;
        }

        .floating-badge strong {
          display: block;
          color: var(--aqua);
          margin-bottom: 6px;
          font-size: 0.95rem;
        }

        .floating-badge span {
          color: var(--muted);
          line-height: 1.6;
          font-size: 0.86rem;
        }

        .feature-section,
        .cta-section {
          position: relative;
          padding: 28px 0 84px;
        }

        .section-head {
          max-width: 760px;
          margin-bottom: 28px;
        }

        .section-head h2 {
          margin: 16px 0 14px;
          font-size: clamp(2rem, 6vw, 4rem);
          line-height: 1.02;
          letter-spacing: -0.04em;
        }

        .section-head p {
          margin: 0;
          color: var(--muted);
          font-size: 1rem;
          line-height: 1.85;
        }

        .benefit-grid {
          display: grid;
          gap: 14px;
          margin-bottom: 22px;
        }

        .benefit-card {
          padding: 18px 18px;
          border-radius: 24px;
          background: rgba(255, 255, 255, 0.04);
          border: 1px solid var(--line);
          box-shadow: var(--shadow);
        }

        .benefit-card strong {
          display: block;
          margin-bottom: 8px;
          color: var(--aqua);
          font-size: 0.98rem;
        }

        .benefit-card p {
          margin: 0;
          color: var(--muted);
          line-height: 1.75;
        }

        .chip-row {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
          margin-bottom: 22px;
        }

        .chip {
          padding: 10px 14px;
          border-radius: 999px;
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.08);
          color: #dbe8ff;
          font-size: 0.88rem;
        }

        .feature-grid {
          display: grid;
          gap: 18px;
        }

        .feature-card,
        .media-card,
        .cta-panel {
          border-radius: 30px;
          background: linear-gradient(180deg, rgba(11, 24, 45, 0.9), rgba(7, 17, 31, 0.88));
          border: 1px solid var(--line);
          box-shadow: var(--shadow);
        }

        .feature-card {
          overflow: hidden;
        }

        .feature-media {
          aspect-ratio: 1 / 1;
        }

        .feature-media img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .feature-copy {
          padding: 22px 20px 24px;
        }

        .feature-copy span {
          display: inline-block;
          margin-bottom: 10px;
          color: var(--gold);
          font-weight: 700;
          font-size: 0.88rem;
          letter-spacing: 0.08em;
          text-transform: uppercase;
        }

        .feature-copy h3 {
          margin: 0 0 12px;
          font-size: 1.38rem;
          line-height: 1.2;
        }

        .feature-copy p {
          margin: 0;
          color: var(--muted);
          line-height: 1.8;
        }

        .support-grid {
          display: grid;
          gap: 18px;
          margin-top: 20px;
        }

        .media-card {
          overflow: hidden;
        }

        .media-card img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .comparison-list {
          display: grid;
          gap: 12px;
          padding: 22px 20px;
        }

        .comparison-item {
          padding: 16px;
          border-radius: 22px;
          background: rgba(255, 255, 255, 0.04);
          border: 1px solid rgba(255, 255, 255, 0.06);
        }

        .comparison-item strong {
          display: block;
          color: var(--aqua);
          margin-bottom: 8px;
        }

        .comparison-item p {
          margin: 0;
          color: var(--muted);
          line-height: 1.75;
        }

        .internal-links {
          display: flex;
          flex-wrap: wrap;
          gap: 12px;
          margin-top: 24px;
        }

        .internal-links a {
          padding: 12px 16px;
          border-radius: 999px;
          border: 1px solid rgba(255, 255, 255, 0.1);
          background: rgba(255, 255, 255, 0.04);
          color: #dce8ff;
          font-weight: 600;
        }

        .cta-panel {
          position: relative;
          overflow: hidden;
          padding: 24px;
        }

        .cta-panel::before {
          content: "";
          position: absolute;
          inset: auto -10% -50% auto;
          width: 260px;
          height: 260px;
          background: radial-gradient(circle, rgba(122, 242, 255, 0.24), transparent 64%);
          pointer-events: none;
        }

        .cta-grid {
          display: grid;
          gap: 18px;
          align-items: center;
        }

        .cta-copy h2 {
          margin: 16px 0 14px;
          font-size: clamp(2rem, 6vw, 3.8rem);
          line-height: 1.02;
          letter-spacing: -0.04em;
        }

        .cta-copy p {
          margin: 0;
          color: var(--muted);
          line-height: 1.85;
        }

        .cta-note {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
          margin-top: 18px;
        }

        .cta-note span {
          padding: 10px 14px;
          border-radius: 999px;
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(255, 255, 255, 0.08);
          color: #d7e6ff;
          font-size: 0.88rem;
        }

        .cta-visual {
          position: relative;
          min-height: 320px;
          border-radius: 30px;
          overflow: hidden;
        }

        .cta-visual img {
          position: absolute;
          inset: 0;
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .cta-visual::after {
          content: "";
          position: absolute;
          inset: 0;
          background: linear-gradient(180deg, rgba(4, 9, 18, 0.12), rgba(4, 9, 18, 0.45));
        }

        @media (min-width: 768px) {
          .xspace-shell {
            width: min(1200px, calc(100% - 48px));
          }

          .hero {
            padding: 32px 0 112px;
          }

          .hero-meta,
          .benefit-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
          }

          .feature-grid {
            grid-template-columns: repeat(3, minmax(0, 1fr));
          }

          .support-grid {
            grid-template-columns: 1.05fr 0.95fr;
          }

          .cta-grid {
            grid-template-columns: 1.05fr 0.95fr;
          }
        }

        @media (min-width: 1024px) {
          .hero-grid {
            grid-template-columns: minmax(0, 1.06fr) minmax(420px, 0.94fr);
            gap: 40px;
          }

          .hero-copy {
            padding-top: 72px;
          }

          .feature-section,
          .cta-section {
            padding-bottom: 112px;
          }

          .cta-panel {
            padding: 34px;
          }
        }
      `}</style>

      <main className="xspace-page">
        <section className="hero">
          <div className="xspace-shell hero-grid">
            <div className="hero-copy">
              <div className="eyebrow">探索者輕奢啟航</div>
              <div className="hero-kicker">Horizon X-Space 太空漂浮安眠脖枕</div>
              <h1 className="hero-title">
                告別旅行疲勞：
                <span>Horizon X-Space 創新科技完美解決方案</span>
              </h1>
              <p className="hero-text">
                當旅程越拉越長，真正先崩潰的通常不是行程，而是頸部痠痛、難以入睡與姿勢不良帶來的疲勞感。
                Horizon X-Space 以調節式固定扣與高效率支撐設計，重新定義旅行頸枕該有的穩定、包覆與恢復力，
                讓每一次起飛、轉乘與落地，都還保有繼續探索的精神。
              </p>

              <div className="hero-actions">
                <a className="button-primary" href="#cta">
                  立即體驗太空級舒適！
                </a>
                <a className="button-secondary" href="#features">
                  看懂它如何改善旅行睡眠
                </a>
              </div>

              <div className="hero-meta">
                <div className="metric">
                  <strong>旅行頸枕升級</strong>
                  <span>不只柔軟，更重視固定、貼合與長途支撐效率。</span>
                </div>
                <div className="metric">
                  <strong>探索者導向</strong>
                  <span>為頻繁移動、需要快速恢復的人設計更穩定的休息方案。</span>
                </div>
                <div className="metric">
                  <strong>姿勢支援</strong>
                  <span>幫助降低頸部前傾、側倒與突然驚醒造成的中斷感。</span>
                </div>
                <div className="metric">
                  <strong>多場景使用</strong>
                  <span>適用飛行、候機、高鐵、客運、短暫補眠與移動工作時段。</span>
                </div>
              </div>
            </div>

            <div className="hero-visual">
              <div className="visual-frame">
                <div className="visual-main">
                  <img
                    src={productImages.hero}
                    alt="Horizon X-Space 太空漂浮安眠脖枕置於高級座艙場景"
                    loading="eager"
                  />
                </div>
                <div className="floating-badge">
                  <strong>消除旅行疲勞</strong>
                  <span>用更穩的頭頸支撐，換回更好的補眠品質與落地精神。</span>
                </div>
                <div className="floating-card">
                  <img
                    src={productImages.traveler}
                    alt="旅客在機場佩戴 Horizon X-Space 脖枕"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="feature-section" id="features">
          <div className="xspace-shell">
            <div className="section-head">
              <div className="eyebrow">Feature Section</div>
              <h2>為長途旅行頸部痠痛而生的高效率支撐設計</h2>
              <p>
                這不是一顆只為拍照而存在的旅行頸枕，而是一個從實際痛點出發的恢復工具。
                我們把常見的旅行問題拆解成三件事：頭部支撐不穩、入睡姿勢失衡、醒來後精神仍然沉重。
                Horizon X-Space 正是針對這三個環節，提供更完整的解法。
              </p>
            </div>

            <div className="chip-row" aria-label="產品重點標籤">
              {benefitChips.map((chip) => (
                <span className="chip" key={chip}>
                  {chip}
                </span>
              ))}
            </div>

            <div className="feature-grid">
              {coreFeatures.map((feature) => (
                <article className="feature-card" key={feature.title}>
                  <div className="feature-media">
                    <img src={feature.image} alt={feature.alt} loading="lazy" />
                  </div>
                  <div className="feature-copy">
                    <span>{feature.eyebrow}</span>
                    <h3>{feature.title}</h3>
                    <p>{feature.copy}</p>
                  </div>
                </article>
              ))}
            </div>

            <div className="support-grid">
              <div className="media-card">
                <img
                  src={productImages.duo}
                  alt="Horizon X-Space 灰色與湖水綠兩款旅行頸枕"
                  loading="lazy"
                />
              </div>

              <div className="benefit-grid">
                {comparisonPoints.map((item) => (
                  <div className="benefit-card" key={item.label}>
                    <strong>{item.label}</strong>
                    <p>{item.value}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="section-head" style={{ marginTop: 28 }}>
              <h2>不只是脖枕推薦品牌，更是一套探索前的恢復節奏</h2>
              <p>
                對經常移動的人來說，真正的奢侈不是艙等，而是能不能在抵達前先恢復一點精神。
                Horizon X-Space 把自然包覆、穩定固定與科技感造型結合，讓你在機場、車站與飛行途中都更容易維持舒適姿勢，
                也讓「改善旅行睡眠」不再只是口號。
              </p>
            </div>

            <div className="comparison-list">
              <div className="comparison-item">
                <strong>適合誰使用？</strong>
                <p>
                  長途飛行旅客、經常轉乘的差旅族、需要在通勤或移動途中補眠的人，
                  以及正在尋找頸枕選購指南的人，都能明顯感受到這類高支撐結構的差異。
                </p>
              </div>
              <div className="comparison-item">
                <strong>為什麼它更有轉換力？</strong>
                <p>
                  因為它直接回應最真實的需求：消除旅行疲勞、改善姿勢不良、減少醒來後的痠痛。
                  這種價值不是抽象的舒適，而是每趟旅程都能感受到的體感升級。
                </p>
              </div>
            </div>

            <nav className="internal-links" aria-label="建議內部連結">
              <a href="/blog/how-to-choose-neck-pillow">頸枕選購指南</a>
              <a href="/product/horizon-x-space-benefits">了解 Horizon X-Space 產品優勢</a>
              <a href="/faq">前往常見問題 FAQ</a>
            </nav>
          </div>
        </section>

        <section className="cta-section" id="cta">
          <div className="xspace-shell">
            <div className="cta-panel">
              <div className="cta-grid">
                <div className="cta-copy">
                  <div className="eyebrow">CTA Section</div>
                  <h2>探索無垠，輕盈啟程！</h2>
                  <p>
                    如果你正在尋找一款真正能改善旅行睡眠、減少頸部負擔、並讓旅程更像冒險而不是消耗的旅行頸枕，
                    Horizon X-Space 就是值得率先體驗的選擇。帶上它，不只是多一件旅行裝備，而是多一份穩定、恢復與出發的底氣。
                  </p>
                  <div className="cta-note">
                    <span>高對比視覺</span>
                    <span>太空感造型</span>
                    <span>多功能長途支撐</span>
                  </div>
                  <div className="hero-actions">
                    <a className="button-primary" href="/product/horizon-x-space-benefits">
                      探索無垠，輕盈啟程！
                    </a>
                    <a className="button-secondary" href="/faq">
                      立即查看常見問題
                    </a>
                  </div>
                </div>

                <div className="cta-visual">
                  <img
                    src={productImages.cta}
                    alt="Horizon X-Space 太空漂浮安眠脖枕在宇宙旋渦場景中"
                    loading="lazy"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </>
  );
}
