const ALLOWED_ORIGINS = new Set([
  'https://tw.elitefasion.com',
  'https://www.tw.elitefasion.com',
  'https://mkhsu2002.github.io',
]);

function isAllowedOrigin(origin) {
  if (!origin) {
    return true;
  }

  if (ALLOWED_ORIGINS.has(origin)) {
    return true;
  }

  return /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin);
}

const PURPOSES = new Set([
  '品牌聯名 / 商業合作',
  '媒體採訪 / 新聞稿',
  '文章授權 / 轉載',
  '投稿 / 專家觀點',
  '產品或服務推薦',
  '活動邀約 / 講座合作',
  '內容更正 / 讀者回饋',
  '網站技術問題',
  '其他',
]);

function getCorsHeaders(request) {
  const origin = request.headers.get('Origin') || '';
  const allowOrigin = !origin ? '*' : isAllowedOrigin(origin) ? origin : 'https://tw.elitefasion.com';

  return {
    'Access-Control-Allow-Origin': allowOrigin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Vary': 'Origin',
  };
}

function jsonResponse(request, body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      ...getCorsHeaders(request),
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
    },
  });
}

function sanitizeText(value, maxLength) {
  return String(value || '')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, maxLength);
}

function sanitizeMultiline(value, maxLength) {
  return String(value || '')
    .replace(/\r/g, '')
    .trim()
    .slice(0, maxLength);
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function isValidUrl(value) {
  if (!value) {
    return true;
  }

  try {
    const url = new URL(value);
    return url.protocol === 'https:' || url.protocol === 'http:';
  } catch {
    return false;
  }
}

async function parsePayload(request) {
  const contentType = request.headers.get('Content-Type') || '';
  if (!contentType.includes('application/json')) {
    return null;
  }

  try {
    return await request.json();
  } catch {
    return null;
  }
}

function buildEmailHtml(payload) {
  const rows = [
    ['姓名', payload.name],
    ['Email', payload.email],
    ['公司 / 品牌 / 單位', payload.organization || '未提供'],
    ['聯繫目的', payload.purpose],
    ['主旨', payload.subject || '未提供'],
    ['網站 / 社群連結', payload.website || '未提供'],
  ];

  const rowsHtml = rows
    .map(([label, value]) => `
      <tr>
        <th align="left" style="padding:8px 12px;border-bottom:1px solid #eee;width:160px;color:#555;">${escapeHtml(label)}</th>
        <td style="padding:8px 12px;border-bottom:1px solid #eee;color:#111;">${escapeHtml(value)}</td>
      </tr>
    `)
    .join('');

  return `
    <div style="font-family:Arial,'Noto Sans TC',sans-serif;line-height:1.7;color:#111;">
      <h2 style="margin:0 0 16px;">Elite Fashion 訪客留言</h2>
      <table cellspacing="0" cellpadding="0" style="border-collapse:collapse;width:100%;max-width:720px;">${rowsHtml}</table>
      <h3 style="margin:24px 0 8px;">訊息內容</h3>
      <div style="white-space:pre-wrap;padding:16px;background:#fafafa;border:1px solid #eee;">${escapeHtml(payload.message)}</div>
    </div>
  `;
}

function buildEmailText(payload) {
  return [
    'Elite Fashion 訪客留言',
    '',
    `姓名：${payload.name}`,
    `Email：${payload.email}`,
    `公司 / 品牌 / 單位：${payload.organization || '未提供'}`,
    `聯繫目的：${payload.purpose}`,
    `主旨：${payload.subject || '未提供'}`,
    `網站 / 社群連結：${payload.website || '未提供'}`,
    '',
    '訊息內容：',
    payload.message,
  ].join('\n');
}

async function handleContact(request, env) {
  const payload = await parsePayload(request);
  if (!payload) {
    return jsonResponse(request, { ok: false, error: '請使用正確的表單格式送出。' }, 400);
  }

  if (sanitizeText(payload.company, 120)) {
    return jsonResponse(request, { ok: true });
  }

  const clean = {
    name: sanitizeText(payload.name, 120),
    email: sanitizeText(payload.email, 180),
    organization: sanitizeText(payload.organization, 180),
    purpose: sanitizeText(payload.purpose, 80),
    subject: sanitizeText(payload.subject, 160),
    website: sanitizeText(payload.website, 240),
    message: sanitizeMultiline(payload.message, 4000),
  };

  if (!clean.name || !isValidEmail(clean.email) || !PURPOSES.has(clean.purpose) || clean.message.length < 10) {
    return jsonResponse(request, { ok: false, error: '請確認必填欄位已正確填寫。' }, 400);
  }

  if (!isValidUrl(clean.website)) {
    return jsonResponse(request, { ok: false, error: '網站或社群連結格式不正確。' }, 400);
  }

  const apiKey = env.RESEND_API_KEY;
  const from = env.CONTACT_FROM_EMAIL || 'Elite Fashion <northpathca@insightestate.ca>';
  const to = env.CONTACT_TO_EMAIL || 'mkhsu2002@gmail.com';

  if (!apiKey) {
    return jsonResponse(request, { ok: false, error: '聯絡表單尚未完成寄信設定。' }, 500);
  }

  const subjectSuffix = clean.subject ? `：${clean.subject}` : `：${clean.purpose}`;
  const resendResponse = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from,
      to: [to],
      reply_to: clean.email,
      subject: `Elite Fashion 訪客留言｜${subjectSuffix.replace(/^：/, '')}`,
      html: buildEmailHtml(clean),
      text: buildEmailText(clean),
    }),
  });

  if (!resendResponse.ok) {
    const details = await resendResponse.text();
    console.error('Resend delivery failed', details);
    return jsonResponse(request, { ok: false, error: '訊息暫時無法送出，請稍後再試。' }, 502);
  }

  const result = await resendResponse.json();
  return jsonResponse(request, { ok: true, id: result.id });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: getCorsHeaders(request),
      });
    }

    if (url.pathname !== '/api/contact') {
      return jsonResponse(request, { ok: false, error: 'Not found' }, 404);
    }

    if (request.method !== 'POST') {
      return jsonResponse(request, { ok: false, error: 'Method not allowed' }, 405);
    }

    return handleContact(request, env);
  },
};
