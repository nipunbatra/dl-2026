"""Build the DL 2026 mockup pages from the lecture data extracted from schedule.qmd."""
import json, html, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
MODS = json.load(open(os.path.join(HERE, '..', 'lectures.json')))
LIVE = 'https://nipunbatra.github.io/dl-2026/'
SLACK = 'https://join.slack.com/t/dl26workspace/shared_invite/zt-43b3v79vb-bVZl1_sJVCrBkVMDsq5TYA'
PLAYLIST_FULL = 'https://www.youtube.com/playlist?list=PLGRBnxCA2r9c'
PLAYLIST_SHORT = 'https://www.youtube.com/playlist?list=PLP_52n19dyQM'
MATERIALS = 'https://nipunbatra.github.io/dl-teaching/'
e = html.escape

SHORT = {'foundations-title': ('foundations', 'Foundations'),
         'gradients-optimization-title': ('optimization', 'Gradients and optimization'),
         'generalization-title': ('generalization', 'Generalization'),
         'attention-and-language-title': ('attention', 'Attention and language'),
         'vision-title': ('vision', 'Vision and language')}
for m in MODS:
    m['slug'], m['name'] = SHORT[m['id']]
    ns = [int(L['n']) for L in m['lectures']]
    m['range'] = f'{ns[0]}–{ns[-1]}' if len(ns) > 1 else str(ns[0])
LECTURES = [(m, L) for m in MODS for L in m['lectures']]

# Today in the mockups: Monday 5 October 2026, week 10 of the semester.
DEADLINES = [
    ('2026-08-04', '04 Aug', 'Course begins', None, ''),
    ('2026-08-17', '17 Aug', 'Add–drop period ends', None, ''),
    ('2026-08-19', '19 Aug', 'Assignment 1 released', 'a-assignment.html#a1', 'a'),
    ('2026-08-27', '27 Aug', 'Assignment 1 due', 'a-assignment.html#a1', 'a'),
    ('2026-09-10', '10 Sep', 'Quiz 1', None, 'q'),
    ('2026-09-30', '30 Sep', 'Assignment 2 released', 'a-assignment.html', 'a'),
    ('2026-10-08', '08 Oct, 6:30 pm', 'Assignment 2 due', 'a-assignment.html', 'a'),
    ('2026-10-08', '08 Oct, 6:30 pm', 'Assignment 2 quiz', None, 'q'),
    ('2026-10-15', '15 Oct', 'Quiz 2', None, 'q'),
    ('2026-10-16', '16 Oct', 'Assignment 3 released', None, 'a'),
    ('2026-11-02', '02 Nov', 'Assignment 3 due', None, 'a'),
    ('2026-11-10', '10 Nov', 'Quiz 3', None, 'q'),
]
TODAY = '2026-10-05'
WEEKDAY = {'2026-10-08': 'Thu', '2026-10-15': 'Thu', '2026-10-16': 'Fri', '2026-11-02': 'Mon', '2026-11-10': 'Tue'}
DAYS_LEFT = {'2026-10-08': 3, '2026-10-15': 10, '2026-10-16': 11, '2026-11-02': 28, '2026-11-10': 36}

LINK_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1.2 1.2"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1.2-1.2"/></svg>'


ICONS = {
    'notes': ('Notes', '<path d="M3 5.5c3-1.3 6-1.3 9 .8 3-2.1 6-2.1 9-.8V19c-3-1.3-6-1.3-9 .8-3-2.1-6-2.1-9-.8z"/><path d="M12 6.3v13.5"/>'),
    'slides': ('Slides', '<rect x="3" y="4" width="18" height="12" rx="1"/><path d="M12 16v4M8 20h8M8 12.5v-2M12 12.5V8M16 12.5v-3"/>'),
    'cheat': ('Cheat sheet', '<rect x="4" y="6" width="12" height="15" rx="1"/><path d="M8 6V3h12v15h-4M7 11h6M7 14h6M7 17h3.5"/>'),
    'pdf': ('PDF handout', '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M12.5 10v7m-3-3 3 3 3-3"/>'),
    'recording': ('Full recording', '<rect x="3" y="6" width="13" height="12" rx="1.5"/><path d="m16 10.5 5-3v9l-5-3z"/>'),
    'short': ('3-minute summary', '<circle cx="12" cy="13.5" r="7.5"/><path d="M12 13.5V10M10 2.5h4M12 2.5V6M18 6.5l1.3-1.3"/>'),
    'notebook': ('Notebook', '<rect x="3" y="4" width="18" height="16" rx="1.5"/><path d="m9.5 9.5-3 2.5 3 2.5M14.5 9.5l3 2.5-3 2.5"/>'),
    'lab': ('Interactive lab', '<path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2"/><circle cx="9" cy="17" r="2"/>'),
}


def icon(k):
    return f'<svg class="ic ic-{k}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[k][1]}</svg>'


def res(k, href, text, dur=''):
    d = f'<span class="dur">{dur}</span>' if dur else ''
    ext = ' target="_blank" rel="noopener noreferrer"' if href.startswith('http') else ''
    return f'<a class="r r-{k}" href="{e(href)}"{ext} title="{ICONS[k][0]}">{icon(k)}<span class="t">{text}</span>{d}</a>'


def key_html():
    return '<div class="key" aria-label="Key">' + ''.join(f'<span>{icon(k)}{t}</span>' for k, (t, _) in ICONS.items()) + '</div>'


def anchor(page, target, what):
    url = f'{LIVE}{page}#{target}'
    return (f'<button type="button" class="anchor" data-url="{url}" data-target="{target}" '
            f'aria-label="Copy link to {e(what)}" title="Copy link">{LINK_SVG}<span class="done">Copied</span></button>')


def kind(label):
    l = label.lower()
    if 'cheat' in l: return 'cheat'
    if 'colab' in l: return 'practice'
    if l.startswith('pdf'): return 'pdf'
    if 'slide' in l: return 'slides'
    return 'notes'


def short_label(label):
    """Consistent labels: Notes, Slides, Cheat sheet, PDF (n pp.), keeping the topic for split lectures."""
    l = label
    m = re.match(r'PDF · (\d+) pages', l)
    if m: return f'PDF · {m.group(1)} pp.'
    if l in ('HTML lecture', 'Interactive notes', 'Lecture slides'): return 'Notes' if l != 'Lecture slides' else 'Slides'
    if l == 'PDF handout': return 'PDF'
    if l == 'Applications Colab': return 'Colab'
    return l


def read_links(L):
    return [(short_label(lab), href, kind(lab)) for lab, href in L['buttons'] if kind(lab) != 'practice']


def extras(L, k):
    out = []
    for x in L['extras']:
        if x['kind'] == k: out += x['items']
    return out


def practice(L):
    p = [(t, h) for t, h, _ in extras(L, 'resource-code')]
    p += [('Applications Colab', h) for lab, h in L['buttons'] if kind(lab) == 'practice']
    return p


def practice_k(L):
    out = []
    for x in L['extras']:
        if x['kind'] == 'resource-code':
            k = 'lab' if 'nteractive' in x['title'] else 'notebook'
            out += [(k, t, h) for t, h, _ in x['items']]
    out += [('notebook', 'Applications Colab', h) for lab, h in L['buttons'] if kind(lab) == 'practice']
    return out


def a(href, text, cls=''):
    ext = href.startswith('http')
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="{e(href)}"' + (' target="_blank" rel="noopener noreferrer"' if ext else '') + f'>{text}</a>'


def head(title, extra_css=''):
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="dl.css"><script src="dl.js"></script>
<style>{extra_css}</style>'''


MOCKS = [('index.html', 'Overview'), ('a-home.html', 'Home'), ('a-lectures.html', 'Lectures'),
         ('a-assessment.html', 'Assessment'), ('a-assignment.html', 'Assignment')]


def mockbar(cur):
    items = ''.join(f'<a href="{h}"' + (' aria-current="page"' if h == cur else '') + f'>{t}</a>' for h, t in MOCKS)
    return f'<div class="mockbar"><div class="mockbar-in"><strong>Mockup · ES 667</strong>{items}</div></div>'


SWITCH = ('<div class="appearance"><button type="button" class="mode" role="switch" aria-checked="false" aria-label="Switch to dark mode">'
          '<span class="sky"></span><span class="stars"><b style="left:9px;top:6px"></b><b style="left:15px;top:15px"></b>'
          '<b style="left:5px;top:17px"></b></span><span class="knob"></span></button></div>')


def rail(cur, items, spy=False):
    nav = ''
    for href, text in items:
        cls = ' class="ext"' if href.startswith('http') else ''
        cur_attr = ' aria-current="page"' if href == cur else ''
        nav += f'<a{cls} href="{href}"{cur_attr}>{text}</a>'
    sp = ' data-spy' if spy else ''
    return (f'<aside class="rail"><a class="code" href="{items[0][0]}" style="text-decoration:none">ES 667</a>'
            f'<span class="inst">IIT Gandhinagar</span>{SWITCH}<nav aria-label="Course"{sp}>{nav}</nav></aside>')


FOOT = ('<footer class="foot"><span>Prof. Nipun Batra · IIT Gandhinagar · Semester I, 2026–27</span>'
        f'<span>{a("https://nipunbatra.github.io", "nipunbatra.github.io")}</span></footer>')


def page(fname, title, css, cur_mock, rail_html, body):
    out = head(title, css) + mockbar(cur_mock) + f'<div class="frame">{rail_html}<main id="main">{body}</main>{FOOT}</div>'
    open(os.path.join(HERE, fname), 'w').write(out)


def upcoming(n=None):
    rows = [d for d in DEADLINES if d[0] >= TODAY]
    return rows[:n] if n else rows


FACTS = [('Instructor', a('https://nipunbatra.github.io', 'Prof. Nipun Batra')),
         ('Office', '13/401C'),
         ('Credits', '3-0-0-4'),
         ('Email', 'nipun.batra@iitgn.ac.in'),
         ('Discussion', a(SLACK, 'Course Slack'))]

INTRO = 'ES 667 develops deep-learning models from their statistical and computational foundations.'
OVERVIEW = ('The course begins with likelihood, loss functions and multilayer networks, and proceeds to '
            'convolutional models, sequence models, Transformers, representation learning and generative models.')
REFS = [('Simon J. D. Prince', 'Understanding Deep Learning', 'https://udlbook.github.io/udlbook/'),
        ('Christopher M. Bishop and Hugh Bishop', 'Deep Learning: Foundations and Concepts', None),
        ('Aston Zhang, Zachary C. Lipton, Mu Li and Alexander J. Smola', 'Dive into Deep Learning', 'https://d2l.ai/')]


def refs_html():
    li = ''
    for who, t, url in REFS:
        li += f'<li>{e(who)}, <i>{e(t)}</i>' + (f' ({a(url, "online")})' if url else '') + '</li>'
    return f'<ul class="refs">{li}</ul>'


GRADING = [('Quizzes', 54, 'Three closed-book quizzes; the best two count, 27 marks each. No makeup quizzes.'),
           ('Assignments', 39, 'Three programming assignments in Python and PyTorch, 13 marks each, each followed by a short individual viva on your own submission.'),
           ('Attendance', 7, 'Biometric. Full marks for up to four missed classes, then 5, 3, 1 and 0.')]
ATTEND = [('≤ 4', 7), ('5–6', 5), ('7–8', 3), ('9–10', 1), ('> 10', 0)]
FAQ = [('Is there a final project?', 'No separate final project. Each of the three assignments is a substantial programming task, so you get project-scale practice throughout the semester.'),
       ('How are assignments graded?', 'You submit code by the deadline, then take a short individual quiz or viva on your own submission. The viva is where the marks are decided: be ready to explain your code, your plots and your choices.'),
       ('Language and framework?', 'Python and PyTorch. No other frameworks (TensorFlow, JAX) unless explicitly allowed.'),
       ('Do I need a GPU?', 'Not for everything, but some assignments benefit from one. A free Colab GPU is enough; any extra compute credits will be announced on Slack.'),
       ('Where are the slides and notebooks?', 'In the lecture list on this site. Every lecture links its notes, slides, cheat sheet, notebooks and videos.'),
       ('Can I use AI tools?', 'Yes, honestly and with meaningful assistance documented. What is assessed is your ability to explain your own work in the viva.')]

# ---------------------------------------------------------------- Direction A
A_NAV = [('a-home.html', 'Home'), ('a-lectures.html', 'Lectures'), ('a-assessment.html', 'Assessment'),
         ('a-assignment.html', 'Assignments'), ('a-home.html#faq', 'FAQ'), (SLACK, 'Slack')]

A_CSS = '''
.top { display:grid; grid-template-columns:minmax(0,1fr) 300px; gap:28px 44px; }
.facts { display:grid; grid-template-columns:auto 1fr; gap:4px 18px; font-size:14px; margin:0; border-top:1px solid var(--rule); padding-top:14px; }
.facts dt { color:var(--muted); } .facts dd { margin:0; }
.next { background:var(--soft); padding:18px 20px; align-self:start; }
.next ol { list-style:none; margin:0; padding:0; display:grid; gap:12px; }
.next li { display:grid; grid-template-columns:84px 1fr; gap:10px; font-size:14px; line-height:1.4; }
.next .d { font:700 15px/1.2 var(--heading); letter-spacing:-.02em; font-variant-numeric:tabular-nums; }
.next .d small { display:block; font:500 11px/1.4 var(--body); color:var(--muted); letter-spacing:.02em; }
.next li.hot .d { color:var(--accent); }
.latest { display:grid; grid-template-columns:72px minmax(0,1fr); gap:6px 20px; }
.latest .big { font:800 64px/0.9 var(--heading); letter-spacing:-.06em; color:var(--accent); font-variant-numeric:tabular-nums; }
.modules { list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); border-top:2px solid var(--ink); }
.modules li { padding:12px 14px 4px 0; min-width:0; }
.modules li + li { border-left:1px solid var(--rule); padding-left:14px; }
.modules .r { font:700 22px/1.1 var(--heading); letter-spacing:-.04em; font-variant-numeric:tabular-nums; display:block; color:var(--ink); }
.modules a { color:var(--ink); font-size:14px; line-height:1.35; display:block; margin-top:6px; }
.modules a:hover { color:var(--accent); }
.modules .c { font-size:12px; color:var(--muted); }
.refs { padding-left:18px; margin:0; font-size:15px; } .refs li { padding:3px 0; }
details.q { border-top:1px solid var(--rule); padding:10px 0; }
details.q summary { cursor:pointer; font-weight:600; }
details.q p { margin:8px 0 2px; max-width:66ch; color:var(--ink); }
.two { display:grid; grid-template-columns:1fr 1fr; gap:34px; }
.two > section { min-width:0; }
.two > section + section { border-left:1px solid var(--rule); padding-left:34px; }
/* Lectures index */
.mod-h { display:flex; align-items:baseline; gap:12px; margin:36px 0 0; padding-bottom:8px; border-bottom:2px solid var(--ink); }
.mod-h h2 { margin:0; font:700 26px/1.2 var(--heading); letter-spacing:-.035em; }
.mod-h .r { color:var(--muted); font-size:13px; font-variant-numeric:tabular-nums; margin-left:auto; }
.lt { width:100%; border-collapse:collapse; }
.lt td { padding:14px 16px 14px 0; border-bottom:1px solid var(--rule); vertical-align:top; }
.lt td.no { width:52px; font:700 22px/1.1 var(--heading); letter-spacing:-.04em; color:var(--muted); font-variant-numeric:tabular-nums; }
.lt tr:hover td.no { color:var(--accent); }
.lt h3 { font:600 17px/1.3 var(--heading); letter-spacing:-.02em; margin:0 0 3px; }
.lt .sub { font-size:13.5px; color:var(--muted); margin:0; max-width:56ch; }
.lt td.res { width:46%; }
.rl { display:flex; flex-wrap:wrap; gap:6px 16px; padding:3px 0; }
.rl + .rl { border-top:1px dashed var(--rule); margin-top:5px; padding-top:7px; }
.rl.vids, .rl.prac { flex-direction:column; gap:4px; }
.r { display:inline-flex; align-items:flex-start; gap:7px; font-size:13.5px; line-height:1.35; color:var(--ink); }
.r:hover { color:var(--accent); text-decoration:none; } .r:hover .t { text-decoration:underline; text-underline-offset:3px; }
.r .dur { margin-left:2px; }
.ic { width:18px; height:18px; flex:none; fill:none; stroke:currentColor; stroke-width:1.6; stroke-linecap:round; stroke-linejoin:round; color:var(--accent); margin-top:-1px; }
.r-recording .ic, .r-short .ic { color:var(--ink); }
.r-recording .t { font-weight:600; }
.r-notebook .ic, .r-lab .ic { color:var(--muted); }
.key { display:flex; flex-wrap:wrap; gap:8px 20px; font-size:13px; color:var(--muted); padding:12px 0 14px; }
.key span { display:inline-flex; align-items:center; gap:6px; }
.key .ic { margin:0; }
.key .ic-recording, .key .ic-short { color:var(--ink); } .key .ic-notebook, .key .ic-lab { color:var(--muted); }
.btn.ib { display:inline-flex; align-items:center; gap:7px; } .btn.ib .ic { color:currentColor; margin:0; }
.lt .grp { display:grid; grid-template-columns:62px minmax(0,1fr); gap:2px 10px; font-size:13.5px; padding:2px 0; }
.lt .grp > span { color:var(--muted); font-size:11px; letter-spacing:.07em; text-transform:uppercase; padding-top:2px; }
.lt .grp .links { font-size:13.5px; } .lt .v { white-space:nowrap; } .lt .v a { white-space:normal; }
.jump { display:flex; flex-wrap:wrap; gap:6px 22px; font-size:14px; padding:12px 0; border-top:1px solid var(--rule); border-bottom:1px solid var(--rule); }
.jump a { color:var(--ink); } .jump a:hover { color:var(--accent); }
.jump .num { color:var(--muted); font-size:12px; margin-left:4px; }
.playlists { display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; }
@media (max-width:1000px) { .top { grid-template-columns:1fr; } .modules { grid-template-columns:repeat(3,minmax(0,1fr)); row-gap:10px; } .modules li:nth-child(4) { border-left:0; padding-left:0; } }
@media (max-width:760px) {
  .two { grid-template-columns:1fr; } .two > section + section { border-left:0; padding-left:0; border-top:1px solid var(--rule); padding-top:22px; }
  .lt, .lt tbody, .lt tr, .lt td { display:block; width:auto !important; }
  .lt tr { display:grid; grid-template-columns:44px minmax(0,1fr); border-bottom:1px solid var(--rule); padding:12px 0; }
  .lt td { border:0; padding:0; } .lt td.res { grid-column:2; padding-top:8px; }
}
@media (max-width:560px) { .modules { grid-template-columns:1fr 1fr; } .modules li:nth-child(odd) { border-left:0; padding-left:0; } .modules li:nth-child(4) { border-left:1px solid var(--rule); padding-left:14px; } .latest { grid-template-columns:1fr; } }
'''


def a_lecture_row(m, L, page='schedule.html'):
    rid = f'lecture-{L["n"]}'
    mats = ''.join(res(k, h, e(t)) for t, h, k in read_links(L))
    recs = extras(L, 'resource-recording')
    vids = ''.join(res('recording', h, 'Full recording' + (f' {i + 1}' if len(recs) > 1 else ''), d) for i, (t, h, d) in enumerate(recs))
    vids += ''.join(res('short', h, e(t), d) for t, h, d in extras(L, 'resource-short'))
    prac = ''.join(res(k, h, e(t)) for k, t, h in practice_k(L))
    grp = f'<div class="rl mats">{mats}</div>'
    if vids: grp += f'<div class="rl vids">{vids}</div>'
    if prac: grp += f'<div class="rl prac">{prac}</div>'
    sub = f'<p class="sub">{e(L["sub"])}</p>' if L['sub'] else ''
    sub = re.sub(r' \d+ slides including the cover\.', '', sub)
    return (f'<tr id="{rid}" data-lecture data-module="{m["slug"]}"><td class="no">{int(L["n"]):02d}</td>'
            f'<td><h3>{e(L["title"])}{anchor(page, rid, "lecture " + L["n"])}</h3>{sub}</td><td class="res">{grp}</td></tr>')


def build_a():
    nxt = ''
    groups = {}
    for iso, d, what, href, k in upcoming():
        groups.setdefault(iso, []).append((d, what, href))
    for iso in list(groups)[:4]:
        evs = groups[iso]; d = evs[0][0]
        hot = ' class="hot"' if DAYS_LEFT.get(iso, 99) <= 3 else ''
        when = f'{d.split(",")[0]}<small>{WEEKDAY.get(iso, "")}' + (f' {d.split(", ")[1]}' if ', ' in d else '') + f'<br>in {DAYS_LEFT[iso]} days</small>'
        what = '<br>'.join(a(h, e(w)) if h else e(w) for _, w, h in evs)
        nxt += f'<li{hot}><span class="d">{when}</span><span>{what}</span></li>'
    m, L = LECTURES[-1]
    latest_links = ' '.join(a(h, t) for t, h, k in read_links(L)) + ''.join(a(h, e(t)) for t, h in practice(L))
    mods = ''.join(f'<li><span class="r">{m["range"]}</span><a href="a-lectures.html#{m["slug"]}">{e(m["name"])}</a>'
                   f'<span class="c">{len(m["lectures"])} lecture{"s" if len(m["lectures"]) > 1 else ""}</span></li>' for m in MODS)
    facts = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in FACTS)
    faq = ''.join(f'<details class="q"><summary>{e(q)}</summary><p>{e(t)}</p></details>' for q, t in FAQ)
    body = f'''
<div class="top">
 <div style="min-width:0">
  <h1 class="h1">Deep Learning</h1>
  <p class="role">ES 667 · IIT Gandhinagar · Semester I, 2026–27</p>
  <p class="lede" style="margin-top:18px">{e(INTRO)} {e(OVERVIEW)}</p>
  <dl class="facts">{facts}</dl>
 </div>
 <aside class="next" aria-labelledby="next-h"><span class="label" id="next-h">Coming up</span><ol>{nxt}</ol>
  <p class="small" style="margin:14px 0 0">{a("a-assessment.html#deadlines", "All dates")}</p></aside>
</div>

<section class="rule-top" id="lectures"><h2 class="h2">Lectures{anchor("index.html", "lectures", "lectures")}</h2>
 <ul class="modules">{mods}</ul>
 <div class="playlists"><a class="btn ib" href="{PLAYLIST_FULL}" target="_blank" rel="noopener noreferrer">{icon("recording")}Full lecture playlist</a><a class="btn ib" href="{PLAYLIST_SHORT}" target="_blank" rel="noopener noreferrer">{icon("short")}3-minute summaries playlist</a>{a("a-lectures.html", "All 20 lectures", "btn solid")}</div>
</section>

<div class="two rule-top">
 <section id="faq"><h2 class="h2">Questions{anchor("index.html", "faq", "questions")}</h2>{faq}
  <p class="small muted" style="margin-top:12px">Anything else: ask on {a(SLACK, "the course Slack")}.</p></section>
 <section id="references"><h2 class="h2">References{anchor("index.html", "references", "references")}</h2>
  <p class="small muted">There is no required textbook.</p>{refs_html()}</section>
</div>'''
    page('a-home.html', 'ES 667 Home', A_CSS, 'a-home.html', rail('a-home.html', A_NAV), body)

    jump = ''.join(f'<a href="#{m["slug"]}">{e(m["name"])}<span class="num">{m["range"]}</span></a>' for m in MODS)
    blocks = ''
    for m in MODS:
        rows = ''.join(a_lecture_row(m, L) for L in m['lectures'])
        blocks += (f'<section id="{m["slug"]}"><div class="mod-h"><h2>{e(m["name"])}{anchor("schedule.html", m["slug"], m["name"])}</h2>'
                   f'<span class="r">Lectures {m["range"]}</span></div><table class="lt"><tbody>{rows}</tbody></table></section>')
    body = f'''<h1 class="h1">Lectures</h1>
<p class="lede">Each lecture lists its reading material first, then its videos, then practice. Every kind of resource has its own icon.</p>
{key_html()}
<nav class="jump" aria-label="Modules">{jump}</nav>
<div class="playlists"><a class="btn ib" href="{PLAYLIST_FULL}" target="_blank" rel="noopener noreferrer">{icon("recording")}Full lecture playlist</a><a class="btn ib" href="{PLAYLIST_SHORT}" target="_blank" rel="noopener noreferrer">{icon("short")}3-minute summaries playlist</a></div>
{blocks}'''
    page('a-lectures.html', 'ES 667 Lectures', A_CSS, 'a-lectures.html', rail('a-lectures.html', A_NAV), body)

    rows = ''
    for iso, d, what, href, k in DEADLINES:
        cls = 'past' if iso < TODAY else ''
        if iso >= TODAY and not any(x[0] >= TODAY for x in DEADLINES if x[0] < iso): cls = ''
        w = a(href, e(what)) if href else e(what)
        if k == 'q': w = f'<b>{w}</b>'
        tag = '<span class="pill now">This week</span>' if DAYS_LEFT.get(iso, 99) <= 3 else ''
        rows += f'<tr class="{cls}"><td class="n">{d}</td><td>{w}</td><td style="text-align:right">{tag}</td></tr>'
        if iso < TODAY and DEADLINES[DEADLINES.index((iso, d, what, href, k)) + 1][0] >= TODAY:
            rows += '<tr class="today"><td class="n" style="color:var(--accent);font-weight:600">Today, 05 Oct</td><td colspan="2" class="muted small">Week 10</td></tr>'
    grade = ''.join(f'<tr><th>{c}</th><td class="n" style="font:700 22px/1.1 var(--heading);letter-spacing:-.03em">{n}</td><td>{e(t)}</td></tr>' for c, n, t in GRADING)
    att = ''.join(f'<tr><td class="n">{x}</td><td class="n">{y}</td></tr>' for x, y in ATTEND)
    body = f'''<h1 class="h1">Assessment</h1>
<p class="lede">Grading and every dated event in one place. All times are IST. Each assignment is followed by a short individual viva, separate from the three course quizzes.</p>
<div class="two rule-top" style="margin-top:22px">
<section id="deadlines"><h2 class="h2">Dates{anchor("assessment.html", "deadlines", "dates")}</h2>
 <div class="tablewrap"><table class="t"><tbody>{rows}</tbody></table></div></section>
<section id="grading"><h2 class="h2">Grading{anchor("assessment.html", "grading", "grading")}</h2>
 <div class="tablewrap"><table class="t"><thead><tr><th>Component</th><th class="n">Marks</th><th>How</th></tr></thead><tbody>{grade}
 <tr><th>Total</th><td class="n" style="font:700 22px/1.1 var(--heading)">100</td><td></td></tr></tbody></table></div>
 <h3 class="h3" id="attendance" style="margin-top:26px">Attendance{anchor("assessment.html", "attendance", "attendance")}</h3>
 <table class="t" style="max-width:260px"><thead><tr><th>Classes missed</th><th class="n">Marks</th></tr></thead><tbody>{att}</tbody></table>
 <p class="small muted" style="margin-top:10px">There is no leave-request system. For an emergency that forces several missed classes in a row, talk to the instructor.</p>
 <h3 class="h3" id="ai" style="margin-top:22px">AI tools{anchor("assessment.html", "ai", "AI tools policy")}</h3>
 <p class="small" style="max-width:56ch">Use AI tools honestly and document meaningful assistance. What is assessed is your ability to explain your own decisions and results in the viva.</p>
</section></div>'''
    page('a-assessment.html', 'ES 667 Assessment', A_CSS, 'a-assessment.html', rail('a-assessment.html', A_NAV), body)


# ---------------------------------------------------------------- Direction B
B_CSS = '''
.sec { border-top:1px solid var(--rule); padding-top:24px; margin-top:40px; scroll-margin-top:16px; }
.sec:first-of-type { border-top:0; margin-top:0; padding-top:0; }
.sec > h2 { font:700 30px/1.15 var(--heading); letter-spacing:-.04em; margin-bottom:16px; }
.cal { position:relative; margin:8px 0 6px; overflow-x:auto; }
.cal-in { position:relative; min-width:680px; height:196px; margin:0 46px; }
.cal .axis { position:absolute; left:0; right:0; top:84px; height:2px; background:var(--ink); }
.cal .mon { position:absolute; top:92px; font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); }
.cal .tick { position:absolute; top:78px; width:1px; height:14px; background:var(--ink); }
.cal .ev { position:absolute; transform:translateX(-50%); font-size:11.5px; line-height:1.25; text-align:center; width:86px; }
.cal .ev.up { top:28px; } .cal .ev.down { top:116px; } .cal .ev.down2 { top:156px; }
.cal .ev b { display:block; font-variant-numeric:tabular-nums; font-size:11px; color:var(--muted); font-weight:600; }
.cal .dot { position:absolute; top:79px; width:12px; height:12px; border-radius:50%; transform:translateX(-50%); background:var(--paper); border:2px solid var(--ink); }
.cal .dot.q { background:var(--ink); }
.cal .dot.past { border-color:var(--muted); background:var(--paper); } .cal .dot.q.past { background:var(--muted); }
.cal .ev.past { color:var(--muted); }
.cal .today { position:absolute; top:18px; height:96px; width:2px; background:var(--accent); }
.cal .today span { position:absolute; top:-16px; left:50%; transform:translateX(-50%); font:700 11px/1 var(--body); color:var(--accent); letter-spacing:.08em; text-transform:uppercase; white-space:nowrap; }
.legend { display:flex; gap:18px; font-size:12px; color:var(--muted); }
.legend i { display:inline-block; width:10px; height:10px; border-radius:50%; border:2px solid var(--ink); margin-right:6px; vertical-align:-1px; }
.legend i.q { background:var(--ink); }
.week { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); border-top:2px solid var(--accent); }
.week > div { padding:14px 18px 6px 0; min-width:0; }
.week > div + div { border-left:1px solid var(--rule); padding-left:18px; }
.week .k { font:600 11px/1.3 var(--body); letter-spacing:.09em; text-transform:uppercase; color:var(--muted); display:block; margin-bottom:6px; }
.week .big { font:800 34px/1 var(--heading); letter-spacing:-.05em; display:block; margin-bottom:6px; font-variant-numeric:tabular-nums; }
.week p { font-size:14px; margin:0; }
.mlist { display:grid; grid-template-columns:minmax(0,1fr); }
.lrow { display:grid; grid-template-columns:40px minmax(0,1fr) auto; gap:4px 16px; padding:11px 0; border-bottom:1px solid var(--rule); align-items:baseline; scroll-margin-top:16px; }
.lrow .no { font:700 15px/1.3 var(--heading); color:var(--muted); font-variant-numeric:tabular-nums; }
.lrow h3 { font:600 16px/1.35 var(--body); margin:0; }
.lrow .links { justify-content:flex-end; font-size:13px; }
.lrow details { grid-column:2/-1; font-size:13.5px; }
.lrow summary { cursor:pointer; color:var(--muted); font-size:12.5px; }
.lrow details .links { justify-content:flex-start; margin-top:6px; }
.mhead { font:700 13px/1.3 var(--body); letter-spacing:.08em; text-transform:uppercase; color:var(--accent); margin:26px 0 0; padding-bottom:6px; border-bottom:2px solid var(--ink); display:flex; gap:10px; }
.mhead span { color:var(--muted); font-weight:500; margin-left:auto; letter-spacing:0; text-transform:none; }
.marks { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:0; border-top:2px solid var(--ink); }
.marks > div { padding:14px 18px 0 0; min-width:0; } .marks > div + div { border-left:1px solid var(--rule); padding-left:18px; }
.marks .big { font:800 48px/1 var(--heading); letter-spacing:-.06em; display:block; font-variant-numeric:tabular-nums; }
.marks h3 { font:600 16px/1.3 var(--heading); margin:6px 0 4px; } .marks p { font-size:13.5px; color:var(--muted); margin:0; }
details.q { border-top:1px solid var(--rule); padding:10px 0; } details.q summary { cursor:pointer; font-weight:600; } details.q p { margin:8px 0 2px; max-width:66ch; }
.faqcols { display:grid; grid-template-columns:1fr 1fr; gap:0 34px; }
.refs { padding-left:18px; margin:0; font-size:15px; } .refs li { padding:3px 0; }
@media (max-width:760px) { .week, .marks { grid-template-columns:1fr; } .week > div + div, .marks > div + div { border-left:0; padding-left:0; border-top:1px solid var(--rule); padding-top:12px; margin-top:8px; }
  .faqcols { grid-template-columns:1fr; } .lrow { grid-template-columns:34px minmax(0,1fr); } .lrow .links { grid-column:2; justify-content:flex-start; } }
'''


def build_b():
    nav = [('#overview', 'Overview'), ('#this-week', 'This week'), ('#calendar', 'Calendar'), ('#lectures', 'Lectures'),
           ('#assessment', 'Assessment'), ('#questions', 'Questions'), (SLACK, 'Slack')]
    # Calendar scale: 1 Aug to 15 Nov.
    import datetime as dt
    t0, t1 = dt.date(2026, 8, 1), dt.date(2026, 11, 15)
    span = (t1 - t0).days
    pos = lambda iso: 100 * (dt.date.fromisoformat(iso) - t0).days / span
    cal = '<div class="axis"></div>'
    for mo, iso in (('Aug', '2026-08-01'), ('Sep', '2026-09-01'), ('Oct', '2026-10-01'), ('Nov', '2026-11-01')):
        cal += f'<span class="tick" style="left:{pos(iso):.2f}%"></span><span class="mon" style="left:calc({pos(iso):.2f}% + 4px)">{mo}</span>'
    TIER = {'2026-08-04': 'up', '2026-08-19': 'down', '2026-08-27': 'up', '2026-09-10': 'down', '2026-09-30': 'up',
            '2026-10-08': 'down', '2026-10-15': 'up', '2026-10-16': 'down2', '2026-11-02': 'up', '2026-11-10': 'down'}
    shown = [d for d in DEADLINES if d[2] not in ('Add–drop period ends',)]
    merged = {}
    for iso, d, what, href, k in shown:
        merged.setdefault(iso, []).append((d, what, k))
    for iso, evs in merged.items():
        past = ' past' if iso < TODAY else ''
        k = 'q' if any(x[2] == 'q' for x in evs) else ''
        label = ' and '.join(x[1] for x in evs).replace('Assignment 2 due and Assignment 2 quiz', 'Assignment 2 due and quiz')
        cal += f'<span class="dot {k}{past}" style="left:{pos(iso):.2f}%"></span>'
        cal += f'<span class="ev {TIER[iso]}{past}" style="left:{pos(iso):.2f}%"><b>{evs[0][0].split(",")[0]}</b>{e(label)}</span>'
    cal += f'<span class="today" style="left:{pos(TODAY):.2f}%"><span>Today</span></span>'

    lec = ''
    for m in MODS:
        lec += f'<div class="mhead" id="{m["slug"]}">{e(m["name"])}{anchor("index.html", m["slug"], m["name"])}<span>{m["range"]}</span></div>'
        for L in m['lectures']:
            rid = f'lecture-{L["n"]}'
            main = ' '.join(a(h, t) for t, h, k in read_links(L) if k in ('notes', 'slides', 'cheat'))
            more = [a(h, t) for t, h, k in read_links(L) if k == 'pdf']
            more += [a(h, e(t)) + (f'<span class="dur">{d}</span>' if d else '') for t, h, d in extras(L, 'resource-recording')]
            more += [a(h, e(t)) + (f'<span class="dur">{d}</span>' if d else '') for t, h, d in extras(L, 'resource-short')]
            more += [a(h, e(t)) for t, h in practice(L)]
            det = (f'<details><summary>{len(more)} more: videos, notebooks and labs</summary><div class="links">{"".join(more)}</div></details>' if more else '')
            lec += (f'<div class="lrow" id="{rid}"><span class="no">{int(L["n"]):02d}</span><h3>{e(L["title"])}{anchor("index.html", rid, "lecture " + L["n"])}</h3>'
                    f'<div class="links">{main}</div>{det}</div>')
    m, L = LECTURES[-1]
    marks = ''.join(f'<div><span class="big">{n}</span><h3>{c}</h3><p>{e(t)}</p></div>' for c, n, t in GRADING)
    faq = ''.join(f'<details class="q"><summary>{e(q)}</summary><p>{e(t)}</p></details>' for q, t in FAQ)
    facts = ' · '.join(f'{k} {v}' for k, v in FACTS[:3])
    body = f'''
<section class="sec" id="overview">
 <h1 class="h1">Deep Learning</h1>
 <p class="role">ES 667 · IIT Gandhinagar · Semester I, 2026–27</p>
 <p class="lede" style="margin-top:18px">{e(INTRO)} {e(OVERVIEW)}</p>
 <p class="small muted" style="margin:0">{facts} · nipun.batra@iitgn.ac.in</p>
</section>

<section class="sec" id="this-week"><h2>This week{anchor("index.html", "this-week", "this week")}</h2>
 <div class="week">
  <div><span class="k">Due Thursday 8 Oct, 6:30 pm</span><span class="big" style="color:var(--accent)">3 days</span><p>{a("a-assignment.html", "Assignment 2")}, small models and attention, and its individual quiz.</p></div>
  <div><span class="k">Latest lecture</span><span class="big">L{L["n"]}</span><p>{e(L["title"])}. {a(read_links(L)[0][1], "Notes")} · {a(read_links(L)[1][1], "Slides")}</p></div>
  <div><span class="k">Next quiz</span><span class="big">15 Oct</span><p>Quiz 2, closed book. Best two of three quizzes count.</p></div>
 </div>
</section>

<section class="sec" id="calendar"><h2>Calendar{anchor("index.html", "calendar", "calendar")}</h2>
 <div class="legend"><span><i></i>Assignment</span><span><i class="q"></i>Quiz</span><span>All times IST</span></div>
 <div class="cal"><div class="cal-in">{cal}</div></div>
</section>

<section class="sec" id="lectures"><h2>Lectures{anchor("index.html", "lectures", "lectures")}</h2>
 <p class="small muted" style="margin:0">Notes, slides and cheat sheet on each row; videos, notebooks and labs under "more". {a(PLAYLIST_FULL, "Full lecture playlist")} · {a(PLAYLIST_SHORT, "3-minute summaries")}</p>
 <div class="mlist">{lec}</div>
</section>

<section class="sec" id="assessment"><h2>Assessment{anchor("index.html", "assessment", "assessment")}</h2>
 <div class="marks">{marks}</div>
 <p class="small" style="margin-top:16px;max-width:70ch">Each assignment is followed by a short individual viva on your own submission; your marks reflect that conversation. Use AI tools honestly and document meaningful assistance.</p>
</section>

<section class="sec" id="questions"><h2>Questions{anchor("index.html", "questions", "questions")}</h2>
 <div class="faqcols"><div>{"".join(faq.split("</details>")[i] + "</details>" for i in range(3))}</div><div>{"".join(faq.split("</details>")[i] + "</details>" for i in range(3, 6))}</div></div>
 <h3 class="h3" style="margin-top:26px">References</h3><p class="small muted" style="margin-bottom:6px">There is no required textbook.</p>{refs_html()}
</section>'''
    page('b-course.html', 'ES 667 One Page', B_CSS, 'b-course.html', rail('#overview', nav, spy=True), body)


# ---------------------------------------------------------------- Direction C
C_CSS = '''
.duebar { display:flex; flex-wrap:wrap; gap:6px 18px; align-items:baseline; background:var(--accent); color:var(--on-accent); padding:10px 16px; font-size:14px; margin-bottom:26px; }
.duebar b { font-weight:700; } .duebar a { color:var(--on-accent); text-decoration:underline; } .duebar .r { margin-left:auto; opacity:.85; }
.hero { display:grid; grid-template-columns:minmax(0,1fr) 260px; gap:20px 40px; align-items:end; }
.facts { font-size:13.5px; display:grid; gap:2px; margin:0; } .facts dt { color:var(--muted); font-size:11px; letter-spacing:.07em; text-transform:uppercase; margin-top:6px; } .facts dd { margin:0; }
.tools { display:flex; flex-wrap:wrap; gap:10px 16px; align-items:center; margin:26px 0 8px; padding:12px 0; border-top:2px solid var(--ink); border-bottom:1px solid var(--rule); position:sticky; top:0; background:var(--paper); z-index:2; }
.chip { border:1px solid var(--rule); background:none; padding:5px 10px; font-size:13px; cursor:pointer; }
.chip[aria-pressed="true"] { background:var(--ink); color:var(--paper); border-color:var(--ink); }
.chip .num { color:inherit; opacity:.65; margin-left:4px; font-size:11.5px; }
.search { margin-left:auto; display:flex; align-items:center; gap:8px; border-bottom:1px solid var(--ink); padding:3px 0; min-width:0; }
.search input { border:0; background:transparent; font:inherit; font-size:14px; color:var(--ink); width:220px; max-width:100%; outline:none; }
.search svg { width:16px; height:16px; fill:none; stroke:currentColor; stroke-width:1.8; }
.mblock { margin-top:26px; }
.mblock > h2 { font:700 22px/1.2 var(--heading); letter-spacing:-.03em; margin:0 0 12px; display:flex; align-items:baseline; gap:8px; }
.mblock > h2 .r { color:var(--muted); font:500 13px/1 var(--body); margin-left:auto; }
.cards { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:14px; }
.card { border:1px solid var(--rule); padding:14px 16px 12px; display:flex; flex-direction:column; gap:8px; min-width:0; background:var(--paper); }
.card:hover { border-color:var(--ink); }
.card .no { font:800 30px/1 var(--heading); letter-spacing:-.05em; color:var(--accent); font-variant-numeric:tabular-nums; }
.card h3 { font:600 15.5px/1.3 var(--heading); margin:0; letter-spacing:-.015em; }
.card p { font-size:13px; color:var(--muted); margin:0; }
.card .links { font-size:13px; margin-top:auto; padding-top:8px; border-top:1px solid var(--rule); }
.card .tags { display:flex; flex-wrap:wrap; gap:4px; }
.shelf { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:0 22px; }
.shelf a { display:grid; grid-template-columns:minmax(0,1fr) auto; gap:10px; padding:8px 0; border-bottom:1px solid var(--rule); color:var(--ink); font-size:14px; }
.shelf a:hover { color:var(--accent); text-decoration:none; }
.shelf .l { color:var(--muted); font-size:11.5px; display:block; }
@media (max-width:860px) { .hero { grid-template-columns:1fr; } .search { margin-left:0; width:100%; } .search input { width:100%; } .tools { position:static; } .duebar .r { margin-left:0; } }
'''


def build_c():
    m, L = LECTURES[-1]
    chips = f'<button type="button" class="chip" data-module="all" aria-pressed="true">All<span class="num">20</span></button>'
    chips += ''.join(f'<button type="button" class="chip" data-module="{m["slug"]}" aria-pressed="false">{e(m["name"].split(" and ")[0] if m["slug"] != "attention" else "Attention")}<span class="num">{m["range"]}</span></button>' for m in MODS)
    blocks = ''
    for m in MODS:
        cards = ''
        for L in m['lectures']:
            rid = f'lecture-{L["n"]}'
            tags = []
            if extras(L, 'resource-recording'): tags.append('Recording')
            if extras(L, 'resource-short'): tags.append(f'{len(extras(L, "resource-short"))} × 3-min')
            if practice(L): tags.append('Practice')
            if any(k == 'cheat' for _, _, k in read_links(L)): tags.append('Cheat sheet')
            tag_html = ''.join(f'<span class="pill">{t}</span>' for t in tags)
            links = ' '.join(a(h, t) for t, h, k in read_links(L) if k != 'cheat')
            sub = re.sub(r' \d+ slides including the cover\.', '', L['sub'])
            cards += (f'<article class="card" id="{rid}" data-lecture data-module="{m["slug"]}"><span class="no">{int(L["n"]):02d}</span>'
                      f'<h3>{e(L["title"])}{anchor("index.html", rid, "lecture " + L["n"])}</h3>' + (f'<p>{e(sub)}</p>' if sub else '') +
                      f'<div class="tags">{tag_html}</div><div class="links">{links}</div></article>')
        blocks += (f'<section class="mblock" id="{m["slug"]}" data-module-block><h2>{e(m["name"])}{anchor("index.html", m["slug"], m["name"])}'
                   f'<span class="r">Lectures {m["range"]}</span></h2><div class="cards">{cards}</div></section>')
    shorts = ''
    for m, L in LECTURES:
        for t, h, d in extras(L, 'resource-short'):
            shorts += f'<a href="{e(h)}" target="_blank" rel="noopener noreferrer"><span>{e(t)}<span class="l">Lecture {L["n"]}</span></span><span class="dur">{d}</span></a>'
    facts = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in FACTS)
    nav = [('c-library.html', 'Lectures'), ('#shorts', '3-minute videos'), ('a-assessment.html', 'Assessment'),
           ('a-assignment.html', 'Assignments'), ('a-home.html#faq', 'FAQ'), (SLACK, 'Slack')]
    body = f'''
<div class="duebar"><b>Due Thursday 8 Oct, 6:30 pm</b><span>{a("a-assignment.html", "Assignment 2")} and its quiz</span><span class="r">Next: Quiz 2 on Thursday 15 Oct</span></div>
<div class="hero">
 <div style="min-width:0"><h1 class="h1">Deep Learning</h1><p class="role">ES 667 · IIT Gandhinagar · Semester I, 2026–27</p>
 <p class="lede" style="margin:16px 0 0">{e(INTRO)} Every lecture below has notes and slides; most add a cheat sheet, 3-minute summaries and notebooks.</p></div>
 <dl class="facts">{facts}</dl>
</div>
<div class="tools" role="search">{chips}
 <label class="search" for="lecture-search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>
 <input id="lecture-search" type="search" placeholder="Search lectures, e.g. Adam, CLIP, NMS" autocomplete="off" aria-label="Search lectures"></label>
 <span class="small muted" id="lecture-count" aria-live="polite">20 lectures</span></div>
{blocks}
<section class="rule-top" id="shorts"><h2 class="h2">3-minute summaries{anchor("index.html", "shorts", "3-minute summaries")}</h2>
 <p class="small muted">22 short videos, one idea each, in lecture order. {a(PLAYLIST_SHORT, "Open the playlist")}</p>
 <div class="shelf">{shorts}</div></section>'''
    page('c-library.html', 'ES 667 Library', C_CSS, 'c-library.html', rail('c-library.html', nav), body)


# ---------------------------------------------------------------- Assignment page (shared by A and C)
def build_assignment():
    body = f'''<span class="label">Assignment 2 · 13 marks</span><h1 class="h1">Small models and attention</h1>
<p class="lede">Released 30 Sep. Due <b>Thursday 8 Oct, 6:30 pm IST</b>, followed by a short individual quiz on your submission.</p>
<nav class="jump" aria-label="On this page" style="display:flex;flex-wrap:wrap;gap:6px 22px;font-size:14px;padding:12px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)">
<a href="#data">Data and training</a><a href="#q1">Q1. Softer targets <span class="muted small">5</span></a><a href="#q2">Q2. Predict the next letter <span class="muted small">5</span></a></nav>
<section class="rule-top" id="data"><h2 class="h2">Data and training{anchor("Assignments/assignment2.html", "data", "data and training")}</h2>
<p class="muted" style="max-width:62ch">Section content from Assignments/assignment2.qmd would render here unchanged. The mockup shows only the frame: a dated header, the marks per question and a link icon on each heading so a question can be shared on Slack.</p></section>
<section class="rule-top" id="q1"><h2 class="h2">Q1. Softer targets (5 marks){anchor("Assignments/assignment2.html", "q1", "Q1")}</h2>
<p class="muted">(a) Train and report, 2 marks · (b) Compare confidence, 1 mark · (c) Explain, 2 marks</p></section>
<section class="rule-top" id="q2"><h2 class="h2">Q2. Predict the next letter (5 marks){anchor("Assignments/assignment2.html", "q2", "Q2")}</h2>
<p class="muted">(a) Train and evaluate, 2 marks · (b) Generate names, 1 mark · …</p></section>
<section class="rule-top" id="a1"><h2 class="h2">Earlier assignments</h2><p>{a("https://nipunbatra.github.io/dl-2026/Assignments/assignment1_optimization.html", "Assignment 1 · Optimization")}, due 27 Aug.</p></section>'''
    page('a-assignment.html', 'ES 667 Assignment 2', A_CSS, 'a-assignment.html', rail('a-assignment.html', A_NAV), body)


build_a(); build_b(); build_c(); build_assignment()
print('ok')
