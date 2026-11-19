#!/usr/bin/env python3
"""Create/update the Contact Form 7 "Contact" form and the /contact/ page (idempotent).
The form mails to shop@7inchrare.com; its id is stored in option _7inch_contact_form."""
import base64, os, sys
sys.path.insert(0, os.path.dirname(__file__)); import deploy
B = lambda t: base64.b64encode(t.encode()).decode()

FORM = """<div class="pf">
<div><label>Your name *[text* your-name autocomplete:name]</label></div>
<div><label>E-mail *[email* your-email autocomplete:email]</label></div>
<div><label>Topic[select topic "Order question" "Shipping" "Returns and warranty" "Wholesale / distribution" "Other"]</label></div>
<div><label>Order number (optional)[text order autocomplete:off]</label></div>
<div class="pf-wide"><label>Message *[textarea* your-message 6x4]</label></div>
<div class="pf-check">[acceptance consent] I agree that 7inch.rare may process my details to answer my enquiry, as described in the <a href="/privacy-policy/" target="_blank" rel="noopener">Privacy Policy</a>. [/acceptance]</div>
<div class="pf-submit">[submit "Send message"]</div>
</div>"""

MAIL = """Message from the Contact form

Name: [your-name]
E-mail: [your-email]
Topic: [topic]
Order number: [order]

[your-message]

--
Sent from the Contact form on [_site_url]"""

PAGE = """<!-- wp:group {"className":"wrap partner-page pp-wide","layout":{"type":"default"}} -->
<div class="wp-block-group wrap partner-page pp-wide"><!-- wp:paragraph {"className":"eyebrow"} -->
<p class="eyebrow">Contact</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":1,"className":"pp-title"} -->
<h1 class="wp-block-heading pp-title">Get in touch</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"className":"pp-lead"} -->
<p class="pp-lead">Questions about an order, shipping or a release? Write to us and we will get back to you as soon as we can.</p>
<!-- /wp:paragraph -->

<!-- wp:group {"className":"pp-grid","layout":{"type":"default"}} -->
<div class="wp-block-group pp-grid"><!-- wp:group {"className":"pp-login pp-contact","layout":{"type":"default"}} -->
<div class="wp-block-group pp-login pp-contact"><!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">7inch.rare</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Vibetown Entertainment<br>Harkortstr. 29<br>48163 Münster, Germany</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>EU VAT number:<br>DE207201101</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Bank account:<br>IBAN DE20 4005 0150 0000 0725 46<br>BIC WELADED1MST</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Shop &amp; orders:<br><a href="mailto:shop@7inchrare.com">shop@7inchrare.com</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Instagram:<br><a href="https://instagram.com/7inch.rare">@7inch.rare</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"className":"pp-note"} -->
<p class="pp-note">Returns only to: 7inch.rare, Birkenweg 16 B, 48155 Münster, Germany. Faulty record? Please send your order number, a short description and photos. See our <a href="/terms/">terms</a>.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->

<!-- wp:group {"className":"pp-apply pp-boxed","layout":{"type":"default"}} -->
<div class="wp-block-group pp-apply pp-boxed"><!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">Send a message</h2>
<!-- /wp:heading -->

<!-- wp:shortcode -->
[contact-form-7 id="%ID%" html_class="pf-form"]
<!-- /wp:shortcode --></div>
<!-- /wp:group --></div>
<!-- /wp:group --></div>
<!-- /wp:group -->"""

code = f"""
$cf = null; $id = (int) get_option('_7inch_contact_form');
if ($id) $cf = WPCF7_ContactForm::get_instance($id);
if (!$cf) $cf = WPCF7_ContactForm::get_template(['title'=>'Contact', 'locale'=>'en_US']);
$cf->set_title('Contact');
$props = $cf->get_properties();
$props['form'] = base64_decode('{B(FORM)}');
$props['mail'] = array_merge($props['mail'], [
  'subject' => 'Contact: [topic] – [your-name]',
  'sender'  => '7inch.rare <shop@7inchrare.com>',
  'recipient' => 'shop@7inchrare.com',
  'additional_headers' => 'Reply-To: [your-email]',
  'body' => base64_decode('{B(MAIL)}'),
  'use_html' => 0, 'exclude_blank' => 0,
]);
$props['messages'] = array_merge($props['messages'], [
  'mail_sent_ok' => "Thank you. We have received your message and will get back to you soon.",
  'validation_error' => 'Please check the highlighted fields and try again.',
  'accept_terms' => 'Please confirm that we may process your details.',
]);
$cf->set_properties($props);
$fid = $cf->save();
update_option('_7inch_contact_form', $fid);
$c = str_replace('%ID%', $fid, base64_decode('{B(PAGE)}'));
$ex = get_page_by_path('contact', OBJECT, 'page');
$a = ['post_title'=>'Contact','post_name'=>'contact','post_content'=>wp_slash($c),'post_status'=>'publish','post_type'=>'page'];
if ($ex) {{ $a['ID'] = $ex->ID; $pid = wp_update_post($a, true); }} else {{ $pid = wp_insert_post($a, true); }}
if (is_wp_error($pid)) return $pid->get_error_message();
if (function_exists('pll_set_post_language')) pll_set_post_language($pid, 'en');
return ['form'=>$fid, 'page'=>$pid, 'url'=>get_permalink($pid)];
"""
print(deploy.php(code))
