const $ = id => document.getElementById(id);
let latestReport = '';
let latestRaw = '';

async function loadDocs() {
  try {
    const r = await fetch('/api/documents');
    const d = await r.json();
    $('doccount').textContent = `${d.length} statute${d.length === 1 ? '' : 's'} indexed`;
  } catch {
    $('doccount').textContent = 'Library active';
  }
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

// ── Quick Topic Chips ────────────────────────────────────────────────────────
document.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => {
    $('question').value = chip.getAttribute('data-q');
    $('question').focus();
    $('question').scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
});

// ── Visual Markdown & Card Parser ────────────────────────────────────────────
function parseMarkdownToVisual(text) {
  if (!text) return '<p>No content generated.</p>';

  // Split into sections by H3 headers (### )
  const rawSections = text.split(/(?=###\s+)/g);
  let html = '';

  for (const raw of rawSections) {
    const trimmed = raw.trim();
    if (!trimmed) continue;

    // Extract header and body
    const match = trimmed.match(/^###\s+([^\n]+)\n?([\s\S]*)$/);
    if (!match) {
      // General paragraph/content
      html += `<div class="vcard general-card">${renderInlineFormatting(trimmed)}</div>`;
      continue;
    }

    const title = match[1].trim();
    const content = match[2].trim();

    // 1. Quick Summary Card
    if (title.includes('Quick Summary') || title.includes('Summary')) {
      html += `
        <div class="vcard summary-card">
          <div class="vcard-header">
            <span class="vcard-icon">📌</span>
            <h4>Executive Summary</h4>
          </div>
          <div class="summary-body">
            ${renderParagraphs(content)}
          </div>
        </div>`;
    }
    // 2. Applicable Law & Exact Sections
    else if (title.includes('Applicable Law') || title.includes('Law') || title.includes('Sections')) {
      html += `
        <div class="vcard law-card">
          <div class="vcard-header">
            <span class="vcard-icon">⚖️</span>
            <h4>Applicable Statutes & Exact Sections</h4>
            <span class="tag-badge">Indian Law</span>
          </div>
          <div class="law-items-grid">
            ${renderLawItems(content)}
          </div>
        </div>`;
    }
    // 3. Step-by-Step Action Roadmap
    else if (title.includes('Step-by-Step') || title.includes('Action Plan') || title.includes('Roadmap')) {
      html += `
        <div class="vcard roadmap-card">
          <div class="vcard-header">
            <span class="vcard-icon">🗺️</span>
            <h4>Visual Step-by-Step Roadmap</h4>
            <span class="tag-badge green-badge">Action Path</span>
          </div>
          <div class="stepper-timeline">
            ${renderStepper(content)}
          </div>
        </div>`;
    }
    // 4. Evidence Checklist
    else if (title.includes('Evidence') || title.includes('Checklist')) {
      html += `
        <div class="vcard checklist-card">
          <div class="vcard-header">
            <span class="vcard-icon">📋</span>
            <h4>Evidence & Records Checklist</h4>
            <span class="tag-badge purple-badge">Click to track</span>
          </div>
          <div class="checklist-progress-wrap">
            <div class="progress-info">
              <span id="evidence-counter">0 documents checked</span>
            </div>
            <div class="progress-bar">
              <div id="evidence-bar" class="progress-fill" style="width:0%"></div>
            </div>
          </div>
          <div class="checklist-items">
            ${renderChecklist(content)}
          </div>
        </div>`;
    }
    // 5. Deadlines & Limitations
    else if (title.includes('Deadlines') || title.includes('Time Limits') || title.includes('Timeline')) {
      html += `
        <div class="vcard deadline-card">
          <div class="vcard-header">
            <span class="vcard-icon">⏳</span>
            <h4>Statutory Deadlines & Time Limits</h4>
            <span class="tag-badge alert-badge">Important</span>
          </div>
          <div class="deadline-body">
            ${renderBullets(content)}
          </div>
        </div>`;
    }
    // 6. Do's and Don'ts Matrix
    else if (title.includes("Do's") || title.includes("Dos and Don'ts") || title.includes("Precautions")) {
      html += `
        <div class="vcard dos-donts-card">
          <div class="vcard-header">
            <span class="vcard-icon">🚦</span>
            <h4>Do's and Don'ts (Avoid Mistakes)</h4>
          </div>
          <div class="dos-donts-grid">
            ${renderDosDonts(content)}
          </div>
        </div>`;
    }
    // 7. Portals & Escalation
    else if (title.includes('Portals') || title.includes('Where to File') || title.includes('Escalation')) {
      html += `
        <div class="vcard portals-card">
          <div class="vcard-header">
            <span class="vcard-icon">🏛️</span>
            <h4>Official Grievance Portals & Helplines</h4>
          </div>
          <div class="portals-body">
            ${renderPortals(content)}
          </div>
        </div>`;
    }
    // 8. Advocate Consultation
    else if (title.includes('Advocate') || title.includes('Lawyer')) {
      html += `
        <div class="vcard advocate-card">
          <div class="vcard-header">
            <span class="vcard-icon">💼</span>
            <h4>When to Consult an Advocate</h4>
          </div>
          <div class="advocate-body">
            ${renderBullets(content)}
          </div>
        </div>`;
    }
    // Default fallback card
    else {
      html += `
        <div class="vcard default-card">
          <div class="vcard-header">
            <h4>${esc(title)}</h4>
          </div>
          <div class="card-body">
            ${renderParagraphs(content)}
          </div>
        </div>`;
    }
  }

  return html;
}

// ── Specific Card Renderers ──────────────────────────────────────────────────

function renderLawItems(content) {
  const lines = content.split('\n').filter(l => l.trim().length > 0);
  let html = '';

  for (const line of lines) {
    const clean = line.replace(/^\s*[\*\-]\s*/, '').trim();
    if (!clean) continue;

    // Pattern: **Act Name — Section X**: Description
    const parts = clean.split(/:\s*(.+)/);
    if (parts.length >= 2) {
      const heading = renderInlineFormatting(parts[0]);
      const desc = renderInlineFormatting(parts[1]);
      html += `
        <div class="law-item">
          <div class="law-title">
            <span class="gavel-icon">⚖️</span>
            <strong>${heading}</strong>
          </div>
          <p class="law-desc">${desc}</p>
        </div>`;
    } else {
      html += `<div class="law-item"><p>${renderInlineFormatting(clean)}</p></div>`;
    }
  }

  return html || `<p>${renderInlineFormatting(content)}</p>`;
}

function renderStepper(content) {
  const lines = content.split('\n').filter(l => l.trim().length > 0);
  let html = '';
  let stepIndex = 1;

  for (const line of lines) {
    const clean = line.replace(/^\s*[\*\-]\s*/, '').trim();
    if (!clean) continue;

    // Check for Step X pattern
    const stepMatch = clean.match(/^\*\*Step\s*(\d+|[A-Za-z0-9\s\/\(\)]+)\*\*\s*[:-]\s*(.+)$/i);
    if (stepMatch) {
      const stepLabel = stepMatch[1];
      const stepBody = renderInlineFormatting(stepMatch[2]);
      html += `
        <div class="step-card">
          <div class="step-num">${stepIndex++}</div>
          <div class="step-content">
            <div class="step-badge-tag">${renderInlineFormatting(stepLabel)}</div>
            <p>${stepBody}</p>
          </div>
        </div>`;
    } else {
      html += `
        <div class="step-card">
          <div class="step-num">${stepIndex++}</div>
          <div class="step-content">
            <p>${renderInlineFormatting(clean)}</p>
          </div>
        </div>`;
    }
  }

  return html || `<p>${renderInlineFormatting(content)}</p>`;
}

function renderChecklist(content) {
  const lines = content.split('\n').filter(l => l.trim().length > 0);
  let html = '';

  for (const line of lines) {
    const clean = line.replace(/^\s*[\*\-]\s*(\[\s*\]\s*)?/, '').trim();
    if (!clean) continue;

    html += `
      <label class="check-item">
        <input type="checkbox" class="evidence-chk">
        <span class="custom-chk"></span>
        <span class="chk-text">${renderInlineFormatting(clean)}</span>
      </label>`;
  }

  return html || `<p>${renderInlineFormatting(content)}</p>`;
}

function renderDosDonts(content) {
  const lines = content.split('\n').filter(l => l.trim().length > 0);
  let dos = [];
  let donts = [];

  for (const line of lines) {
    const clean = line.replace(/^\s*[\*\-]\s*/, '').trim();
    if (/✅|DO:|DO\b/i.test(clean)) {
      dos.push(clean.replace(/^[✅\*\s]*(DO:?|DO\b)?/i, '').trim());
    } else if (/❌|DON'T:|DONT:|DON'T\b/i.test(clean)) {
      donts.push(clean.replace(/^[❌\*\s]*(DON'T:?|DONT:?|DON'T\b)?/i, '').trim());
    } else {
      dos.push(clean);
    }
  }

  const dosHtml = dos.map(d => `<li class="do-item">✅ ${renderInlineFormatting(d)}</li>`).join('');
  const dontsHtml = donts.map(d => `<li class="dont-item">❌ ${renderInlineFormatting(d)}</li>`).join('');

  return `
    <div class="dos-col">
      <h5>Recommended (DO)</h5>
      <ul>${dosHtml || '<li>Follow procedural notice guidelines</li>'}</ul>
    </div>
    <div class="donts-col">
      <h5>Avoid (DON'T)</h5>
      <ul>${dontsHtml || '<li>Do not destroy transaction records</li>'}</ul>
    </div>`;
}

function renderPortals(content) {
  const lines = content.split('\n').filter(l => l.trim().length > 0);
  let html = '';

  for (const line of lines) {
    const clean = line.replace(/^\s*[\*\-]\s*/, '').trim();
    if (!clean) continue;

    // Detect portal URLs or numbers
    const linkMatch = clean.match(/(https?:\/\/[^\s\)]+|[0-9]{4,5})/);
    const badge = linkMatch ? `<span class="portal-badge">${linkMatch[1]}</span>` : '';
    html += `
      <div class="portal-item">
        <span class="portal-icon">🔗</span>
        <div class="portal-text">${renderInlineFormatting(clean)}</div>
        ${badge}
      </div>`;
  }

  return html || `<p>${renderInlineFormatting(content)}</p>`;
}

function renderBullets(content) {
  const lines = content.split('\n').filter(l => l.trim().length > 0);
  const items = lines.map(line => {
    const clean = line.replace(/^\s*[\*\-]\s*/, '').trim();
    return `<li>${renderInlineFormatting(clean)}</li>`;
  }).join('');
  return `<ul class="bullet-list">${items}</ul>`;
}

function renderParagraphs(content) {
  return content
    .split(/\n{2,}/)
    .map(p => `<p>${renderInlineFormatting(p.trim())}</p>`)
    .join('');
}

function renderInlineFormatting(str) {
  let s = esc(str);
  // Bold
  s = s.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Italics
  s = s.replace(/\*(.*?)\*/g, '<em>$1</em>');
  // Inline code / sections
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  // URLs to clickable links
  s = s.replace(/(https?:\/\/[^\s\)<]+)/g, '<a href="$1" target="_blank" rel="noopener">$1 ↗</a>');
  return s;
}

// ── Citation Verification Audit Renderer ─────────────────────────────────────
function renderClaimsAudit(claims, summary) {
  const wrap = $('citation-audit-wrap');
  if (!wrap) return;

  const summaryBadge = $('audit-summary-badge');
  const claimsList = $('claims-list');

  if (!claims.length) {
    if (summaryBadge) summaryBadge.innerHTML = '<span class="audit-pill audit-neutral">0 statutory citations detected</span>';
    if (claimsList) claimsList.innerHTML = '<p class="empty-audit">No direct statutory sections required verification.</p>';
    return;
  }

  // Summary Pill bar
  const verified = summary ? summary.verified_claims_count : claims.filter(c => c.is_verified).length;
  const unverified = summary ? summary.unverified_claims_count : claims.filter(c => !c.is_verified).length;
  const cautions = summary ? summary.caution_flags_count : 0;

  if (summaryBadge) {
    summaryBadge.innerHTML = `
      <div class="audit-stats-row">
        <span class="audit-pill audit-pass">✅ ${verified} Verified Against Gazette/Statute</span>
        ${cautions > 0 ? `<span class="audit-pill audit-warn">⚠️ ${cautions} Judicial Cautions / Precedents</span>` : ''}
        ${unverified > 0 ? `<span class="audit-pill audit-fail">❌ ${unverified} Unverified Provisions Flagged</span>` : ''}
        <span class="audit-pill audit-meta">Audited at ${esc(claims[0]?.verification_timestamp ? new Date(claims[0].verification_timestamp).toLocaleTimeString() : 'now')}</span>
      </div>`;
  }

  // Claims cards
  if (claimsList) {
    claimsList.innerHTML = claims.map(c => {
      const typeLabel = (c.claim_type || 'statutory').toUpperCase().replace('_', ' ');
      let badgeClass = 'claim-badge-verified';
      let statusText = 'VERIFIED';

      if (c.confidence_level === 'refuted' || !c.is_verified) {
        badgeClass = 'claim-badge-refuted';
        statusText = 'UNVERIFIED';
      } else if (c.confidence_level === 'caution' || (c.conflicting_interpretations && c.conflicting_interpretations.length > 0)) {
        badgeClass = 'claim-badge-caution';
        statusText = 'JUDICIAL CAUTION';
      }

      return `
        <div class="claim-card ${badgeClass}-border">
          <div class="claim-card-head">
            <div class="claim-title-group">
              <span class="claim-type-tag">${esc(typeLabel)}</span>
              <strong>${esc(c.act_name)} — ${esc(c.section_number)}</strong>
            </div>
            <span class="claim-status-pill ${badgeClass}">${esc(statusText)}</span>
          </div>

          <div class="claim-metadata-grid">
            <div><span class="meta-label">Jurisdiction:</span> ${esc(c.jurisdiction)}</div>
            <div><span class="meta-label">Status:</span> ${esc(c.current_status)}</div>
            <div><span class="meta-label">Commencement Date:</span> ${esc(c.effective_date)}</div>
            <div><span class="meta-label">Official Authority:</span> <a href="${esc(c.official_source)}" target="_blank" rel="noopener">${esc(c.official_source.slice(0, 35))}… ↗</a></div>
          </div>

          <div class="claim-exact-text">
            <div class="exact-text-label">Exact Provision / Ruling Text:</div>
            <blockquote>"${esc(c.exact_provision_text)}"</blockquote>
          </div>

          ${c.relevant_judicial_precedents && c.relevant_judicial_precedents.length ? `
            <div class="claim-precedents">
              <div class="prec-label">🏛️ Relevant Judicial Precedents:</div>
              <ul>${c.relevant_judicial_precedents.map(p => `<li>${esc(p)}</li>`).join('')}</ul>
            </div>` : ''}

          ${c.conflicting_interpretations && c.conflicting_interpretations.length ? `
            <div class="claim-conflicts">
              <div class="conflict-label">⚖️ Judicial Exceptions & Conflicting Views:</div>
              <ul>${c.conflicting_interpretations.map(ci => `<li>${esc(ci)}</li>`).join('')}</ul>
            </div>` : ''}

          ${c.verification_notes ? `
            <div class="claim-notes">
              <span class="meta-label">Audit Notes:</span> ${esc(c.verification_notes)}
            </div>` : ''}
        </div>`;
    }).join('');
  }
}

// ── Evidence Progress Tracker ────────────────────────────────────────────────
function bindChecklistEvents() {
  const chks = document.querySelectorAll('.evidence-chk');
  if (!chks.length) return;

  const update = () => {
    const checked = Array.from(chks).filter(c => c.checked).length;
    const total = chks.length;
    const counter = $('evidence-counter');
    const bar = $('evidence-bar');
    if (counter) counter.textContent = `${checked} of ${total} documents gathered`;
    if (bar) bar.style.width = `${Math.round((checked / total) * 100)}%`;
  };

  chks.forEach(c => c.addEventListener('change', update));
  update();
}

// ── Submit & Run Workflow ────────────────────────────────────────────────────
$('ask').addEventListener('click', async () => {
  const question = $('question').value.trim();
  if (question.length < 8) {
    alert('Please describe your situation in a little more detail (at least 8 characters).');
    $('question').focus();
    return;
  }

  const btn = $('ask');
  btn.disabled = true;
  btn.innerHTML = '<span>Analysing Indian Law & Sections…</span> <span class="spinner">⏳</span>';
  $('result').classList.remove('hidden');

  $('visual-report').innerHTML = `
    <div class="loading-state">
      <div class="loader-ring"></div>
      <h4>Examining statutory provisions…</h4>
      <p>Consulting Indian Acts, Gazette rules, and structuring your actionable roadmap.</p>
    </div>`;
  $('answer').textContent = 'Generating comprehensive legal analysis…';
  $('agents').innerHTML = '';
  $('sources').innerHTML = '';

  const idempotencyKey = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : String(Date.now());
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-Idempotency-Key': idempotencyKey
      },
      body: JSON.stringify({
        question,
        language: $('language').value,
        jurisdiction: $('jurisdiction').value,
        date_of_incident: $('date').value || null,
        context: $('context').value || null
      })
    });

    if (res.status === 401) {
      window.location.replace('/login');
      return;
    }
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Request failed');

    latestRaw = data.answer;
    latestReport = `${data.answer}\n\nRELEVANT SOURCES:\n` +
      data.sources.map(s => `• ${s.title} (${s.status}) — ${s.jurisdiction}`).join('\n') +
      `\n\nDISCLAIMER:\n${data.disclaimer}`;

    // Render visual cards
    $('visual-report').innerHTML = parseMarkdownToVisual(data.answer);
    $('answer').textContent = data.answer;
    bindChecklistEvents();

    // Render Citation Verification Audit & Mandatory Metadata
    renderClaimsAudit(data.claims || [], data.verification_summary);

    // Confidence badge
    $('confidence').innerHTML = `
      <span class="conf-dot"></span>
      <strong>Verification Level:</strong> ${esc(data.confidence)}
      <span class="juris-tag">📍 ${esc($('jurisdiction').value)}</span>`;

    // Agents log
    $('agents').innerHTML = data.agents.map(a => `
      <div class="agent">
        <div class="agent-head">
          <span class="agent-name">${esc(a.agent)}</span>
          <span class="agent-status ${a.status === 'completed' ? 'agent-done' : 'agent-warn'}">${esc(a.status)}</span>
        </div>
        <p>${esc(a.note)}</p>
      </div>`).join('');

    // Sources list
    $('sources').innerHTML = data.sources.length ? data.sources.map(s => `
      <div class="source">
        <div class="source-header">
          <strong>${esc(s.title)}</strong>
          <span class="source-status-badge">${esc(s.status)}</span>
        </div>
        <div class="source-meta">${esc(s.jurisdiction)} · ${esc(s.document_type)}</div>
        <p class="source-excerpt">"${esc(s.chunk_excerpt)}"</p>
        ${s.source_url ? `<a href="${esc(s.source_url)}" target="_blank" rel="noopener">Open Official Source ↗</a>` : ''}
      </div>`).join('') : `
      <div class="source empty-source">
        <p>ℹ️ Direct answer formulated from authoritative Indian statutory frameworks (e.g. Consumer Protection Act, Transfer of Property Act, IT Act, NI Act, etc.). No custom administrator documents were required.</p>
      </div>`;

    $('disclaimer').textContent = data.disclaimer;
    $('result').scrollIntoView({ behavior: 'smooth', block: 'start' });

  } catch (e) {
    $('visual-report').innerHTML = `
      <div class="error-card">
        <h4>Unable to complete analysis</h4>
        <p>${esc(e.message)}</p>
        <button class="secondary" onclick="$('ask').click()">Retry</button>
      </div>`;
    $('answer').textContent = 'Error: ' + e.message;
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>Analyse My Rights & Actions</span> <span>→</span>';
  }
});

// ── Copy Clean Report ────────────────────────────────────────────────────────
$('copy').addEventListener('click', async () => {
  if (latestReport) {
    await navigator.clipboard.writeText(latestReport);
    const orig = $('copy').innerHTML;
    $('copy').innerHTML = '✅ Copied!';
    setTimeout(() => { $('copy').innerHTML = orig; }, 2000);
  }
});

// ── Print Report ─────────────────────────────────────────────────────────────
$('print').addEventListener('click', () => {
  window.print();
});

// ── Authentication & User Session Header (Strict Login-First) ──────────────
async function initAuthHeader() {
  const badge = $('userBadge');
  let user = null;

  try {
    const res = await fetch('/api/auth/me', { credentials: 'same-origin' });
    if (res.status === 401) {
      localStorage.removeItem('nyaya_user');
      window.location.replace('/login');
      return;
    }
    if (res.ok) {
      const data = await res.json();
      user = data.user;
      localStorage.setItem('nyaya_user', JSON.stringify(user));
    }
  } catch (e) {
    window.location.replace('/login');
    return;
  }

  if (!user) {
    window.location.replace('/login');
    return;
  }

  if (badge) badge.style.display = 'flex';
  const nameEl = $('userDisplayName');
  const roleEl = $('userRoleBadge');
  const avatarEl = $('userAvatar');
  if (nameEl) nameEl.textContent = user.name || user.email;
  if (roleEl) roleEl.textContent = user.role === 'admin' ? 'Admin' : (user.role === 'advocate' ? 'Advocate' : 'Civilian');
  if (avatarEl) avatarEl.textContent = user.role === 'admin' ? '🛡️' : (user.role === 'advocate' ? '👨‍⚖️' : '👤');

  const counselLink = $('counselConsoleLink');
  if (counselLink) {
    counselLink.style.display = (user.role === 'advocate' || user.role === 'admin') ? 'inline-block' : 'none';
  }
  const adminLink = $('adminConsoleLink');
  if (adminLink) {
    adminLink.style.display = (user.role === 'admin') ? 'inline-block' : 'none';
  }

  const outBtn = $('headerSignOut');
  if (outBtn) {
    outBtn.onclick = async () => {
      try { await fetch('/api/auth/logout', { method: 'POST', credentials: 'same-origin' }); } catch (e) {}
      try { localStorage.removeItem('nyaya_user'); } catch (e) {}
      window.location.replace('/login');
    };
  }
}

// Prevent unauthorized access via browser back/forward bfcache after logout
window.addEventListener('pageshow', (event) => {
  if (event.persisted) {
    initAuthHeader();
  }
});

// ── Choose Advocate & Send Complaint Integration ───────────────────────────
let availableAdvocates = [];
let selectedAdvocate = null;

async function loadAdvocates() {
  const select = $('advocateSelect');
  if (!select) return;

  try {
    const res = await fetch('/api/advocates');
    const list = await res.json();
    availableAdvocates = Array.isArray(list) ? list : [];

    select.innerHTML = '';
    availableAdvocates.forEach((adv, idx) => {
      const opt = document.createElement('option');
      opt.value = adv.id;
      opt.textContent = `${adv.name} • Bar: ${adv.bar_council_no} (${adv.jurisdiction})`;
      select.appendChild(opt);
    });

    if (availableAdvocates.length > 0) {
      selectAdvocateByIndex(0);
    }

    select.addEventListener('change', () => {
      const chosen = availableAdvocates.find(a => a.id === select.value);
      if (chosen) updateAdvocateMeta(chosen);
    });
  } catch (err) {
    console.error('Failed to load advocates:', err);
    select.innerHTML = '<option value="adv-giridharan">Advocate Giridharan • Bar D/1847/2019 (Delhi HC / Supreme Court Bar)</option>';
  }
}

function selectAdvocateByIndex(idx) {
  const adv = availableAdvocates[idx];
  if (!adv) return;
  selectedAdvocate = adv;
  updateAdvocateMeta(adv);
}

function updateAdvocateMeta(adv) {
  selectedAdvocate = adv;
  const specEl = $('advocateMetaSpecialization');
  const privEl = $('advocateMetaPrivilege');
  if (specEl) specEl.textContent = `${adv.specialization} • ${adv.experience || 'Verified Bar Counsel'}`;
  if (privEl) privEl.textContent = `Sec 132 BSA Privileged`;
}

// ── Open Send Complaint Modal ────────────────────────────────────────────────
const sendAdvocateBtn = $('sendAdvocateBtn');
const sendModal = $('sendComplaintModal');
const closeSendModalBtn = $('btnCloseSendModal');
const cancelSendModalBtn = $('btnCancelSendModal');
const confirmSendComplaintBtn = $('btnConfirmSendComplaint');

if (sendAdvocateBtn && sendModal) {
  sendAdvocateBtn.addEventListener('click', () => {
    // Populate Advocate summary
    if (!selectedAdvocate && availableAdvocates.length > 0) {
      selectedAdvocate = availableAdvocates[0];
    }
    const adv = selectedAdvocate || { name: 'Advocate Giridharan', bar_council_no: 'D/1847/2019', email: 'mgdharan7@gmail.com' };
    $('modalAdvocateName').textContent = `${adv.name} • Bar ${adv.bar_council_no}`;
    $('modalAdvocateEmail').textContent = adv.email;

    // Prefill civilian details
    let userEmail = 'mgdharan7@gmail.com';
    try {
      const raw = localStorage.getItem('nyaya_user');
      if (raw) {
        const u = JSON.parse(raw);
        if (u.email) userEmail = u.email;
      }
    } catch (e) {}
    $('modalClientEmail').value = userEmail;
    $('modalClientContact').value = '+91 98401 •••••';

    // Prefill Subject & Complaint Letter
    const questionText = $('question') ? $('question').value.trim() : 'Legal Grievance';
    $('modalGrievanceSubject').value = questionText ? questionText.slice(0, 100) : 'Legal Representation Request';

    let draftLetter = `FORMAL LEGAL COMPLAINT & CASE INSTRUCTIONS\n\n`;
    draftLetter += `DATE: ${new Date().toLocaleDateString('en-GB')}\n`;
    draftLetter += `TO: ${adv.name} (Bar Enrollment: ${adv.bar_council_no})\n`;
    draftLetter += `FROM: Civilian Client (${userEmail})\n\n`;
    draftLetter += `SUBJECT: Urgent Legal Grievance - Representation & Notice Drafting Request\n\n`;
    draftLetter += `RESPECTED COUNSEL,\n\n`;
    draftLetter += `I hereby seek your legal representation and advice regarding the following matter:\n\n`;
    draftLetter += `1. STATEMENT OF FACTS:\n${questionText || 'Grievance details as submitted on NyayaAI.'}\n\n`;
    if ($('context') && $('context').value) {
      draftLetter += `2. ADDITIONAL EVIDENCE & MATERIAL:\n${$('context').value}\n\n`;
    }
    draftLetter += `3. LEGAL RELIEF REQUESTED:\nI request you to inspect this matter under Section 132 BSA privilege, draft a formal Statutory Demand Notice, and connect with me for next steps.\n\n`;
    draftLetter += `Yours faithfully,\nClient: ${userEmail}`;

    $('modalComplaintLetter').value = draftLetter;
    sendModal.classList.remove('hidden');
  });

  const closeModal = () => sendModal.classList.add('hidden');
  if (closeSendModalBtn) closeSendModalBtn.addEventListener('click', closeModal);
  if (cancelSendModalBtn) cancelSendModalBtn.addEventListener('click', closeModal);

  if (confirmSendComplaintBtn) {
    confirmSendComplaintBtn.addEventListener('click', async () => {
      const adv = selectedAdvocate || availableAdvocates[0] || {};
      const payload = {
        civilian_name: $('modalClientEmail').value || 'Registered Civilian',
        civilian_email: $('modalClientEmail').value || 'mgdharan7@gmail.com',
        civilian_contact: $('modalClientContact').value || '+91 ••••••••••',
        jurisdiction: $('jurisdiction') ? $('jurisdiction').value : 'India',
        legal_domain: 'Civilian Legal Grievance',
        facts_summary: $('modalGrievanceSubject').value || 'Complaint submitted to Advocate',
        complaint_letter: $('modalComplaintLetter').value,
        advocate_id: adv.id || 'adv-giridharan',
        advocate_name: adv.name || 'Advocate Giridharan',
        advocate_email: adv.email || 'mgdharan7@gmail.com'
      };

      confirmSendComplaintBtn.disabled = true;
      confirmSendComplaintBtn.innerHTML = '<span>⏳ Dispatching to Advocate...</span>';

      try {
        const res = await fetch('/api/civilian/assign-complaint', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
          alert(`⚖️ SUCCESS!\n\nYour complaint letter has been assigned and dispatched to ${payload.advocate_name}.\nCase Reference: ${data.case?.case_id || 'CIV-ASSIGNED'}.\n\nYour advocate can now view your file and connect with you directly in the Advocate Console.`);
          closeModal();
        } else {
          alert(`Error: ${data.detail || 'Could not dispatch complaint.'}`);
        }
      } catch (err) {
        alert(`Failed to dispatch complaint: ${err.message}`);
      } finally {
        confirmSendComplaintBtn.disabled = false;
        confirmSendComplaintBtn.innerHTML = '<span>🚀 Confirm & Dispatch Complaint</span>';
      }
    });
  }
}

// ── Creator Profile & Contact Us Modals ──────────────────────────────────────
function openCreatorModal() {
  const m = $('creatorContactModal');
  if (m) m.classList.remove('hidden');
}

function closeCreatorModal() {
  const m = $('creatorContactModal');
  if (m) m.classList.add('hidden');
}

function openContactModal() {
  openCreatorModal();
  setTimeout(() => {
    const el = $('contactSenderName');
    if (el) el.focus();
  }, 200);
}

async function handleSendCreatorMessage(e) {
  e.preventDefault();
  const btn = $('btnSendCreatorMsg');
  const name = $('contactSenderName').value.trim();
  const email = $('contactSenderEmail').value.trim();
  const msg = $('contactSenderMsg').value.trim();
  if (!name || !email || !msg) return;

  btn.disabled = true;
  btn.textContent = 'Sending Message...';

  try {
    const res = await fetch('/api/contact-creator', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, message: msg })
    });
    const d = await res.json();
    alert(`⭐ ${d.message}`);
    $('contactSenderMsg').value = '';
    closeCreatorModal();
  } catch (err) {
    alert(`Could not send message: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Send Message to Giridharan →';
  }
}

// ── Section 63 BSA Digital Evidence Certificate Generator ────────────────────
const btnGenBSACert = $('btnGenBSACert');
const bsaModal = $('bsaCertModal');

if (btnGenBSACert && bsaModal) {
  btnGenBSACert.addEventListener('click', async () => {
    let userName = 'Deponent';
    try {
      const raw = localStorage.getItem('nyaya_user');
      if (raw) {
        const u = JSON.parse(raw);
        if (u.name || u.email) userName = u.name || u.email;
      }
    } catch (e) {}

    const q = $('question') ? $('question').value.trim() : '';
    $('bsaCertifierName').value = userName;
    $('bsaDeviceModel').value = 'Personal Smartphone / Android & iOS Computing Resource';

    try {
      const res = await fetch('/api/generate-bsa-certificate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          certifier_name: userName,
          device_model: 'Personal Smartphone / Computing Resource',
          mobile_number: '+91 98401 •••••',
          evidence_description: `WhatsApp chat transcripts, electronic UPI payment receipts, and bank transaction statements regarding: ${q.slice(0, 80) || 'disputed transaction'}`
        })
      });
      const data = await res.json();
      $('bsaCertificateText').value = data.text_content || '';
      bsaModal.classList.remove('hidden');
    } catch (err) {
      alert(`Failed to generate Section 63 BSA Certificate: ${err.message}`);
    }
  });
}

function closeBSAModal() {
  if (bsaModal) bsaModal.classList.add('hidden');
}

function copyBSACertText() {
  const text = $('bsaCertificateText').value;
  navigator.clipboard.writeText(text);
  const btn = $('btnCopyBSACert');
  btn.innerHTML = '<span>✅ Copied Certificate!</span>';
  setTimeout(() => { btn.innerHTML = '<span>📋 Copy Certificate</span>'; }, 2000);
}

// ── Police Written Complaint / FIR under Sec 173 BNSS Generator ──────────────
const btnGenPoliceFIR = $('btnGenPoliceFIR');
const policeModal = $('policeFIRModal');

if (btnGenPoliceFIR && policeModal) {
  btnGenPoliceFIR.addEventListener('click', async () => {
    let userName = 'Complainant';
    try {
      const raw = localStorage.getItem('nyaya_user');
      if (raw) {
        const u = JSON.parse(raw);
        if (u.name || u.email) userName = u.name || u.email;
      }
    } catch (e) {}

    const q = $('question') ? $('question').value.trim() : '';
    $('firComplainantName').value = userName;
    $('firPoliceStation').value = 'Cyber Crime Police Station / Local Police Station';

    try {
      const res = await fetch('/api/generate-police-complaint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          complainant_name: userName,
          complainant_address: 'Resident of India',
          complainant_phone: '+91 ••••••••••',
          police_station_name: 'The Station House Officer (SHO), Cyber Crime Police Station',
          district_city: $('jurisdiction') ? $('jurisdiction').value : 'India',
          accused_details: 'Suspect / Beneficiary Entity identified in electronic transaction and WhatsApp chats',
          facts_chronology: q || 'Chronological statement of financial loss and electronic cheating...'
        })
      });
      const data = await res.json();
      $('firComplaintText').value = data.text_content || '';
      policeModal.classList.remove('hidden');
    } catch (err) {
      alert(`Failed to generate Police FIR Complaint: ${err.message}`);
    }
  });
}

function closePoliceModal() {
  if (policeModal) policeModal.classList.add('hidden');
}

function copyPoliceFIRText() {
  const text = $('firComplaintText').value;
  navigator.clipboard.writeText(text);
  const btn = $('btnCopyPoliceFIR');
  btn.innerHTML = '<span>✅ Copied FIR Complaint!</span>';
  setTimeout(() => { btn.innerHTML = '<span>📋 Copy FIR Complaint</span>'; }, 2000);
}

initAuthHeader();
loadDocs();
loadAdvocates();
