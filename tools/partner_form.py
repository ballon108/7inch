#!/usr/bin/env python3
"""Install/activate Contact Form 7 on 7inchrare.com and (re)create the partner application form.
usage: partner_form.py   (idempotent; stores the form id in option _7inch_partner_form)"""
import base64, os, sys
sys.path.insert(0, os.path.dirname(__file__)); import deploy

# All WooCommerce countries except Russia (EU sanctions, not served).
COUNTRIES = ["Afghanistan", "Åland Islands", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla", "Antarctica", "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belau", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bonaire, Saint Eustatius and Saba", "Bosnia and Herzegovina", "Botswana", "Bouvet Island", "Brazil", "British Indian Ocean Territory", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands", "Central African Republic", "Chad", "Chile", "China", "Christmas Island", "Cocos (Keeling) Islands", "Colombia", "Comoros", "Congo (Brazzaville)", "Congo (Kinshasa)", "Cook Islands", "Costa Rica", "Croatia", "Cuba", "Curaçao", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Falkland Islands", "Faroe Islands", "Fiji", "Finland", "France", "French Guiana", "French Polynesia", "French Southern Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard Island and McDonald Islands", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Isle of Man", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jersey", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macao", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "North Korea", "North Macedonia", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palestinian Territory", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romania", "Rwanda", "Saint Barthélemy", "Saint Helena", "Saint Kitts and Nevis", "Saint Lucia", "Saint Martin (Dutch part)", "Saint Martin (French part)", "Saint Pierre and Miquelon", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "São Tomé and Príncipe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Georgia/Sandwich Islands", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Svalbard and Jan Mayen", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tokelau", "Tonga", "Trinidad and Tobago", "Tunisia", "Türkiye", "Turkmenistan", "Turks and Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom (UK)", "United States (US)", "United States (US) Minor Outlying Islands", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican", "Venezuela", "Vietnam", "Virgin Islands (British)", "Virgin Islands (US)", "Wallis and Futuna", "Western Sahara", "Yemen", "Zambia", "Zimbabwe"]
country_opts = " ".join(f'"{c}"' for c in COUNTRIES)

FORM = f"""<div class="pf">
<fieldset class="pf-type"><legend>I am applying as</legend>[radio apply_as use_label_element default:1 "Record shop" "Distributor"]</fieldset>

<div><label>Company name *[text* company autocomplete:organization]</label></div>
<div><label>Contact person *[text* contact autocomplete:name]</label></div>
<div><label>E-mail *[email* your-email autocomplete:email]</label></div>
<div><label>Phone[tel phone autocomplete:tel]</label></div>

<div><label>Country *[select* country include_blank {country_opts}]</label></div>
<div><label>EU VAT number (optional)[text vat]</label></div>
<div class="pf-wide"><label>Company address *[textarea* address 4x2 autocomplete:street-address]</label></div>


<div class="pf-check">[acceptance consent] I accept the <a href="/trade-terms/" target="_blank" rel="noopener">Trade Terms</a> and the <a href="/privacy-policy/" target="_blank" rel="noopener">Privacy Policy</a>, and agree that 7inch.rare may process my details to handle this application. *[/acceptance]</div>
<div class="pf-submit">[submit "Send application"]</div>
</div>"""

MAIL_BODY = """New partner application

Type: [apply_as]
Company: [company]
Contact person: [contact]
E-mail: [your-email]
Phone: [phone]
Country: [country]
EU VAT number: [vat]
Address:
[address]


--
Sent from the "For partners" form on [_site_url]"""

B = lambda t: base64.b64encode(t.encode()).decode()
code = f"""
include_once ABSPATH.'wp-admin/includes/plugin.php';
include_once ABSPATH.'wp-admin/includes/file.php';
include_once ABSPATH.'wp-admin/includes/misc.php';
include_once ABSPATH.'wp-admin/includes/class-wp-upgrader.php';
include_once ABSPATH.'wp-admin/includes/plugin-install.php';
$log = [];
$slug = 'contact-form-7/wp-contact-form-7.php';
if (!file_exists(WP_PLUGIN_DIR.'/'.$slug)) {{
  $api = plugins_api('plugin_information', ['slug'=>'contact-form-7', 'fields'=>['sections'=>false]]);
  if (is_wp_error($api)) return 'plugins_api: '.$api->get_error_message();
  $up = new Plugin_Upgrader(new Automatic_Upgrader_Skin());
  $r = $up->install($api->download_link);
  if (is_wp_error($r) || !$r) return ['install failed', is_wp_error($r) ? $r->get_error_message() : $up->skin->get_upgrade_messages()];
  $log[] = 'installed '.$api->version;
}}
if (!is_plugin_active($slug)) {{
  $a = activate_plugin($slug);
  if (is_wp_error($a)) return 'activate: '.$a->get_error_message();
  $log[] = 'activated';
}}
if (!class_exists('WPCF7_ContactForm')) {{ include_once WP_PLUGIN_DIR.'/'.$slug; do_action('plugins_loaded'); }}
if (!class_exists('WPCF7_ContactForm')) return ['CF7 not loaded', $log];

$id = (int) get_option('_7inch_partner_form');
$cf = $id ? WPCF7_ContactForm::get_instance($id) : null;
if (!$cf) {{ $cf = WPCF7_ContactForm::get_template(['title'=>'Partner application', 'locale'=>'en_US']); }}
$cf->set_title('Partner application');
$props = $cf->get_properties();
$props['form'] = base64_decode('{B(FORM)}');
$props['mail'] = array_merge($props['mail'], [
  'subject' => 'Partner application: [company] ([apply_as], [country])',
  'sender'  => 'Vibetown Entertainment <shop@7inchrare.com>',
  'recipient' => 'shop@7inchrare.com',
  'additional_headers' => 'Reply-To: [your-email]',
  'body' => base64_decode('{B(MAIL_BODY)}'),
  'use_html' => 0, 'exclude_blank' => 0,
]);
$props['messages'] = array_merge($props['messages'], [
  'mail_sent_ok' => "Thank you. We'll review your application and get back to you within 48 hours.",
  'validation_error' => 'Please check the highlighted fields and try again.',
  'accept_terms' => 'Please confirm that we may process your details.',
]);
$cf->set_properties($props);
$id = $cf->save();
update_option('_7inch_partner_form', $id);
return ['form_id'=>$id, 'log'=>$log, 'cf7'=>defined('WPCF7_VERSION') ? WPCF7_VERSION : '?'];
"""
print(deploy.php(code))

if "--pages" not in sys.argv:
    sys.exit(0)  # pass --pages to also (re)write /partners and /partners-register

PAGE_LOGIN = '''<!-- wp:group {"className":"wrap partner-page","layout":{"type":"default"}} -->
<div class="wp-block-group wrap partner-page"><!-- wp:paragraph {"className":"eyebrow"} -->
<p class="eyebrow">Wholesale &amp; distribution</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":1,"className":"pp-title"} -->
<h1 class="wp-block-heading pp-title">For record shops &amp; distributors</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"className":"pp-lead"} -->
<p class="pp-lead">Record shops order from 50 copies, distributors from 100. Log in to see wholesale prices.</p>
<!-- /wp:paragraph -->

<!-- wp:group {"className":"pp-login pp-boxed","layout":{"type":"default"}} -->
<div class="wp-block-group pp-login pp-boxed"><!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Partner login</h2>
<!-- /wp:heading -->

<!-- wp:shortcode -->
[i7_partner_login]
<!-- /wp:shortcode --></div>
<!-- /wp:group -->

<!-- wp:paragraph {"className":"pp-note pp-register-link"} -->
<p class="pp-note pp-register-link">New partner? <a href="/partners-register/">Register new account</a></p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->'''

PAGE_REGISTER = '''<!-- wp:group {"className":"wrap partner-page","layout":{"type":"default"}} -->
<div class="wp-block-group wrap partner-page"><!-- wp:paragraph {"className":"eyebrow"} -->
<p class="eyebrow">Wholesale &amp; distribution</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":1,"className":"pp-title"} -->
<h1 class="wp-block-heading pp-title">Register a partner account</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"className":"pp-lead"} -->
<p class="pp-lead">Fill in the form below. We review every application and activate your account within 48 hours.</p>
<!-- /wp:paragraph -->

<!-- wp:group {"className":"pp-apply pp-boxed","layout":{"type":"default"}} -->
<div class="wp-block-group pp-apply pp-boxed"><!-- wp:shortcode -->
[contact-form-7 id="%ID%" html_class="pf-form"]
<!-- /wp:shortcode --></div>
<!-- /wp:group -->

<!-- wp:paragraph {"className":"pp-note pp-register-link"} -->
<p class="pp-note pp-register-link">Already have an account? <a href="/partners/">Log in</a></p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->'''

UPSERT = """
$c = str_replace('%ID%', (int) get_option('_7inch_partner_form'), base64_decode('@@B64@@'));
$ex = get_page_by_path('@@SLUG@@')@@OLD@@;
$arr = ['post_title'=>'@@TITLE@@','post_name'=>'@@SLUG@@','post_content'=>wp_slash($c),'post_status'=>'publish','post_type'=>'page'];
if ($ex) { $arr['ID'] = $ex->ID; $pid = wp_update_post($arr, true); } else { $pid = wp_insert_post($arr, true); }
$out[] = is_wp_error($pid) ? $pid->get_error_message() : ['page'=>$pid, 'url'=>get_permalink($pid)];
"""

def upsert(old, slug, title, content):
    return (UPSERT.replace('@@B64@@', B(content)).replace('@@SLUG@@', slug).replace('@@TITLE@@', title)
            .replace('@@OLD@@', (" ?: get_page_by_path('%s')" % old) if old else ''))

print(deploy.php("$out=[];" + upsert('for-partners', 'partners', 'For partners', PAGE_LOGIN)
                 + upsert(None, 'partners-register', 'Register a partner account', PAGE_REGISTER) + "return $out;"))
