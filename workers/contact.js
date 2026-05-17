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

async function resendRequest(env, path, body, method = 'POST') {
  const apiKey = env.RESEND_API_KEY;
  if (!apiKey) {
    throw new Error('RESEND_API_KEY is not configured.');
  }

  const response = await fetch(`https://api.resend.com${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  let data = {};
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { message: text };
  }

  if (!response.ok) {
    const error = new Error(data.message || data.name || text || 'Resend request failed.');
    error.status = response.status;
    error.details = data;
    throw error;
  }

  return data;
}

async function ensureNewsletterSegment(env) {
  const configuredId = sanitizeText(env.RESEND_NEWSLETTER_SEGMENT_ID, 120);
  if (configuredId) {
    return configuredId;
  }

  const segmentName = sanitizeText(env.RESEND_NEWSLETTER_SEGMENT_NAME, 120) || 'Elite Fashion Newsletter';
  const payload = await resendRequest(env, '/segments', undefined, 'GET');
  const segments = Array.isArray(payload.data) ? payload.data : Array.isArray(payload) ? payload : [];
  const existing = segments.find((segment) => segment && segment.name === segmentName);
  if (existing && existing.id) {
    return existing.id;
  }

  const created = await resendRequest(env, '/segments', { name: segmentName });
  return created.id;
}

async function addNewsletterContact(env, clean) {
  const segmentId = await ensureNewsletterSegment(env);

  try {
    const created = await resendRequest(env, '/contacts', {
      email: clean.email,
      unsubscribed: false,
      segments: [{ id: segmentId }],
    });
    return { contactId: created.id, segmentId, created: true };
  } catch (error) {
    if (error.status !== 409) {
      throw error;
    }

    await resendRequest(env, `/contacts/${encodeURIComponent(clean.email)}`, {
      unsubscribed: false,
    }, 'PATCH');
    await resendRequest(env, `/contacts/${encodeURIComponent(clean.email)}/segments/${encodeURIComponent(segmentId)}`, {});
    return { contactId: clean.email, segmentId, created: false };
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

async function handleSubscribe(request, env) {
  const payload = await parsePayload(request);
  if (!payload) {
    return jsonResponse(request, { ok: false, error: '請使用正確的訂閱格式送出。' }, 400);
  }

  if (sanitizeText(payload.company, 120)) {
    return jsonResponse(request, { ok: true });
  }

  const clean = {
    email: sanitizeText(payload.email, 180).toLowerCase(),
    source: sanitizeText(payload.source, 80) || 'website',
  };

  if (!isValidEmail(clean.email)) {
    return jsonResponse(request, { ok: false, error: '請填寫有效的電子郵件。' }, 400);
  }

  try {
    const result = await addNewsletterContact(env, clean);
    return jsonResponse(request, { ok: true, id: result.contactId, segmentId: result.segmentId });
  } catch (error) {
    console.error('Newsletter subscribe failed', error.details || error.message);
    return jsonResponse(request, { ok: false, error: '訂閱暫時無法完成，請稍後再試。' }, 502);
  }
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

    if (url.pathname === '/api/contact') {
      if (request.method !== 'POST') {
        return jsonResponse(request, { ok: false, error: 'Method not allowed' }, 405);
      }

      return handleContact(request, env);
    }

    if (url.pathname === '/api/subscribe') {
      if (request.method !== 'POST') {
        return jsonResponse(request, { ok: false, error: 'Method not allowed' }, 405);
      }

      return handleSubscribe(request, env);
    }

    return jsonResponse(request, { ok: false, error: 'Not found' }, 404);
  },
};
