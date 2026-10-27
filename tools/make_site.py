#!/usr/bin/env python3
"""Builds index.html for the ChibyRace downloads page from builds.json.

Each build in builds.json is a GitHub release tagged v<version> with the asset ChibyRace-<version>.apk.
Run from the repo root:  python3 tools/make_site.py
"""
import datetime
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "builds.json").read_text(encoding="utf-8"))
repo = data["repo"]
builds = data["builds"]
latest = builds[0]

MAPS = [
    ("map-fjord-fortress.jpg", "Fjord Fortress", "Viking harbour, longhouses and a stone keep."),
    ("map-sakura-temple.jpg", "Sakura Temple", "Lantern street, koi river and a pagoda finish."),
    ("map-medieval-village.jpg", "Medieval Village", "Cobbled high street, mill river and a castle."),
    ("map-modern-town.jpg", "Modern Town", "Main street, canal, building site and a glass tower."),
    ("map-jungle-temple.jpg", "Jungle Temple", "A climb up a stepped pyramid: four stairs to a shrine 18 m up."),
    ("map-pirate-cove.jpg", "Pirate Cove", "Harbour quay, lagoon, a cannon fort and a lighthouse headland."),
]


def e(text):
    return html.escape(str(text), quote=True)


def size_mb(n):
    return f"{n / 1048576:.1f} MB"


def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b')} {d.year}"


def url(b):
    return f"https://github.com/{repo}/releases/download/v{b['version']}/{b['file']}"


def notes_list(b):
    return "".join(f"<li>{e(n)}</li>" for n in b["notes"])


rows = []
for b in builds:
    tag = '<span class="pill">Latest</span>' if b is latest else ""
    rows.append(f"""
      <li class="build" id="v{e(b['version'].replace('.', '-'))}">
        <div class="build-head">
          <span class="ver">{e(b['version'])}</span>{tag}
          <span class="meta">{e(nice_date(b['date']))} · {e(size_mb(b['size']))}</span>
        </div>
        <ul class="notes">{notes_list(b)}</ul>
        <div class="build-foot">
          <a class="btn-line" href="{e(url(b))}">Download {e(b['version'])}</a>
          <details><summary>SHA-256</summary><code>{e(b['sha256'])}</code></details>
        </div>
      </li>""")

maps = "".join(f"""
      <figure class="map">
        <img src="img/{e(f)}" alt="{e(name)} in ChibyRace" loading="lazy" width="960" height="376">
        <figcaption><strong>{e(name)}</strong><span>{e(line)}</span></figcaption>
      </figure>""" for f, name, line in MAPS)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<title>ChibyRace Builds</title>
<meta name="description" content="Android test builds of ChibyRace, a party obstacle racer.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&family=JetBrains+Mono:wght@500&family=Lilita+One&display=swap">
<style>
/* Layout: a daylight hero with the newest build, then install steps, maps and every build, newest first. */
:root {{
  --bg: #f3f7fb; --card: #ffffff; --ink: #14213d; --muted: #56657c; --line: #d6e1ed;
  --sky: #cfe9ff; --link: #1f7fd1; --sun: #ffc53d; --sun-ink: #2b1d00; --sun-edge: #e0a30f;
  --display: "Lilita One", "Arial Rounded MT Bold", "Trebuchet MS", sans-serif;
  --body: "Figtree", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, Consolas, monospace;
  color-scheme: light;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --bg: #0e1626; --card: #16213a; --ink: #e9eef7; --muted: #9eadc4; --line: #283754;
    --sky: #14304f; --link: #6cc0ff; --sun: #ffc53d; --sun-ink: #2b1d00; --sun-edge: #c98e00;
    color-scheme: dark;
  }}
}}
:root[data-theme="dark"] {{
  --bg: #0e1626; --card: #16213a; --ink: #e9eef7; --muted: #9eadc4; --line: #283754;
  --sky: #14304f; --link: #6cc0ff; --sun: #ffc53d; --sun-ink: #2b1d00; --sun-edge: #c98e00;
  color-scheme: dark;
}}
* {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; }}
body {{
  margin: 0; background: var(--bg); color: var(--ink); font: 400 16px/1.55 var(--body);
}}
img {{ max-width: 100%; height: auto; display: block; }}
a {{ color: var(--link); }}
a:focus-visible, summary:focus-visible {{ outline: 3px solid var(--link); outline-offset: 3px; border-radius: 6px; }}
.wrap {{
  max-width: 1080px; margin: 0 auto;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
}}
h1, h2 {{ font-family: var(--display); font-weight: 400; letter-spacing: 0.01em; text-wrap: balance; margin: 0; }}
h2 {{ font-size: clamp(1.6rem, 4vw, 2.1rem); }}

.hero {{ background: var(--sky); border-bottom: 1px solid var(--line); }}
.hero .wrap {{
  display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: 40px; align-items: center;
  padding-block: calc(40px + env(safe-area-inset-top, 0px)) 44px;
}}
.eyebrow {{ font-weight: 700; font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); margin: 0 0 6px; }}
h1 {{ font-size: clamp(3rem, 9vw, 4.6rem); line-height: 0.95; }}
.lede {{ font-size: 1.12rem; margin: 14px 0 26px; max-width: 34ch; }}
.btn {{
  display: inline-flex; flex-direction: column; gap: 2px; text-decoration: none;
  background: var(--sun); color: var(--sun-ink); border-radius: 999px; padding: 14px 30px 13px;
  box-shadow: inset 0 -5px 0 var(--sun-edge); transition: transform 0.12s ease;
}}
.btn:hover {{ transform: translateY(-2px); }}
.btn:active {{ transform: translateY(1px); }}
.btn b {{ font-family: var(--display); font-weight: 400; font-size: 1.5rem; line-height: 1.1; }}
.btn small {{ font-size: 0.85rem; font-weight: 600; opacity: 0.8; }}
.facts {{ display: flex; flex-wrap: wrap; gap: 6px 18px; margin: 18px 0 0; padding: 0; list-style: none; color: var(--muted); font-size: 0.92rem; }}
.shot {{ border-radius: 22px; overflow: hidden; border: 4px solid var(--card); box-shadow: 0 18px 40px -22px rgba(10, 30, 60, 0.55); }}

section {{ padding-block: 48px 8px; }}
.section-head {{ display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 6px 16px; margin-bottom: 18px; }}
.section-head p {{ margin: 0; color: var(--muted); }}

.steps {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; padding: 0; margin: 0; list-style: none; counter-reset: s; }}
.steps li {{ background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 18px 18px 16px; counter-increment: s; min-width: 0; }}
.steps li::before {{
  content: counter(s); display: grid; place-items: center; width: 34px; height: 34px; border-radius: 50%;
  background: var(--sun); color: var(--sun-ink); font-family: var(--display); font-size: 1.15rem; margin-bottom: 10px;
}}
.steps strong {{ display: block; margin-bottom: 4px; }}
.steps p {{ margin: 0; color: var(--muted); font-size: 0.95rem; }}
.note {{ margin: 14px 0 0; color: var(--muted); font-size: 0.95rem; max-width: 70ch; }}

.new {{ margin: 0; padding-left: 1.2em; max-width: 70ch; }}
.new li {{ margin: 4px 0; }}

.maps {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }}
.map {{ margin: 0; background: var(--card); border: 1px solid var(--line); border-radius: 16px; overflow: hidden; min-width: 0; }}
.map figcaption {{ padding: 12px 16px 14px; display: grid; gap: 2px; }}
.map figcaption span {{ color: var(--muted); font-size: 0.95rem; }}

.builds {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 12px; }}
.build {{ background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 16px 18px; min-width: 0; }}
.build-head {{ display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; }}
.ver {{ font-family: var(--mono); font-weight: 500; font-size: 1.1rem; font-variant-numeric: tabular-nums; }}
.pill {{ background: var(--sun); color: var(--sun-ink); font-size: 0.75rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; border-radius: 999px; padding: 2px 10px; }}
.meta {{ color: var(--muted); font-size: 0.92rem; margin-left: auto; font-variant-numeric: tabular-nums; }}
.notes {{ margin: 8px 0 12px; padding-left: 1.15em; }}
.notes li {{ margin: 2px 0; }}
.build-foot {{ display: flex; flex-wrap: wrap; align-items: center; gap: 10px 18px; }}
.btn-line {{
  display: inline-block; text-decoration: none; font-weight: 700; color: var(--ink);
  border: 2px solid var(--line); border-radius: 999px; padding: 6px 16px;
}}
.btn-line:hover {{ border-color: var(--sun-edge); }}
details {{ color: var(--muted); font-size: 0.9rem; min-width: 0; max-width: 100%; }}
summary {{ cursor: pointer; }}
details code {{ display: block; font-family: var(--mono); font-size: 0.78rem; overflow-wrap: anywhere; margin-top: 6px; }}

footer {{ padding-block: 40px calc(40px + env(safe-area-inset-bottom, 0px)); color: var(--muted); font-size: 0.9rem; }}

@media (max-width: 760px) {{
  .hero .wrap {{ grid-template-columns: minmax(0, 1fr); gap: 28px; padding-block: calc(28px + env(safe-area-inset-top, 0px)) 32px; }}
  .steps, .maps {{ grid-template-columns: minmax(0, 1fr); }}
  .meta {{ margin-left: 0; width: 100%; }}
}}
@media (prefers-reduced-motion: reduce) {{ .btn {{ transition: none; }} }}
</style>
</head>
<body>
<header class="hero">
  <div class="wrap">
    <div>
      <p class="eyebrow">Android test builds</p>
      <h1>ChibyRace</h1>
      <p class="lede">A party obstacle race: 8 racers, {len(MAPS)} maps, a 4-round knockout show with five arena games, and traps that change every race.</p>
      <a class="btn" href="{e(url(latest))}">
        <b>Download {e(latest['version'])}</b>
        <small>APK · {e(size_mb(latest['size']))}</small>
      </a>
      <ul class="facts">
        <li>Built {e(nice_date(latest['date']))}</li>
        <li>Android {e(data['minAndroid'])} or newer</li>
        <li>64-bit phones</li>
      </ul>
    </div>
    <div class="shot"><img src="img/hero-medieval.jpg" alt="A racer at the foot of a cobbled ramp in Medieval Village" width="1062" height="675"></div>
  </div>
</header>

<main>
  <section class="wrap" aria-labelledby="install">
    <div class="section-head"><h2 id="install">Install on your phone</h2></div>
    <ol class="steps">
      <li><strong>Download</strong><p>Open this page on the phone and tap Download. If Chrome says the file might be harmful, choose Download anyway.</p></li>
      <li><strong>Allow the install</strong><p>Open the APK. The first time, Android asks to allow installs from Chrome: turn on "Allow from this source" and go back.</p></li>
      <li><strong>Install</strong><p>Tap Install. If Play Protect warns about an unknown app, choose Install anyway.</p></li>
    </ol>
    <p class="note">A new build installs over the old one, and your skins and settings stay. These are test builds signed with a development key; they are not on Google Play.</p>
  </section>

  <section class="wrap" aria-labelledby="new">
    <div class="section-head"><h2 id="new">New in {e(latest['version'])}</h2></div>
    <ul class="new">{notes_list(latest)}</ul>
  </section>

  <section class="wrap" aria-labelledby="maps">
    <div class="section-head"><h2 id="maps">Maps</h2><p>Pick one with the MAP button on the racer screen.</p></div>
    <div class="maps">{maps}
    </div>
  </section>

  <section class="wrap" aria-labelledby="all">
    <div class="section-head"><h2 id="all">All builds</h2><p>{len(builds)} builds, newest first.</p></div>
    <ul class="builds">{''.join(rows)}
    </ul>
  </section>
</main>

<footer class="wrap">
  <p>ChibyRace is made in Unity. Each build is also listed on the <a href="https://github.com/{e(repo)}/releases">GitHub releases page</a>.</p>
</footer>
</body>
</html>
"""

(ROOT / "index.html").write_text(page, encoding="utf-8")
print(f"index.html: {len(builds)} builds, latest {latest['version']}, repo {repo}")
