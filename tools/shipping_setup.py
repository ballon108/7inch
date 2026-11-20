#!/usr/bin/env python3
"""Create/update the DHL shipping zones and their rates (podatki.md, EUR). Idempotent: missing zones are created,
existing ones (matched by name) get their rates and locations refreshed. Editable later in WooCommerce > Settings > Shipping.
Germany and USA ship tracked even for 1-5 records (label 'tracked'). Per zone: consumer 1-5 records, consumer 6+ (or tracked 1-5), partner parcel 5 kg, partner parcel 10 kg."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__)); import deploy
print(deploy.php(r"""
$EU = ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE'];
$RE = ['AL','AD','BA','BY','FO','GI','GG','IM','JE','IS','XK','LI','MD','MC','ME','MK','NO','SM','RS','TR','UA','VA'];
$c  = fn($a)=>array_map(fn($x)=>[$x,'country'], $a);
$zones = [ // name, locations, small, large, b2b 5kg, b2b 10kg
 ['DHL Germany', $c(['DE']), 4.90, 6.90, 9.90, 12.90],
 ['DHL EU', $c($EU), 7.90, 15.90, 19.90, 24.90],
 ['DHL UK & Switzerland', $c(['GB','CH']), 11.90, 20.90, 28.90, 36.90],
 ['DHL Rest of Europe', $c($RE), 14.50, 24.90, 28.90, 36.90],
 ['DHL USA', $c(['US']), 31.90, 31.90, 51.90, 81.90],
 ['DHL Canada, Mexico, Brazil', $c(['CA','MX','BR']), 18.90, 27.90, 49.90, 79.90],
 ['DHL Asia', [['AS','continent']], 17.90, 26.90, 47.90, 63.90],
 ['DHL Australia & New Zealand', $c(['AU','NZ']), 18.90, 28.90, 57.90, 98.90],
];
$existing = [];
foreach (WC_Shipping_Zones::get_zones() as $z) { $existing[$z['zone_name']] = $z['id']; }
WC()->shipping()->load_shipping_methods();
$out = [];
foreach ($zones as $i => [$name,$locs,$small,$large,$b5,$b10]) {
  $zone = isset($existing[$name]) ? new WC_Shipping_Zone($existing[$name]) : new WC_Shipping_Zone();
  $zone->set_zone_name($name); $zone->set_zone_order($i+1);
  $zone->clear_locations(['country','continent']);
  foreach ($locs as [$code,$type]) $zone->add_location($code,$type);
  $zone->save();
  $ms = $zone->get_shipping_methods();
  $iid = $ms ? array_values($ms)[0]->instance_id : $zone->add_shipping_method('i7_dhl');
  update_option('woocommerce_i7_dhl_'.$iid.'_settings', ['title'=>'DHL','cost_small'=>$small,'cost_large'=>$large,'small_label'=>in_array($name,['DHL Germany','DHL USA'],true)?'tracked':'untracked','large_label'=>'tracked','b2b_5kg'=>$b5,'b2b_10kg'=>$b10]);
  $out[] = [$name, $iid];
}
update_option('woocommerce_calc_shipping', 'yes');
return $out;
"""))
