import json
import os
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output')

def score_class(score):
    if score >= 7: return 'green'
    if score >= 4: return 'amber'
    return 'red'

def score_emoji(score):
    if score >= 7: return '\u2705'
    if score >= 4: return '\u26a0\ufe0f'
    return '\U0001f534'

def make_pill(text, color):
    return '<span class="pill pill-{}">{}</span>'.format(color, text)

def flags_html(flags):
    if not flags: return ''
    items = ''.join('<span class="flag-item">{}</span>'.format(f) for f in flags if f)
    return '<div class="card-flags">{}</div>'.format(items)

def notes_html(notes, css_class='card-notes'):
    if not notes: return ''
    return '<div class="{}">{}</div>'.format(css_class, notes)

def price_html(r):
    price = r.get('smallest_unit_price')
    size  = r.get('smallest_unit_size')
    if price and str(price) != 'NOT FOUND':
        lbl = '/ mo' + (' · ' + str(size) if size and size != 'NOT FOUND' else '')
        return '<div class="card-price"><div class="price-from">from</div><div class="price-amount">${}</div><div class="price-unit">{}</div></div>'.format(price, lbl)
    return '<div class="card-price"><div class="price-na">Visit site<br>for pricing</div></div>'

def facility_pills(r):
    pills = []
    disclosed = r.get('ongoing_rate_disclosed', '')
    if disclosed == 'YES':
        pills.append(make_pill('Full pricing published', 'green'))
    elif disclosed == 'PARTIAL':
        pills.append(make_pill('Pricing visible in browser', 'amber'))
    lock = r.get('price_lock', '')
    if lock and lock != 'NOT FOUND' and 'no' not in str(lock).lower():
        pills.append(make_pill('Price Lock', 'green'))
    if r.get('climate_control_available') == 'YES':
        pills.append(make_pill('Climate control', 'blue'))
    if r.get('drive_up_access') == 'YES':
        pills.append(make_pill('Drive-up', 'blue'))
    hours = r.get('access_hours', '')
    if hours and hours != 'NOT FOUND':
        pills.append(make_pill(hours, 'gray'))
    cc = r.get('credit_card_fee', '')
    if cc and cc != 'NOT FOUND':
        pills.append(make_pill('CC fee: {}'.format(cc), 'red'))
    if r.get('insurance_required') == 'YES':
        pills.append(make_pill('Mandatory insurance', 'red'))
    return ''.join(pills)

def make_card(r, tier):
    score = r.get('transparency_score')
    sc = score_class(score)
    em = score_emoji(score)
    name = r.get('facility_name', '')
    notes = r.get('notes', '')
    addr = ''
    if notes:
        first = notes.split('.')[0]
        if any(c.isdigit() for c in first):
            addr = first
    return '''
    <div class="card" data-tier="{tier}">
      <div class="card-main">
        <div class="score-badge {sc}">
          <div class="score-num">{score}</div>
          <div class="score-denom">/10</div>
          <div class="score-icon">{em}</div>
        </div>
        <div class="card-body">
          <div class="card-name">{name}</div>
          <div class="card-meta">{addr}</div>
          <div class="card-pills">{pills}</div>
        </div>
        {price}
      </div>
      {flags}
      {notes_div}
    </div>'''.format(
        tier=tier, sc=sc, score=score, em=em, name=name, addr=addr,
        pills=facility_pills(r), price=price_html(r),
        flags=flags_html(r.get('red_flags', [])),
        notes_div=notes_html(notes)
    )

def make_local_card(r):
    name = r.get('facility_name', '')
    notes = r.get('notes', '')
    return '''
    <div class="card" data-tier="purple">
      <div class="card-main">
        <div class="score-badge purple">
          <div class="score-icon" style="font-size:1.6rem;margin:0;">\U0001f4de</div>
          <div class="score-label">Local &amp;<br>Call-First</div>
        </div>
        <div class="card-body">
          <div class="card-name">{name}</div>
          <div class="card-meta"></div>
          <div class="card-pills"><span class="pill pill-purple">Locally owned</span><span class="pill pill-gray">Call for rates</span></div>
        </div>
        <div class="card-price"><div class="price-na">Call for<br>pricing</div></div>
      </div>
      {notes_div}
    </div>'''.format(name=name, notes_div=notes_html(notes, 'card-local-note'))

def make_nodata_card(r):
    name = r.get('facility_name', '')
    notes = r.get('notes', '')
    return '''
    <div class="card" data-tier="gray">
      <div class="card-main">
        <div class="score-badge" style="background:#F3F4F6;">
          <div class="score-icon" style="font-size:1.6rem;margin:0;">\u26ab</div>
          <div class="score-label" style="color:var(--muted);">No<br>Data</div>
        </div>
        <div class="card-body">
          <div class="card-name">{name}</div>
          <div class="card-meta"></div>
          <div class="card-pills"><span class="pill pill-gray">No pricing anywhere online</span></div>
        </div>
        <div class="card-price"><div class="price-na">Contact<br>for info</div></div>
      </div>
      {notes_div}
    </div>'''.format(name=name, notes_div=notes_html(notes))

CSS = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--navy:#0F1923;--cream:#F7F4EF;--green:#22C55E;--amber:#F59E0B;--red:#EF4444;--blue:#3B82F6;--purple:#8B5CF6;--green-bg:#F0FDF4;--amber-bg:#FFFBEB;--red-bg:#FEF2F2;--purple-bg:#F5F3FF;--muted:#6B7280;--border:#E5E7EB}
html{scroll-behavior:smooth}
body{font-family:'Inter',sans-serif;background:var(--cream);color:var(--navy);line-height:1.6;font-size:16px}
.hero{background:var(--navy);color:var(--cream);padding:80px 24px 72px;text-align:center;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(59,130,246,0.15) 0%,transparent 70%);pointer-events:none}
.hero-eyebrow{font-size:11px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:var(--blue);margin-bottom:20px}
.hero h1{font-family:'Playfair Display',serif;font-size:clamp(2.4rem,6vw,4.2rem);font-weight:900;line-height:1.1;margin-bottom:20px;max-width:800px;margin-left:auto;margin-right:auto}
.hero h1 span{color:var(--blue)}
.hero-sub{font-size:1.05rem;color:rgba(247,244,239,0.7);max-width:560px;margin:0 auto 52px;font-weight:300}
.meter-wrap{display:inline-flex;flex-direction:column;align-items:center;gap:12px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:32px 48px}
.meter-label{font-size:11px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:rgba(247,244,239,0.5)}
.meter-number{font-family:'Playfair Display',serif;font-size:5rem;font-weight:900;line-height:1;color:var(--red)}
.meter-desc{font-size:0.85rem;color:rgba(247,244,239,0.6);max-width:220px;text-align:center}
.meter-bar{width:220px;height:6px;background:rgba(255,255,255,0.1);border-radius:3px;overflow:hidden}
.meter-fill{height:100%;width:0%;background:linear-gradient(90deg,var(--red),var(--amber));border-radius:3px;transition:width 1.8s cubic-bezier(0.4,0,0.2,1)}
.stats{background:white;border-bottom:1px solid var(--border)}
.stats-inner{max-width:1000px;margin:0 auto;padding:0 24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr))}
.stat-item{padding:28px 16px;text-align:center;border-right:1px solid var(--border)}
.stat-item:last-child{border-right:none}
.stat-number{font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:700;line-height:1;margin-bottom:6px}
.stat-label{font-size:0.72rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted)}
.stat-green{color:var(--green)}.stat-amber{color:var(--amber)}.stat-red{color:var(--red)}.stat-blue{color:var(--blue)}.stat-purple{color:var(--purple)}
.container{max-width:920px;margin:0 auto;padding:0 24px}
.section-header{padding:56px 0 24px;display:flex;align-items:baseline;gap:16px}
.section-header h2{font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:700}
.section-count{font-size:0.8rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--muted)}
.tier-label{display:flex;align-items:center;gap:12px;margin:32px 0 16px}
.tier-label-text{font-size:0.72rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;white-space:nowrap}
.tier-label-line{flex:1;height:1px;background:var(--border)}
.tier-green{color:var(--green)}.tier-amber{color:var(--amber)}.tier-red{color:var(--red)}.tier-purple{color:var(--purple)}
.cards{display:flex;flex-direction:column;gap:12px;margin-bottom:16px}
.card{background:white;border-radius:12px;border:1px solid var(--border);overflow:hidden;transition:box-shadow 0.2s}
.card:hover{box-shadow:0 4px 20px rgba(15,25,35,0.08)}
.card-main{display:grid;grid-template-columns:auto 1fr auto;align-items:stretch}
.score-badge{width:68px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:16px 8px;border-right:1px solid var(--border);flex-shrink:0}
.score-badge.green{background:var(--green-bg)}.score-badge.amber{background:var(--amber-bg)}.score-badge.red{background:var(--red-bg)}.score-badge.purple{background:var(--purple-bg)}
.score-num{font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;line-height:1}
.score-denom{font-size:0.65rem;color:var(--muted);font-weight:500}
.score-icon{font-size:1rem;margin-top:2px}
.score-label{font-size:0.6rem;font-weight:700;letter-spacing:0.05em;text-transform:uppercase;margin-top:2px;text-align:center;line-height:1.2}
.score-badge.green .score-num{color:var(--green)}.score-badge.amber .score-num{color:var(--amber)}.score-badge.red .score-num{color:var(--red)}.score-badge.purple .score-label{color:var(--purple)}
.card-body{padding:14px 18px;min-width:0}
.card-name{font-weight:700;font-size:0.95rem;margin-bottom:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card-meta{font-size:0.78rem;color:var(--muted);margin-bottom:8px}
.card-pills{display:flex;flex-wrap:wrap;gap:5px}
.pill{font-size:0.68rem;font-weight:600;padding:2px 8px;border-radius:100px;white-space:nowrap}
.pill-green{background:var(--green-bg);color:#15803D}.pill-amber{background:var(--amber-bg);color:#B45309}.pill-red{background:var(--red-bg);color:#B91C1C}.pill-blue{background:#EFF6FF;color:#1D4ED8}.pill-gray{background:#F3F4F6;color:#374151}.pill-purple{background:var(--purple-bg);color:#6D28D9}
.card-price{padding:14px 18px 14px 0;display:flex;flex-direction:column;align-items:flex-end;justify-content:center;flex-shrink:0;min-width:100px}
.price-from{font-size:0.65rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted)}
.price-amount{font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;line-height:1.1;color:var(--navy)}
.price-unit{font-size:0.7rem;color:var(--muted)}
.price-na{font-size:0.78rem;color:var(--muted);font-style:italic;text-align:right}
.card-flags{border-top:1px solid var(--border);padding:10px 18px 10px 86px;background:var(--red-bg);display:flex;flex-wrap:wrap;gap:6px}
.flag-item{font-size:0.72rem;color:#B91C1C;display:flex;align-items:center;gap:4px}
.flag-item::before{content:'\\26A0';font-size:0.65rem}
.card-notes{border-top:1px solid var(--border);padding:10px 18px 10px 86px;font-size:0.78rem;color:var(--muted);background:#FAFAFA;line-height:1.5}
.card-local-note{border-top:1px solid #DDD6FE;padding:10px 18px 10px 86px;font-size:0.78rem;color:#5B21B6;background:var(--purple-bg);line-height:1.5}
.local-callout{background:var(--purple-bg);border:1px solid #DDD6FE;border-radius:12px;padding:24px 28px;margin:0 0 20px;display:flex;gap:16px;align-items:flex-start}
.local-callout-icon{font-size:1.6rem;flex-shrink:0;margin-top:2px}
.local-callout-title{font-weight:700;font-size:0.95rem;color:#5B21B6;margin-bottom:6px}
.local-callout-text{font-size:0.82rem;color:#4C1D95;line-height:1.6}
.nuance-box{background:#EFF6FF;border:1px solid #BFDBFE;border-radius:12px;padding:24px 28px;margin:32px 0;display:flex;gap:16px;align-items:flex-start}
.nuance-icon{font-size:1.4rem;flex-shrink:0;margin-top:2px}
.nuance-title{font-weight:700;font-size:0.9rem;color:#1D4ED8;margin-bottom:6px}
.nuance-text{font-size:0.82rem;color:#1E40AF;line-height:1.6}
.tips-section{margin:48px 0;background:var(--navy);border-radius:16px;padding:40px;color:var(--cream)}
.tips-section h2{font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;margin-bottom:8px}
.tips-intro{font-size:0.88rem;color:rgba(247,244,239,0.6);margin-bottom:28px;font-weight:300}
.tips-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px}
.tip-card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:20px}
.tip-icon{font-size:1.4rem;margin-bottom:10px}
.tip-title{font-weight:700;font-size:0.88rem;margin-bottom:6px;color:var(--cream)}
.tip-text{font-size:0.78rem;color:rgba(247,244,239,0.6);line-height:1.5}
.methodology{border-top:1px solid var(--border);padding:40px 0 60px;margin-top:48px}
.methodology h3{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;margin-bottom:12px}
.methodology p{font-size:0.8rem;color:var(--muted);line-height:1.7;max-width:680px;margin-bottom:8px}
.footer{background:var(--navy);color:rgba(247,244,239,0.4);text-align:center;padding:24px;font-size:0.75rem}
.footer strong{color:var(--cream)}
.filter-bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:4px;padding-top:8px}
.filter-btn{font-size:0.75rem;font-weight:600;padding:6px 14px;border-radius:100px;border:1.5px solid var(--border);background:white;color:var(--navy);cursor:pointer;transition:all 0.15s;font-family:'Inter',sans-serif}
.filter-btn:hover{border-color:var(--navy)}
.filter-btn.active{background:var(--navy);color:white;border-color:var(--navy)}
.hidden{display:none!important}
@media(max-width:600px){.card-main{grid-template-columns:68px 1fr}.card-price{display:none}.card-flags,.card-notes,.card-local-note{padding-left:86px}.stats-inner{grid-template-columns:repeat(2,1fr)}.stat-item{border-right:none;border-bottom:1px solid var(--border)}.tips-section{padding:28px 20px}}"""

JS = """
  window.addEventListener('load', function() {
    var pct = PCT_PLACEHOLDER;
    var numEl = document.getElementById('meterNum');
    var fillEl = document.getElementById('meterFill');
    setTimeout(function() {
      fillEl.style.width = pct + '%';
      var current = 0;
      var interval = setInterval(function() {
        current++;
        numEl.textContent = current + '%';
        if (current >= pct) clearInterval(interval);
      }, 80);
    }, 400);
  });
  function filterCards(tier, btn) {
    document.querySelectorAll('.filter-btn').forEach(function(b) { b.classList.remove('active'); });
    btn.classList.add('active');
    document.querySelectorAll('.card').forEach(function(card) {
      var show = tier === 'all' || card.dataset.tier === tier;
      card.classList.toggle('hidden', !show);
    });
    document.querySelectorAll('[data-tier-label]').forEach(function(label) {
      if (tier === 'all') { label.classList.remove('hidden'); }
      else { label.classList.toggle('hidden', label.dataset.tierLabel !== tier); }
    });
    var lc = document.querySelector('.local-callout');
    if (lc) lc.classList.toggle('hidden', tier !== 'all' && tier !== 'purple');
  }
"""

def generate_html_report(results, label="lincoln"):
    timestamp = datetime.now().strftime("%B %d, %Y")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    green   = sorted([r for r in results if isinstance(r.get('transparency_score'), (int, float)) and r['transparency_score'] >= 7], key=lambda x: -x['transparency_score'])
    amber   = sorted([r for r in results if isinstance(r.get('transparency_score'), (int, float)) and 4 <= r['transparency_score'] < 7], key=lambda x: -x['transparency_score'])
    red     = sorted([r for r in results if isinstance(r.get('transparency_score'), (int, float)) and 1 <= r['transparency_score'] < 4], key=lambda x: -x['transparency_score'])
    local   = [r for r in results if r.get('category') == 'local']
    no_data = [r for r in results if not isinstance(r.get('transparency_score'), (int, float)) and r.get('category') != 'local']

    total   = len(results)
    n_green = len(green)
    n_amber = len(amber)
    n_red   = len(red)
    n_local = len(local)
    n_nodata = len(no_data)
    pct_transparent = round((n_green / total) * 100) if total else 0

    green_cards  = '\n'.join(make_card(r, 'green') for r in green)
    amber_cards  = '\n'.join(make_card(r, 'amber') for r in amber)
    red_cards    = '\n'.join(make_card(r, 'red')   for r in red)
    local_cards  = '\n'.join(make_local_card(r)    for r in local)
    nodata_cards = '\n'.join(make_nodata_card(r)   for r in no_data)

    local_section = ''
    if local_cards:
        local_section = '''
  <div class="tier-label tier-purple" data-tier-label="purple">
    <span class="tier-label-text">\U0001f4de Local &amp; Call-First \u2014 Independently Verified</span>
    <div class="tier-label-line"></div>
  </div>
  <div class="local-callout">
    <div class="local-callout-icon">\U0001f3e1</div>
    <div>
      <div class="local-callout-title">These are verified locally owned, independent operators</div>
      <div class="local-callout-text">They don\'t list prices online \u2014 not because they\'re hiding anything, but because that\'s how they\'ve always done business. <strong>Call them directly.</strong> Ask: <strong>"What\'s my rate in month 4?"</strong> and <strong>"Do you price-match?"</strong></div>
    </div>
  </div>
  <div class="cards">''' + local_cards + '</div>'

    nodata_section = ''
    if nodata_cards:
        nodata_section = '''
  <div class="tier-label" style="color:var(--muted)" data-tier-label="gray">
    <span class="tier-label-text" style="color:var(--muted)">\u26ab Minimal Web Presence \u2014 Unable to Score</span>
    <div class="tier-label-line"></div>
  </div>
  <div class="cards">''' + nodata_cards + '</div>'

    js_final = JS.replace('PCT_PLACEHOLDER', str(pct_transparent))

    parts = [
        '<!DOCTYPE html><html lang="en"><head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>TrueStore \u2014 Lincoln, NE Storage Transparency Report</title>',
        '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">',
        '<style>', CSS, '</style>',
        '</head><body>',
        '<section class="hero">',
        '  <div class="hero-eyebrow">TrueStore \u00b7 Lincoln, NE \u00b7 {}</div>'.format(timestamp),
        '  <h1>Who\'s being <span>honest</span> about<br>your storage rate?</h1>',
        '  <p class="hero-sub">We analyzed {} storage facilities in Lincoln so you don\'t sign a lease before you know what month 4 actually costs.</p>'.format(total),
        '  <div class="meter-wrap">',
        '    <div class="meter-label">Fully Transparent Facilities</div>',
        '    <div class="meter-number" id="meterNum">0%</div>',
        '    <div class="meter-bar"><div class="meter-fill" id="meterFill"></div></div>',
        '    <div class="meter-desc">of Lincoln storage facilities clearly disclose ongoing rates upfront</div>',
        '  </div>',
        '</section>',
        '<div class="stats"><div class="stats-inner">',
        '  <div class="stat-item"><div class="stat-number stat-blue">{}</div><div class="stat-label">Analyzed</div></div>'.format(total),
        '  <div class="stat-item"><div class="stat-number stat-green">{}</div><div class="stat-label">Transparent</div></div>'.format(n_green),
        '  <div class="stat-item"><div class="stat-number stat-amber">{}</div><div class="stat-label">Partial</div></div>'.format(n_amber),
        '  <div class="stat-item"><div class="stat-number stat-red">{}</div><div class="stat-label">Deceptive</div></div>'.format(n_red),
        '  <div class="stat-item"><div class="stat-number stat-purple">{}</div><div class="stat-label">Local / Call-First</div></div>'.format(n_local),
        '  <div class="stat-item"><div class="stat-number" style="color:var(--muted)">{}</div><div class="stat-label">No Info</div></div>'.format(n_nodata),
        '</div></div>',
        '<div class="container">',
        '  <div class="nuance-box" style="margin-top:40px;"><div class="nuance-icon">\U0001f4a1</div><div>',
        '    <div class="nuance-title">Pricing online isn\'t the only measure of a good storage facility</div>',
        '    <div class="nuance-text">A chain with a polished website and deceptive fine print is worse for your wallet than a local operator who simply prefers a phone call. <strong>The "Local &amp; Call-First" category is not a red flag</strong> \u2014 it\'s a different kind of facility that may offer better value and more flexibility than any corporate chain.</div>',
        '  </div></div>',
        '  <div class="section-header"><h2>All Facilities Ranked</h2><span class="section-count">{} locations</span></div>'.format(total),
        '  <div class="filter-bar">',
        '    <button class="filter-btn active" onclick="filterCards(\'all\',this)">All ({})</button>'.format(total),
        '    <button class="filter-btn" onclick="filterCards(\'green\',this)">\u2705 Transparent ({})</button>'.format(n_green),
        '    <button class="filter-btn" onclick="filterCards(\'amber\',this)">\u26a0\ufe0f Partial ({})</button>'.format(n_amber),
        '    <button class="filter-btn" onclick="filterCards(\'red\',this)">\U0001f534 Deceptive ({})</button>'.format(n_red),
        '    <button class="filter-btn" onclick="filterCards(\'purple\',this)">\U0001f4de Local / Call-First ({})</button>'.format(n_local),
        '    <button class="filter-btn" onclick="filterCards(\'gray\',this)">\u26ab No Info ({})</button>'.format(n_nodata),
        '  </div>',
        '  <div class="tier-label tier-green" data-tier-label="green"><span class="tier-label-text">\u2705 Transparent \u2014 Score 7\u20138 out of 10</span><div class="tier-label-line"></div></div>',
        '  <div class="cards">', green_cards, '</div>',
        '  <div class="tier-label tier-amber" data-tier-label="amber"><span class="tier-label-text">\u26a0\ufe0f Partial Disclosure \u2014 Score 4\u20136 out of 10</span><div class="tier-label-line"></div></div>',
        '  <div class="cards">', amber_cards, '</div>',
        '  <div class="tier-label tier-red" data-tier-label="red"><span class="tier-label-text">\U0001f534 Deceptive Pricing Language \u2014 Score 3 out of 10</span><div class="tier-label-line"></div></div>',
        '  <div class="cards">', red_cards, '</div>',
        local_section,
        nodata_section,
        '''  <div class="tips-section">
    <h2>5 Questions to Ask Before You Sign</h2>
    <p class="tips-intro">The lease is where storage facilities make their money. Here\'s how to protect yourself.</p>
    <div class="tips-grid">
      <div class="tip-card"><div class="tip-icon">\U0001f4c5</div><div class="tip-title">"What\'s my rate in month 4?"</div><div class="tip-text">The most important question. If the answer differs from what\'s advertised, that\'s your red flag. Get the ongoing rate in writing before you sign.</div></div>
      <div class="tip-card"><div class="tip-icon">\U0001f4c8</div><div class="tip-title">"How often do you raise rates?"</div><div class="tip-text">Industry average is 8\u201310% annually. Facilities with "at our discretion" language can raise rates anytime with 30 days notice.</div></div>
      <div class="tip-card"><div class="tip-icon">\U0001f512</div><div class="tip-title">"Is there a price lock?"</div><div class="tip-text">U-Haul offers a 1-year price lock as standard \u2014 the gold standard in Lincoln. Ask any facility if they\'ll match it in writing.</div></div>
      <div class="tip-card"><div class="tip-icon">\U0001f4b3</div><div class="tip-title">"Are there fees beyond rent?"</div><div class="tip-text">Watch for: admin fees, mandatory insurance ($15\u201320/mo), credit card surcharges (StorageMart charges 2.5%), and required lock purchases.</div></div>
      <div class="tip-card"><div class="tip-icon">\U0001f91d</div><div class="tip-title">"Do you price-match?"</div><div class="tip-text">Powerful with local operators especially. Show them a competitor\'s rate \u2014 many will match or beat it rather than lose the rental.</div></div>
    </div>
  </div>''',
        '''  <div class="methodology">
    <h3>How We Score</h3>
    <p>TrueStore\'s transparency score (1\u201310) measures how clearly a facility discloses real ongoing pricing before a consumer commits. We evaluate: whether ongoing rates are published online, whether rate-increase language appears in fine print, whether fees are disclosed upfront, and whether a price lock exists.</p>
    <p>A score of 7\u20138 means a consumer can make a fully informed decision from the website alone. A score of 4\u20136 means pricing exists and is accessible in a browser but requires extra steps. A score of 3 means fine print allows rates to change "at any time at our discretion."</p>
    <p><strong>The "Local &amp; Call-First" category is not scored</strong> \u2014 these are verified independently owned operators. A family business serving Lincoln for 35+ years is not comparable to a corporate chain with deceptive fine print.</p>
    <p style="margin-top:12px;">Data collected {}. Prices subject to change \u2014 verify before signing. TrueStore is not affiliated with any storage facility.</p>
  </div>'''.format(timestamp),
        '</div>',
        '<div class="footer"><strong>TrueStore</strong> \u2014 Consumer Price Transparency for Self-Storage &nbsp;\u00b7&nbsp; Lincoln, NE &nbsp;\u00b7&nbsp; {}<br><span style="margin-top:4px;display:block;">Independent research. Not affiliated with any storage facility. Always verify rates before signing.</span></div>'.format(timestamp),
        '<script>', js_final, '</script>',
        '</body></html>'
    ]

    html = '\n'.join(parts)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_path = os.path.join(OUTPUT_DIR, 'report_lincoln_{}.html'.format(ts))
    latest_path      = os.path.join(OUTPUT_DIR, 'TrueStore_Lincoln_Report.html')

    with open(timestamped_path, 'w', encoding='utf-8') as f: f.write(html)
    with open(latest_path,      'w', encoding='utf-8') as f: f.write(html)

    print('HTML report saved: {}'.format(timestamped_path))
    print('Latest report:     {}'.format(latest_path))
    return latest_path
