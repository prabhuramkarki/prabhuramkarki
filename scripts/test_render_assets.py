"""Offline rendering checks: trustworthy labels and self-contained GitHub SVGs."""

import json
from datetime import date, timedelta
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from render_assets import render_dashboard, hero, project_cover, architecture, PROJECTS, PALETTES


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((Path(__file__).resolve().parents[1]/'assets/dashboard/data.json').read_text())

    def test_assets_are_accessible_and_self_contained(self):
        assets=list(render_dashboard(self.data).values())
        for theme in ['dark','light']:
            for mobile in [False, True]:
                assets.extend([hero(theme,mobile),architecture(theme,mobile)])
                assets.extend(project_cover(key,theme,mobile) for key in PROJECTS)
        for content in assets:
            root=ET.fromstring(content)
            self.assertEqual(root.tag,'{http://www.w3.org/2000/svg}svg')
            self.assertIsNotNone(root.find('{http://www.w3.org/2000/svg}title'))
            self.assertIsNotNone(root.find('{http://www.w3.org/2000/svg}desc'))
            for element in root.iter():
                self.assertNotIn(element.tag.split('}')[-1],['script','foreignObject','image'])
                for attribute in element.attrib:
                    self.assertFalse(attribute.lower().startswith('on'))

    def test_language_names_are_escaped_and_empty_data_is_honest(self):
        self.data['languages']=[{'name':'A&B <tag>','bytes':3}]
        assets=render_dashboard(self.data)
        self.assertIn('A&amp;B &lt;tag&gt;',assets['languages-dark.svg'])
        self.assertIn('100.0%',assets['languages-dark.svg'])
        self.data['languages']=[]
        self.assertIn('No language bytes reported',render_dashboard(self.data)['languages-dark.svg'])

    def test_activity_displays_qualifying_count_and_api_limit(self):
        self.data['activity']['events_count']=7
        self.data['activity']['events_returned']=12
        self.data['activity']['limited']=True
        content=render_dashboard(self.data)['activity-dark.svg']
        self.assertIn('7 events in this snapshot',content)
        self.assertNotIn('12 events in this snapshot',content)
        self.assertIn('API cap reached',content)

    def test_motion_has_reduced_motion_fallback(self):
        content=hero('dark')
        self.assertIn('prefers-reduced-motion:reduce',content)
        self.assertIn('animation:none',content)

    def test_peak_activity_bars_stay_below_the_summary(self):
        for day in self.data['activity']['days']:
            day['count']=10
        content=render_dashboard(self.data)['activity-dark.svg']
        root=ET.fromstring(content)
        bars=[r for r in root.iter('{http://www.w3.org/2000/svg}rect') if r.get('fill')=='#39C5CF']
        self.assertTrue(bars)
        self.assertTrue(all(float(bar.get('y'))>=128 for bar in bars))

    def test_mobile_activity_groups_every_day_without_losing_events(self):
        self.data['activity']['window_start']='2026-09-20'
        self.data['activity']['window_end']='2026-10-19'
        self.data['activity']['days']=[
            {'date':(date(2026,9,20)+timedelta(days=i)).isoformat(),'count':0}
            for i in range(30)
        ]
        self.data['activity']['days'][0]['count']=2
        self.data['activity']['days'][6]['count']=3
        self.data['activity']['days'][7]['count']=7
        self.data['activity']['days'][29]['count']=11
        self.data['activity']['events_count']=23
        root=ET.fromstring(render_dashboard(self.data)['activity-mobile-dark.svg'])
        groups=root.findall('.//{http://www.w3.org/2000/svg}g[@data-events]')
        self.assertEqual([int(group.get('data-events')) for group in groups],[5,7,0,0,11])
        self.assertIn('2026-09-20 to 2026-09-26',groups[0].find('{http://www.w3.org/2000/svg}title').text)
        self.assertIn('2026-10-18 to 2026-10-19',groups[-1].find('{http://www.w3.org/2000/svg}title').text)

    def test_creation_timeline_counts_current_originals_only(self):
        self.data['repositories']=[
            {'created_at':'2024-01-01T00:00:00Z','fork':False},
            {'created_at':'2024-12-31T23:59:00Z','fork':False},
            {'created_at':'2026-01-01T00:00:00Z','fork':False},
            {'created_at':'2025-01-01T00:00:00Z','fork':True},
        ]
        root=ET.fromstring(render_dashboard(self.data)['timeline-dark.svg'])
        groups=root.findall('.//{http://www.w3.org/2000/svg}g[@data-year]')
        self.assertEqual([(g.get('data-year'),g.get('data-count')) for g in groups],[('2024','2'),('2026','1')])

    def test_empty_event_window_has_no_positive_bars(self):
        self.data['activity']['events_count']=0
        for day in self.data['activity']['days']:
            day['count']=0
        for name,content in render_dashboard(self.data).items():
            if name.startswith('activity-') and name.endswith('dark.svg'):
                root=ET.fromstring(content)
                bars=[r for r in root.iter('{http://www.w3.org/2000/svg}rect') if r.get('fill')=='#39C5CF']
                self.assertEqual(bars,[])
                self.assertIn('0 events in this snapshot',content)

    def test_text_colors_meet_normal_text_contrast_on_every_surface(self):
        def luminance(color):
            channels=[int(color[i:i+2],16)/255 for i in (1,3,5)]
            channels=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in channels]
            return sum(v*weight for v,weight in zip(channels,[.2126,.7152,.0722]))
        for theme,palette in PALETTES.items():
            for foreground in ['text','muted','blue','cyan']:
                for surface in ['bg','panel','soft']:
                    with self.subTest(theme=theme,text=foreground,surface=surface):
                        a,b=sorted([luminance(palette[foreground]),luminance(palette[surface])])
                        self.assertGreaterEqual((b+.05)/(a+.05),4.5)


if __name__=='__main__':
    unittest.main()
