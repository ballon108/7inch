#!/usr/bin/env python3
"""Bring the German series (term meta) and product descriptions in line with the EN/DE translation table.
usage: fix_de_db.py [--apply]   (without --apply: dry run, prints what would change)"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deploy import php

TERM = {  # German series terms: 48 My Philosophy, 51 Lowrider Anthems
 48: {'eyebrow': 'Serie 01 · 90er Hip-Hop & R&B',
      'blurb': 'Bekannte und fast vergessene Klassiker, Episode für Episode. Kleine, nummerierte Auflagen.',
      'hero_lead': 'Zwei Seiten 90er Hip-Hop & R&B – neu editiert und auf 7" gepresst.',
      'story_text': 'Jede Episode bringt zwei Songs zusammen, die zusammengehören: bekannte Klassiker und Tracks, die nur echte Digger in der Plattentasche haben – als limitierte 7" mit eigener Labelfarbe.'},
 51: {'eyebrow': 'Serie 02 · West Coast / G-Funk',
      'blurb': 'Nur West Coast und G-Funk, neu editiert für den Boulevard. In vollfarbigen Bildhüllen.',
      'hero_lead': 'Zwei West-Coast-Klassiker, neu editiert für den Boulevard und auf 7" gepresst.',
      'story_heading': 'Gemacht fürs Sonntags-Cruisen',
      'story_text': 'LOWRIDER ANTHEMS ist die West-Coast-Seite von 7inch.rare: nur G-Funk und West-Coast-Hip-Hop – der Soundtrack zu Chrom, Hydraulik und langsamen Runden über palmengesäumte Boulevards.'},
}
PROD = {  # old German lead -> table wording (descriptions of all German products)
 'Zwei Seiten 90er Hip Hop & R&B, neu editiert und auf 7" gepresst.': 'Zwei Seiten 90er Hip-Hop & R&B – neu editiert und auf 7" gepresst.',
 'Zwei West Coast Klassiker, neu editiert für den Boulevard und auf 7" geschnitten.': 'Zwei West-Coast-Klassiker, neu editiert für den Boulevard und auf 7" gepresst.',
}
apply = '--apply' in sys.argv
code = f"""
$apply = {'true' if apply else 'false'}; $log = [];
foreach (json_decode({json.dumps(json.dumps(TERM))}, true) as $tid => $m) foreach ($m as $k => $v) {{
  $old = get_term_meta($tid, $k, true); if ($old !== $v) {{ $log[] = "term $tid $k: $old => $v"; if ($apply) update_term_meta($tid, $k, $v); }}
}}
$ids = get_posts(['post_type'=>'product','post_status'=>'any','numberposts'=>-1,'fields'=>'ids','lang'=>'de']);
foreach ($ids as $id) {{
  $c = get_post_field('post_content', $id); $n = strtr($c, json_decode({json.dumps(json.dumps(PROD))}, true));
  if ($n !== $c) {{ $log[] = "product $id: $c => $n"; if ($apply) wp_update_post(['ID'=>$id,'post_content'=>$n]); }}
}}
return $log;"""
for l in php(code): print(l)
