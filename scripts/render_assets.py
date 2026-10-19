"""Repository-hosted SVG artwork and public-data charts; Python standard library only."""

from collections import Counter
from datetime import date
from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    'dark': dict(bg='#090F17', panel='#0E1924', soft='#162B3A', text='#E5EDF5',
                 muted='#A5B8C9', border='#294253', blue='#65C9F3', cyan='#1BE0AC'),
    'light': dict(bg='#F4F8FC', panel='#FFFFFF', soft='#E7F0F7', text='#14293B',
                  muted='#4B6174', border='#BDCEDC', blue='#075FBF', cyan='#00745A'),
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
    definitions = ('<defs><linearGradient id="surface" x2="0" y2="1">'
                   '<stop stop-color="'+PALETTES[theme]['soft']+'"/>'
                   '<stop offset="1" stop-color="'+PALETTES[theme]['panel']+'"/></linearGradient>'
                   '<linearGradient id="area" x2="0" y2="1">'
                   '<stop stop-color="'+PALETTES[theme]['cyan']+'" stop-opacity=".4"/>'
                   '<stop offset="1" stop-color="'+PALETTES[theme]['cyan']+'" stop-opacity=".02"/></linearGradient>'
                   '<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">'
                   '<path d="M24 0H0V24" fill="none" stroke="'+PALETTES[theme]['border']+'" stroke-opacity=".24"/></pattern>'
                   '<filter id="glow" x="-80%" y="-80%" width="260%" height="260%">'
                   '<feGaussianBlur stdDeviation="3"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>\n'
            + definitions + motion + body + '\n</svg>\n')


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


def console_header(width, label):
    p=[path(f'M1 42H{width-1}'),text(86,27,label,13,'muted',mono=True)]
    for i,color in enumerate(['#FF6B6B','#F4C45E','#28C895']):
        p += [circle(24+i*18,22,4.5,color)]
    return p


def hero(theme, mobile=False):
    w,h=(360,374) if mobile else (960,390)
    p=[rect(.5,.5,w-1,h-1,'bg',radius=6),rect(1,43,w-2,h-44,'url(#grid)','none',0)]
    p += console_header(w,'~/profile' if mobile else '~/prabhuramkarki / profile.console')
    if mobile:
        p += [text(24,79,'Full-Stack Software Engineer',17,'muted'),
              text(21,134,'Prabhuram',46,weight=600),text(21,184,'Karki',46,weight=600),
              text(24,240,'build products.',29,'cyan'),text(24,280,'understand systems.',29),
              path('M24 305H336'),text(24,334,'Vue / Nuxt / Laravel',16,'muted',mono=True),
              text(24,359,'Kathmandu, Nepal',15,'muted',mono=True)]
        route='M258 345H331'
    else:
        p += [text(32,89,'// Full-Stack Software Engineer',19,'muted',mono=True),
              text(28,153,'Prabhuram Karki',65,weight=600),
              text(32,223,'build products.',47,'cyan'),text(32,280,'understand systems.',47),
              text(32,321,'Vue / Nuxt / Quasar / Laravel',18,'muted',mono=True),
              rect(650,64,278,265,'url(#surface)',radius=3),text(670,91,'// working set',15,'muted',mono=True)]
        for i,(label,value) in enumerate([('interface','Vue / Nuxt / Quasar'),('application','Laravel / Node'),('exploration','Rust / Linux')]):
            y=126+i*69
            p += [text(670,y,label,14,'muted',mono=True),text(670,y+26,value,19,'blue' if i<2 else 'cyan'),path(f'M670 {y+43}H908')]
        p += [path('M32 347H928'),text(32,374,'prabhuram@kathmandu:~/github $',15,'muted',mono=True),
              text(379,374,'explore --source',15,'cyan',mono=True)]
        route='M791 368H909'
    p += [path(route,'border',1),path(route,'cyan',2,extra='class="signal" stroke-dasharray="8 88"'),
          rect(w-42,h-35,7,15,'cyan','none',0).replace('/>',' class="cursor"/>')]
    return document('Prabhuram Karki · Full-Stack Software Engineer',
                    'Build products. Understand systems. Full-stack software engineer in Kathmandu, Nepal. Vue, Nuxt, Quasar and Laravel; exploring Rust and Linux. Terminal motion is decorative and stops within four seconds.',w,h,p,theme)


PROJECTS = {
    'code-shell': ('Code Shell','Developer tooling','A prompt, with boundaries.'),
    'easy-invoice': ('Easy Invoice','Document processing','An image becomes a record.'),
    'manducart': ('ManduCart v2','Full-stack product','A storefront meets its API.'),
    'linux-runtime': ('Windows apps on Linux','Systems exploration','An app meets its host.'),
}


def project_cover(key, theme, mobile=False):
    title,category,summary=PROJECTS[key]
    if key=='linux-runtime':title='Windows runtime'
    w,h=(360,254) if mobile else (460,254)
    lines={
        'code-shell':('A native Rust coding agent.','Streaming models. Controlled tools.',('Rust','Tokio','CLI'),'core / providers / tools / cli'),
        'easy-invoice':('Invoice images into structured data.','OCR, field extraction, database + CSV.',('React','Django','OCR'),'image → text → fields → record'),
        'manducart':('A storefront connected to its API.','Catalog, accounts, and cart operations.',('Vue','Pinia','Laravel'),'prototype / checkout unfinished'),
        'linux-runtime':('Windows applications on a Linux host.','Per-app prefixes and sandbox policies.',('Rust','Wine','GTK 4'),'experimental / Wine-backed'),
    }
    first,second,tags,note=lines[key]
    p=[rect(.5,.5,w-1,h-1,'url(#surface)',radius=8),path(f'M18 1H{w-18}','blue',1.5),
       '<g transform="translate(23 24)">'+path('M12 0l12 7v14l-12 7L0 21V7ZM0 7l12 7 12-7M12 14v14','blue',1.5)+'</g>',
       text(62,44,title,24,weight=600),
       path(f'M{w-38} 27h14v14M{w-24} 27l-16 16M{w-29} 48h-18V30','muted',1.3),
       text(24,91,first,16 if mobile else 19),text(24,119,second,15 if mobile else 18,'muted')]
    x=24
    for tag in tags:
        tw=round(len(tag)*9+22)
        p += [rect(x,143,tw,29,'soft','border',3),text(x+11,163,tag,15,'blue')]
        x += tw+8
    p += [path(f'M24 194H{w-24}'),text(24,220,category,14,'cyan'),
          text(24,242,note,12 if mobile else 13,'muted',mono=True)]
    return document(title,f'{first} {second} {category}. {note}. Repository card, not an application screenshot.',w,h,p,theme)


def system_node(x, y, label, detail, color='cyan'):
    p=[f'<g transform="translate({x} {y})">',
       path('M0-27L35-8V15L0 35L-35 15V-8Z','border',1,'soft'),
       path('M0-35L35-15L0 5L-35-15Z',color,1.5,'url(#surface)'),
       path('M0 5V35M-35-15V15M35-15V15',color,1.2),
       path('M0-25L19-14L0-3L-19-14Z',color,1,color,extra='opacity=".7" filter="url(#glow)"'),
       text(0,65,label,21,weight=600,anchor='middle'),text(0,91,detail,15,'muted',anchor='middle'),'</g>']
    return p


def architecture(theme, mobile=False):
    w,h=(360,557) if mobile else (960,400)
    p=[rect(.5,.5,w-1,h-1,'bg',radius=6),rect(1,43,w-2,h-44,'url(#grid)','none',0)]
    p += console_header(w,'system.map' if mobile else 'system.map / illustrative architecture')
    if mobile:
        p += [path('M180 110V420','blue',2,extra='opacity=".4"')]
        for i,(label,detail) in enumerate([('Interface','Components / state'),('Application','API / rules / permissions'),('Work and data','Queues / cache / database')]):
            p += system_node(180,115+i*141,label,detail,'blue' if i==0 else 'cyan')
        p += [path('M24 518H336'),text(180,544,'Linux / containers / CI/CD',16,'muted',anchor='middle')]
    else:
        p += [text(32,81,'Follow the feature through the system.',24,weight=500),
              path('M176 174L460 206L770 174M460 206V293','blue',2,extra='opacity=".55"'),
              path('M176 174L460 206L770 174','cyan',7,extra='opacity=".1" filter="url(#glow)"')]
        for x,y,label,detail,color in [(176,160,'Interface','Components / state','blue'),(460,192,'Application','API / validation / authorization','cyan'),(770,160,'Work and data','Queues / cache / database','blue')]:
            p += system_node(x,y,label,detail,color)
        p += [rect(339,309,242,36,'panel',radius=3),text(460,333,'Linux / containers / CI/CD',16,'cyan',anchor='middle'),
              path('M32 366H928'),text(32,388,'Conceptual architecture / delivery supports every layer',15,'muted',mono=True)]
    return document('Illustrative full-stack system map','Components and state connect to application APIs, rules and authorization, then queues, cache and databases. Linux, containers and CI/CD support all layers. Conceptual architecture, not a deployed system or live telemetry.',w,h,p,theme)


def overview(data, theme, mobile=False):
    w,h=(360,843) if mobile else (960,516)
    m=data['metrics'];a=data['activity']
    p=[rect(.5,.5,w-1,h-1,'bg',radius=6),rect(1,43,w-2,h-44,'url(#grid)','none',0)]
    p += console_header(w,'public.profile' if mobile else 'public.profile / GitHub REST API snapshot')
    items=[('Public repos',m['public_repos'],'Including forks'),('Stars',m['total_stars'],'Public repositories'),
           ('Originals',m['original_repos'],'Excluding forks'),('Featured',m['featured_projects'],'Verified source')]
    for i,(label,value,detail) in enumerate(items):
        x,y=(16+(i%2)*170,60+(i//2)*110) if mobile else (20+i*235,62)
        cw=158 if mobile else 215
        p += [rect(x,y,cw,96 if mobile else 110,'url(#surface)',radius=4),
              path(f'M{x+14} {y+16}h20','cyan',2),text(x+14,y+43,label,16,'muted'),
              text(x+14,y+83,value,40,weight=600),path(f'M{x+cw-30} {y+66}v13h14v-13Z','blue',1.3)]
        if not mobile:p += [text(x+76,y+83,detail,13,'muted')]
    # Every plotted point is a returned event count. The area uses straight segments.
    px,py,pw,ph=(16,294,328,224) if mobile else (20,195,556,278)
    p += [rect(px,py,pw,ph,'panel',radius=4),text(px+18,py+31,'Public events / 30 UTC dates',15 if mobile else 18,'muted'),
          text(px+18,py+62,f'{a["events_count"]} returned events',22 if mobile else 26,'cyan')]
    left,right,bottom,top=px+35,px+pw-18,py+ph-45,py+92
    days=a['days'];peak=max((d['count'] for d in days),default=0)
    for tick in sorted({0,(peak+1)//2,peak}):
        yy=bottom-(tick/peak*(bottom-top) if peak else 0)
        p += [path(f'M{left} {yy}H{right}','border',.7),text(left-8,yy+4,tick,11 if mobile else 13,'muted',mono=True,anchor='end')]
    points=[]
    bw=(right-left)/max(1,len(days))
    for i,day in enumerate(days):
        bh=(day['count']/peak*(bottom-top)) if peak else 0
        xx=left+(i+.5)*bw;yy=bottom-bh;points.append((xx,yy))
        p += [rect(round(left+i*bw,2),round(yy,2),round(max(1,bw-2),2),round(bh,2),'cyan','none',0).replace('/>',f' data-events="{day["count"]}"/>')]
    if points:
        route='M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in points)
        area=route+f'L{points[-1][0]:.2f} {bottom}L{points[0][0]:.2f} {bottom}Z'
        p += [path(area,'none',0,'url(#area)'),path(route,'cyan',1.5)]
    p += [text(left,bottom+23,date.fromisoformat(a['window_start']).strftime('%b %d'),13,'muted',mono=True),
          text(right,bottom+23,date.fromisoformat(a['window_end']).strftime('%b %d'),13,'muted',mono=True,anchor='end')]
    if a['limited']:p += [text(px+pw-18,py+60,'API cap',12,'muted',anchor='end')]
    lx,ly,lw,lh=(16,534,328,264) if mobile else (596,195,344,278)
    p += [rect(lx,ly,lw,lh,'panel',radius=4),text(lx+18,ly+31,'Language bytes / originals',15 if mobile else 18,'muted')]
    raw=sorted(data['languages'],key=lambda row:row['bytes'],reverse=True);total=sum(row['bytes'] for row in raw)
    rows=raw[:5]
    if len(raw)>5:rows += [{'name':'Other','bytes':sum(row['bytes'] for row in raw[5:])}]
    for i,row in enumerate(rows):
        yy=ly+63+i*30;share=row['bytes']/total*100 if total else 0
        p += [f'<g data-language="{escape(row["name"],quote=True)}" data-share="{share:.1f}">',
              text(lx+18,yy,row['name'],16),text(lx+lw-18,yy,f'{share:.1f}%',16,'muted',mono=True,anchor='end'),
              rect(lx+18,yy+8,lw-36,4,'soft','none',2)]
        if share:p += [rect(lx+18,yy+8,round((lw-36)*share/100,2),4,'blue' if i%2 else 'cyan','none',2)]
        p += ['</g>']
    if not rows:p += [text(lx+18,ly+86,'No language bytes reported',17,'muted')]
    p += [text(20,h-24,f'{data["updated_at"]} UTC / public-data snapshot',12 if mobile else 14,'muted',mono=True)]
    if not mobile:p += [text(w-20,h-24,'Events ≠ commits / bytes ≠ proficiency',13,'muted',mono=True,anchor='end')]
    desc='; '.join(f'{label}: {value} ({detail})' for label,value,detail in items)
    desc += f'. {a["events_count"]} returned events from {a["window_start"]} to {a["window_end"]}; capped and possibly incomplete. Language shares represent repository bytes, not proficiency.'
    return document('Public engineering console',desc,w,h,p,theme)


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
