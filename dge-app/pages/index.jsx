import { useState, useEffect, useCallback } from 'react';
import Head from 'next/head';

// ── Brand DNA ────────────────────────────────────────────────
const MY_BRANDS = {
  EE: {
    id:'EE', name:'Emmanuel Ehigbai', color:'#0F1A2E', accent:'#B8860B',
    profile: {
      positioning:'I build bridges between where businesses are and where they know they need to be.',
      audience:'CEE/Nigerian founders and SME decision-makers',
      tone:'Sharp, grounded, human, thinking-out-loud',
      voiceRules:['Short sentences — max 15 words','ZERO em dashes','ZERO AI slop','Specific: real numbers, real cities, real outcomes','Faith in values, never preachy'],
      pillars:['AI for Business','Build Logs','CEE/Africa Business Bridge','Client Results','The Solopreneur\'s Edge'],
      noFly:['game-changer','leverage','revolutionize','seamless','cutting-edge','dive into'],
      visualDNA:'Ivory #F5F0E8, Navy #0F1A2E, Gold #B8860B, Sage #4A6741. Playfair Display + Inter. Editorial, premium, founder authority. Never: corporate stock, fake smiles.',
    }
  },
  BW: {
    id:'BW', name:'BridgeWorks Studio', color:'#4A6741', accent:'#B8860B',
    profile: {
      positioning:'AI-powered consulting studio helping SMEs in Hungary/CEE and Nigeria build working digital growth systems.',
      audience:'SME founders and directors in Hungary, CEE, and Nigeria',
      tone:'Studio precision — deliverables and outcomes, not promises',
      voiceRules:['Studio voice: precision, capability, proof','Deliverables not promises','Short sentences backed by numbers','ZERO em dashes, ZERO AI slop'],
      pillars:['Digital Growth','AI Implementation','GEO Visibility','Client Results','SME Strategy'],
      noFly:['passionate about','holistic','innovative','solutions-driven'],
      visualDNA:'Ivory #F5F0E8, Sage #4A6741, Gold #B8860B, Navy #0F1A2E. Inter. Modern studio, clean systems. Never: generic agency stock.',
    }
  },
  MK: {
    id:'MK', name:'MindOfAKing', color:'#1C2B3A', accent:'#B8860B',
    profile: {
      positioning:'Nigerian poet in Budapest writing at the intersection of faith, identity, and displacement.',
      audience:'Diaspora creatives, faith community, fellow poets',
      tone:'Raw and honest — words that land, not words that fill space',
      voiceRules:['Raw and honest OVER polished','Faith-rooted naturally, never preachy','Nigerian AND Budapest context — both present','Short deliberate lines','ZERO em dashes'],
      pillars:['Faith & Life','Nigerian in Budapest','Inner Growth','Poetry','Creative Process'],
      noFly:['inspirational','motivational','hustle','grind'],
      visualDNA:'Deep Navy #1C2B3A, Gold #B8860B, Ivory #F5F0E8. Poetic, contemplative, moody. Faith-rooted without religious imagery.',
    }
  },
};

// ── Storage helpers ──────────────────────────────────────────
const LS = {
  get: (k) => { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : null; } catch { return null; } },
  set: (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
  del: (k) => { try { localStorage.removeItem(k); } catch {} },
};

// ── API call ─────────────────────────────────────────────────
function parseJSON(t) {
  try { return JSON.parse(t.replace(/```json\s*/g,'').replace(/```\s*/g,'').trim()); }
  catch { return null; }
}
async function callAI(system, user, maxTokens = 1400) {
  const res = await fetch('/api/claude', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ system, user, max_tokens: maxTokens }),
  });
  const data = await res.json();
  if (data.error) throw new Error(data.error.message || data.error);
  return parseJSON(data.content?.find(b => b.type === 'text')?.text || '');
}

// ── Build system prompt ──────────────────────────────────────
function buildSys(brand, profile, intel) {
  const p = profile || brand.profile || {};
  let s = `You write content for ${brand.name}.\n`;
  if (p.positioning) s += `Positioning: ${p.positioning}\n`;
  if (p.audience) s += `Audience: ${p.audience}\n`;
  if (p.tone) s += `Tone: ${p.tone}\n`;
  if (p.voiceRules?.length) s += `Voice rules: ${p.voiceRules.join('; ')}\n`;
  if (p.noFly?.length) s += `Never use these phrases: ${p.noFly.join(', ')}\n`;
  if (p.visualDNA) s += `Visual DNA: ${p.visualDNA}\n`;
  if (intel) {
    s += `\nContent intelligence (${intel.postCount || '?'} posts analyzed):\n`;
    s += `Voice fingerprint: ${intel.voiceFingerprint}\n`;
    s += `What works: ${intel.whatWorked}\n`;
    s += `Continuity to preserve: ${intel.continuityNotes}\n`;
    if (intel.contentGaps?.length) s += `Content gaps to address: ${intel.contentGaps.join(', ')}\n`;
  }
  s += 'Return only valid JSON.';
  return s;
}

// ── Shared UI ─────────────────────────────────────────────────
const C = { iv:'#F5F0E8', nv:'#0F1A2E', gd:'#B8860B', sg:'#4A6741', wg:'#6B6560', lc:'#E0D9CE', ow:'#F9F5EE' };

function CopyBtn({ text, label = 'Copy', sm }) {
  const [done, setDone] = useState(false);
  const copy = () => { navigator.clipboard.writeText(text); setDone(true); setTimeout(() => setDone(false), 2000); };
  return (
    <button onClick={copy} style={{ padding: sm ? '3px 8px' : '5px 12px', borderRadius: 5, border: `1px solid ${C.lc}`, background: C.iv, fontSize: sm ? 10 : 11, cursor: 'pointer', color: C.nv, fontWeight: 600, flexShrink: 0 }}>
      {done ? 'Copied!' : label}
    </button>
  );
}

function Skel() {
  return (
    <div>
      {[80, 55, 90, 45, 70].map((w, i) => (
        <div key={i} style={{ height: 9, width: `${w}%`, background: '#E0D9CE', borderRadius: 3, marginBottom: 8, animation: `sk 1.4s ease-in-out infinite`, animationDelay: `${i * 0.12}s` }} />
      ))}
    </div>
  );
}

function Lbl({ t, c }) {
  return <div style={{ fontSize: 10, fontWeight: 700, color: c || C.wg, letterSpacing: '0.07em', textTransform: 'uppercase', marginBottom: 5 }}>{t}</div>;
}

function Fld({ label, val, onChange, placeholder, rows = 3, inline = false }) {
  const s = { width: '100%', padding: '8px 10px', border: `1px solid ${C.lc}`, borderRadius: 6, background: '#fff', fontSize: 12, color: C.nv, lineHeight: '1.6', outline: 'none', fontFamily: 'inherit', resize: inline ? 'none' : 'vertical', boxSizing: 'border-box' };
  return (
    <div style={{ marginBottom: 10 }}>
      {label && <div style={{ fontSize: 11, color: C.wg, marginBottom: 4, fontWeight: 500 }}>{label}</div>}
      {inline
        ? <input value={val} onChange={e => onChange(e.target.value)} placeholder={placeholder} style={{ ...s, height: 36 }} />
        : <textarea value={val} onChange={e => onChange(e.target.value)} placeholder={placeholder} rows={rows} style={s} />}
    </div>
  );
}

function PBtn({ label, onClick, disabled, color, full, sm }) {
  return (
    <button onClick={onClick} disabled={disabled} style={{
      padding: sm ? '6px 12px' : '10px 18px', width: full ? '100%' : undefined,
      background: disabled ? '#E8E1D8' : color || C.nv, color: disabled ? '#9B8E82' : color === C.gd ? C.nv : C.iv,
      border: 'none', borderRadius: 7, fontSize: sm ? 11 : 13, fontWeight: 700,
      cursor: disabled ? 'not-allowed' : 'pointer',
    }}>{label}</button>
  );
}

function ErrBox({ msg }) {
  return msg ? <div style={{ padding: '8px 10px', background: '#FEE2E2', color: '#DC2626', borderRadius: 5, fontSize: 12, marginBottom: 10 }}>{msg}</div> : null;
}

function Card({ children, accent, style = {} }) {
  return (
    <div style={{ border: `1px solid ${C.lc}`, borderTop: `3px solid ${accent || C.gd}`, borderRadius: 8, background: '#fff', padding: 14, marginBottom: 10, ...style }}>
      {children}
    </div>
  );
}

// ── DISCOVER ─────────────────────────────────────────────────
function DiscoverView({ intake, existingProfile, onSave }) {
  const [src, setSrc] = useState('');
  const [result, setResult] = useState(existingProfile || null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  const [saved, setSaved] = useState(!!existingProfile);

  const run = async () => {
    setErr(''); setLoading(true); setResult(null); setSaved(false);
    try {
      const iStr = intake ? Object.entries(intake).filter(([k, v]) => v && k !== 'mode').map(([k, v]) => `${k}: ${v}`).join('\n') : '';
      const user = `${iStr ? `CLIENT INTAKE:\n${iStr}\n\n` : ''}${src ? `SOURCE MATERIAL:\n${src}\n\n` : ''}Extract a complete brand content profile. Return ONLY this JSON:\n{"businessName":"name","tagline":"short positioning","whatTheyDo":"1-2 sentences","whoTheyServe":"specific audience","tone":"tone descriptors","voiceRules":["rule 1","rule 2","rule 3","rule 4","rule 5"],"noFly":["phrase 1","phrase 2","phrase 3","phrase 4"],"visualDirection":"colors, style, mood","contentPillars":["pillar 1","pillar 2","pillar 3","pillar 4","pillar 5"],"ctaStyle":"how they invite action","keyMessages":["message 1","message 2","message 3"]}`;
      const r = await callAI('You are an expert brand strategist. Extract a precise, actionable brand content profile from any input. Be specific — never generic. Return only valid JSON.', user, 1200);
      setResult(r);
    } catch (e) { setErr(e.message); }
    setLoading(false);
  };

  return (
    <div>
      <Fld val={src} onChange={setSrc} rows={6} label="Source material — paste website copy, social bios, old posts, or any brand text"
        placeholder={'Paste any combination of:\n• Website copy / About page\n• Instagram or LinkedIn bio and posts\n• Business description\n• Old captions or marketing copy\n\nLeave blank to extract from intake data only.'} />
      <ErrBox msg={err} />
      <div style={{ display: 'flex', gap: 8, marginBottom: 14, flexWrap: 'wrap' }}>
        <PBtn label={loading ? 'Extracting...' : 'Extract Brand Profile →'} onClick={run} disabled={loading} />
        {result && !saved && <PBtn label="Save Profile →" onClick={() => { onSave(result); setSaved(true); }} color={C.gd} />}
        {saved && <span style={{ color: '#2D6A4F', fontWeight: 700, fontSize: 13, padding: '10px 0' }}>✓ Profile saved</span>}
      </div>
      {loading && <Skel />}
      {result && !loading && (
        <Card accent={C.nv}>
          <div style={{ fontSize: 16, fontWeight: 700, color: C.nv, marginBottom: 2 }}>{result.businessName}</div>
          {result.tagline && <div style={{ fontSize: 12, color: C.wg, fontStyle: 'italic', marginBottom: 12 }}>{result.tagline}</div>}
          {[['What they do', result.whatTheyDo], ['Who they serve', result.whoTheyServe], ['Tone', result.tone]].map(([k, v]) => v && (
            <div key={k} style={{ marginBottom: 8 }}>
              <Lbl t={k} />
              <div style={{ fontSize: 12, color: C.nv, lineHeight: '1.6' }}>{v}</div>
            </div>
          ))}
          {result.contentPillars?.length > 0 && (
            <div style={{ marginBottom: 8 }}>
              <Lbl t="Content Pillars" />
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 5 }}>
                {result.contentPillars.map((p, i) => (
                  <span key={i} style={{ padding: '3px 10px', borderRadius: 4, background: `${C.nv}15`, border: `1px solid ${C.nv}30`, fontSize: 11, fontWeight: 600, color: C.nv }}>{p}</span>
                ))}
              </div>
            </div>
          )}
          {result.voiceRules?.length > 0 && (
            <div style={{ marginBottom: 8 }}>
              <Lbl t="Voice Rules" />
              {result.voiceRules.map((r, i) => <div key={i} style={{ fontSize: 11, color: C.nv, lineHeight: '1.6', marginBottom: 2 }}>— {r}</div>)}
            </div>
          )}
          {result.noFly?.length > 0 && (
            <div>
              <Lbl t="Avoid" c="#C0392B" />
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                {result.noFly.map((n, i) => <span key={i} style={{ padding: '2px 8px', borderRadius: 4, background: '#FFF4F4', border: '1px solid #F0C0C0', fontSize: 11, color: '#C0392B' }}>✕ {n}</span>)}
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}

// ── INTELLIGENCE ─────────────────────────────────────────────
function IntelView({ brand, profile, intel, onSave }) {
  const [posts, setPosts] = useState('');
  const [notes, setNotes] = useState('');
  const [result, setResult] = useState(intel || null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');

  useEffect(() => setResult(intel || null), [intel]);

  const run = async () => {
    if (!posts.trim()) { setErr('Paste past posts first.'); return; }
    setErr(''); setLoading(true);
    try {
      const count = posts.split(/\n---+\n|\n\n\n+/).filter(p => p.trim().length > 20).length;
      const p = profile || brand.profile || {};
      const user = `Brand: ${brand.name}\n${p.positioning ? `Positioning: ${p.positioning}\n` : ''}\nPast posts:\n${posts}\n${notes ? `\nPerformance notes:\n${notes}` : ''}\n\nReturn ONLY this JSON:\n{"voiceFingerprint":"how this brand actually sounds — evidence from posts","writingPatterns":["pattern 1","pattern 2","pattern 3"],"topTopics":["topic 1","topic 2","topic 3"],"whatWorked":"what generates engagement","whatDidnt":"weak patterns","continuityNotes":"CRITICAL — what must be preserved for recognition","avoidRepeating":["thing 1","thing 2"],"contentGaps":["gap 1","gap 2","gap 3"],"repurposeCandidates":["strong post worth repurposing","second candidate"],"nextIdeas":["specific idea 1","idea 2","idea 3","idea 4","idea 5"],"recommendations":["recommendation 1","recommendation 2","recommendation 3"],"postCount":${count}}`;
      const r = await callAI('You are an expert content analyst. Analyze past posts for precise, actionable intelligence. Be specific — reference actual patterns. Return only valid JSON.', user, 1500);
      if (r) {
        const m = { ...r, date: new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) };
        setResult(m); onSave(m);
      }
    } catch (e) { setErr(e.message); }
    setLoading(false);
  };

  return (
    <div>
      {result && (
        <div style={{ padding: '8px 12px', background: '#F0FBF5', border: '1px solid #A8D5B8', borderRadius: 6, marginBottom: 12, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ fontSize: 12, color: '#2D6A4F', fontWeight: 600 }}>✓ Intelligence active — {result.postCount} posts analyzed ({result.date})</div>
          <button onClick={() => setResult(null)} style={{ fontSize: 11, color: C.wg, background: 'none', border: 'none', cursor: 'pointer' }}>Update</button>
        </div>
      )}
      <Fld val={posts} onChange={setPosts} rows={7} label="Past posts — separate with --- or blank lines"
        placeholder={'Paste 5-20 past posts.\nSeparate with --- or double blank lines.\n\nExample:\nMost businesses need a better system.\n---\nI built a website from zero. No code.'} />
      <Fld val={notes} onChange={setNotes} rows={2} label="Performance notes (optional)"
        placeholder="e.g. 'AI post got 3x reach' or 'corporate posts got no comments'" />
      <ErrBox msg={err} />
      <PBtn label={loading ? 'Analyzing...' : 'Analyze Past Content →'} onClick={run} disabled={loading || !posts.trim()} full color="#1B3A2B" />
      {loading && <div style={{ marginTop: 12 }}><Skel /></div>}
      {result && !loading && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 14 }}>
          <Card accent="#1B3A2B">
            <Lbl t="Voice Fingerprint" c="#1B3A2B" />
            <div style={{ fontSize: 12, color: C.nv, lineHeight: '1.7', marginBottom: 8 }}>{result.voiceFingerprint}</div>
            {result.writingPatterns?.map((p, i) => <div key={i} style={{ fontSize: 11, color: C.wg, marginBottom: 2 }}>— {p}</div>)}
          </Card>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
            <Card accent="#4A9B6F" style={{ marginBottom: 0 }}>
              <Lbl t="What Worked" c="#2D6A4F" />
              <div style={{ fontSize: 11, color: C.nv, lineHeight: '1.65', marginBottom: 8 }}>{result.whatWorked}</div>
              {result.topTopics?.map((t, i) => <div key={i} style={{ fontSize: 10, color: '#2D6A4F', marginBottom: 2 }}>✓ {t}</div>)}
            </Card>
            <Card accent="#C0392B" style={{ marginBottom: 0 }}>
              <Lbl t="What Didn't" c="#C0392B" />
              <div style={{ fontSize: 11, color: C.nv, lineHeight: '1.65', marginBottom: 8 }}>{result.whatDidnt}</div>
              {result.avoidRepeating?.map((t, i) => <div key={i} style={{ fontSize: 10, color: '#C0392B', marginBottom: 2 }}>✕ {t}</div>)}
            </Card>
          </div>
          <Card accent={C.gd}>
            <Lbl t="Continuity — Must Preserve" c={C.gd} />
            <div style={{ fontSize: 12, color: C.nv, lineHeight: '1.7' }}>{result.continuityNotes}</div>
          </Card>
          <Card accent="#0A66C2">
            <Lbl t="Content Gaps" c="#0A66C2" />
            {result.contentGaps?.map((g, i) => <div key={i} style={{ fontSize: 11, color: C.nv, marginBottom: 3 }}>→ {g}</div>)}
          </Card>
          <Card accent={C.nv}>
            <Lbl t="Next 5 Content Ideas" c={C.nv} />
            {result.nextIdeas?.map((idea, i) => (
              <div key={i} style={{ display: 'flex', justifyContent: 'space-between', gap: 8, padding: '6px 8px', background: C.ow, borderRadius: 5, marginBottom: 4 }}>
                <div style={{ fontSize: 11, color: C.nv, flex: 1 }}><b style={{ color: C.gd }}>{i + 1}.</b> {idea}</div>
                <CopyBtn text={idea} sm label="Use" />
              </div>
            ))}
          </Card>
          {result.repurposeCandidates?.length > 0 && (
            <Card accent="#833AB4">
              <Lbl t="Repurpose Candidates" c="#833AB4" />
              {result.repurposeCandidates.map((r, i) => (
                <div key={i} style={{ display: 'flex', justifyContent: 'space-between', gap: 8, padding: '6px 8px', background: C.ow, borderRadius: 5, marginBottom: 4 }}>
                  <div style={{ fontSize: 11, color: C.nv, fontStyle: 'italic', flex: 1 }}>{r}</div>
                  <CopyBtn text={r} sm />
                </div>
              ))}
            </Card>
          )}
        </div>
      )}
    </div>
  );
}

// ── PLAN ─────────────────────────────────────────────────────
function PlanView({ brand, profile, intel }) {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  const [open, setOpen] = useState(0);

  const run = async () => {
    setErr(''); setLoading(true); setResult(null);
    try {
      const p = profile || brand.profile || {};
      const user = `Brand: ${brand.name}\nPillars: ${(p.contentPillars || p.pillars || []).join(', ')}\nAudience: ${p.audience || ''}\nTone: ${p.tone || ''}\n${intel ? `What works: ${intel.whatWorked || ''}\nContent gaps: ${(intel.contentGaps || []).join(', ')}` : ''}\n\nGenerate a practical 30-day content plan across 4 weeks. Each post must have specific hooks and ideas — no generic placeholders. Return ONLY this JSON:\n{"weeks":[{"week":1,"theme":"weekly theme","rationale":"why this theme now","posts":[{"day":"Mon","platform":"LinkedIn","format":"long-form post","pillar":"pillar name","hook":"specific hook line","idea":"specific content idea","cta":"specific CTA"},{"day":"Wed","platform":"Instagram","format":"Carousel","pillar":"pillar","hook":"hook","idea":"idea","cta":"cta"},{"day":"Fri","platform":"TikTok","format":"Talking head 30 sec","pillar":"pillar","hook":"hook","idea":"idea","cta":"cta"}]},{"week":2,"theme":"theme","rationale":"rationale","posts":[{"day":"Mon","platform":"LinkedIn","format":"post","pillar":"p","hook":"h","idea":"i","cta":"c"},{"day":"Wed","platform":"Instagram","format":"Reel","pillar":"p","hook":"h","idea":"i","cta":"c"},{"day":"Fri","platform":"X","format":"Thread","pillar":"p","hook":"h","idea":"i","cta":"c"}]},{"week":3,"theme":"theme","rationale":"rationale","posts":[{"day":"Tue","platform":"LinkedIn","format":"post","pillar":"p","hook":"h","idea":"i","cta":"c"},{"day":"Thu","platform":"Instagram","format":"Carousel","pillar":"p","hook":"h","idea":"i","cta":"c"},{"day":"Sat","platform":"WhatsApp","format":"Status","pillar":"p","hook":"h","idea":"i","cta":"c"}]},{"week":4,"theme":"theme","rationale":"rationale","posts":[{"day":"Mon","platform":"LinkedIn","format":"post","pillar":"p","hook":"h","idea":"i","cta":"c"},{"day":"Wed","platform":"TikTok","format":"Talking head","pillar":"p","hook":"h","idea":"i","cta":"c"},{"day":"Fri","platform":"Instagram","format":"Carousel","pillar":"p","hook":"h","idea":"i","cta":"c"}]}],"monthGoal":"what this plan achieves","cadenceSummary":"posting rhythm"}`;
      const r = await callAI('You are an expert content strategist. Generate a practical, specific 30-day content plan. Return only valid JSON.', user, 1800);
      setResult(r);
    } catch (e) { setErr(e.message); }
    setLoading(false);
  };

  const PC = { LinkedIn: '#0A66C2', Instagram: '#E1306C', TikTok: '#FF004F', X: '#1A1A1A', WhatsApp: '#128C7E', Facebook: '#1877F2', Reel: '#833AB4' };

  return (
    <div>
      <ErrBox msg={err} />
      <PBtn label={loading ? 'Generating 30-day plan...' : 'Generate 30-Day Plan →'} onClick={run} disabled={loading} full color={C.sg} />
      {loading && <div style={{ marginTop: 12 }}><Skel /></div>}
      {result && !loading && (
        <div style={{ marginTop: 14 }}>
          {result.monthGoal && (
            <div style={{ padding: '12px 14px', background: C.nv, borderRadius: 8, marginBottom: 12 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: C.gd, textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 4 }}>Month Goal</div>
              <div style={{ fontSize: 12, color: C.iv, lineHeight: '1.6' }}>{result.monthGoal}</div>
              {result.cadenceSummary && <div style={{ fontSize: 11, color: 'rgba(245,240,232,0.45)', marginTop: 4 }}>{result.cadenceSummary}</div>}
            </div>
          )}
          {result.weeks?.map((week, wi) => (
            <div key={wi} style={{ marginBottom: 6, border: `1px solid ${C.lc}`, borderRadius: 8, overflow: 'hidden' }}>
              <button onClick={() => setOpen(open === wi ? -1 : wi)} style={{ width: '100%', padding: '11px 14px', background: open === wi ? C.nv : C.ow, border: 'none', cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontFamily: 'inherit' }}>
                <div style={{ textAlign: 'left' }}>
                  <div style={{ fontSize: 12, fontWeight: 700, color: open === wi ? C.iv : C.nv }}>Week {week.week}: {week.theme}</div>
                  <div style={{ fontSize: 10, color: open === wi ? 'rgba(245,240,232,0.5)' : C.wg, marginTop: 2 }}>{week.rationale}</div>
                </div>
                <span style={{ color: open === wi ? C.iv : C.wg, fontSize: 12 }}>{open === wi ? '▲' : '▼'}</span>
              </button>
              {open === wi && (
                <div style={{ padding: 10, background: '#fff' }}>
                  {week.posts?.map((post, pi) => (
                    <div key={pi} style={{ padding: '9px 11px', background: C.ow, borderRadius: 6, borderLeft: `3px solid ${PC[post.platform] || C.nv}`, marginBottom: 5 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 5, flexWrap: 'wrap', gap: 4 }}>
                        <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap' }}>
                          <span style={{ fontSize: 10, fontWeight: 700, color: PC[post.platform] || C.nv }}>{post.day}</span>
                          <span style={{ fontSize: 10, color: C.wg }}>{post.platform}</span>
                          <span style={{ fontSize: 9, color: C.wg, background: C.lc, padding: '1px 6px', borderRadius: 3 }}>{post.format}</span>
                          <span style={{ fontSize: 9, color: C.gd, fontWeight: 600 }}>{post.pillar}</span>
                        </div>
                        <CopyBtn text={`${post.day} | ${post.platform} | ${post.format}\nHook: ${post.hook}\nIdea: ${post.idea}\nCTA: ${post.cta}`} sm />
                      </div>
                      <div style={{ fontSize: 12, fontWeight: 600, color: C.nv, marginBottom: 2 }}>{post.hook}</div>
                      <div style={{ fontSize: 11, color: C.wg, marginBottom: 2 }}>{post.idea}</div>
                      <div style={{ fontSize: 10, color: '#9B8E82' }}>CTA: {post.cta}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ── GENERATE ─────────────────────────────────────────────────
const PLATS = [
  { id:'li', name:'LinkedIn', icon:'in', color:'#0A66C2', desc:'Authority post', q:(i,c)=>`Core idea: "${i}"${c?`\nContext: ${c}`:''}\nReturn ONLY: {"post":"Full post. \\n for line breaks. First 2 lines = standalone hook. Max 3 lines/para. No hashtags in body. End with thought or question."}` },
  { id:'ig', name:'Carousel', icon:'IG', color:'#E1306C', desc:'6-slide Instagram', q:(i,c)=>`Core idea: "${i}"${c?`\nContext: ${c}`:''}\nReturn ONLY: {"slides":["Slide 1: bold hook — one line","Slide 2: problem/tension","Slide 3: insight 1 — headline + sentence","Slide 4: insight 2 — headline + sentence","Slide 5: takeaway","Slide 6: CTA"],"caption":"2-3 lines + CTA."}` },
  { id:'rl', name:'Reel Script', icon:'▶', color:'#833AB4', desc:'30-45 sec', q:(i,c)=>`Core idea: "${i}"${c?`\nContext: ${c}`:''}\nReturn ONLY: {"hook":"First 3 sec. One striking line.","script":"Full spoken script. Natural. Short sentences. 30-40 sec.","caption":"2-3 lines + CTA."}` },
  { id:'tk', name:'TikTok', icon:'♪', color:'#FF004F', desc:'20-35 sec', q:(i,c)=>`Core idea: "${i}"${c?`\nContext: ${c}`:''}\nReturn ONLY: {"screen_hook":"MAX 5 words on screen.","spoken_script":"Fast. Short sentences. 20-25 sec.","caption":"1-2 lines. 2-3 hashtags."}` },
  { id:'x', name:'X / Twitter', icon:'𝕏', color:'#1A1A1A', desc:'Post + thread', q:(i,c)=>`Core idea: "${i}"${c?`\nContext: ${c}`:''}\nReturn ONLY: {"single_post":"1-2 sharp sentences. Under 280 chars.","thread":["Tweet 1: hook","Tweet 2: tension","Tweet 3: reframe","Tweet 4: proof","Tweet 5: CTA"]}` },
  { id:'wa', name:'WhatsApp', icon:'W', color:'#128C7E', desc:'Status + broadcast', q:(i,c)=>`Core idea: "${i}"${c?`\nContext: ${c}`:''}\nReturn ONLY: {"status_frames":["Frame 1: hook","Frame 2: insight","Frame 3: proof","Frame 4: CTA"],"broadcast":"3-5 lines. Warm, direct."}` },
];

function GenCard({ platform, result, loading }) {
  const ROW = { border: `1px solid ${C.lc}`, borderRadius: 6, padding: '10px 12px', marginBottom: 4, fontSize: 12, lineHeight: '1.7', color: C.nv, whiteSpace: 'pre-wrap', background: '#fff' };
  const renderers = {
    li: ({ d }) => !d?.post ? null : <div><div style={{ display:'flex', justifyContent:'flex-end', marginBottom:6 }}><CopyBtn text={d.post} /></div><div style={{ ...ROW, border:'1px solid #D0DEF0', padding:14, fontSize:13, lineHeight:'1.85' }}>{d.post}</div></div>,
    ig: ({ d }) => { if (!d?.slides) return null; const all = d.slides.map((s,i) => `SLIDE ${i+1}:\n${s}`).join('\n\n') + (d.caption ? `\n\nCAPTION:\n${d.caption}` : ''); return <div><div style={{ display:'flex', justifyContent:'flex-end', marginBottom:6 }}><CopyBtn text={all} /></div>{d.slides.map((s,i) => <div key={i} style={ROW}><Lbl t={`Slide ${i+1}`} c="#E1306C" />{s}</div>)}{d.caption && <div style={{ ...ROW, background:'#FEF0F5' }}><Lbl t="Caption" c="#E1306C" />{d.caption}</div>}</div>; },
    rl: ({ d }) => { if (!d?.script) return null; const all = `HOOK:\n${d.hook}\n\nSCRIPT:\n${d.script}\n\nCAPTION:\n${d.caption}`; return <div><div style={{ display:'flex', justifyContent:'flex-end', marginBottom:6 }}><CopyBtn text={all} /></div>{[['HOOK',d.hook,'#833AB4'],['SCRIPT',d.script,'#5B2D8E'],['CAPTION',d.caption,'#833AB4']].map(([l,t,c],i) => <div key={i} style={ROW}><Lbl t={l} c={c} />{t}</div>)}</div>; },
    tk: ({ d }) => { if (!d?.spoken_script) return null; const all = `ON SCREEN:\n${d.screen_hook}\n\nSPOKEN:\n${d.spoken_script}\n\nCAPTION:\n${d.caption}`; return <div><div style={{ display:'flex', justifyContent:'flex-end', marginBottom:6 }}><CopyBtn text={all} /></div><div style={{ ...ROW, border:'2px solid #FF004F' }}><Lbl t="ON SCREEN" c="#FF004F" /><div style={{ fontSize:18, fontWeight:700, color:'#FF004F' }}>{d.screen_hook}</div></div><div style={ROW}><Lbl t="SPOKEN" />{d.spoken_script}</div><div style={ROW}><Lbl t="CAPTION" c={C.wg} />{d.caption}</div></div>; },
    x: ({ d }) => { if (!d?.single_post) return null; const thr = (d.thread||[]).map((t,i) => `${i+1}/ ${t}`).join('\n\n'); return <div><div style={{ marginBottom:10 }}><div style={{ display:'flex', justifyContent:'space-between', marginBottom:4 }}><Lbl t="Single Post" /><CopyBtn text={d.single_post} sm /></div><div style={{ ...ROW, border:'2px solid #1A1A1A', borderRadius:12, fontSize:13, fontWeight:500 }}>{d.single_post}</div></div><div style={{ display:'flex', justifyContent:'space-between', marginBottom:4 }}><Lbl t="Thread" /><CopyBtn text={thr} sm /></div>{(d.thread||[]).map((tw,i) => <div key={i} style={{ ...ROW, marginBottom:4 }}><span style={{ fontWeight:800 }}>{i+1}/</span> {tw}</div>)}</div>; },
    wa: ({ d }) => { if (!d?.status_frames) return null; const all = `STATUS:\n${(d.status_frames||[]).map((f,i) => `Frame ${i+1}: ${f}`).join('\n')}\n\nBROADCAST:\n${d.broadcast}`; return <div><div style={{ display:'flex', justifyContent:'flex-end', marginBottom:6 }}><CopyBtn text={all} /></div><Lbl t="Status Frames" c="#128C7E" /><div style={{ display:'flex', gap:5, marginBottom:10, flexWrap:'wrap' }}>{(d.status_frames||[]).map((f,i) => <div key={i} style={{ background:'#128C7E', borderRadius:7, padding:'9px 10px', fontSize:11, lineHeight:'1.6', color:'#fff', flex:'1', minWidth:90 }}><div style={{ fontSize:8, opacity:.6, marginBottom:2, fontWeight:700 }}>Frame {i+1}</div>{f}</div>)}</div><Lbl t="Broadcast" c="#128C7E" /><div style={{ background:'#DCF8C6', borderRadius:8, padding:12, fontSize:12, lineHeight:'1.75', color:C.nv }}>{d.broadcast}</div></div>; },
  };
  const Renderer = renderers[platform.id];
  return (
    <div style={{ border:`1px solid ${C.lc}`, borderTop:`3px solid ${platform.color}`, borderRadius:8, background:C.ow, padding:14, marginBottom:8 }}>
      <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:12 }}>
        <div style={{ width:24, height:24, background:platform.color, borderRadius:4, display:'flex', alignItems:'center', justifyContent:'center', fontSize:10, fontWeight:800, color:'#fff', flexShrink:0 }}>{platform.icon}</div>
        <div style={{ flex:1 }}><div style={{ fontSize:12, fontWeight:700, color:C.nv }}>{platform.name}</div><div style={{ fontSize:10, color:C.wg }}>{platform.desc}</div></div>
        {loading && <div style={{ fontSize:10, color:platform.color, fontWeight:600 }}>Writing...</div>}
      </div>
      {loading && <Skel />}
      {!loading && result && Renderer && <Renderer d={result} />}
      {!loading && !result && <div style={{ textAlign:'center', padding:12, color:'#C0B8B0', fontSize:11 }}>Failed — try again.</div>}
    </div>
  );
}

function GenerateView({ brand, profile, intel }) {
  const [idea, setIdea] = useState('');
  const [ctx, setCtx] = useState('');
  const [sel, setSel] = useState(['li','ig','tk','x','wa']);
  const [copyRes, setCopyRes] = useState({});
  const [copyLoad, setCopyLoad] = useState({});
  const [canva, setCanva] = useState(null);
  const [img, setImg] = useState(null);
  const [cLoad, setCLoad] = useState(false);
  const [iLoad, setILoad] = useState(false);
  const [gen, setGen] = useState(false);
  const [tab, setTab] = useState('copy');
  const [err, setErr] = useState('');
  const toggle = pid => setSel(s => s.includes(pid) ? s.filter(x => x !== pid) : [...s, pid]);
  const sys = buildSys(brand, profile, intel);

  const run = useCallback(async () => {
    if (!idea.trim()) { setErr('Enter a core idea.'); return; }
    if (!sel.length) { setErr('Select at least one platform.'); return; }
    setErr(''); setGen(true); setCopyRes({}); setCanva(null); setImg(null); setTab('copy');
    const nl = {}; sel.forEach(p => { nl[p] = true; }); setCopyLoad(nl);
    setCLoad(true); setILoad(true);
    const plats = PLATS.filter(p => sel.includes(p.id));
    await Promise.allSettled([
      ...plats.map(async p => {
        try { const r = await callAI(sys, p.q(idea.trim(), ctx.trim())); setCopyRes(prev => ({ ...prev, [p.id]: r })); }
        catch { setCopyRes(prev => ({ ...prev, [p.id]: null })); }
        setCopyLoad(l => ({ ...l, [p.id]: false }));
      }),
      (async () => {
        try { setCanva(await callAI(sys, `Core idea: "${idea}"${ctx ? `\nContext: ${ctx}` : ''}\nReturn ONLY Canva carousel brief JSON:\n{"brief_title":"title","brand_specs":{"primary_color":"hex","secondary_color":"hex","accent_color":"hex","headline_font":"font","body_font":"font","background":"desc"},"slide_briefs":[{"slide":1,"type":"Hook","headline":"exact text","body":"body","visual_note":"visual","layout":"layout"},{"slide":2,"type":"Problem","headline":"text","body":"","visual_note":"v","layout":"l"},{"slide":3,"type":"Insight 1","headline":"text","body":"","visual_note":"v","layout":"l"},{"slide":4,"type":"Insight 2","headline":"text","body":"","visual_note":"v","layout":"l"},{"slide":5,"type":"Takeaway","headline":"text","body":"","visual_note":"v","layout":"l"},{"slide":6,"type":"CTA","headline":"text","body":"","visual_note":"v","layout":"l"}],"canva_notes":"assembly notes"}`)); }
        catch { setCanva(null); } setCLoad(false);
      })(),
      (async () => {
        try { setImg(await callAI(sys, `Core idea: "${idea}"${ctx ? `\nContext: ${ctx}` : ''}\nReturn ONLY GPT Image 2 prompt JSON:\n{"prompt":"Complete 150-200 word prompt for ChatGPT Thinking Mode. Scene, subject, mood, lighting, style, exact palette with hex codes, what to avoid.","aspect_ratio":"4:5 or 9:16 or 1:1","usage":"carousel cover / story / reel cover / header","variations":["variation 1","variation 2"]}`)); }
        catch { setImg(null); } setILoad(false);
      })(),
    ]);
  }, [idea, ctx, sel, sys]);

  const anyLoad = Object.values(copyLoad).some(Boolean) || cLoad || iLoad;
  const active = PLATS.filter(p => sel.includes(p.id));
  const ROW = { border:`1px solid ${C.lc}`, borderRadius:6, padding:'10px 12px', marginBottom:4, fontSize:12, lineHeight:'1.7', color:C.nv, whiteSpace:'pre-wrap', background:'#fff' };

  return (
    <div>
      {intel && <div style={{ padding:'7px 12px', background:'#F0FBF5', border:'1px solid #A8D5B8', borderRadius:6, marginBottom:12, fontSize:11, color:'#2D6A4F', fontWeight:600 }}>🧠 Intelligence active — {intel.postCount} posts analyzed ({intel.date}). Generation informed by what works for {brand.name}.</div>}
      <Fld val={idea} onChange={setIdea} rows={3} label="Core Idea *" placeholder="Specific. Concrete. One sharp point — real outcome or proof, not a vague topic." />
      <Fld val={ctx} onChange={setCtx} rows={2} label="Context (optional)" placeholder="Real data, must-mentions, what NOT to say..." />
      <div style={{ marginBottom:10 }}>
        <div style={{ fontSize:12, color:C.wg, marginBottom:6, fontWeight:500 }}>Platforms ({sel.length} selected)</div>
        <div style={{ display:'flex', gap:5, flexWrap:'wrap' }}>
          {PLATS.map(p => { const on = sel.includes(p.id); return (
            <button key={p.id} onClick={() => toggle(p.id)} style={{ display:'flex', alignItems:'center', gap:5, padding:'5px 10px', borderRadius:5, border:`1px solid ${on ? p.color : C.lc}`, background: on ? `${p.color}18` : '#fff', cursor:'pointer', fontFamily:'inherit' }}>
              <div style={{ width:16, height:16, background: on ? p.color : '#D4C8B8', borderRadius:3, display:'flex', alignItems:'center', justifyContent:'center', fontSize:8, fontWeight:800, color:'#fff' }}>{p.icon}</div>
              <span style={{ fontSize:11, fontWeight: on ? 700 : 400, color: on ? p.color : C.wg }}>{p.name}</span>
            </button>);
          })}
        </div>
      </div>
      <ErrBox msg={err} />
      <PBtn label={anyLoad ? 'Generating full pack...' : 'Generate production pack →'} onClick={run} disabled={anyLoad || !idea.trim() || !sel.length} full />
      {gen && (
        <div style={{ marginTop:14 }}>
          <div style={{ display:'flex', gap:2, borderBottom:`1px solid ${C.lc}`, marginBottom:14 }}>
            {[{id:'copy',label:'Copy',icon:'✍️'},{id:'canva',label:'Canva Brief',icon:'📐'},{id:'image',label:'GPT Image 2',icon:'🎨'}].map(t => {
              const l = t.id==='canva' ? cLoad : t.id==='image' ? iLoad : Object.values(copyLoad).some(Boolean);
              return <button key={t.id} onClick={() => setTab(t.id)} style={{ padding:'7px 12px', border:'none', borderBottom: tab===t.id ? `2px solid ${C.nv}` : '2px solid transparent', background:'transparent', fontSize:11, fontWeight: tab===t.id ? 700 : 400, color: tab===t.id ? C.nv : C.wg, cursor:'pointer', marginBottom:-1, display:'flex', alignItems:'center', gap:4, fontFamily:'inherit' }}>
                <span>{t.icon}</span><span>{t.label}</span>{l ? <span style={{ fontSize:9, color:C.nv }}>●</span> : <span style={{ fontSize:9, color:'#4A9B6F', fontWeight:800 }}>✓</span>}
              </button>;
            })}
            {!anyLoad && <button onClick={() => { setGen(false); setCopyRes({}); setCanva(null); setImg(null); }} style={{ marginLeft:'auto', border:'none', background:'transparent', color:C.wg, fontSize:10, cursor:'pointer', fontFamily:'inherit', padding:7 }}>Clear</button>}
          </div>
          {tab==='copy' && active.map(p => <GenCard key={p.id} platform={p} result={copyRes[p.id]} loading={copyLoad[p.id]} />)}
          {tab==='canva' && (cLoad ? <Skel /> : canva ? (
            <div>
              <div style={{ display:'flex', justifyContent:'flex-end', marginBottom:8 }}><CopyBtn text={JSON.stringify(canva, null, 2)} label="Copy Brief" /></div>
              {canva.brand_specs && <div style={{ display:'flex', gap:5, flexWrap:'wrap', marginBottom:10 }}>
                {[['Primary',canva.brand_specs.primary_color],['Secondary',canva.brand_specs.secondary_color],['Accent',canva.brand_specs.accent_color]].map(([n,h]) => h && (
                  <div key={n} style={{ display:'flex', alignItems:'center', gap:4, padding:'4px 8px', background:'#fff', border:`1px solid ${C.lc}`, borderRadius:4, fontSize:10 }}>
                    <div style={{ width:10, height:10, borderRadius:2, background:h, flexShrink:0 }} />
                    <span style={{ color:C.wg }}>{n}</span><span style={{ fontWeight:700, color:C.nv }}>{h}</span>
                  </div>
                ))}
                <div style={{ padding:'4px 8px', background:'#fff', border:`1px solid ${C.lc}`, borderRadius:4, fontSize:10, color:C.wg }}><b style={{ color:C.nv }}>{canva.brand_specs.headline_font}</b> / {canva.brand_specs.body_font}</div>
              </div>}
              {canva.slide_briefs?.map((s, i) => (
                <div key={i} style={{ borderRadius:6, overflow:'hidden', border:`1px solid ${C.lc}`, marginBottom:4 }}>
                  <div style={{ background:'#E1306C', padding:'5px 10px', display:'flex', justifyContent:'space-between' }}>
                    <span style={{ fontSize:10, fontWeight:700, color:'#fff' }}>Slide {s.slide} — {s.type}</span>
                    <CopyBtn text={`Slide ${s.slide}: ${s.headline}${s.body ? ` / ${s.body}` : ''}\nVisual: ${s.visual_note}\nLayout: ${s.layout}`} sm label="Copy" />
                  </div>
                  <div style={{ padding:'8px 10px', background:'#fff' }}>
                    <div style={{ fontSize:13, fontWeight:700, color:C.nv, marginBottom:2 }}>{s.headline}</div>
                    {s.body && <div style={{ fontSize:11, color:C.wg, marginBottom:2 }}>{s.body}</div>}
                    <div style={{ fontSize:10, color:'#9B8E82' }}>Visual: {s.visual_note} · Layout: {s.layout}</div>
                  </div>
                </div>
              ))}
              {canva.canva_notes && <div style={{ padding:10, background:'#FFF8E8', border:`1px solid #E8D098`, borderRadius:6, fontSize:11, color:C.wg, lineHeight:'1.65', marginTop:6 }}><Lbl t="Notes" c={C.gd} />{canva.canva_notes}</div>}
            </div>
          ) : <div style={{ textAlign:'center', padding:20, color:'#C0B8B0', fontSize:12 }}>Failed — try again.</div>)}
          {tab==='image' && (iLoad ? <Skel /> : img ? (
            <div>
              <div style={{ background:C.nv, borderRadius:8, padding:14, marginBottom:8, position:'relative' }}>
                <Lbl t="GPT Image 2 — Paste into ChatGPT Thinking Mode (Plus/Pro)" c={C.gd} />
                <div style={{ fontSize:12, lineHeight:'1.8', color:'rgba(245,240,232,0.85)', whiteSpace:'pre-wrap', paddingRight:70 }}>{img.prompt}</div>
                <div style={{ position:'absolute', top:10, right:10 }}><CopyBtn text={img.prompt} label="Copy" /></div>
              </div>
              <div style={{ display:'flex', gap:6, marginBottom:10, flexWrap:'wrap' }}>
                {img.aspect_ratio && <div style={{ padding:'4px 10px', background:'#fff', border:`1px solid ${C.lc}`, borderRadius:4, fontSize:10 }}><span style={{ color:C.wg }}>Ratio: </span><b style={{ color:C.nv }}>{img.aspect_ratio}</b></div>}
                {img.usage && <div style={{ padding:'4px 10px', background:'#fff', border:`1px solid ${C.lc}`, borderRadius:4, fontSize:10 }}><span style={{ color:C.wg }}>Use: </span><b style={{ color:C.nv }}>{img.usage}</b></div>}
              </div>
              {img.variations?.map((v, i) => (
                <div key={i} style={{ ...ROW, marginBottom:5, fontSize:11 }}>
                  <div style={{ display:'flex', justifyContent:'space-between', gap:8 }}>
                    <span><b style={{ color:C.nv }}>Var {i+1}:</b> {v}</span><CopyBtn text={v} sm />
                  </div>
                </div>
              ))}
            </div>
          ) : <div style={{ textAlign:'center', padding:20, color:'#C0B8B0', fontSize:12 }}>Failed — try again.</div>)}
        </div>
      )}
    </div>
  );
}

// ── LEARN ─────────────────────────────────────────────────────
function LearnView({ brand, profile, intel }) {
  const [data, setData] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');

  const run = async () => {
    if (!data.trim()) { setErr('Paste performance data first.'); return; }
    setErr(''); setLoading(true);
    try {
      const p = profile || brand.profile || {};
      const user = `Brand: ${brand.name}\n${p.positioning ? `Positioning: ${p.positioning}\n` : ''}${intel ? `Voice fingerprint: ${intel.voiceFingerprint || ''}\nWhat worked: ${intel.whatWorked || ''}\nContinuity: ${intel.continuityNotes || ''}` : ''}\n\nMonthly performance data:\n${data}\n\nReturn ONLY this JSON:\n{"period":"month if mentioned","topPosts":["best post and why","second","third"],"weakPosts":["underperformer and why"],"bestPillar":"strongest pillar","bestFormat":"strongest format","audienceSignals":["signal 1","signal 2","signal 3"],"doubleDown":["thing to do more 1","thing 2","thing 3"],"stopDoing":["stop this 1","stop this 2"],"repurposeNow":["repurpose candidate 1","candidate 2"],"nextMonthTheme":"recommended theme for next 30 days","nextMonthPillars":["pillar 1","pillar 2","pillar 3"],"contentIdeas":["specific idea 1","idea 2","idea 3","idea 4","idea 5"],"updatedStrategy":"2-3 sentence updated strategic direction"}`;
      const r = await callAI('You are a senior content strategist reviewing monthly performance. Be specific and actionable. Return only valid JSON.', user, 1500);
      setResult(r);
    } catch (e) { setErr(e.message); }
    setLoading(false);
  };

  return (
    <div>
      <Fld val={data} onChange={setData} rows={8} label="Monthly Performance Data"
        placeholder={'Paste any of:\n• Post topics with engagement numbers\n• What got comments or shares\n• What flopped\n• Client feedback or audience DMs\n• Notes from your content log\n\nExample:\n\'AI website post: 847 impressions, 23 likes, 8 comments — best.\nFM industry post: 120 impressions, 2 likes — worst.\n3 DMs asking about content systems after no-code post.\''} />
      <ErrBox msg={err} />
      <PBtn label={loading ? 'Generating report...' : 'Generate Monthly Report →'} onClick={run} disabled={loading || !data.trim()} full color="#1C2B3A" />
      {loading && <div style={{ marginTop:12 }}><Skel /></div>}
      {result && !loading && (
        <div style={{ marginTop:14, display:'flex', flexDirection:'column', gap:8 }}>
          <div style={{ padding:'12px 14px', background:C.nv, borderRadius:8 }}>
            <div style={{ fontSize:10, fontWeight:700, color:C.gd, textTransform:'uppercase', letterSpacing:'0.07em', marginBottom:6 }}>Updated Strategy{result.period ? ` — ${result.period}` : ''}</div>
            <div style={{ fontSize:13, color:C.iv, lineHeight:'1.7' }}>{result.updatedStrategy}</div>
            <div style={{ display:'flex', gap:8, marginTop:10, flexWrap:'wrap' }}>
              {result.bestPillar && <div style={{ padding:'3px 10px', background:'rgba(184,134,11,0.2)', border:'1px solid rgba(184,134,11,0.4)', borderRadius:4, fontSize:10, color:C.gd }}>Top pillar: {result.bestPillar}</div>}
              {result.bestFormat && <div style={{ padding:'3px 10px', background:'rgba(184,134,11,0.2)', border:'1px solid rgba(184,134,11,0.4)', borderRadius:4, fontSize:10, color:C.gd }}>Best format: {result.bestFormat}</div>}
            </div>
          </div>
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:8 }}>
            <Card accent="#4A9B6F" style={{ marginBottom:0 }}><Lbl t="Top Posts" c="#2D6A4F" />{result.topPosts?.map((p,i) => <div key={i} style={{ fontSize:11, color:C.nv, lineHeight:'1.6', marginBottom:4, paddingLeft:6, borderLeft:'2px solid #4A9B6F' }}>✓ {p}</div>)}</Card>
            <Card accent="#C0392B" style={{ marginBottom:0 }}><Lbl t="Weak Posts" c="#C0392B" />{result.weakPosts?.map((p,i) => <div key={i} style={{ fontSize:11, color:C.nv, lineHeight:'1.6', marginBottom:4, paddingLeft:6, borderLeft:'2px solid #C0392B' }}>✕ {p}</div>)}</Card>
          </div>
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:8 }}>
            <Card accent="#4A9B6F" style={{ marginBottom:0 }}><Lbl t="Double Down" c="#2D6A4F" />{result.doubleDown?.map((d,i) => <div key={i} style={{ fontSize:11, color:C.nv, marginBottom:2 }}>↑ {d}</div>)}</Card>
            <Card accent="#C0392B" style={{ marginBottom:0 }}><Lbl t="Stop Doing" c="#C0392B" />{result.stopDoing?.map((d,i) => <div key={i} style={{ fontSize:11, color:C.nv, marginBottom:2 }}>✕ {d}</div>)}</Card>
          </div>
          <Card accent="#833AB4"><Lbl t="Repurpose Now" c="#833AB4" />{result.repurposeNow?.map((r,i) => <div key={i} style={{ display:'flex', justifyContent:'space-between', gap:8, padding:'6px 8px', background:C.ow, borderRadius:5, marginBottom:4 }}><div style={{ fontSize:11, color:C.nv, flex:1 }}>→ {r}</div><CopyBtn text={r} sm /></div>)}</Card>
          <Card accent={C.nv}>
            <div style={{ marginBottom:8 }}>
              <Lbl t="Next Month" c="#0A66C2" />
              <div style={{ fontSize:13, fontWeight:700, color:C.nv }}>{result.nextMonthTheme}</div>
            </div>
            {result.nextMonthPillars?.length > 0 && <div style={{ display:'flex', gap:5, flexWrap:'wrap', marginBottom:10 }}>{result.nextMonthPillars.map((p,i) => <span key={i} style={{ padding:'3px 10px', borderRadius:4, background:`${C.nv}15`, border:`1px solid ${C.nv}30`, fontSize:11, fontWeight:600, color:C.nv }}>{p}</span>)}</div>}
            {result.contentIdeas?.map((idea,i) => <div key={i} style={{ display:'flex', justifyContent:'space-between', gap:8, padding:'6px 8px', background:C.ow, borderRadius:5, marginBottom:4 }}><div style={{ fontSize:11, color:C.nv, flex:1 }}><b style={{ color:C.gd }}>{i+1}.</b> {idea}</div><CopyBtn text={idea} sm label="Use" /></div>)}
          </Card>
        </div>
      )}
    </div>
  );
}

// ── MAIN APP ──────────────────────────────────────────────────
const STAGES = [
  { id:'generate', label:'Generate', icon:'✦', desc:'Full production pack' },
  { id:'discover', label:'Discover', icon:'◎', desc:'Extract brand profile' },
  { id:'intelligence', label:'Intelligence', icon:'🧠', desc:'Analyze past content' },
  { id:'plan', label:'Plan', icon:'📅', desc:'30-day content plan' },
  { id:'learn', label:'Learn', icon:'📈', desc:'Monthly report' },
];
const CLIENT_STAGES = [
  { id:'intake', label:'Intake', icon:'📋', desc:'Collect client info' },
  ...STAGES,
];
const INTAKE_MODES = [
  { id:'zero', label:'Ground Zero', desc:'No brand kit — build from scratch' },
  { id:'existing', label:'Existing Presence', desc:'Has website/socials — audit and improve' },
  { id:'known', label:'Known Brand', desc:'Retained client already in system' },
];

export default function Home() {
  const [clients, setClients] = useState([]);
  const [activeId, setActiveId] = useState('EE');
  const [stage, setStage] = useState('generate');
  const [profiles, setProfiles] = useState({});
  const [intels, setIntels] = useState({});
  const [intakes, setIntakes] = useState({});
  const [showAdd, setShowAdd] = useState(false);
  const [newIn, setNewIn] = useState({ mode:'zero', name:'', industry:'', location:'', website:'', offer:'', audience:'', goal:'', tone:'', avoid:'' });
  const [apiKeyMissing, setApiKeyMissing] = useState(false);

  useEffect(() => {
    const c = LS.get('dge-clients') || [];
    setClients(c);
    const prof = {}; const int = {}; const inta = {};
    c.forEach(b => {
      const p = LS.get(`dge-profile-${b.id}`); if (p) prof[b.id] = p;
      const i = LS.get(`dge-intel-${b.id}`); if (i) int[b.id] = i;
      if (b.intake) inta[b.id] = b.intake;
    });
    Object.keys(MY_BRANDS).forEach(id => {
      const p = LS.get(`dge-profile-${id}`); if (p) prof[id] = p;
      const i = LS.get(`dge-intel-${id}`); if (i) int[id] = i;
    });
    setProfiles(prof); setIntels(int); setIntakes(inta);

    fetch('/api/claude', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ system:'reply ok', user:'ping', max_tokens:5 }) })
      .then(r => r.json())
      .then(d => { if (d.error?.includes('ANTHROPIC_API_KEY')) setApiKeyMissing(true); })
      .catch(() => {});
  }, []);

  const activeBrand = MY_BRANDS[activeId] || clients.find(c => c.id === activeId);
  const activeProfile = profiles[activeId] || activeBrand?.profile || null;
  const activeIntel = intels[activeId] || null;
  const activeIntake = intakes[activeId] || null;
  const isMyBrand = !!MY_BRANDS[activeId];

  const saveProfile = (id, p) => { setProfiles(prev => ({ ...prev, [id]: p })); LS.set(`dge-profile-${id}`, p); };
  const saveIntel = (id, i) => { setIntels(prev => ({ ...prev, [id]: i })); LS.set(`dge-intel-${id}`, i); };

  const addClient = () => {
    if (!newIn.name.trim()) return;
    const id = 'client_' + Date.now();
    const client = { id, type:'client', name: newIn.name, mode: newIn.mode, color:'#2D4A6A', accent:'#5B8DB8', intake: newIn };
    const updated = [...clients, client];
    setClients(updated); LS.set('dge-clients', updated);
    setIntakes(prev => ({ ...prev, [id]: newIn }));
    setActiveId(id); setStage('discover'); setShowAdd(false);
    setNewIn({ mode:'zero', name:'', industry:'', location:'', website:'', offer:'', audience:'', goal:'', tone:'', avoid:'' });
  };

  const delClient = id => {
    const updated = clients.filter(c => c.id !== id);
    setClients(updated); LS.set('dge-clients', updated);
    LS.del(`dge-profile-${id}`); LS.del(`dge-intel-${id}`);
    if (activeId === id) setActiveId('EE');
  };

  const nu = k => v => setNewIn(p => ({ ...p, [k]: v }));
  const visibleStages = isMyBrand ? STAGES : CLIENT_STAGES;

  const sb = { width: 210, flexShrink: 0, borderRight: `1px solid ${C.lc}`, background: C.ow, display:'flex', flexDirection:'column', overflowY:'auto' };
  const main = { flex:1, overflowY:'auto', padding: '20px 22px' };
  const sBtn = (active, color) => ({ display:'flex', alignItems:'center', gap:7, width:'100%', padding:'7px 8px', borderRadius:5, border:`1px solid ${active ? color : 'transparent'}`, background: active ? `${color}18` : 'transparent', cursor:'pointer', marginBottom:3, textAlign:'left', fontFamily:'inherit' });

  return (
    <>
      <Head>
        <title>BridgeWorks Digital Growth Engine</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" type="image/png" href="/favicon.png" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet" />
      </Head>

      <div style={{ display:'flex', flexDirection:'column', height:'100vh', fontFamily:"'Inter', system-ui, sans-serif" }}>
        {/* Header */}
        <div style={{ background:C.nv, height:52, display:'flex', alignItems:'center', padding:'0 18px', gap:16, flexShrink:0, borderBottom:`2px solid ${C.gd}` }}>
          <div style={{ display:'flex', alignItems:'center', gap:10 }}>
            <img src="/bw-icon.png" alt="BridgeWorks" style={{ height:30, width:'auto', flexShrink:0 }} />
            <div>
              <div style={{ color:C.iv, fontSize:14, fontWeight:700, lineHeight:1, fontFamily:"'Playfair Display', Georgia, serif", letterSpacing:'0.01em' }}>Digital Growth Engine</div>
              <div style={{ color:'rgba(245,240,232,0.45)', fontSize:9, letterSpacing:'0.1em', textTransform:'uppercase', marginTop:2 }}>BridgeWorks Studio</div>
            </div>
          </div>
          {activeBrand && <div style={{ display:'flex', alignItems:'center', gap:8, marginLeft:'auto' }}>
            <div style={{ width:7, height:7, borderRadius:'50%', background: activeBrand.accent || C.gd }} />
            <span style={{ color:C.iv, fontSize:11, fontWeight:600 }}>{activeBrand.name}</span>
            {activeIntel && <span style={{ fontSize:9, color:'#4A9B6F', fontWeight:700, background:'rgba(74,155,111,0.2)', padding:'2px 7px', borderRadius:3 }}>🧠 Intel</span>}
            {activeProfile && <span style={{ fontSize:9, color:C.gd, fontWeight:700, background:'rgba(184,134,11,0.15)', padding:'2px 7px', borderRadius:3 }}>◎ Profile</span>}
          </div>}
        </div>

        {apiKeyMissing && (
          <div style={{ background:'#FEF3CD', borderBottom:`1px solid #E8D098`, padding:'10px 18px', fontSize:12, color:'#7D5A00' }}>
            ⚠️ <b>ANTHROPIC_API_KEY not set.</b> Go to Vercel → Your Project → Settings → Environment Variables → add <code>ANTHROPIC_API_KEY</code> with your Anthropic API key, then redeploy.
          </div>
        )}

        <div style={{ display:'flex', flex:1, overflow:'hidden' }}>
          {/* Sidebar */}
          <div style={sb}>
            <div style={{ padding:'12px 12px 6px' }}>
              <div style={{ fontSize:9, fontWeight:700, color:C.wg, textTransform:'uppercase', letterSpacing:'0.08em', marginBottom:8 }}>My Brands</div>
              {Object.values(MY_BRANDS).map(b => (
                <button key={b.id} onClick={() => { setActiveId(b.id); setStage('generate'); setShowAdd(false); }} style={sBtn(activeId === b.id, b.color)}>
                  <div style={{ width:7, height:7, borderRadius:'50%', background:b.color, flexShrink:0 }} />
                  <span style={{ fontSize:11, fontWeight: activeId===b.id ? 700 : 400, color: activeId===b.id ? b.color : C.wg, flex:1 }}>{b.name}</span>
                  {intels[b.id] && <span style={{ fontSize:9 }}>🧠</span>}
                </button>
              ))}
            </div>

            <div style={{ padding:'8px 12px 6px', borderTop:`1px solid ${C.lc}`, marginTop:4 }}>
              <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:8 }}>
                <div style={{ fontSize:9, fontWeight:700, color:C.wg, textTransform:'uppercase', letterSpacing:'0.08em' }}>Clients</div>
                <button onClick={() => setShowAdd(a => !a)} style={{ fontSize:11, color:C.gd, fontWeight:700, background:'none', border:'none', cursor:'pointer', fontFamily:'inherit' }}>+ Add</button>
              </div>
              {clients.length === 0 && !showAdd && <div style={{ fontSize:10, color:'#C0B8B0', lineHeight:'1.7', paddingBottom:4 }}>No clients yet.</div>}
              {clients.map(c => (
                <div key={c.id} style={{ display:'flex', alignItems:'center', gap:3, marginBottom:2 }}>
                  <button onClick={() => { setActiveId(c.id); setStage('generate'); setShowAdd(false); }} style={{ ...sBtn(activeId===c.id, '#2D4A6A'), flex:1 }}>
                    <div style={{ width:7, height:7, borderRadius:'50%', background:'#2D4A6A', flexShrink:0 }} />
                    <span style={{ fontSize:11, fontWeight: activeId===c.id ? 700 : 400, color: activeId===c.id ? '#2D4A6A' : C.wg, flex:1 }}>{c.name}</span>
                    {intels[c.id] && <span style={{ fontSize:9 }}>🧠</span>}
                    {profiles[c.id] && <span style={{ fontSize:9, color:C.gd }}>◎</span>}
                  </button>
                  <button onClick={() => { if (window.confirm(`Remove ${c.name}?`)) delClient(c.id); }} style={{ fontSize:11, color:'#C0B8B0', background:'none', border:'none', cursor:'pointer', padding:4, flexShrink:0 }}>×</button>
                </div>
              ))}
            </div>

            {activeBrand && !showAdd && (
              <div style={{ padding:'8px 12px', borderTop:`1px solid ${C.lc}`, marginTop:4, flex:1 }}>
                <div style={{ fontSize:9, fontWeight:700, color:C.wg, textTransform:'uppercase', letterSpacing:'0.08em', marginBottom:8 }}>Pipeline</div>
                {visibleStages.map(s => {
                  const done = (s.id==='discover' && !!activeProfile) || (s.id==='intelligence' && !!activeIntel);
                  return (
                    <button key={s.id} onClick={() => setStage(s.id)} style={{ display:'flex', alignItems:'center', gap:7, width:'100%', padding:'6px 8px', borderRadius:5, border:`1px solid ${stage===s.id ? C.nv : 'transparent'}`, background: stage===s.id ? C.nv : 'transparent', cursor:'pointer', marginBottom:2, textAlign:'left', fontFamily:'inherit' }}>
                      <span style={{ fontSize:12 }}>{s.icon}</span>
                      <div style={{ flex:1 }}>
                        <div style={{ fontSize:10, fontWeight: stage===s.id ? 700 : 400, color: stage===s.id ? C.iv : C.wg }}>{s.label}</div>
                        <div style={{ fontSize:8, color: stage===s.id ? 'rgba(245,240,232,0.35)' : C.lc }}>{s.desc}</div>
                      </div>
                      {done && <span style={{ fontSize:9, color:'#4A9B6F', fontWeight:800 }}>✓</span>}
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {/* Main */}
          <div style={main}>
            {/* Add Client Form */}
            {showAdd && (
              <div style={{ maxWidth:640 }}>
                <div style={{ fontSize:16, fontWeight:700, color:C.nv, marginBottom:4 }}>New Client Intake</div>
                <div style={{ fontSize:12, color:C.wg, marginBottom:14, lineHeight:'1.6' }}>Only the business name is required. Everything else improves the brand extraction.</div>
                <div style={{ marginBottom:12 }}>
                  <div style={{ fontSize:11, color:C.wg, marginBottom:6, fontWeight:500 }}>Client Mode</div>
                  <div style={{ display:'flex', flexDirection:'column', gap:5 }}>
                    {INTAKE_MODES.map(m => (
                      <button key={m.id} onClick={() => nu('mode')(m.id)} style={{ display:'flex', alignItems:'flex-start', gap:8, padding:'8px 10px', borderRadius:6, border:`1px solid ${newIn.mode===m.id ? C.nv : C.lc}`, background: newIn.mode===m.id ? '#F0F3F8' : '#fff', cursor:'pointer', textAlign:'left', fontFamily:'inherit' }}>
                        <span style={{ fontSize:14, color: newIn.mode===m.id ? C.nv : C.wg, marginTop:1 }}>{m.id==='zero' ? '◎' : m.id==='existing' ? '◑' : '●'}</span>
                        <div>
                          <div style={{ fontSize:12, fontWeight: newIn.mode===m.id ? 700 : 400, color:C.nv }}>{m.label}</div>
                          <div style={{ fontSize:10, color:C.wg, marginTop:1 }}>{m.desc}</div>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
                <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:'0 12px' }}>
                  <Fld label="Business Name *" val={newIn.name} onChange={nu('name')} placeholder="e.g. Olivik's Kitchen" inline />
                  <Fld label="Industry" val={newIn.industry} onChange={nu('industry')} placeholder="e.g. F&B, FM, Consulting" inline />
                  <Fld label="Location / Market" val={newIn.location} onChange={nu('location')} placeholder="e.g. Budapest, Hungary" inline />
                  <Fld label="Website URL" val={newIn.website} onChange={nu('website')} placeholder="e.g. example.com" inline />
                </div>
                <Fld label="What They Sell" val={newIn.offer} onChange={nu('offer')} rows={2} placeholder="Products, services, price points..." />
                <Fld label="Who They Serve" val={newIn.audience} onChange={nu('audience')} rows={2} placeholder="Target customer — demographics, location, needs..." />
                <Fld label="Main Goal (30 days)" val={newIn.goal} onChange={nu('goal')} rows={2} placeholder="e.g. Get 10 bookings/week, generate B2B leads..." />
                <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:'0 12px' }}>
                  <Fld label="Preferred Tone" val={newIn.tone} onChange={nu('tone')} rows={2} placeholder="e.g. warm and approachable, direct..." />
                  <Fld label="Avoid Sounding Like" val={newIn.avoid} onChange={nu('avoid')} rows={2} placeholder="e.g. corporate, generic, salesy..." />
                </div>
                <div style={{ display:'flex', gap:8 }}>
                  <PBtn label={newIn.name.trim() ? 'Save & Start Discovery →' : 'Enter business name'} onClick={addClient} disabled={!newIn.name.trim()} />
                  <PBtn label="Cancel" onClick={() => setShowAdd(false)} color={C.wg} />
                </div>
              </div>
            )}

            {/* Empty state */}
            {!showAdd && !activeBrand && (
              <div style={{ display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', height:'100%', textAlign:'center', color:C.wg, gap:14 }}>
                <div style={{ fontSize:28, opacity:.2 }}>◈</div>
                <div>
                  <div style={{ fontSize:14, fontWeight:700, color:C.wg, marginBottom:4 }}>Select a brand or add a client</div>
                  <div style={{ fontSize:12, maxWidth:260, lineHeight:'1.7' }}>Choose from My Brands or click + Add to onboard a new client.</div>
                </div>
              </div>
            )}

            {/* Brand stages */}
            {!showAdd && activeBrand && (
              <div style={{ maxWidth:680 }}>
                <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:14, paddingBottom:12, borderBottom:`1px solid ${C.lc}` }}>
                  <div style={{ width:8, height:8, borderRadius:'50%', background: activeBrand.accent || C.gd }} />
                  <span style={{ fontSize:15, fontWeight:700, color:C.nv }}>{activeBrand.name}</span>
                  <span style={{ fontSize:11, color:C.wg }}>—</span>
                  <span style={{ fontSize:13, color:C.wg }}>
                    {visibleStages.find(s => s.id === stage)?.label}
                  </span>
                </div>

                {!isMyBrand && stage === 'intake' && (
                  <div>
                    <div style={{ fontSize:12, color:C.wg, marginBottom:14, lineHeight:'1.6' }}>Update intake information for {activeBrand.name}.</div>
                    {[['name','Business Name'],['industry','Industry'],['location','Location'],['website','Website'],['offer','Main Offer'],['audience','Who They Serve'],['goal','Main Goal'],['tone','Preferred Tone'],['avoid','Avoid Sounding Like']].map(([k,l]) => (
                      <Fld key={k} label={l} val={activeIntake?.[k]||''} onChange={v => setIntakes(prev => ({ ...prev, [activeId]: { ...(prev[activeId]||{}), [k]:v } }))} placeholder="" inline={['name','industry','location','website'].includes(k)} rows={2} />
                    ))}
                    <PBtn label="Save & Continue to Discovery →" onClick={() => setStage('discover')} full />
                  </div>
                )}

                {stage === 'discover' && (
                  <div>
                    <div style={{ fontSize:12, color:C.wg, marginBottom:14, lineHeight:'1.6' }}>Extract a brand profile from any starting point — website copy, social bios, old posts, or a description. Intake data feeds the extraction automatically.</div>
                    <DiscoverView intake={activeIntake} existingProfile={activeProfile} onSave={p => saveProfile(activeId, p)} />
                  </div>
                )}

                {stage === 'intelligence' && (
                  <div>
                    <div style={{ fontSize:12, color:C.wg, marginBottom:14, lineHeight:'1.6' }}>Paste 5–20 past posts to extract voice fingerprint, what works, continuity notes, and content ideas. Saved and wired into every future generation for this brand.</div>
                    <IntelView brand={activeBrand} profile={activeProfile} intel={activeIntel} onSave={i => saveIntel(activeId, i)} />
                  </div>
                )}

                {stage === 'plan' && (
                  <div>
                    <div style={{ fontSize:12, color:C.wg, marginBottom:14, lineHeight:'1.6' }}>4-week content plan with specific hooks, ideas, CTAs, and platforms. Uses brand profile and intelligence together.</div>
                    <PlanView brand={activeBrand} profile={activeProfile} intel={activeIntel} />
                  </div>
                )}

                {stage === 'generate' && (
                  <div>
                    <div style={{ fontSize:12, color:C.wg, marginBottom:14, lineHeight:'1.6' }}>Full production pack: platform-native copy, Canva design brief, and GPT Image 2 prompt — all generated simultaneously in your brand voice.</div>
                    <GenerateView brand={activeBrand} profile={activeProfile} intel={activeIntel} />
                  </div>
                )}

                {stage === 'learn' && (
                  <div>
                    <div style={{ fontSize:12, color:C.wg, marginBottom:14, lineHeight:'1.6' }}>Paste this month's performance data and get a full learning report: what worked, what didn't, what to repurpose, and next month's strategy.</div>
                    <LearnView brand={activeBrand} profile={activeProfile} intel={activeIntel} />
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
