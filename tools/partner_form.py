#!/usr/bin/env python3
"""Install/activate Contact Form 7 on 7inchrare.com and (re)create the partner application form.
usage: partner_form.py   (idempotent; stores the form id in option _7inch_partner_form)"""
import base64, os, sys
sys.path.insert(0, os.path.dirname(__file__)); import deploy

COUNTRIES = ["Germany", "France", "Spain", "Italy", "Netherlands", "Belgium", "Austria", "Poland", "United Kingdom",
             "United States", "Mexico", "Canada", "Japan", "Australia", "New Zealand", "Brazil", "Other country"]
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


<div class="pf-dist" hidden>
<div><label>Distribution area (country / countries)[text area]</label></div>
<div><label>Number of shops you supply[number shops min:0]</label></div>
</div>

<div class="pf-check">[acceptance consent] I accept the <a href="/trade-terms/" target="_blank" rel="noopener">Trade Terms</a> and the <a href="/privacy-policy/" target="_blank" rel="noopener">Privacy Policy</a>, and agree that 7inch.rare may process my details to handle this application. [/acceptance]</div>
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


Distributor only
Distribution area: [area]
Shops supplied: [shops]

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
  'sender'  => '[_site_title] <wordpress@7inchrare.com>',
  'recipient' => 'peet@7inchrare.com',
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

PAGE = '''<!-- wp:group {"className":"wrap partner-page pp-wide","layout":{"type":"default"}} -->
<div class="wp-block-group wrap partner-page pp-wide"><!-- wp:paragraph {"className":"eyebrow"} -->
<p class="eyebrow">Wholesale &amp; distribution</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":1,"className":"pp-title"} -->
<h1 class="wp-block-heading pp-title">For record shops &amp; distributors</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"className":"pp-lead"} -->
<p class="pp-lead">Record shops order from 50 copies, distributors from 100. Log in to see wholesale prices, or apply for a partner account.</p>
<!-- /wp:paragraph -->

<!-- wp:group {"className":"pp-grid","layout":{"type":"default"}} -->
<div class="wp-block-group pp-grid"><!-- wp:group {"className":"pp-login","layout":{"type":"default"}} -->
<div class="wp-block-group pp-login"><!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Partner login</h2>
<!-- /wp:heading -->

<!-- wp:shortcode -->
[i7_partner_login]
<!-- /wp:shortcode --></div>
<!-- /wp:group -->

<!-- wp:group {"className":"pp-apply","layout":{"type":"default"}} -->
<div class="wp-block-group pp-apply"><!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">New partner? Register</h2>
<!-- /wp:heading -->

<!-- wp:paragraph {"className":"pp-note"} -->
<p class="pp-note">Fill in the form below. We review every application and activate your account within 48 hours.</p>
<!-- /wp:paragraph -->

<!-- wp:shortcode -->
[contact-form-7 id="%ID%" html_class="pf-form"]
<!-- /wp:shortcode --></div>
<!-- /wp:group --></div>
<!-- /wp:group --></div>
<!-- /wp:group -->'''
print(deploy.php(f"""
$id = (int) get_option('_7inch_partner_form');
$c = str_replace('%ID%', $id, base64_decode('{B(PAGE)}'));
$ex = get_page_by_path('for-partners');
$arr = ['post_title'=>'For partners','post_name'=>'for-partners','post_content'=>wp_slash($c),'post_status'=>'publish','post_type'=>'page'];
if ($ex) {{ $arr['ID'] = $ex->ID; $pid = wp_update_post($arr, true); }} else {{ $pid = wp_insert_post($arr, true); }}
return is_wp_error($pid) ? $pid->get_error_message() : ['page'=>$pid, 'url'=>get_permalink($pid)];
"""))
