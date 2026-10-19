"""Small, dependency-free SVG design system for the GitHub profile.

Run this script to rebuild the static artwork; update_stats.py owns the dashboard.
"""

from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    "dark": dict(bg="#0D1117", panel="#161B22", soft="#1C2430", text="#E6EDF3",
                 muted="#A0ADBC", border="#303D4D", blue="#58A6FF", cyan="#39C5CF"),
    "light": dict(bg="#F6F8FA", panel="#FFFFFF", soft="#EAF0F6", text="#17283B",
                  muted="#526477", border="#CBD5E1", blue="#0969DA", cyan="#087F8C"),
}


def text(x, y, value, size=20, color="text", weight=400, mono=False, anchor="start"):
    family = "'JetBrains Mono', Consolas, monospace" if mono else "'Segoe UI', Arial, sans-serif"
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(str(value))}</text>')


def rect(x, y, width, height, fill="panel", stroke="border", radius=12):
    return (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}"/>')


def path(d, stroke="border", width=1.5, fill="none", extra=""):
    return f'<path d="{d}" stroke="{stroke}" stroke-width="{width}" fill="{fill}" {extra}/>'


def circle(x, y, radius=4, fill="cyan", extra=""):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" {extra}/>'


def document(title, description, width, height, content, theme):
    palette = PALETTES[theme]
    body = "\n".join(content)
    for token, color in palette.items():
        body = body.replace(f'="{token}"', f'="{color}"')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>\n'
            '<style>.signal{animation:signal 7s linear infinite}.cursor{animation:cursor 3s ease-in-out infinite}'
            '@keyframes signal{to{stroke-dashoffset:-120}}@keyframes cursor{50%{opacity:.2}}'
            '@media(prefers-reduced-motion:reduce){.signal,.cursor{animation:none}}</style>\n'
            + body + '\n</svg>\n')


def contours(cx, cy):
    lines = []
    for i in range(9):
        spread = 23 + i * 17
        d = (f'M{cx-spread} {cy+spread*.46} Q{cx-spread*.88} {cy-spread*.65} '
             f'{cx-spread*.2} {cy-spread*.6} Q{cx+spread*.55} {cy-spread*1.3} '
             f'{cx+spread} {cy-spread*.12} Q{cx+spread*1.25} {cy+spread*.7} '
             f'{cx+spread*.25} {cy+spread*.8} Q{cx-spread*.6} {cy+spread*1.2} '
             f'{cx-spread} {cy+spread*.46}Z')
        lines.append(path(d, "border", .8))
    return ''.join(lines)


def hero(theme, mobile=False):
    w, h = (560, 560) if mobile else (960, 440)
    parts = [rect(.5, .5, w-1, h-1, "bg", radius=18)]
    parts += [path(f'M32 42H{w-32}', "border"), text(32, 28, 'PK / ENGINEERING ATLAS', 13, "muted", mono=True)]
    if mobile:
        parts += ['<g opacity=".45">'+contours(570,174)+'</g>',
                  text(30, 130, 'Prabhuram', 70, weight=700), text(30, 207, 'Karki', 70, weight=700),
                  text(32, 250, 'Full-Stack Software Engineer', 24, "blue"),
                  text(32, 300, 'Care in the interface.', 28), text(32, 337, 'Clarity in the system.', 28)]
        tx, ty, tw = 32, 385, 496
    else:
        parts += [text(38, 130, 'Prabhuram', 82, weight=700), text(38, 218, 'Karki', 82, weight=700),
                  text(42, 263, 'Full-Stack Software Engineer', 23, "blue"),
                  text(42, 318, 'Care in the interface.', 29), text(42, 356, 'Clarity in the system.', 29),
                  contours(750, 153)]
        # A route through abstract terrain, not a geographic map or telemetry.
        route = 'M625 85H712V157H816V230H888'
        parts += [path(route, "blue", 2), path(route, "cyan", 3, extra='class="signal" stroke-dasharray="6 114"')]
        for x, y, label in [(625,85,'UI'), (816,157,'API'), (888,230,'DATA')]:
            parts += [circle(x,y,6,"bg"), circle(x,y,3), text(x-10,y-16,label,14,"muted",mono=True)]
        tx, ty, tw = 600, 274, 318
    parts += [rect(tx, ty, tw, 116), circle(tx+17,ty+17,3,"blue"),
              text(tx+32,ty+22,'identity.sh',14,"muted",mono=True),
              text(tx+18,ty+53,'$ whoami',18,"cyan",mono=True),
              text(tx+18,ty+82,'Prabhuram Karki',21,mono=True),
              rect(tx+220,ty+65,9,20,"blue","blue",0).replace('/>', ' class="cursor"/>')]
    parts += [path(f'M32 {h-38}H{w-32}'), text(32,h-14,'Kathmandu, Nepal',16,"muted",mono=True)]
    if not mobile:
        parts += [text(w-32,h-14,'interface / application / system',14,"muted",mono=True,anchor="end")]
    return document('Prabhuram Karki · Full-Stack Software Engineer',
                    'Care in the interface. Clarity in the system. Kathmandu, Nepal. A terminal and abstract contour map connect UI, API and data.', w,h,parts,theme)


PROJECTS = {
    'code-shell': ('Code Shell', 'Developer tooling / Rust', 'A coding agent at home in the terminal.', 'CLI  /  CORE  /  PROVIDERS  /  TOOLS'),
    'easy-invoice': ('Easy Invoice', 'Document processing / React + Django', 'From invoice images to structured records.', 'IMAGE  /  OCR  /  FIELDS  /  CSV'),
    'manducart': ('ManduCart v2', 'Product engineering / Vue + Laravel', 'A storefront connected to an application API.', 'STOREFRONT  /  API  /  CATALOG'),
    'linux-runtime': ('Windows apps, Linux host.', 'Systems exploration / Rust', 'An experimental application runtime.', 'CLI  /  DAEMON  /  WINE  /  SANDBOX'),
}


def project_cover(key, theme):
    title, category, summary, labels = PROJECTS[key]
    p = [rect(.5,.5,959,259,"bg",radius=16), rect(590,18,351,224,"soft",radius=10),
         text(34,45,category,18,"cyan"), text(32,106,title,40,weight=700),
         text(34,150,summary,20,"muted"), path('M34 185H548'), text(34,222,labels,13,"muted",mono=True)]
    if key == 'code-shell':
        p += [rect(610,39,311,183,"panel",radius=8), text(628,68,'code-shell >',17,"cyan",mono=True),
              text(628,105,'prompt',15,"muted",mono=True), path('M697 100H894',"blue",3),
              text(628,140,'plan',15,"muted",mono=True), path('M697 135H857',"blue",3),
              text(628,175,'tools',15,"muted",mono=True)]
        for i in range(3):
            p += [rect(697+i*65,158,51,25,"soft",radius=4), path(f'M{706+i*65} 171h32',"cyan",2)]
        p += [text(628,207,'permission → execution',13,"muted",mono=True)]
    elif key == 'easy-invoice':
        p += [rect(614,42,98,158,"panel",radius=4)]
        for i in range(6):
            p += [path(f'M630 {66+i*20}h{53 if i%2 else 65}',"border",2)]
        p += [path('M727 119H772',"cyan",2), path('M762 109l10 10-10 10',"cyan",2),
              rect(790,70,132,118,"panel",radius=4)]
        for i, label in enumerate(['number','date','vendor','total']):
            p += [text(802,94+i*26,label,15,"blue",mono=True)]
        p += [path('M608 117H720',"blue",2), text(614,224,'ILLUSTRATIVE OCR FLOW',12,"muted",mono=True)]
    elif key == 'manducart':
        p += [rect(611,41,311,176,"panel",radius=7), path('M611 77H922'),
              text(627,66,'manducart',16,"blue",weight=700)]
        for i in range(3):
            x = 629 + i*94
            p += [rect(x,94,75,75,"soft",radius=5),
                  path(f'M{x+20} 117l12-8h12l12 8-8 10-4-3v27h-12v-27l-4 3Z',"cyan",1.5),
                  path(f'M{x+3} 186h55',"border",3)]
        p += [text(614,239,'CATALOG SCHEMATIC · NOT A SCREENSHOT',11,"muted",mono=True)]
    else:
        for x,y,label in [(615,48,'CLI'),(783,48,'GTK'),(696,118,'JSON-RPC'),(696,182,'Wine')]:
            p += [rect(x,y,128,38,"panel",radius=5),text(x+64,y+25,label,17,"cyan" if label=='Wine' else 'text',mono=True,anchor="middle")]
        p += [path('M679 86v14h81v18M847 86v14h-87M760 156v26',"blue",2)]
    return document(title, f'{summary} {category}. Illustration, not a product screenshot.',960,260,p,theme)


def architecture(theme):
    w,h=600,570
    p=[rect(.5,.5,w-1,h-1,"bg",radius=16),text(32,47,'Follow the feature.',31,weight=700),
       text(32,80,'An illustrative full-stack architecture',18,"muted")]
    nodes=[('01','Experience','Components · state · interaction'),
           ('02','Application','API · validation · authorization'),
           ('03','Work and data','Queues · cache · databases'),
           ('04','Delivery','Linux · containers · CI/CD')]
    for i,(index,title,detail) in enumerate(nodes):
        y=112+i*106
        p += [rect(32,y,536,84), text(52,y+34,index,20,"cyan",mono=True),
              text(106,y+34,title,25,weight=600),text(106,y+63,detail,18,"muted")]
        if i<3:
            p += [path(f'M300 {y+84}v22',"blue",2), circle(300,y+96,3)]
    p += [text(32,553,'A pattern to reason about, not every project’s stack.',15,"muted")]
    return document('Illustrative full-stack architecture','Experience feeds application logic, work and data, then delivery. Components, APIs, authorization, queues, cache, databases, Linux and CI/CD. This is a conceptual pattern.',w,h,p,theme)


def overview(data, theme, mobile=False):
    w,h=(560,340) if mobile else (960,190)
    metrics=data['metrics']
    items=[('Public repos',metrics['public_repos'],'Including forks'),('Stars',metrics['total_stars'],'Across public repos'),
           ('Original repos',metrics['original_repos'],'Excluding forks'),('Featured',metrics['featured_projects'],'Verified repositories')]
    p=[rect(.5,.5,w-1,h-1,"bg",radius=14)]
    for i,(label,value,detail) in enumerate(items):
        x,y=(22+(i%2)*270,22+(i//2)*144) if mobile else (22+i*236,20)
        cw=246 if mobile else 210
        p += [rect(x,y,cw,126,"panel",radius=8),path(f'M{x+16} {y+18}h22',"cyan",2),
              text(x+16,y+46,label,20 if mobile else 18,"muted"),
              text(x+16,y+91,value,43,"text",weight=700),text(x+16,y+114,detail,14,"muted")]
    p += [text(22,h-12,f'GitHub REST API · snapshot {data["updated_at"]} UTC',13,"muted",mono=True)]
    desc='; '.join(f'{label}: {value} ({detail})' for label,value,detail in items)
    return document('Public engineering dashboard',desc,w,h,p,theme)


def languages(data, theme):
    raw=sorted(data['languages'],key=lambda item:item['bytes'],reverse=True)
    total=sum(item['bytes'] for item in raw)
    rows=raw[:5]
    remainder=sum(item['bytes'] for item in raw[5:])
    if remainder:
        rows=rows+[{'name':'Other','bytes':remainder}]
    h=145+len(rows)*65 if rows else 210
    p=[rect(.5,.5,599,h-1,"bg",radius=16),text(30,44,'The public codebase',30,weight=700),
       text(30,76,'Language bytes · original repositories',18,"muted")]
    descriptions=[]
    for i,item in enumerate(rows):
        y=116+i*65
        percentage=item['bytes']/total*100 if total else 0
        descriptions.append(f'{item["name"]}: {percentage:.1f}%')
        p += [text(30,y,item['name'],21),text(570,y,f'{percentage:.1f}%',20,"muted",mono=True,anchor="end"),
              rect(30,y+13,540,8,"soft","soft",4),
              rect(30,y+13,max(.5,540*percentage/100),8,"blue" if i%2==0 else "cyan","none",4)]
    if not rows:
        p += [text(30,130,'No language bytes reported by GitHub.',19,"muted")]
    p += [text(30,h-29,'Repository bytes are not a measure of proficiency.',16,"muted")]
    return document('Public repository language distribution','; '.join(descriptions)+'. Original public repositories; excludes forks and the profile repository. Byte distribution is not a skill rating.',600,h,p,theme)


def activity(data, theme):
    a=data['activity']
    days=a['days']
    maximum=max((day['count'] for day in days),default=0)
    p=[rect(.5,.5,599,329,"bg",radius=16),text(30,44,'Work in the open',30,weight=700),
       text(30,76,'Returned public events · daily',18,"muted")]
    for value in range(3):
        y=228-value*50
        p += [path(f'M30 {y}H570',"border",.7)]
    bw=540/max(1,len(days))
    for i,day in enumerate(days):
        bh=day['count']/maximum*100 if maximum else 0
        if bh:
            p += [rect(round(30+i*bw,2),round(228-bh,2),round(max(1,bw-5),2),round(bh,2),"cyan","none",2)]
    p += [text(30,259,a['window_start'],16,"muted",mono=True),text(570,259,a['window_end'],16,"muted",mono=True,anchor="end"),
          text(30,114,f'{a["events_count"]} events in this snapshot',19,"blue"),
          text(30,291,'30-day feed · at most 300 events · not contributions',15,"muted"),
          text(30,315,'No bar = no returned event; the API can omit activity.',14,"muted")]
    if a['limited']:
        p += [text(570,114,'API cap reached',14,"muted",anchor="end")]
    desc=(f'Public events returned between {a["window_start"]} and {a["window_end"]}: {a["events_count"]}. '
          'GitHub retains at most 300 events for 30 days. Events are not commits or contributions. '
          + '; '.join(f'{d["date"]}: {d["count"]}' for d in days if d['count']))
    return document('Recent public GitHub activity',desc,600,330,p,theme)


def render_dashboard(data):
    assets={}
    for theme in PALETTES:
        assets[f'overview-{theme}.svg']=overview(data,theme)
        assets[f'overview-mobile-{theme}.svg']=overview(data,theme,True)
        assets[f'languages-{theme}.svg']=languages(data,theme)
        assets[f'activity-{theme}.svg']=activity(data,theme)
    return assets


def build_static():
    for theme in PALETTES:
        for suffix,mobile in [('',False),('-mobile',True)]:
            p=ROOT/f'assets/hero/hero{suffix}-{theme}.svg'
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(hero(theme,mobile))
        for key in PROJECTS:
            p=ROOT/f'assets/projects/{key}-{theme}.svg'
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(project_cover(key,theme))
        p=ROOT/f'assets/architecture/engineering-flow-{theme}.svg'
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(architecture(theme))


if __name__=='__main__':
    build_static()
    snapshot=ROOT/'assets/dashboard/data.json'
    if snapshot.exists():
        for name,svg in render_dashboard(json.loads(snapshot.read_text())).items():
            (snapshot.parent/name).write_text(svg)
    print('Profile SVG assets rebuilt.')
