#!/usr/bin/env python3
"""Create the DHL shipping zones (only if missing) and enable shipping + a separate shipping address at checkout.
Rates (brief, retail): 1-3 records / 4+ records. Editable later in WooCommerce > Settings > Shipping."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__)); import deploy
print(deploy.php(r"""
$EU = ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE'];
$zones = [
 ['DHL Germany', [['DE','country']], 3.90, 6.90, 'Großbrief (no tracking)', 'DHL Paket'],
 ['DHL EU', array_map(fn($c)=>[$c,'country'], $EU), 8.90, 16.90, 'Päckchen XS', 'DHL Paket'],
 ['DHL UK & Switzerland', [['GB','country'],['CH','country']], 10.90, 21.90, 'Päckchen XS', 'DHL Paket'],
 ['DHL Americas', [['US','country'],['CA','country'],['MX','country'],['BR','country']], 17.90, 28.90, 'Päckchen XS', 'DHL Paket'],
 ['DHL Asia', [['AS','continent']], 16.90, 27.90, 'Päckchen XS', 'DHL Paket'],
 ['DHL Australia & New Zealand', [['AU','country'],['NZ','country']], 18.90, 29.90, 'Päckchen XS', 'DHL Paket'],
];
$have = array_map(fn($z)=>$z['zone_name'], WC_Shipping_Zones::get_zones());
WC()->shipping()->load_shipping_methods();
$out = [];
foreach ($zones as $i => [$name,$locs,$small,$large,$sl,$ll]) {
  if (in_array($name, $have, true)) { $out[] = [$name, 'exists']; continue; }
  $zone = new WC_Shipping_Zone(); $zone->set_zone_name($name); $zone->set_zone_order($i+1);
  foreach ($locs as [$code,$type]) $zone->add_location($code,$type);
  $zone->save();
  $iid = $zone->add_shipping_method('i7_dhl');
  $m = WC_Shipping_Zones::get_shipping_method($iid);
  update_option($m->get_instance_option_key(), ['title'=>'DHL','cost_small'=>$small,'cost_large'=>$large,'small_label'=>$sl,'large_label'=>$ll]);
  $out[] = [$name, $iid];
}
update_option('woocommerce_calc_shipping', 'yes');
update_option('woocommerce_ship_to_destination', 'shipping');   // separate shipping address at checkout
return $out;
"""))
