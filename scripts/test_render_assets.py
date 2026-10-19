"""Offline rendering checks: trustworthy labels and self-contained GitHub SVGs."""

import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from render_assets import render_dashboard, hero, project_cover, architecture, PROJECTS


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((Path(__file__).resolve().parents[1]/'assets/dashboard/data.json').read_text())

    def test_assets_are_accessible_and_self_contained(self):
        assets=list(render_dashboard(self.data).values())
        for theme in ['dark','light']:
            assets.extend([hero(theme),hero(theme,True),architecture(theme)])
            assets.extend(project_cover(key,theme) for key in PROJECTS)
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


if __name__=='__main__':
    unittest.main()
