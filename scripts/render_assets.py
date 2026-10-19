"""Repository-hosted SVG artwork and public-data charts; Python standard library only."""

from collections import Counter
from datetime import date
from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    'dark': dict(bg='#0D1117', panel='#161B22', soft='#1C2430', text='#E6EDF3',
                 muted='#A0ADBC', border='#303D4D', blue='#58A6FF', cyan='#39C5CF'),
    'light': dict(bg='#F6F8FA', panel='#FFFFFF', soft='#EAF0F6', text='#17283B',
                  muted='#526477', border='#CBD5E1', blue='#0969DA', cyan='#087580'),
}


def text(x, y, value, size=20, color='text', weight=400, mono=False, anchor='start'):
    family = "'JetBrains Mono', Consolas, monospace" if mono else "'Segoe UI', Arial, sans-serif"
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(str(value))}</text>')


def rect(x, y, width, height, fill='panel', stroke='border', radius=10):
    return (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}"/>')


def path(d, stroke='border', width=1.5, fill='none', extra=''):
    return f'<path d="{d}" stroke="{stroke}" stroke-width="{width}" fill="{fill}" {extra}/>'


def circle(x, y, radius=4, fill='cyan', extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" {extra}/>'


def document(title, description, width, height, content, theme):
    body = '\n'.join(content)
    for token, color in PALETTES[theme].items():
        body = body.replace(f'="{token}"', f'="{color}"')
    motion = ''
    if 'class="signal"' in body:
        # Motion ends within four seconds; the finished illustration stays readable.
        motion = ('<style>.signal{opacity:0;animation:signal 3s ease-out 1}'
                  '.cursor{animation:cursor 1.6s ease-in-out 2}'
                  '@keyframes signal{0%{stroke-dashoffset:120;opacity:0}20%,80%{opacity:1}'
                  '100%{stroke-dashoffset:-120;opacity:0}}@keyframes cursor{50%{opacity:.2}}'
                  '@media(prefers-reduced-motion:reduce){.signal,.cursor{animation:none}}</style>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>\n'
            + motion + body + '\n</svg>\n')


def contours(cx, cy):
    lines = []
    for i in range(8):
        spread = 20 + i * 14
        d = (f'M{cx-spread} {cy+spread*.46} Q{cx-spread*.88} {cy-spread*.65} '
             f'{cx-spread*.2} {cy-spread*.6} Q{cx+spread*.55} {cy-spread*1.3} '
             f'{cx+spread} {cy-spread*.12} Q{cx+spread*1.25} {cy+spread*.7} '
             f'{cx+spread*.25} {cy+spread*.8} Q{cx-spread*.6} {cy+spread*1.2} '
             f'{cx-spread} {cy+spread*.46}Z')
        lines.append(path(d, 'border', .8))
    return ''.join(lines)


def hero(theme, mobile=False):
    w, h = (360, 330) if mobile else (960, 330)
    p = [rect(.5,.5,w-1,h-1,'bg',radius=12)]
    if mobile:
        p += ['<g opacity=".45">'+contours(287,126)+'</g>',
              text(24,32,'prabhuramkarki / engineering',13,'muted',mono=True),
              text(22,91,'Prabhuram',45,weight=700),text(22,139,'Karki',45,weight=700),
              text(24,175,'Full-Stack Software Engineer',18,'blue'),
              text(24,217,'From the interface down.',24),
              rect(24,238,312,52),text(38,272,'$ whoami',18,'cyan',mono=True),
              text(24,313,'Kathmandu, Nepal',16,'muted',mono=True)]
        route = 'M177 264H303'
        p += [path(route,'border'),path(route,'cyan',2,extra='class="signal" stroke-dasharray="8 88"'),
              rect(310,254,8,19,'blue','none',0).replace('/>',' class="cursor"/>')]
    else:
        p += [text(32,35,'prabhuramkarki / engineering',14,'muted',mono=True),
              text(29,119,'Prabhuram Karki',64,weight=700),
              text(32,160,'Full-Stack Software Engineer',23,'blue'),
              text(32,219,'From the interface down.',31),
              text(32,252,'Products, APIs, and the systems beneath them.',18,'muted'),
              '<g opacity=".3">'+contours(535,178)+'</g>',rect(620,54,308,220),
              text(640,83,'identity.sh',14,'muted',mono=True),path('M620 98H928'),
              text(640,128,'$ whoami',18,'cyan',mono=True),text(640,157,'Prabhuram Karki',20,mono=True),
              text(640,194,'$ working_set',18,'cyan',mono=True),
              text(640,224,'Vue / Nuxt / Laravel',17,mono=True)]
        route = 'M640 249H713V242H799V249H905'
        p += [path(route,'blue'),path(route,'cyan',2,extra='class="signal" stroke-dasharray="8 88"'),
              rect(883,208,8,19,'blue','none',0).replace('/>',' class="cursor"/>'),
              path('M32 293H928'),text(32,317,'Kathmandu, Nepal',14,'muted',mono=True),
              text(928,317,'interface / application / system',14,'muted',mono=True,anchor='end')]
    return document('Prabhuram Karki · Full-Stack Software Engineer',
                    'From the interface down. Products, APIs, and the systems beneath them. Kathmandu, Nepal. A terminal and abstract contour lines; motion is decorative and stops after four seconds.',w,h,p,theme)


PROJECTS = {
    'code-shell': ('Code Shell','Developer tooling','A prompt, with boundaries.'),
    'easy-invoice': ('Easy Invoice','Document processing','An image becomes a record.'),
    'manducart': ('ManduCart v2','Full-stack product','A storefront meets its API.'),
    'linux-runtime': ('Windows apps on Linux','Systems exploration','An app meets its host.'),
}


def project_cover(key, theme, mobile=False):
    title, category, summary = PROJECTS[key]
    w,h = (360,258) if mobile else (960,280 if key=='code-shell' else 224)
    p=[rect(.5,.5,w-1,h-1,'bg',radius=12)]
    if mobile:
        p += [text(24,31,category,14,'cyan'),text(23,68,title,25,weight=700),path('M24 86H336')]
        x,y,scale=24,102,1
    else:
        p += [path(f'M0 24V{h-24}','blue',3),text(32,36,category,15,'cyan'),
              text(30,91,title,36,weight=700),text(32,131,summary,23,'muted'),
              text(32,h-26,'Source-based illustration',14,'muted',mono=True),
              rect(560,18,380,h-36,'panel',radius=8)]
        x,y,scale=590,56 if key=='code-shell' else 29,1
    p += [f'<g transform="translate({x} {y}) scale({scale})">']
    if key=='code-shell':
        p += [text(0,22,'> prompt',19,'cyan',mono=True),path('M0 37H312'),
              text(0,65,'agent loop',19,mono=True),path('M142 58H312','blue',2),
              text(0,101,'approval',19,mono=True),path('M142 94H312','cyan',2),
              text(0,137,'tools',19,mono=True),text(142,137,'edit / shell',17,'muted',mono=True)]
        if not mobile:
            p += [text(0,181,'core / providers / tools / cli',14,'muted',mono=True)]
    elif key=='easy-invoice':
        p += [rect(0,0,98,131,'soft',radius=4),text(14,30,'invoice',17,'blue')]
        for i in range(4):p += [path(f'M14 {50+i*18}H82','border',2)]
        p += [path('M113 65H160','cyan',2),path('M152 57l8 8-8 8','cyan',2)]
        for i,label in enumerate(['number','date','vendor','total']):
            p += [text(177,25+i*33,label,18,mono=True)]
        if not mobile:p += [text(0,165,'Tesseract → fields → database + CSV',14,'muted',mono=True)]
    elif key=='manducart':
        for i,label in enumerate(['Catalog','Account','Cart']):
            bx=i*108
            p += [rect(bx,0,96,55,'soft',radius=5),text(bx+48,34,label,17,anchor='middle')]
        p += [path('M48 55V77H264V55M156 55V96','blue',2),
              rect(52,96,208,46,'panel',radius=5),text(156,125,'Laravel API',20,'cyan',anchor='middle')]
        if not mobile:p += [text(0,174,'Vue + Pinia / API / product data',14,'muted',mono=True)]
    else:
        for i,label in enumerate(['GTK client','JSON-RPC daemon','runtime CLI','Wine + prefix']):
            bx,by=(i%2)*166,(i//2)*85
            p += [rect(bx,by,146,52,'soft',radius=5),text(bx+73,by+32,label,15 if i==1 else 17,anchor='middle')]
        p += [path('M146 26H166M239 52V70H73V85M146 111H166','blue',2)]
        if not mobile:p += [text(0,174,'Experimental / Wine-backed',14,'muted',mono=True)]
    p += ['</g>']
    return document(title,f'{summary} {category}. Source-based illustration, not a screenshot or live demo.',w,h,p,theme)


def architecture(theme, mobile=False):
    w,h=(360,528) if mobile else (960,330)
    p=[rect(.5,.5,w-1,h-1,'bg',radius=12),text(24 if mobile else 32,43,'One feature. Clear boundaries.',22 if mobile else 32,weight=700),
       text(24 if mobile else 32,72,'An illustrative architecture',17,'muted')]
    nodes=[('Interface','Components / state','Interaction / feedback'),
           ('Application','API / authorization','Validation / business rules'),
           ('Work and data','Queues / cache','Schema / queries / storage')]
    for i,(title,detail,detail2) in enumerate(nodes):
        x,y,nw=(24,94+i*105,312) if mobile else (32+i*310,104,276)
        p += [rect(x,y,nw,87 if mobile else 124),text(x+18,y+28,title,23,weight=600),
              text(x+18,y+54,detail,17 if mobile else 19,'muted'),text(x+18,y+77 if mobile else y+87,detail2,17 if mobile else 19,'muted')]
        if i<2:
            p += [path(f'M180 {y+87}v18' if mobile else f'M{x+nw} 166h34','blue',2)]
    p += [rect(24 if mobile else 32,420 if mobile else 256,312 if mobile else 896,84 if mobile else 51,'soft'),
          text(42 if mobile else 50,448 if mobile else 288,'Delivery supports every layer',18 if mobile else 20,'blue')]
    p += [text(42,477,'Linux / containers / CI/CD',17,'muted')] if mobile else [text(910,288,'Linux / containers / CI/CD',18,'muted',mono=True,anchor='end')]
    return document('Illustrative full-stack architecture','Interface, application logic, and work and data have explicit boundaries. Delivery supports all layers. This is a conceptual pattern, not every project’s architecture.',w,h,p,theme)


def overview(data, theme, mobile=False):
    w,h=(360,274) if mobile else (960,180)
    m=data['metrics']
    items=[('Public repos',m['public_repos'],'Including forks'),('Stars',m['total_stars'],'Across public repos'),
           ('Originals' if mobile else 'Original repos',m['original_repos'],'Excluding forks'),('Featured',m['featured_projects'],'Verified repositories')]
    icons=['M0 3h18v14H0ZM4 0v3M4 7h10M4 11h7','M9 0l3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1Z',
           'M3 0v12h12V0M3 6h12M3 12v6','M0 0h7v7H0ZM11 0h7v7h-7ZM0 11h7v7H0ZM11 11h7v7h-7Z']
    p=[]
    for i,(label,value,detail) in enumerate(items):
        x,y=(8+(i%2)*178,8+(i//2)*120) if mobile else (i*242,4)
        cw=166 if mobile else 234
        p += [rect(x+.5,y+.5,cw-1,109 if mobile else 144,'panel',radius=8),
              text(x+14,y+28,label,16 if mobile else 18,'muted'),
              text(x+14,y+83,value,45 if mobile else 53,weight=700),
              f'<g transform="translate({x+cw-29} {y+57})">'+path(icons[i],'blue',1.5)+'</g>']
        if not mobile:p += [text(x+14,y+125,detail,15,'muted')]
    p += [text(8 if mobile else 0,h-8,f'GitHub / {data["updated_at"]} UTC',13 if mobile else 14,'muted',mono=True)]
    desc='; '.join(f'{label}: {value} ({detail})' for label,value,detail in items)
    return document('Public engineering snapshot',desc,w,h,p,theme)


def languages(data, theme, mobile=False):
    w=360 if mobile else 600
    raw=sorted(data['languages'],key=lambda item:item['bytes'],reverse=True)
    total=sum(item['bytes'] for item in raw)
    rows=raw[:5]
    remainder=sum(item['bytes'] for item in raw[5:])
    if remainder:rows=rows+[{'name':'Other','bytes':remainder}]
    h=145+len(rows)*58 if rows else 210
    p=[rect(.5,.5,w-1,h-1,'bg',radius=12),text(24,42,'The public codebase',25 if mobile else 30,weight=700),
       text(24,73,'Share of language bytes',17 if mobile else 18,'muted')]
    descriptions=[]
    for i,item in enumerate(rows):
        y=113+i*58
        percentage=item['bytes']/total*100 if total else 0
        descriptions.append(f'{item["name"]}: {percentage:.1f}%')
        p += [text(24,y,item['name'],19 if mobile else 21),text(w-24,y,f'{percentage:.1f}%',18 if mobile else 20,'muted',mono=True,anchor='end'),
              rect(24,y+12,w-48,7,'soft','none',3)]
        if percentage:p += [rect(24,y+12,round((w-48)*percentage/100,2),7,'blue' if i%2==0 else 'cyan','none',3)]
    if not rows:p += [text(24,130,'No language bytes reported',18,'muted')]
    p += [text(24,h-29,'Original repos; profile excluded.',15 if mobile else 17,'muted')]
    return document('Public repository language distribution','; '.join(descriptions)+'. GitHub language bytes, excluding forks and this profile. Not proficiency or time spent.',w,h,p,theme)


def activity(data, theme, mobile=False):
    a=data['activity'];days=a['days']
    w,h=(360,478) if mobile else (600,350)
    p=[rect(.5,.5,w-1,h-1,'bg',radius=12),text(24,42,'Work in the open',25 if mobile else 30,weight=700),
       text(24,74,'Returned public events',17 if mobile else 18,'muted'),
       text(24,108,f'{a["events_count"]} events in this snapshot',18 if mobile else 20,'blue')]
    if mobile:
        groups=[days[i:i+7] for i in range(0,len(days),7)]
        peak=max((sum(day['count'] for day in group) for group in groups),default=0)
        for i,group in enumerate(groups):
            count=sum(day['count'] for day in group);y=145+i*57
            start,end=(date.fromisoformat(group[0]['date']),date.fromisoformat(group[-1]['date']))
            label=f'{start:%b %d} – {end:%b %d}'
            p += [f'<g data-events="{count}"><title>{group[0]["date"]} to {group[-1]["date"]}: {count} returned events</title>',
                  text(24,y,label,17,'muted'),text(336,y,count,18,mono=True,anchor='end'),rect(24,y+11,312,6,'soft','none',3)]
            if count:p += [rect(24,y+11,round(312*count/peak,2),6,'cyan','none',3)]
            p += ['</g>']
        p += [text(24,440,'Grouped by 7-day intervals.',15,'muted'),text(24,463,'Feed may omit events; not commits.',14,'muted')]
    else:
        maximum=max((day['count'] for day in days),default=0)
        for value in sorted({0,(maximum+1)//2,maximum}):
            y=248-(value/maximum*110 if maximum else 0)
            p += [path(f'M48 {y}H576','border',.7),text(38,y+5,value,14,'muted',mono=True,anchor='end')]
        bw=528/max(1,len(days))
        for i,day in enumerate(days):
            bh=day['count']/maximum*110 if maximum else 0
            if bh:p += [f'<g><title>{day["date"]}: {day["count"]} returned events</title>',rect(round(48+i*bw,2),round(248-bh,2),round(max(1,bw-5),2),round(bh,2),'cyan','none',2),'</g>']
        p += [text(48,277,a['window_start'],16,'muted',mono=True),text(576,277,a['window_end'],16,'muted',mono=True,anchor='end'),
              text(24,309,'Daily events / 30 dates / feed may omit activity',16,'muted'),text(24,334,'No bar = no returned event. Events are not commits.',15,'muted')]
    if a['limited']:p += [text(w-24,74,'API cap reached',12,'muted',anchor='end')]
    desc=(f'Public events returned between {a["window_start"]} and {a["window_end"]}: {a["events_count"]}. '
          'Feed limited to 300 events over 30 days; may omit activity. Events are not commits or contributions. '
          + '; '.join(f'{d["date"]}: {d["count"]}' for d in days if d['count']))
    return document('Recent public GitHub events',desc,w,h,p,theme)


def timeline(data, theme, mobile=False):
    years=Counter(repo['created_at'][:4] for repo in data['repositories'] if not repo['fork'])
    w=360 if mobile else 600
    h=145+len(years)*48
    p=[rect(.5,.5,w-1,h-1,'bg',radius=12),text(24,42,'The repository archive',24 if mobile else 30,weight=700),
       text(24,75,'Original repos by creation year',17 if mobile else 18,'muted')]
    peak=max(years.values(),default=1)
    for i,(year,count) in enumerate(sorted(years.items())):
        y=110+i*48
        p += [f'<g data-year="{year}" data-count="{count}"><title>{year}: {count} currently public original repositories</title>',
              text(24,y+16,year,18,'muted',mono=True),rect(91,y,w-151,20,'soft','none',3),
              rect(91,y,round((w-151)*count/peak,2),20,'blue','none',3),text(w-24,y+16,count,18,mono=True,anchor='end'),'</g>']
    p += [text(24,h-15,'Currently public originals only.',15 if mobile else 17,'muted')]
    return document('Public original repository creation years','; '.join(f'{year}: {count}' for year,count in sorted(years.items()))+'. Counts of currently public original repositories by creation year; deleted and private repositories excluded.',w,h,p,theme)


def render_dashboard(data):
    assets={}
    for theme in PALETTES:
        for mobile in [False,True]:
            suffix=('-mobile' if mobile else '')+'-'+theme+'.svg'
            for name,renderer in [('overview',overview),('languages',languages),('activity',activity),('timeline',timeline)]:
                assets[name+suffix]=renderer(data,theme,mobile)
    return assets


def build_static():
    for theme in PALETTES:
        for mobile in [False,True]:
            suffix=('-mobile' if mobile else '')+'-'+theme+'.svg'
            assets={'assets/hero/hero'+suffix:hero(theme,mobile),
                    'assets/architecture/engineering-flow'+suffix:architecture(theme,mobile)}
            assets.update({'assets/projects/'+key+suffix:project_cover(key,theme,mobile) for key in PROJECTS})
            for name,content in assets.items():
                p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)


if __name__=='__main__':
    build_static()
    snapshot=ROOT/'assets/dashboard/data.json'
    if snapshot.exists():
        for name,svg in render_dashboard(json.loads(snapshot.read_text())).items():
            (snapshot.parent/name).write_text(svg)
    print('Profile SVG assets rebuilt.')
