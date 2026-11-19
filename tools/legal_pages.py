#!/usr/bin/env python3
"""Create/update the legal pages from "7inchrare.com – Legal texts (EN)" (Nov 17, 2026) and wire them into
WooCommerce (terms, privacy). Idempotent. Internal notes of the source PDF (draft remark, shop notes) are not published.
Open placeholders in [square brackets] are kept as in the source: delivery times, log retention."""
import base64, html, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); import deploy

CONTACT = "Vibetown Entertainment (7inch.rare), owner Philipp Mühlen, Harkortstr. 29, 48163 Münster, Germany"
RETURNS = "Philipp Mühlen, Birkenweg 16 B, 48155 Münster, Germany"

PAGES = {}

PAGES["legal-notice"] = ("Legal Notice", """
## Information pursuant to § 5 DDG (German Digital Services Act)

Vibetown Entertainment (7inch.rare)
Owner: Philipp Mühlen
Harkortstr. 29, 48163 Münster, Germany

## Contact

Phone: +49 174 322 63 09
Email: philo@7inchrare.com

## VAT identification number

Pursuant to § 27a UStG: DE207201101

## Return address (returns only)

Philipp Mühlen, Birkenweg 16 B, 48155 Münster, Germany

## Responsible for content

Pursuant to § 18 (2) MStV: Philipp Mühlen, address as above.

## Consumer dispute resolution

We are neither willing nor obliged to participate in dispute resolution proceedings before a consumer arbitration board.

## German Packaging Register LUCID

Registration number DE2543281617810
""")

PAGES["terms"] = ("General Terms and Conditions", """
## § 1 Scope

(1) These terms apply to all orders placed by consumers via the online shop 7inchrare.com with Vibetown Entertainment (7inch.rare), owner Philipp Mühlen, Harkortstr. 29, 48163 Münster, Germany ("we").

(2) A consumer is any natural person who enters into a legal transaction for purposes that are predominantly outside their trade, business or profession (§ 13 BGB).

(3) Orders from retailers (shops and distributors) are governed exclusively by our Trade Terms.

## § 2 Conclusion of contract

(1) The presentation of products in the shop is not a legally binding offer but an invitation to order.

(2) By clicking "Order and pay" you submit a binding offer to purchase the goods in your basket. You can check and correct your details at any time before submitting.

(3) We confirm receipt of your order by email without delay. The contract is concluded with this order confirmation; for payment by PayPal, credit card, Apple Pay or Google Pay, it is concluded on completion of the payment.

(4) The contract languages are German and English. We store the contract text and send you the order details and these terms by email.

## § 3 Prices and shipping costs

(1) All prices are final prices in euros and include statutory VAT.

(2) Shipping costs including packaging are added depending on the destination country; they are shown on the "Shipping and payment" page and in the basket before you order.

(3) For deliveries to countries outside the EU, customs duties, import taxes and carrier fees may apply. These are borne by the recipient. Exception: deliveries to the United Kingdom with a value of up to GBP 135, where UK VAT is already included in the final price.

## § 4 Payment

(1) We offer the following payment methods: credit card, Apple Pay, Google Pay, PayPal and SEPA bank transfer. Payments are processed by the payment service provider Mollie. For SEPA bank transfer, you receive the payment details at checkout; we ship once payment has been received.

(2) We do not charge a surcharge for any payment method.

(3) The purchase price is due immediately on conclusion of the contract, including for pre-orders.

## § 5 Delivery and delivery times

(1) We deliver to the countries offered at checkout.

(2) Items in stock are shipped within 3 days of receipt of payment; delivery takes the time stated for each country on the "Shipping and payment" page.

(3) The delivery time is stated on the product page.

## § 6 Pre-orders

(1) Items not yet released are marked as "Pre-order". On the product page and at checkout we state the expected release month and the date by which we will ship at the latest ("Ships by").

(2) Vinyl production can be delayed. We ship pre-orders as soon as the goods arrive with us, at the latest by the date stated.

(3) If the stated date is exceeded, we will inform you by email. You may then withdraw from the contract; we will refund the purchase price without delay. Your statutory rights remain unaffected.

(4) If an order contains both in-stock and pre-order items, we ship the entire order together unless you select partial shipment at checkout.

## § 7 Limited editions

Our releases are produced in limited quantities. If an item is no longer available despite your order, we will inform you without delay and refund any payment already made.

## § 8 Retention of title

The goods remain our property until paid in full.

## § 9 Right of withdrawal

Consumers have a right of withdrawal as set out in the <a href="/withdrawal-policy/">withdrawal policy</a>. Please send returns only to: Philipp Mühlen, Birkenweg 16 B, 48155 Münster, Germany.

## § 10 Warranty and transport damage

(1) The statutory warranty rights apply. We are liable only for defects that already exist at the time of delivery, in particular manufacturing defects (pressing faults, cracks, warping, wrong label, wrong pressing) and transport damage. Wear from playing (e.g. crackle, scratches, groove wear) and damage caused after delivery by improper handling, storage or unsuitable playback equipment are not defects.

(2) Please check the record on receipt and report any faults, if possible within 14 days, to philo@7inchrare.com with your order number, a short description and photos; your statutory rights do not depend on this period. We replace a defective record or refund the purchase price if no replacement is available, and we bear the cost of the return. Please send returns only to: Philipp Mühlen, Birkenweg 16 B, 48155 Münster, Germany.

(3) Please report obvious transport damage to the carrier and to us as soon as possible.

## § 11 Liability

We are liable without limitation for intent and gross negligence, for injury to life, body or health, and under the German Product Liability Act. In the event of slightly negligent breach of essential contractual obligations, liability is limited to the foreseeable damage typical for the contract. Otherwise, liability is excluded.

## § 12 Final provisions

(1) The law of the Federal Republic of Germany applies, excluding the UN Convention on Contracts for the International Sale of Goods. For consumers, this choice of law applies only insofar as it does not deprive them of the protection of mandatory consumer protection provisions of the country in which they have their habitual residence.

(2) If any provision is invalid, the remainder of the contract remains valid.
""")

PAGES["withdrawal-policy"] = ("Withdrawal Policy", """
Based on the statutory model (Annex 1 to Art. 246a § 1 (2) EGBGB), adapted for 7inch.rare.

## Right of withdrawal

You have the right to withdraw from this contract within fourteen days without giving any reason.

The withdrawal period is fourteen days from the day on which you, or a third party other than the carrier indicated by you, acquire physical possession of the goods. If you ordered several goods in one order and they are delivered separately, the period starts on the day on which you, or a third party other than the carrier indicated by you, acquire physical possession of the last item.

To exercise your right of withdrawal, you must inform us (Vibetown Entertainment (7inch.rare), owner Philipp Mühlen, Harkortstr. 29, 48163 Münster, Germany, phone +49 174 322 63 09, email philo@7inchrare.com) of your decision to withdraw from this contract by an unequivocal statement (e.g. a letter sent by post or an email). You may use the attached model withdrawal form, but it is not obligatory.

To meet the withdrawal deadline, it is sufficient for you to send your communication concerning your exercise of the right of withdrawal before the withdrawal period has expired.

## Effects of withdrawal

If you withdraw from this contract, we shall reimburse to you all payments received from you, including the costs of delivery (with the exception of the supplementary costs resulting from your choice of a type of delivery other than the least expensive standard delivery offered by us), without undue delay and in any event not later than fourteen days from the day on which we are informed about your decision to withdraw from this contract. We will carry out such reimbursement using the same means of payment as you used for the initial transaction, unless you have expressly agreed otherwise; in any event, you will not incur any fees as a result of such reimbursement.

We may withhold reimbursement until we have received the goods back or you have supplied evidence of having sent back the goods, whichever is the earliest.

You shall send back the goods or hand them over to Philipp Mühlen, Birkenweg 16 B, 48155 Münster, Germany without undue delay and in any event not later than fourteen days from the day on which you communicate your withdrawal from this contract to us. The deadline is met if you send back the goods before the period of fourteen days has expired.

You will bear the direct cost of returning the goods.

You are only liable for any diminished value of the goods resulting from handling other than what is necessary to establish the nature, characteristics and functioning of the goods.

## Exclusion of the right of withdrawal

There is no right of withdrawal for the supply of sealed audio or video recordings if the seal has been removed after delivery (§ 312g (2) no. 6 BGB). Records in the LOWRIDER ANTHEMS series are delivered shrink-wrapped; this shrink-wrap is such a seal. You may withdraw from the purchase of unopened records within 14 days; once the shrink-wrap has been opened, the right of withdrawal no longer applies. Your warranty rights for a defective record remain unaffected (see Terms § 10).

Records in the MY PHILOSOPHY series are delivered without shrink-wrap; the right of withdrawal applies to them without this restriction.

## Model withdrawal form

(Complete and return this form only if you wish to withdraw from the contract.)

- To: Vibetown Entertainment (7inch.rare), owner Philipp Mühlen, Harkortstr. 29, 48163 Münster, Germany, email philo@7inchrare.com
- I/We (*) hereby give notice that I/We (*) withdraw from my/our (*) contract of sale of the following goods (*):
- Ordered on (*) / received on (*):
- Name of consumer(s):
- Address of consumer(s):
- Signature of consumer(s) (only if this form is notified on paper):
- Date:

(*) Delete as appropriate.
""")

PAGES["trade-terms"] = ("Trade Terms (Shops and Distributors)", """
## § 1 Scope

These terms apply to all orders from businesses within the meaning of § 14 BGB (record stores, online retailers, distributors) placed via the trade area of 7inchrare.com, by email or by pro-forma invoice. Deviating terms of the retailer apply only if we agree to them in writing. There is no right of withdrawal.

## § 2 Trade account

Access to the trade area requires an application and our approval. We verify business status on the basis of a business or tax registration document, a website or a physical store. Providing a VAT ID is optional. Without a valid VAT ID, deliveries within the EU are invoiced with German VAT (19%); with a valid VAT ID from another EU member state, they are tax-exempt under the reverse charge procedure. We may reject applications without giving reasons. Login details must be kept confidential.

## § 3 Order and conclusion of contract

An order in the trade area is a binding offer. The contract is concluded with our order confirmation or pro-forma invoice. The minimum order quantity is 50 records per order; titles can be combined freely. We reserve ordered quantities for up to 7 days pending receipt of payment; after that we may cancel the reservation.

## § 4 Prices and quantity tiers

The prices shown in the trade area for the respective country apply. They depend on the total quantity of the order (50–99, 100–249, 250+ units). Prices are net plus statutory VAT where applicable. Deliveries to businesses in other EU member states with a valid VAT ID are tax-exempt (reverse charge); without a VAT ID, 19% German VAT applies. Export deliveries to non-EU countries are tax-exempt. Where "carriage paid" is stated, shipping costs are included.

## § 5 Payment

We deliver against prepayment. Up to 249 units, payment can be made online (credit card, PayPal) or by bank transfer; from 250 units, by bank transfer only. Invoices are in euros. Goods are shipped only once the full amount has been received in our account. Bank and transfer fees are borne by the retailer.

## § 6 Delivery, transfer of risk, customs

Unless otherwise agreed, deliveries are made DAP (Incoterms 2020) to the delivery address given. Risk passes to the retailer when the goods are handed over to the carrier. Import duties, customs and import VAT in the destination country are borne by the retailer. Delivery dates stated for pre-orders are estimates; production delays do not give rise to claims for damages.

## § 7 Pre-orders

Pre-orders placed before pressing are binding and are taken into account when planning the edition. Payment is due with the pro-forma invoice unless otherwise agreed.

## § 8 Inspection and notice of defects

The retailer shall inspect the goods immediately on receipt (§ 377 HGB). Obvious defects and transport damage must be reported in writing with photos within 7 days of receipt. For justified defects, we will, at our option, supply a replacement or issue a credit. The warranty period is 12 months. Returns only by prior arrangement to: Philipp Mühlen, Birkenweg 16 B, 48155 Münster, Germany.

## § 9 Exclusivity

Territorial exclusivity is granted only to distributors and only by separate written agreement (minimum purchase, term, prices).

## § 10 Resale, images and texts

The retailer may use the covers, labels, press photos, audio samples and texts provided solely to promote and sell our goods. Resale to consumers below our retail price is permitted; there is no resale price maintenance.

## § 11 Retention of title

The goods remain our property until paid in full.

## § 12 Liability

We are liable without limitation for intent, gross negligence and injury to life, body or health. In the case of slight negligence, we are liable only for breach of essential contractual obligations and limited to the foreseeable damage typical for the contract; loss of profit is excluded.

## § 13 Governing law and jurisdiction

German law applies, excluding the UN Convention on Contracts for the International Sale of Goods (CISG). Place of jurisdiction for merchants is Münster. The contract language is German; this English translation is for information only.
""")

PAGES["privacy-policy"] = ("Privacy Policy", """
## 1. Controller

Vibetown Entertainment (7inch.rare), owner Philipp Mühlen, Harkortstr. 29, 48163 Münster, Germany, email philo@7inchrare.com, phone +49 174 322 63 09. No data protection officer has been appointed, as there is no legal obligation to do so.

## 2. Hosting and server log files

The website is hosted by ALL-INKL.COM – Neue Medien Münnich, Hauptstraße 68, 02742 Friedersdorf, Germany, on servers in Germany. When you visit the site, technically necessary data is processed (IP address, date and time, page accessed, browser, operating system, referrer). The legal basis is Art. 6 (1) (f) GDPR (secure operation). A data processing agreement is in place with ALL-INKL. Log files are deleted after [7] days. The connection is encrypted via SSL/TLS.

## 3. Orders and customer account

For orders, we process your name, address, email, phone number (optional), order and payment data to perform the contract (Art. 6 (1) (b) GDPR). A customer account is optional; guest orders are possible. For trade accounts, we additionally process company details, VAT ID and sales territory for verification and approval. Invoice data is retained for 8 to 10 years due to commercial and tax law obligations (Art. 6 (1) (c) GDPR).

## 4. Payment service providers

Depending on the payment method chosen, we pass the data required for payment to:

- Mollie B.V., Keizersgracht 126, 1015 CW Amsterdam, Netherlands (credit card, Apple Pay, Google Pay, SEPA bank transfer and processing of PayPal payments). Mollie processes the data within the EU.
- PayPal (Europe) S.à r.l. et Cie, S.C.A., 22–24 Boulevard Royal, 2449 Luxembourg.

The legal basis is Art. 6 (1) (b) GDPR. The privacy notices of the respective provider also apply.

## 5. Shipping

For delivery, we pass your name and delivery address to the shipping provider, currently Deutsche Post AG / DHL Paket GmbH, Charles-de-Gaulle-Straße 20, 53113 Bonn, Germany (Art. 6 (1) (b) GDPR). We pass on your email address or phone number for delivery notifications only with your consent (Art. 6 (1) (a) GDPR). For shipments outside the EU, the data required for customs clearance is transmitted to the customs authorities of the destination country.

## 6. Contact by email or form

If you contact us, we process your details to handle your enquiry (Art. 6 (1) (b) or (f) GDPR) and delete them when they are no longer needed and no retention obligations apply.

## 7. Cookies and local storage

We use only technically necessary cookies and local storage (§ 25 (2) TDDDG, Art. 6 (1) (f) GDPR). We do not use analytics, advertising or tracking cookies, and fonts are loaded locally from our server, not from Google. Because only necessary cookies are used, no cookie consent banner is required. You can block or delete cookies in your browser settings; the basket, login and checkout may then no longer work.

The following cookies and storage entries are set by the shop:

| Name | Purpose | Duration |
| woocommerce_cart_hash, woocommerce_items_in_cart | Detect changes to the basket so that it is displayed correctly | Session |
| wp_woocommerce_session_* | Stores your basket and checkout data (also for guests) | 2 days |
| woocommerce_recently_viewed | Remembers recently viewed products | Session |
| wordpress_logged_in_*, wordpress_sec_*, wordpress_test_cookie | Login to your customer account and check that cookies are enabled | Session, up to 14 days with "Remember me" |
| wp-settings-*, wp-settings-time-* | Stores interface settings for logged-in users | 1 year |
| pll_language | Stores the selected language | 1 year |
| theme (local storage) | Stores your light/dark mode choice; stays in your browser and is not sent to us | Until deleted |

Payment is made on the page of the payment provider (see section 4), which may set its own cookies there.

## 8. Links to social networks

Our site links to our Instagram profile @7inch.rare. These are simple links; data is only transmitted when you click the link and visit Instagram (Meta Platforms Ireland Ltd.).

## 9. Your rights

You have the right of access, rectification, erasure, restriction of processing, data portability and the right to object to processing based on Art. 6 (1) (f) GDPR. You may withdraw any consent given at any time with effect for the future. You may lodge a complaint with a data protection supervisory authority; the authority responsible for us is the State Commissioner for Data Protection and Freedom of Information of North Rhine-Westphalia (LDI NRW), Düsseldorf.

## 10. Last updated

November 2026
""")

PAGES["shipping-and-payment"] = ("Shipping and Payment", """
Shipping costs including packaging, per order. Items in stock ship within 3 days of receipt of payment; pre-orders by the date stated on the product page.

For 11 or more records or other countries: shipping costs on request. No shipping to Russia.

| Destination | 1–3 records | 4–10 records | Delivery within |
| Germany | €3.90 | €6.90 | up to [4] days |
| EU | €8.90 | €16.90 | up to [10] days |
| United Kingdom, Switzerland | €10.90 | €21.90 | up to [12] days |
| USA, Canada, Mexico, Brazil | €17.90 | €28.90 | up to [21] days |
| Japan, Asia | €16.90 | €27.90 | up to [21] days |
| Australia, New Zealand | €18.90 | €29.90 | up to [28] days |

## Payment methods

Credit card, Apple Pay, Google Pay, PayPal, SEPA bank transfer (processed by Mollie). No surcharges.

## Customs and taxes

For deliveries outside the EU, import duties and carrier fees may apply and are borne by the recipient. United Kingdom up to GBP 135: UK VAT is already included in the price.

## Returns

Returns only to: Philipp Mühlen, Birkenweg 16 B, 48155 Münster, Germany.
""")

# ── conversion to Gutenberg blocks ──────────────────────────────────
MAIL = re.compile(r"([\w.+-]+@7inchrare\.com)")
def inline(t):
    if "<a " in t: return t  # trusted inline link written above
    t = html.escape(t, quote=False)
    return MAIL.sub(r'<a href="mailto:\1">\1</a>', t)

def blocks(src):
    out = []
    for chunk in re.split(r"\n\s*\n", src.strip()):
        lines = [l for l in chunk.split("\n") if l.strip()]
        if lines[0].startswith("## "):
            out.append(f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{html.escape(lines[0][3:], quote=False)}</h2>\n<!-- /wp:heading -->')
            lines = lines[1:]
            if not lines: continue
        if lines[0].startswith("- "):
            items = "".join(f"<!-- wp:list-item -->\n<li>{inline(l[2:])}</li>\n<!-- /wp:list-item -->\n" for l in lines)
            out.append(f'<!-- wp:list -->\n<ul class="wp-block-list">{items}</ul>\n<!-- /wp:list -->')
        elif lines[0].startswith("|"):
            rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
            head = "".join(f"<th>{html.escape(c, quote=False)}</th>" for c in rows[0])
            body = "".join("<tr>" + "".join(f"<td>{html.escape(c, quote=False)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<!-- wp:table {{"className":"legal-table"}} -->\n<figure class="wp-block-table legal-table"><table class="has-fixed-layout"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></figure>\n<!-- /wp:table -->')
        else:
            out.append(f'<!-- wp:paragraph -->\n<p>{"<br>".join(inline(l) for l in lines)}</p>\n<!-- /wp:paragraph -->')
    return "\n\n".join(out)

def page_html(title, src):
    return f'''<!-- wp:group {{"className":"wrap partner-page about-page legal-page","layout":{{"type":"default"}}}} -->
<div class="wp-block-group wrap partner-page about-page legal-page"><!-- wp:paragraph {{"className":"eyebrow"}} -->
<p class="eyebrow">Legal</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":1,"className":"pp-title"}} -->
<h1 class="wp-block-heading pp-title">{html.escape(title, quote=False)}</h1>
<!-- /wp:heading -->

{blocks(src)}</div>
<!-- /wp:group -->'''

payload = {slug: [title, page_html(title, src)] for slug, (title, src) in PAGES.items()}
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "content", "legal"), exist_ok=True)
for slug, (title, content) in payload.items():
    open(os.path.join(os.path.dirname(__file__), "..", "content", "legal", slug + ".html"), "w", encoding="utf-8").write(content)

import json
b = base64.b64encode(json.dumps(payload).encode()).decode()
print(deploy.php(f"""
$pages = json_decode(base64_decode('{b}'), true); $out = [];
foreach ($pages as $slug => [$title, $content]) {{
  $ex = get_page_by_path($slug, OBJECT, 'page');
  $a = ['post_title'=>$title,'post_name'=>$slug,'post_content'=>wp_slash($content),'post_status'=>'publish','post_type'=>'page'];
  if ($ex) {{ $a['ID'] = $ex->ID; $id = wp_update_post($a, true); }} else {{ $id = wp_insert_post($a, true); }}
  if (is_wp_error($id)) {{ $out[$slug] = $id->get_error_message(); continue; }}
  if (function_exists('pll_set_post_language')) pll_set_post_language($id, 'en');
  $out[$slug] = [$id, get_permalink($id)];
}}
update_option('wp_page_for_privacy_policy', $out['privacy-policy'][0]);
update_option('woocommerce_terms_page_id', $out['terms'][0]);
return $out;
"""))
