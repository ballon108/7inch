#!/usr/bin/env python3
"""German page content for 7inch.rare (Polylang "de").

Builds content/de/<slug>.html from the live English pages (dumped as JSON by the deploy step) by replacing text nodes
with German. Proper names are NOT translated: product / series names, track titles, company, person, street and brand
names (7inch.rare, Vibetown Entertainment, My Philosophy, Lowrider Anthems ...).

Usage: de_content.py <dump_dir> <out_dir>   (dump_dir has pNN.json = {slug,title,content})
Prints unmatched keys and the text nodes left untranslated, so nothing is missed silently.
"""
import json, re, sys, os

# --- link rewriting (English root-relative → German) -------------------------------------------
LINKS = {
    '/#releases': '/de/#releases', '/for-partners/': '/de/partner/', '/partners-register/': '/de/partner-registrierung/',
    '/partners/': '/de/partner/', '/terms/': '/de/agb/', '/withdrawal-policy/': '/de/widerrufsbelehrung/',
    '/my-account/': '/de/mein-konto/', '/trade-terms/': '/de/haendler-agb/', '/privacy-policy/': '/de/datenschutz/',
    '/shipping-and-payment/': '/de/versand-und-zahlung/', '/legal-notice/': '/de/impressum/', '/about/': '/de/ueber-uns/',
    '/contact/': '/de/kontakt/', '/register/': '/de/registrierung/',
}

RN = 'Philipp Mühlen, Birkenweg 16 B, 48155 Münster, Germany'
RN_DE = 'Philipp Mühlen, Birkenweg 16 B, 48155 Münster, Deutschland'
LEGAL = {'Legal': 'Rechtliches'}

PAGES = {
 # id: (german slug, german title, {text: german})
 93: ('ueber-uns', 'Über uns', {
    'About': 'Über uns',
    'A crate under a single light.': 'Eine Kiste unter einem einzigen Licht.',
    '7inch.rare releases limited 7" records in two series. Every title is a small, numbered run: when it is gone, it is gone.':
        '7inch.rare veröffentlicht limitierte 7"-Schallplatten in zwei Serien. Jeder Titel ist eine kleine, nummerierte Auflage: Ist sie weg, ist sie weg.',
    '90s Hip Hop &amp; R&amp;B, one episode at a time. Each record pairs two songs that belong together: well-known classics and cuts only diggers carry in their record bag, re-edited and pressed on 7" with its own label colour.':
        '90er Hip Hop &amp; R&amp;B, Episode für Episode. Jede Platte kombiniert zwei Songs, die zusammengehören: bekannte Klassiker und Cuts, die nur Digger in der Plattentasche haben, neu editiert und auf 7" gepresst, jeweils mit eigener Labelfarbe.',
    'West Coast and G-Funk only, re-edited for the boulevard and released in full-colour picture sleeves. The soundtrack of chrome, hydraulics and slow rides down palm-lined streets.':
        'Nur West Coast und G-Funk, neu editiert für den Boulevard und veröffentlicht in vollfarbigen Picture-Sleeves. Der Soundtrack für Chrom, Hydraulik und langsame Fahrten durch palmengesäumte Straßen.',
    'How it works': 'So funktioniert’s',
    'Small editions, stock shown live. First come, first served.': 'Kleine Auflagen, der Bestand wird live angezeigt. Wer zuerst kommt, mahlt zuerst.',
    'Pre-orders are shipped together as soon as the run arrives.': 'Vorbestellungen werden gemeinsam versandt, sobald die Auflage eintrifft.',
    'We ship worldwide from Germany.': 'Wir versenden weltweit ab Deutschland.',
    'Record shops and distributors can order wholesale from a partner account.': 'Plattenläden und Vertriebe können mit einem Partnerkonto im Großhandel bestellen.',
    'Browse releases': 'Releases ansehen', 'For partners': 'Für Partner', 'Questions?': 'Fragen?',
 }),
 89: ('partner', 'Für Partner', {
    'Wholesale &amp; distribution': 'Großhandel &amp; Vertrieb',
    'For record shops &amp; distributors': 'Für Plattenläden &amp; Vertriebe',
    'Record shops order from 50 copies, distributors from 100. Log in to see wholesale prices.':
        'Plattenläden bestellen ab 50 Exemplaren, Vertriebe ab 100. Melden Sie sich an, um die Großhandelspreise zu sehen.',
    'Partner login': 'Partner-Login', 'New partner?': 'Neuer Partner?', 'Register new account': 'Neues Konto registrieren',
 }),
 102: ('kontakt', 'Kontakt', {
    'Contact': 'Kontakt', 'Get in touch': 'Schreiben Sie uns',
    'Questions about an order, shipping or a release? Write to us and we will get back to you as soon as we can.':
        'Fragen zu einer Bestellung, zum Versand oder zu einem Release? Schreiben Sie uns, wir melden uns so schnell wie möglich.',
    '48163 Münster, Germany': '48163 Münster, Deutschland',
    'EU VAT number:': 'USt-IdNr.:', 'Bank account:': 'Bankverbindung:', 'Shop &amp; orders:': 'Shop &amp; Bestellungen:',
    'Returns only to: 7inch.rare, Birkenweg 16 B, 48155 Münster, Germany. Faulty record? Please send your order number, a short description and photos. See our':
        'Rücksendungen nur an: 7inch.rare, Birkenweg 16 B, 48155 Münster, Deutschland. Fehlerhafte Platte? Bitte senden Sie uns Ihre Bestellnummer, eine kurze Beschreibung und Fotos. Siehe unsere',
    'terms': 'AGB', 'Send a message': 'Nachricht senden',
 }),
 147: ('partner-registrierung', 'Partnerkonto registrieren', {
    'Wholesale &amp; distribution': 'Großhandel &amp; Vertrieb',
    'Register a partner account': 'Partnerkonto registrieren',
    'Fill in the form below. We review every application and activate your account within 48 hours.':
        'Füllen Sie das Formular aus. Wir prüfen jede Anfrage und aktivieren Ihr Konto innerhalb von 48 Stunden.',
    'Already have an account?': 'Sie haben bereits ein Konto?', 'Log in': 'Anmelden',
 }),
 148: ('registrierung', 'Konto erstellen', {
    'Create account': 'Konto erstellen',
    'Create a customer account to track your orders and check out faster.':
        'Erstellen Sie ein Kundenkonto, um Ihre Bestellungen zu verfolgen und schneller zur Kasse zu gehen.',
    'Already have an account?': 'Sie haben bereits ein Konto?', 'Log in': 'Anmelden',
    '&middot; Record shop or distributor?': '&middot; Plattenladen oder Vertrieb?',
    'Apply for a partner account': 'Partnerkonto beantragen',
 }),
 95: ('impressum', 'Impressum', dict(LEGAL, **{
    'Legal Notice': 'Impressum',
    'Information pursuant to § 5 DDG (German Digital Services Act)': 'Angaben gemäß § 5 DDG (Digitale-Dienste-Gesetz)',
    'Owner: Philipp Mühlen': 'Inhaber: Philipp Mühlen',
    'Harkortstr. 29, 48163 Münster, Germany': 'Harkortstr. 29, 48163 Münster, Deutschland',
    'Contact': 'Kontakt', 'Phone: +49 174 322 63 09': 'Telefon: +49 174 322 63 09', 'Email:': 'E-Mail:',
    'VAT identification number': 'Umsatzsteuer-Identifikationsnummer', 'Pursuant to § 27a UStG: DE207201101': 'Gemäß § 27a UStG: DE207201101',
    'Return address (returns only)': 'Rücksendeadresse (nur Rücksendungen)', RN: RN_DE,
    'Responsible for content': 'Verantwortlich für den Inhalt',
    'Pursuant to § 18 (2) MStV: Philipp Mühlen, address as above.': 'Gemäß § 18 Abs. 2 MStV: Philipp Mühlen, Anschrift wie oben.',
    'Consumer dispute resolution': 'Verbraucherstreitbeilegung',
    'We are neither willing nor obliged to participate in dispute resolution proceedings before a consumer arbitration board.':
        'Wir sind weder bereit noch verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.',
    'German Packaging Register LUCID': 'Verpackungsregister LUCID', 'Registration number DE25432816178102': 'Registrierungsnummer DE25432816178102',
 })),
 100: ('versand-und-zahlung', 'Versand und Zahlung', dict(LEGAL, **{
    'Shipping and Payment': 'Versand und Zahlung',
    'Shipping costs including packaging, per order. Items in stock ship within 3 days of receipt of payment; pre-orders by the date stated on the product page.':
        'Versandkosten inklusive Verpackung, pro Bestellung. Lagernde Artikel werden innerhalb von 3 Tagen nach Zahlungseingang versandt; Vorbestellungen bis zu dem auf der Produktseite angegebenen Datum.',
    'For 11 or more records or other countries: shipping costs on request. No shipping to Russia.':
        'Bei 11 oder mehr Schallplatten oder anderen Ländern: Versandkosten auf Anfrage. Kein Versand nach Russland.',
    'Destination': 'Zielland', '1–3 records': '1–3 Schallplatten', '4–10 records': '4–10 Schallplatten', 'Delivery within': 'Lieferzeit',
    'Germany': 'Deutschland', 'United Kingdom, Switzerland': 'Vereinigtes Königreich, Schweiz', 'USA, Canada, Mexico, Brazil': 'USA, Kanada, Mexiko, Brasilien',
    'Japan, Asia': 'Japan, Asien', 'Australia, New Zealand': 'Australien, Neuseeland',
    '€3.90': '3,90 €', '€6.90': '6,90 €', '€8.90': '8,90 €', '€16.90': '16,90 €', '€10.90': '10,90 €', '€21.90': '21,90 €',
    '€17.90': '17,90 €', '€28.90': '28,90 €', '€27.90': '27,90 €', '€18.90': '18,90 €', '€29.90': '29,90 €',
    'up to [4] days': 'bis zu [4] Tage', 'up to [10] days': 'bis zu [10] Tage', 'up to [12] days': 'bis zu [12] Tage',
    'up to [21] days': 'bis zu [21] Tage', 'up to [28] days': 'bis zu [28] Tage',
    'Payment methods': 'Zahlungsarten',
    'Credit card, Apple Pay, Google Pay, PayPal, SEPA bank transfer (processed by Mollie). No surcharges.':
        'Kreditkarte, Apple Pay, Google Pay, PayPal, SEPA-Überweisung (abgewickelt über Mollie). Keine Aufpreise.',
    'Customs and taxes': 'Zoll und Steuern',
    'For deliveries outside the EU, import duties and carrier fees may apply and are borne by the recipient. United Kingdom up to GBP 135: UK VAT is already included in the price.':
        'Bei Lieferungen außerhalb der EU können Einfuhrzölle und Gebühren des Transportunternehmens anfallen; diese trägt der Empfänger. Vereinigtes Königreich bis 135 GBP: Die britische Umsatzsteuer ist bereits im Preis enthalten.',
    'Returns': 'Rücksendungen', 'Returns only to: ' + RN + '.': 'Rücksendungen nur an: ' + RN_DE + '.',
 })),
 97: ('widerrufsbelehrung', 'Widerrufsbelehrung', dict(LEGAL, **{
    'Withdrawal Policy': 'Widerrufsbelehrung',
    'Based on the statutory model (Annex 1 to Art. 246a § 1 (2) EGBGB), adapted for 7inch.rare.':
        'Auf Grundlage des gesetzlichen Musters (Anlage 1 zu Art. 246a § 1 Abs. 2 EGBGB), angepasst für 7inch.rare.',
    'Right of withdrawal': 'Widerrufsrecht',
    'You have the right to withdraw from this contract within fourteen days without giving any reason.':
        'Sie haben das Recht, binnen vierzehn Tagen ohne Angabe von Gründen diesen Vertrag zu widerrufen.',
    'The withdrawal period is fourteen days from the day on which you, or a third party other than the carrier indicated by you, acquire physical possession of the goods. If you ordered several goods in one order and they are delivered separately, the period starts on the day on which you, or a third party other than the carrier indicated by you, acquire physical possession of the last item.':
        'Die Widerrufsfrist beträgt vierzehn Tage ab dem Tag, an dem Sie oder ein von Ihnen benannter Dritter, der nicht der Beförderer ist, die Waren in Besitz genommen haben bzw. hat. Haben Sie mehrere Waren im Rahmen einer einheitlichen Bestellung bestellt und werden diese getrennt geliefert, beträgt die Frist vierzehn Tage ab dem Tag, an dem Sie oder ein von Ihnen benannter Dritter, der nicht der Beförderer ist, die letzte Ware in Besitz genommen haben bzw. hat.',
    'To exercise your right of withdrawal, you must inform us (Vibetown Entertainment (7inch.rare), owner Philipp Mühlen, Harkortstr. 29, 48163 Münster, Germany, phone +49 174 322 63 09, email':
        'Um Ihr Widerrufsrecht auszuüben, müssen Sie uns (Vibetown Entertainment (7inch.rare), Inhaber Philipp Mühlen, Harkortstr. 29, 48163 Münster, Deutschland, Telefon +49 174 322 63 09, E-Mail',
    ') of your decision to withdraw from this contract by an unequivocal statement (e.g. a letter sent by post or an email). You may use the attached model withdrawal form, but it is not obligatory.':
        ') mittels einer eindeutigen Erklärung (z. B. ein mit der Post versandter Brief oder eine E-Mail) über Ihren Entschluss, diesen Vertrag zu widerrufen, informieren. Sie können dafür das beigefügte Muster-Widerrufsformular verwenden, das jedoch nicht vorgeschrieben ist.',
    'To meet the withdrawal deadline, it is sufficient for you to send your communication concerning your exercise of the right of withdrawal before the withdrawal period has expired.':
        'Zur Wahrung der Widerrufsfrist reicht es aus, dass Sie die Mitteilung über die Ausübung des Widerrufsrechts vor Ablauf der Widerrufsfrist absenden.',
    'Effects of withdrawal': 'Folgen des Widerrufs',
    'If you withdraw from this contract, we shall reimburse to you all payments received from you, including the costs of delivery (with the exception of the supplementary costs resulting from your choice of a type of delivery other than the least expensive standard delivery offered by us), without undue delay and in any event not later than fourteen days from the day on which we are informed about your decision to withdraw from this contract. We will carry out such reimbursement using the same means of payment as you used for the initial transaction, unless you have expressly agreed otherwise; in any event, you will not incur any fees as a result of such reimbursement.':
        'Wenn Sie diesen Vertrag widerrufen, haben wir Ihnen alle Zahlungen, die wir von Ihnen erhalten haben, einschließlich der Lieferkosten (mit Ausnahme der zusätzlichen Kosten, die sich daraus ergeben, dass Sie eine andere Art der Lieferung als die von uns angebotene, günstigste Standardlieferung gewählt haben), unverzüglich und spätestens binnen vierzehn Tagen ab dem Tag zurückzuzahlen, an dem die Mitteilung über Ihren Widerruf dieses Vertrags bei uns eingegangen ist. Für diese Rückzahlung verwenden wir dasselbe Zahlungsmittel, das Sie bei der ursprünglichen Transaktion eingesetzt haben, es sei denn, mit Ihnen wurde ausdrücklich etwas anderes vereinbart; in keinem Fall werden Ihnen wegen dieser Rückzahlung Entgelte berechnet.',
    'We may withhold reimbursement until we have received the goods back or you have supplied evidence of having sent back the goods, whichever is the earliest.':
        'Wir können die Rückzahlung verweigern, bis wir die Waren wieder zurückerhalten haben oder bis Sie den Nachweis erbracht haben, dass Sie die Waren zurückgesandt haben, je nachdem, welches der frühere Zeitpunkt ist.',
    'You shall send back the goods or hand them over to ' + RN + ' without undue delay and in any event not later than fourteen days from the day on which you communicate your withdrawal from this contract to us. The deadline is met if you send back the goods before the period of fourteen days has expired.':
        'Sie haben die Waren unverzüglich und in jedem Fall spätestens binnen vierzehn Tagen ab dem Tag, an dem Sie uns über den Widerruf dieses Vertrags unterrichten, an ' + RN_DE + ' zurückzusenden oder zu übergeben. Die Frist ist gewahrt, wenn Sie die Waren vor Ablauf der Frist von vierzehn Tagen absenden.',
    'You will bear the direct cost of returning the goods.': 'Sie tragen die unmittelbaren Kosten der Rücksendung der Waren.',
    'You are only liable for any diminished value of the goods resulting from handling other than what is necessary to establish the nature, characteristics and functioning of the goods.':
        'Sie müssen für einen etwaigen Wertverlust der Waren nur aufkommen, wenn dieser Wertverlust auf einen zur Prüfung der Beschaffenheit, Eigenschaften und Funktionsweise der Waren nicht notwendigen Umgang mit ihnen zurückzuführen ist.',
    'Exclusion of the right of withdrawal': 'Ausschluss des Widerrufsrechts',
    'There is no right of withdrawal for the supply of sealed audio or video recordings if the seal has been removed after delivery (§ 312g (2) no. 6 BGB). Records in the LOWRIDER ANTHEMS series are delivered shrink-wrapped; this shrink-wrap is such a seal. You may withdraw from the purchase of unopened records within 14 days; once the shrink-wrap has been opened, the right of withdrawal no longer applies. Your warranty rights for a defective record remain unaffected (see Terms § 10).':
        'Das Widerrufsrecht besteht nicht bei der Lieferung versiegelter Ton- oder Videoaufnahmen, wenn die Versiegelung nach der Lieferung entfernt wurde (§ 312g Abs. 2 Nr. 6 BGB). Schallplatten der Serie LOWRIDER ANTHEMS werden eingeschweißt geliefert; diese Folie ist eine solche Versiegelung. Sie können den Kauf ungeöffneter Schallplatten innerhalb von 14 Tagen widerrufen; sobald die Folie geöffnet wurde, entfällt das Widerrufsrecht. Ihre Gewährleistungsrechte bei einer mangelhaften Schallplatte bleiben unberührt (siehe AGB § 10).',
    'Records in the MY PHILOSOPHY series are delivered without shrink-wrap; the right of withdrawal applies to them without this restriction.':
        'Schallplatten der Serie MY PHILOSOPHY werden ohne Schrumpffolie geliefert; für sie gilt das Widerrufsrecht ohne diese Einschränkung.',
    'Model withdrawal form': 'Muster-Widerrufsformular',
    '(Complete and return this form only if you wish to withdraw from the contract.)':
        '(Wenn Sie den Vertrag widerrufen wollen, dann füllen Sie bitte dieses Formular aus und senden Sie es zurück.)',
    'To: Vibetown Entertainment (7inch.rare), owner Philipp Mühlen, Harkortstr. 29, 48163 Münster, Germany, email':
        'An: Vibetown Entertainment (7inch.rare), Inhaber Philipp Mühlen, Harkortstr. 29, 48163 Münster, Deutschland, E-Mail',
    'I/We (*) hereby give notice that I/We (*) withdraw from my/our (*) contract of sale of the following goods (*):':
        'Hiermit widerrufe(n) ich/wir (*) den von mir/uns (*) abgeschlossenen Vertrag über den Kauf der folgenden Waren (*):',
    'Ordered on (*) / received on (*):': 'Bestellt am (*) / erhalten am (*):',
    'Name of consumer(s):': 'Name des/der Verbraucher(s):', 'Address of consumer(s):': 'Anschrift des/der Verbraucher(s):',
    'Signature of consumer(s) (only if this form is notified on paper):': 'Unterschrift des/der Verbraucher(s) (nur bei Mitteilung auf Papier):',
    'Date:': 'Datum:', '(*) Delete as appropriate.': '(*) Unzutreffendes streichen.',
 })),
 96: ('agb', 'Allgemeine Geschäftsbedingungen', dict(LEGAL, **{
    'General Terms and Conditions': 'Allgemeine Geschäftsbedingungen',
    '§ 1 Scope': '§ 1 Geltungsbereich',
    '(1) These terms apply to all orders placed by consumers via the online shop 7inchrare.com with Vibetown Entertainment (7inch.rare), owner Philipp Mühlen, Harkortstr. 29, 48163 Münster, Germany ("we").':
        '(1) Diese Bedingungen gelten für alle Bestellungen von Verbrauchern über den Online-Shop 7inchrare.com bei Vibetown Entertainment (7inch.rare), Inhaber Philipp Mühlen, Harkortstr. 29, 48163 Münster, Deutschland („wir“).',
    '(2) A consumer is any natural person who enters into a legal transaction for purposes that are predominantly outside their trade, business or profession (§ 13 BGB).':
        '(2) Verbraucher ist jede natürliche Person, die ein Rechtsgeschäft zu Zwecken abschließt, die überwiegend weder ihrer gewerblichen noch ihrer selbständigen beruflichen Tätigkeit zugerechnet werden können (§ 13 BGB).',
    '(3) Orders from retailers (shops and distributors) are governed exclusively by our Trade Terms.':
        '(3) Bestellungen von Wiederverkäufern (Plattenläden und Vertriebe) unterliegen ausschließlich unseren Händler-AGB.',
    '§ 2 Conclusion of contract': '§ 2 Vertragsschluss',
    '(1) The presentation of products in the shop is not a legally binding offer but an invitation to order.':
        '(1) Die Darstellung der Produkte im Shop stellt kein rechtlich bindendes Angebot, sondern eine Aufforderung zur Bestellung dar.',
    '(2) By clicking "Order and pay" you submit a binding offer to purchase the goods in your basket. You can check and correct your details at any time before submitting.':
        '(2) Mit dem Klick auf „Zahlungspflichtig bestellen“ geben Sie ein verbindliches Angebot zum Kauf der Waren in Ihrem Warenkorb ab. Sie können Ihre Angaben vor dem Absenden jederzeit prüfen und korrigieren.',
    '(3) We confirm receipt of your order by email without delay. The contract is concluded with this order confirmation; for payment by PayPal, credit card, Apple Pay or Google Pay, it is concluded on completion of the payment.':
        '(3) Wir bestätigen den Eingang Ihrer Bestellung unverzüglich per E-Mail. Der Vertrag kommt mit dieser Bestellbestätigung zustande; bei Zahlung per PayPal, Kreditkarte, Apple Pay oder Google Pay kommt er mit Abschluss der Zahlung zustande.',
    '(4) The contract languages are German and English. We store the contract text and send you the order details and these terms by email.':
        '(4) Vertragssprachen sind Deutsch und Englisch. Wir speichern den Vertragstext und senden Ihnen die Bestelldaten und diese AGB per E-Mail zu.',
    '§ 3 Prices and shipping costs': '§ 3 Preise und Versandkosten',
    '(1) All prices are final prices in euros and include statutory VAT.': '(1) Alle Preise sind Endpreise in Euro und enthalten die gesetzliche Umsatzsteuer.',
    '(2) Shipping costs including packaging are added depending on the destination country; they are shown on the "Shipping and payment" page and in the basket before you order.':
        '(2) Je nach Bestimmungsland kommen Versandkosten einschließlich Verpackung hinzu; sie werden vor der Bestellung auf der Seite „Versand und Zahlung“ und im Warenkorb angezeigt.',
    '(3) For deliveries to countries outside the EU, customs duties, import taxes and carrier fees may apply. These are borne by the recipient. Exception: deliveries to the United Kingdom with a value of up to GBP 135, where UK VAT is already included in the final price.':
        '(3) Bei Lieferungen in Länder außerhalb der EU können Zölle, Einfuhrabgaben und Gebühren des Transportunternehmens anfallen. Diese trägt der Empfänger. Ausnahme: Lieferungen in das Vereinigte Königreich mit einem Wert von bis zu 135 GBP, bei denen die britische Umsatzsteuer bereits im Endpreis enthalten ist.',
    '§ 4 Payment': '§ 4 Zahlung',
    '(1) We offer the following payment methods: credit card, Apple Pay, Google Pay, PayPal and SEPA bank transfer. Payments are processed by the payment service provider Mollie. For SEPA bank transfer, you receive the payment details at checkout; we ship once payment has been received.':
        '(1) Wir bieten folgende Zahlungsarten an: Kreditkarte, Apple Pay, Google Pay, PayPal und SEPA-Überweisung. Die Zahlungen werden vom Zahlungsdienstleister Mollie abgewickelt. Bei SEPA-Überweisung erhalten Sie die Zahlungsdaten an der Kasse; wir versenden nach Zahlungseingang.',
    '(2) We do not charge a surcharge for any payment method.': '(2) Für keine Zahlungsart erheben wir einen Aufpreis.',
    '(3) The purchase price is due immediately on conclusion of the contract, including for pre-orders.':
        '(3) Der Kaufpreis ist mit Vertragsschluss sofort fällig, auch bei Vorbestellungen.',
    '§ 5 Delivery and delivery times': '§ 5 Lieferung und Lieferzeiten',
    '(1) We deliver to the countries offered at checkout.': '(1) Wir liefern in die an der Kasse angebotenen Länder.',
    '(2) Items in stock are shipped within 3 days of receipt of payment; delivery takes the time stated for each country on the "Shipping and payment" page.':
        '(2) Lagernde Artikel werden innerhalb von 3 Tagen nach Zahlungseingang versandt; die Lieferung dauert so lange, wie für das jeweilige Land auf der Seite „Versand und Zahlung“ angegeben.',
    '(3) The delivery time is stated on the product page.': '(3) Die Lieferzeit wird auf der Produktseite angegeben.',
    '§ 6 Pre-orders': '§ 6 Vorbestellungen',
    '(1) Items not yet released are marked as "Pre-order". On the product page and at checkout we state the expected release month and the date by which we will ship at the latest ("Ships by").':
        '(1) Noch nicht erschienene Artikel sind als „Vorbestellung“ gekennzeichnet. Auf der Produktseite und an der Kasse nennen wir den voraussichtlichen Erscheinungsmonat und das Datum, bis zu dem wir spätestens versenden („Versand bis“).',
    '(2) Vinyl production can be delayed. We ship pre-orders as soon as the goods arrive with us, at the latest by the date stated.':
        '(2) Die Vinylproduktion kann sich verzögern. Wir versenden Vorbestellungen, sobald die Ware bei uns eintrifft, spätestens bis zum angegebenen Datum.',
    '(3) If the stated date is exceeded, we will inform you by email. You may then withdraw from the contract; we will refund the purchase price without delay. Your statutory rights remain unaffected.':
        '(3) Wird das angegebene Datum überschritten, informieren wir Sie per E-Mail. Sie können dann vom Vertrag zurücktreten; wir erstatten den Kaufpreis unverzüglich. Ihre gesetzlichen Rechte bleiben unberührt.',
    '(4) If an order contains both in-stock and pre-order items, we ship the entire order together unless you select partial shipment at checkout.':
        '(4) Enthält eine Bestellung sowohl lagernde als auch vorbestellte Artikel, versenden wir die gesamte Bestellung gemeinsam, sofern Sie an der Kasse nicht Teillieferung wählen.',
    '§ 7 Limited editions': '§ 7 Limitierte Auflagen',
    'Our releases are produced in limited quantities. If an item is no longer available despite your order, we will inform you without delay and refund any payment already made.':
        'Unsere Releases werden in limitierter Stückzahl produziert. Ist ein Artikel trotz Ihrer Bestellung nicht mehr verfügbar, informieren wir Sie unverzüglich und erstatten bereits geleistete Zahlungen.',
    '§ 8 Retention of title': '§ 8 Eigentumsvorbehalt', 'The goods remain our property until paid in full.': 'Die Ware bleibt bis zur vollständigen Bezahlung unser Eigentum.',
    '§ 9 Right of withdrawal': '§ 9 Widerrufsrecht',
    'Consumers have a right of withdrawal as set out in the': 'Verbrauchern steht ein Widerrufsrecht gemäß der',
    'withdrawal policy': 'Widerrufsbelehrung',
    '. Please send returns only to: ' + RN + '.': ' zu. Bitte senden Sie Rücksendungen nur an: ' + RN_DE + '.',
    '§ 10 Warranty and transport damage': '§ 10 Gewährleistung und Transportschäden',
    '(1) The statutory warranty rights apply. We are liable only for defects that already exist at the time of delivery, in particular manufacturing defects (pressing faults, cracks, warping, wrong label, wrong pressing) and transport damage. Wear from playing (e.g. crackle, scratches, groove wear) and damage caused after delivery by improper handling, storage or unsuitable playback equipment are not defects.':
        '(1) Es gelten die gesetzlichen Gewährleistungsrechte. Wir haften nur für Mängel, die bereits bei Lieferung vorhanden sind, insbesondere Herstellungsfehler (Pressfehler, Risse, Verformungen, falsches Label, falsche Pressung) und Transportschäden. Abnutzung durch das Abspielen (z. B. Knistern, Kratzer, Rillenverschleiß) sowie Schäden, die nach der Lieferung durch unsachgemäße Behandlung, Lagerung oder ungeeignete Abspielgeräte entstehen, sind keine Mängel.',
    '(2) Please check the record on receipt and report any faults, if possible within 14 days, to':
        '(2) Bitte prüfen Sie die Schallplatte bei Erhalt und melden Sie Mängel möglichst innerhalb von 14 Tagen an',
    'with your order number, a short description and photos; your statutory rights do not depend on this period. We replace a defective record or refund the purchase price if no replacement is available, and we bear the cost of the return. Please send returns only to: ' + RN + '.':
        ' unter Angabe Ihrer Bestellnummer, mit einer kurzen Beschreibung und Fotos; Ihre gesetzlichen Rechte hängen nicht von dieser Frist ab. Wir ersetzen eine mangelhafte Schallplatte oder erstatten den Kaufpreis, wenn kein Ersatz verfügbar ist, und tragen die Kosten der Rücksendung. Bitte senden Sie Rücksendungen nur an: ' + RN_DE + '.',
    '(3) Please report obvious transport damage to the carrier and to us as soon as possible.':
        '(3) Bitte melden Sie offensichtliche Transportschäden so schnell wie möglich dem Transportunternehmen und uns.',
    '§ 11 Liability': '§ 11 Haftung',
    'We are liable without limitation for intent and gross negligence, for injury to life, body or health, and under the German Product Liability Act. In the event of slightly negligent breach of essential contractual obligations, liability is limited to the foreseeable damage typical for the contract. Otherwise, liability is excluded.':
        'Wir haften unbeschränkt für Vorsatz und grobe Fahrlässigkeit, für Verletzungen des Lebens, des Körpers oder der Gesundheit sowie nach dem Produkthaftungsgesetz. Bei leicht fahrlässiger Verletzung wesentlicher Vertragspflichten ist die Haftung auf den vorhersehbaren, vertragstypischen Schaden begrenzt. Im Übrigen ist die Haftung ausgeschlossen.',
    '§ 12 Final provisions': '§ 12 Schlussbestimmungen',
    '(1) The law of the Federal Republic of Germany applies, excluding the UN Convention on Contracts for the International Sale of Goods. For consumers, this choice of law applies only insofar as it does not deprive them of the protection of mandatory consumer protection provisions of the country in which they have their habitual residence.':
        '(1) Es gilt das Recht der Bundesrepublik Deutschland unter Ausschluss des UN-Kaufrechts. Für Verbraucher gilt diese Rechtswahl nur insoweit, als dadurch nicht der durch zwingende Verbraucherschutzvorschriften des Staates, in dem sie ihren gewöhnlichen Aufenthalt haben, gewährte Schutz entzogen wird.',
    '(2) If any provision is invalid, the remainder of the contract remains valid.': '(2) Sollte eine Bestimmung unwirksam sein, bleibt der Vertrag im Übrigen wirksam.',
 })),
 98: ('haendler-agb', 'Händler-AGB (Plattenläden und Vertriebe)', dict(LEGAL, **{
    'Trade Terms (Shops and Distributors)': 'Händler-AGB (Plattenläden und Vertriebe)',
    '§ 1 Scope': '§ 1 Geltungsbereich',
    'These terms apply to all orders from businesses within the meaning of § 14 BGB (record stores, online retailers, distributors) placed via the trade area of 7inchrare.com, by email or by pro-forma invoice. Deviating terms of the retailer apply only if we agree to them in writing. There is no right of withdrawal.':
        'Diese Bedingungen gelten für alle Bestellungen von Unternehmern im Sinne des § 14 BGB (Plattenläden, Online-Händler, Vertriebe), die über den Händlerbereich von 7inchrare.com, per E-Mail oder per Proforma-Rechnung aufgegeben werden. Abweichende Bedingungen des Händlers gelten nur, wenn wir ihnen schriftlich zustimmen. Ein Widerrufsrecht besteht nicht.',
    '§ 2 Trade account': '§ 2 Händlerkonto',
    'Access to the trade area requires an application and our approval. We verify business status on the basis of a business or tax registration document, a website or a physical store. Providing a VAT ID is optional. Without a valid VAT ID, deliveries within the EU are invoiced with German VAT (19%); with a valid VAT ID from another EU member state, they are tax-exempt under the reverse charge procedure. We may reject applications without giving reasons. Login details must be kept confidential.':
        'Der Zugang zum Händlerbereich setzt einen Antrag und unsere Freigabe voraus. Den Unternehmerstatus prüfen wir anhand eines Gewerbe- oder Steuerdokuments, einer Website oder eines Ladengeschäfts. Die Angabe einer USt-IdNr. ist optional. Ohne gültige USt-IdNr. werden Lieferungen innerhalb der EU mit deutscher Umsatzsteuer (19 %) abgerechnet; mit gültiger USt-IdNr. eines anderen EU-Mitgliedstaats sind sie im Reverse-Charge-Verfahren steuerfrei. Wir können Anträge ohne Angabe von Gründen ablehnen. Zugangsdaten sind vertraulich zu behandeln.',
    '§ 3 Order and conclusion of contract': '§ 3 Bestellung und Vertragsschluss',
    'An order in the trade area is a binding offer. The contract is concluded with our order confirmation or pro-forma invoice. The minimum order quantity is 50 records per order; titles can be combined freely. We reserve ordered quantities for up to 7 days pending receipt of payment; after that we may cancel the reservation.':
        'Eine Bestellung im Händlerbereich ist ein verbindliches Angebot. Der Vertrag kommt mit unserer Bestellbestätigung oder Proforma-Rechnung zustande. Die Mindestbestellmenge beträgt 50 Schallplatten pro Bestellung; Titel können frei kombiniert werden. Wir reservieren bestellte Mengen bis zu 7 Tage bis zum Zahlungseingang; danach können wir die Reservierung aufheben.',
    '§ 4 Prices and quantity tiers': '§ 4 Preise und Staffelmengen',
    'The prices shown in the trade area for the respective country apply. They depend on the total quantity of the order (50–99, 100–249, 250+ units). Prices are net plus statutory VAT where applicable. Deliveries to businesses in other EU member states with a valid VAT ID are tax-exempt (reverse charge); without a VAT ID, 19% German VAT applies. Export deliveries to non-EU countries are tax-exempt. Where "carriage paid" is stated, shipping costs are included.':
        'Es gelten die im Händlerbereich für das jeweilige Land angezeigten Preise. Sie richten sich nach der Gesamtmenge der Bestellung (50–99, 100–249, 250+ Stück). Preise verstehen sich netto zuzüglich gesetzlicher Umsatzsteuer, soweit anfallend. Lieferungen an Unternehmen in anderen EU-Mitgliedstaaten mit gültiger USt-IdNr. sind steuerfrei (Reverse Charge); ohne USt-IdNr. fallen 19 % deutsche Umsatzsteuer an. Ausfuhrlieferungen in Drittländer sind steuerfrei. Wo „frachtfrei“ angegeben ist, sind die Versandkosten enthalten.',
    '§ 5 Payment': '§ 5 Zahlung',
    'We deliver against prepayment. Up to 249 units, payment can be made online (credit card, PayPal) or by bank transfer; from 250 units, by bank transfer only. Invoices are in euros. Goods are shipped only once the full amount has been received in our account. Bank and transfer fees are borne by the retailer.':
        'Wir liefern gegen Vorkasse. Bis 249 Stück ist die Zahlung online (Kreditkarte, PayPal) oder per Überweisung möglich; ab 250 Stück nur per Überweisung. Rechnungen lauten auf Euro. Die Ware wird erst versandt, wenn der volle Betrag auf unserem Konto eingegangen ist. Bank- und Überweisungsgebühren trägt der Händler.',
    '§ 6 Delivery, transfer of risk, customs': '§ 6 Lieferung, Gefahrübergang, Zoll',
    'Unless otherwise agreed, deliveries are made DAP (Incoterms 2020) to the delivery address given. Risk passes to the retailer when the goods are handed over to the carrier. Import duties, customs and import VAT in the destination country are borne by the retailer. Delivery dates stated for pre-orders are estimates; production delays do not give rise to claims for damages.':
        'Sofern nichts anderes vereinbart ist, erfolgen Lieferungen DAP (Incoterms 2020) an die angegebene Lieferadresse. Die Gefahr geht mit Übergabe der Ware an den Frachtführer auf den Händler über. Einfuhrabgaben, Zölle und Einfuhrumsatzsteuer im Bestimmungsland trägt der Händler. Für Vorbestellungen angegebene Liefertermine sind Schätzungen; Produktionsverzögerungen begründen keine Schadensersatzansprüche.',
    '§ 7 Pre-orders': '§ 7 Vorbestellungen',
    'Pre-orders placed before pressing are binding and are taken into account when planning the edition. Payment is due with the pro-forma invoice unless otherwise agreed.':
        'Vor dem Pressen aufgegebene Vorbestellungen sind verbindlich und werden bei der Planung der Auflage berücksichtigt. Die Zahlung ist mit der Proforma-Rechnung fällig, sofern nichts anderes vereinbart ist.',
    '§ 8 Inspection and notice of defects': '§ 8 Prüfung und Mängelrüge',
    'The retailer shall inspect the goods immediately on receipt (§ 377 HGB). Obvious defects and transport damage must be reported in writing with photos within 7 days of receipt. For justified defects, we will, at our option, supply a replacement or issue a credit. The warranty period is 12 months. Returns only by prior arrangement to: ' + RN + '.':
        'Der Händler hat die Ware unverzüglich bei Erhalt zu prüfen (§ 377 HGB). Offensichtliche Mängel und Transportschäden sind innerhalb von 7 Tagen nach Erhalt schriftlich mit Fotos zu melden. Bei berechtigten Mängeln liefern wir nach unserer Wahl Ersatz oder erteilen eine Gutschrift. Die Gewährleistungsfrist beträgt 12 Monate. Rücksendungen nur nach vorheriger Absprache an: ' + RN_DE + '.',
    '§ 9 Exclusivity': '§ 9 Exklusivität',
    'Territorial exclusivity is granted only to distributors and only by separate written agreement (minimum purchase, term, prices).':
        'Gebietsexklusivität wird nur Vertrieben und nur durch gesonderte schriftliche Vereinbarung gewährt (Mindestabnahme, Laufzeit, Preise).',
    '§ 10 Resale, images and texts': '§ 10 Wiederverkauf, Bilder und Texte',
    'The retailer may use the covers, labels, press photos, audio samples and texts provided solely to promote and sell our goods. Resale to consumers below our retail price is permitted; there is no resale price maintenance.':
        'Der Händler darf die bereitgestellten Cover, Labels, Pressefotos, Hörproben und Texte ausschließlich zur Bewerbung und zum Verkauf unserer Waren verwenden. Der Wiederverkauf an Verbraucher unter unserem Verkaufspreis ist zulässig; eine Preisbindung besteht nicht.',
    '§ 11 Retention of title': '§ 11 Eigentumsvorbehalt', 'The goods remain our property until paid in full.': 'Die Ware bleibt bis zur vollständigen Bezahlung unser Eigentum.',
    '§ 12 Liability': '§ 12 Haftung',
    'We are liable without limitation for intent, gross negligence and injury to life, body or health. In the case of slight negligence, we are liable only for breach of essential contractual obligations and limited to the foreseeable damage typical for the contract; loss of profit is excluded.':
        'Wir haften unbeschränkt für Vorsatz, grobe Fahrlässigkeit und Verletzung von Leben, Körper oder Gesundheit. Bei leichter Fahrlässigkeit haften wir nur für die Verletzung wesentlicher Vertragspflichten und beschränkt auf den vorhersehbaren, vertragstypischen Schaden; entgangener Gewinn ist ausgeschlossen.',
    '§ 13 Governing law and jurisdiction': '§ 13 Anwendbares Recht und Gerichtsstand',
    'German law applies, excluding the UN Convention on Contracts for the International Sale of Goods (CISG). Place of jurisdiction for merchants is Münster. The contract language is German; this English translation is for information only.':
        'Es gilt deutsches Recht unter Ausschluss des UN-Kaufrechts (CISG). Gerichtsstand für Kaufleute ist Münster. Vertragssprache ist Deutsch.',
 })),
 3: ('datenschutz', 'Datenschutzerklärung', dict(LEGAL, **{
    'Privacy Policy': 'Datenschutzerklärung',
    '1. Controller': '1. Verantwortlicher',
    'Vibetown Entertainment (7inch.rare), owner Philipp Mühlen, Harkortstr. 29, 48163 Münster, Germany, email':
        'Vibetown Entertainment (7inch.rare), Inhaber Philipp Mühlen, Harkortstr. 29, 48163 Münster, Deutschland, E-Mail',
    ', phone +49 174 322 63 09. No data protection officer has been appointed, as there is no legal obligation to do so.':
        ', Telefon +49 174 322 63 09. Ein Datenschutzbeauftragter wurde nicht benannt, da hierzu keine gesetzliche Pflicht besteht.',
    '2. Hosting and server log files': '2. Hosting und Server-Logfiles',
    'The website is hosted by ALL-INKL.COM – Neue Medien Münnich, Hauptstraße 68, 02742 Friedersdorf, Germany, on servers in Germany. When you visit the site, technically necessary data is processed (IP address, date and time, page accessed, browser, operating system, referrer). The legal basis is Art. 6 (1) (f) GDPR (secure operation). A data processing agreement is in place with ALL-INKL. Log files are deleted after [7] days. The connection is encrypted via SSL/TLS.':
        'Die Website wird von ALL-INKL.COM – Neue Medien Münnich, Hauptstraße 68, 02742 Friedersdorf, Deutschland, auf Servern in Deutschland gehostet. Beim Besuch der Website werden technisch notwendige Daten verarbeitet (IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Browser, Betriebssystem, Referrer). Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (sicherer Betrieb). Mit ALL-INKL besteht ein Auftragsverarbeitungsvertrag. Logfiles werden nach [7] Tagen gelöscht. Die Verbindung ist per SSL/TLS verschlüsselt.',
    '3. Orders and customer account': '3. Bestellungen und Kundenkonto',
    'For orders, we process your name, address, email, phone number (optional), order and payment data to perform the contract (Art. 6 (1) (b) GDPR). A customer account is optional; guest orders are possible. For trade accounts, we additionally process company details, VAT ID and sales territory for verification and approval. Invoice data is retained for 8 to 10 years due to commercial and tax law obligations (Art. 6 (1) (c) GDPR).':
        'Für Bestellungen verarbeiten wir Ihren Namen, Ihre Anschrift, E-Mail-Adresse, Telefonnummer (optional) sowie Bestell- und Zahlungsdaten zur Vertragserfüllung (Art. 6 Abs. 1 lit. b DSGVO). Ein Kundenkonto ist optional; Gastbestellungen sind möglich. Bei Händlerkonten verarbeiten wir zusätzlich Unternehmensangaben, USt-IdNr. und Verkaufsgebiet zur Prüfung und Freigabe. Rechnungsdaten werden aufgrund handels- und steuerrechtlicher Pflichten 8 bis 10 Jahre aufbewahrt (Art. 6 Abs. 1 lit. c DSGVO).',
    '4. Payment service providers': '4. Zahlungsdienstleister',
    'Depending on the payment method chosen, we pass the data required for payment to:': 'Je nach gewählter Zahlungsart geben wir die für die Zahlung erforderlichen Daten weiter an:',
    'Mollie B.V., Keizersgracht 126, 1015 CW Amsterdam, Netherlands (credit card, Apple Pay, Google Pay, SEPA bank transfer and processing of PayPal payments). Mollie processes the data within the EU.':
        'Mollie B.V., Keizersgracht 126, 1015 CW Amsterdam, Niederlande (Kreditkarte, Apple Pay, Google Pay, SEPA-Überweisung und Abwicklung von PayPal-Zahlungen). Mollie verarbeitet die Daten innerhalb der EU.',
    'PayPal (Europe) S.à r.l. et Cie, S.C.A., 22–24 Boulevard Royal, 2449 Luxembourg.': 'PayPal (Europe) S.à r.l. et Cie, S.C.A., 22–24 Boulevard Royal, 2449 Luxemburg.',
    'The legal basis is Art. 6 (1) (b) GDPR. The privacy notices of the respective provider also apply.':
        'Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO. Ergänzend gelten die Datenschutzhinweise des jeweiligen Anbieters.',
    '5. Shipping': '5. Versand',
    'For delivery, we pass your name and delivery address to the shipping provider, currently Deutsche Post AG / DHL Paket GmbH, Charles-de-Gaulle-Straße 20, 53113 Bonn, Germany (Art. 6 (1) (b) GDPR). We pass on your email address or phone number for delivery notifications only with your consent (Art. 6 (1) (a) GDPR). For shipments outside the EU, the data required for customs clearance is transmitted to the customs authorities of the destination country.':
        'Zur Lieferung geben wir Ihren Namen und Ihre Lieferadresse an den Versanddienstleister weiter, derzeit Deutsche Post AG / DHL Paket GmbH, Charles-de-Gaulle-Straße 20, 53113 Bonn, Deutschland (Art. 6 Abs. 1 lit. b DSGVO). Ihre E-Mail-Adresse oder Telefonnummer geben wir nur mit Ihrer Einwilligung für Zustellbenachrichtigungen weiter (Art. 6 Abs. 1 lit. a DSGVO). Bei Sendungen außerhalb der EU werden die für die Zollabfertigung erforderlichen Daten an die Zollbehörden des Bestimmungslandes übermittelt.',
    '6. Contact by email or form': '6. Kontakt per E-Mail oder Formular',
    'If you contact us, we process your details to handle your enquiry (Art. 6 (1) (b) or (f) GDPR) and delete them when they are no longer needed and no retention obligations apply.':
        'Wenn Sie uns kontaktieren, verarbeiten wir Ihre Angaben zur Bearbeitung Ihrer Anfrage (Art. 6 Abs. 1 lit. b oder f DSGVO) und löschen sie, sobald sie nicht mehr benötigt werden und keine Aufbewahrungspflichten bestehen.',
    '7. Cookies and local storage': '7. Cookies und lokaler Speicher',
    'We use only technically necessary cookies and local storage (§ 25 (2) TDDDG, Art. 6 (1) (f) GDPR). We do not use analytics, advertising or tracking cookies, and fonts are loaded locally from our server, not from Google. Because only necessary cookies are used, no cookie consent banner is required. You can block or delete cookies in your browser settings; the basket, login and checkout may then no longer work.':
        'Wir verwenden ausschließlich technisch notwendige Cookies und lokalen Speicher (§ 25 Abs. 2 TDDDG, Art. 6 Abs. 1 lit. f DSGVO). Wir setzen keine Analyse-, Werbe- oder Tracking-Cookies ein, und Schriftarten werden lokal von unserem Server geladen, nicht von Google. Da nur notwendige Cookies verwendet werden, ist kein Cookie-Banner erforderlich. Sie können Cookies in Ihren Browsereinstellungen blockieren oder löschen; Warenkorb, Login und Kasse funktionieren dann gegebenenfalls nicht mehr.',
    'The following cookies and storage entries are set by the shop:': 'Folgende Cookies und Speichereinträge werden vom Shop gesetzt:',
    'Purpose': 'Zweck', 'Duration': 'Dauer',
    'Detect changes to the basket so that it is displayed correctly': 'Erkennt Änderungen am Warenkorb, damit dieser korrekt angezeigt wird',
    'Session': 'Sitzung',
    'Stores your basket and checkout data (also for guests)': 'Speichert Ihren Warenkorb und Ihre Checkout-Daten (auch für Gäste)',
    '2 days': '2 Tage', 'Remembers recently viewed products': 'Merkt sich zuletzt angesehene Produkte',
    'Login to your customer account and check that cookies are enabled': 'Anmeldung in Ihrem Kundenkonto und Prüfung, ob Cookies aktiviert sind',
    'Session, up to 14 days with "Remember me"': 'Sitzung, bis zu 14 Tage mit „Angemeldet bleiben“',
    'Stores interface settings for logged-in users': 'Speichert Oberflächeneinstellungen für angemeldete Nutzer',
    '1 year': '1 Jahr', 'Stores the selected language': 'Speichert die gewählte Sprache',
    'theme (local storage)': 'theme (lokaler Speicher)',
    'Stores your light/dark mode choice; stays in your browser and is not sent to us': 'Speichert Ihre Wahl zwischen hellem und dunklem Modus; bleibt in Ihrem Browser und wird nicht an uns übermittelt',
    'Until deleted': 'Bis zur Löschung',
    'Payment is made on the page of the payment provider (see section 4), which may set its own cookies there.':
        'Die Zahlung erfolgt auf der Seite des Zahlungsdienstleisters (siehe Abschnitt 4), der dort eigene Cookies setzen kann.',
    '8. Links to social networks': '8. Links zu sozialen Netzwerken',
    'Our site links to our Instagram profile @7inch.rare. These are simple links; data is only transmitted when you click the link and visit Instagram (Meta Platforms Ireland Ltd.).':
        'Unsere Website verlinkt auf unser Instagram-Profil @7inch.rare. Es handelt sich um einfache Links; Daten werden erst übermittelt, wenn Sie den Link anklicken und Instagram besuchen (Meta Platforms Ireland Ltd.).',
    '9. Your rights': '9. Ihre Rechte',
    'You have the right of access, rectification, erasure, restriction of processing, data portability and the right to object to processing based on Art. 6 (1) (f) GDPR. You may withdraw any consent given at any time with effect for the future. You may lodge a complaint with a data protection supervisory authority; the authority responsible for us is the State Commissioner for Data Protection and Freedom of Information of North Rhine-Westphalia (LDI NRW), Düsseldorf.':
        'Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit sowie das Recht, der Verarbeitung auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO zu widersprechen. Eine erteilte Einwilligung können Sie jederzeit mit Wirkung für die Zukunft widerrufen. Sie können sich bei einer Datenschutz-Aufsichtsbehörde beschweren; für uns zuständig ist die Landesbeauftragte für Datenschutz und Informationsfreiheit Nordrhein-Westfalen (LDI NRW), Düsseldorf.',
    '10. Last updated': '10. Stand',
 })),
 11: ('rueckgabe-und-erstattung', 'Rückgabe- und Erstattungsrichtlinie', {
    'This is a sample page.': 'Dies ist eine Beispielseite.', 'Overview': 'Überblick',
    'Our refund and returns policy lasts 30 days. If 30 days have passed since your purchase, we can’t offer you a full refund or exchange.':
        'Unsere Rückgabe- und Erstattungsrichtlinie gilt 30 Tage. Sind seit Ihrem Kauf 30 Tage vergangen, können wir Ihnen leider keine vollständige Erstattung oder keinen Umtausch anbieten.',
    'To be eligible for a return, your item must be unused and in the same condition that you received it. It must also be in the original packaging.':
        'Um eine Rückgabe vornehmen zu können, muss Ihr Artikel unbenutzt und in demselben Zustand sein, in dem Sie ihn erhalten haben. Er muss sich außerdem in der Originalverpackung befinden.',
    'Several types of goods are exempt from being returned. Perishable goods such as food, flowers, newspapers or magazines cannot be returned. We also do not accept products that are intimate or sanitary goods, hazardous materials, or flammable liquids or gases.':
        'Mehrere Warenarten sind von der Rückgabe ausgeschlossen. Verderbliche Waren wie Lebensmittel, Blumen, Zeitungen oder Zeitschriften können nicht zurückgegeben werden. Außerdem nehmen wir keine Intim- oder Hygieneartikel, Gefahrstoffe oder brennbare Flüssigkeiten und Gase zurück.',
    'Additional non-returnable items:': 'Weitere von der Rückgabe ausgeschlossene Artikel:',
    'Gift cards': 'Geschenkgutscheine', 'Downloadable software products': 'Herunterladbare Softwareprodukte',
    'Some health and personal care items': 'Einige Gesundheits- und Körperpflegeartikel',
    'To complete your return, we require a receipt or proof of purchase.': 'Zur Abwicklung Ihrer Rückgabe benötigen wir einen Kaufbeleg oder Kaufnachweis.',
    'Please do not send your purchase back to the manufacturer.': 'Bitte senden Sie Ihren Kauf nicht an den Hersteller zurück.',
    'There are certain situations where only partial refunds are granted:': 'In bestimmten Fällen werden nur Teilerstattungen gewährt:',
    'Book with obvious signs of use': 'Buch mit deutlichen Gebrauchsspuren',
    'CD, DVD, VHS tape, software, video game, cassette tape, or vinyl record that has been opened.': 'CD, DVD, VHS-Kassette, Software, Videospiel, Musikkassette oder Schallplatte, die geöffnet wurde.',
    'Any item not in its original condition, is damaged or missing parts for reasons not due to our error.': 'Jeder Artikel, der nicht im Originalzustand ist, beschädigt ist oder dem Teile fehlen, aus Gründen, die nicht auf unser Verschulden zurückgehen.',
    'Any item that is returned more than 30 days after delivery': 'Jeder Artikel, der mehr als 30 Tage nach der Lieferung zurückgegeben wird',
    'Refunds': 'Erstattungen',
    'Once your return is received and inspected, we will send you an email to notify you that we have received your returned item. We will also notify you of the approval or rejection of your refund.':
        'Sobald Ihre Rücksendung bei uns eingegangen und geprüft ist, senden wir Ihnen eine E-Mail, um den Erhalt des zurückgesendeten Artikels zu bestätigen. Wir informieren Sie außerdem darüber, ob Ihre Erstattung genehmigt oder abgelehnt wurde.',
    'If you are approved, then your refund will be processed, and a credit will automatically be applied to your credit card or original method of payment, within a certain amount of days.':
        'Wird Ihre Erstattung genehmigt, wird sie bearbeitet und innerhalb einer bestimmten Anzahl von Tagen automatisch Ihrer Kreditkarte oder ursprünglichen Zahlungsmethode gutgeschrieben.',
    'Late or missing refunds': 'Verspätete oder fehlende Erstattungen',
    'If you haven’t received a refund yet, first check your bank account again.': 'Wenn Sie noch keine Erstattung erhalten haben, prüfen Sie bitte zunächst erneut Ihr Bankkonto.',
    'Then contact your credit card company, it may take some time before your refund is officially posted.': 'Wenden Sie sich anschließend an Ihr Kreditkartenunternehmen; es kann einige Zeit dauern, bis Ihre Erstattung offiziell verbucht wird.',
    'Next contact your bank. There is often some processing time before a refund is posted.': 'Kontaktieren Sie danach Ihre Bank. Bis eine Erstattung verbucht wird, vergeht häufig einige Bearbeitungszeit.',
    'If you’ve done all of this and you still have not received your refund yet, please contact us at {email address}.':
        'Wenn Sie all dies getan haben und Ihre Erstattung immer noch nicht eingegangen ist, kontaktieren Sie uns bitte unter {email address}.',
    'Sale items': 'Reduzierte Artikel', 'Only regular priced items may be refunded. Sale items cannot be refunded.': 'Nur Artikel zum regulären Preis können erstattet werden. Reduzierte Artikel können nicht erstattet werden.',
    'Exchanges': 'Umtausch',
    'We only replace items if they are defective or damaged. If you need to exchange it for the same item, send us an email at {email address} and send your item to: {physical address}.':
        'Wir ersetzen Artikel nur, wenn sie defekt oder beschädigt sind. Wenn Sie ihn gegen denselben Artikel umtauschen möchten, senden Sie uns eine E-Mail an {email address} und schicken Sie Ihren Artikel an: {physical address}.',
    'Gifts': 'Geschenke',
    'If the item was marked as a gift when purchased and shipped directly to you, you’ll receive a gift credit for the value of your return. Once the returned item is received, a gift certificate will be mailed to you.':
        'Wurde der Artikel beim Kauf als Geschenk gekennzeichnet und direkt an Sie versandt, erhalten Sie eine Geschenkgutschrift in Höhe des Werts Ihrer Rückgabe. Sobald der zurückgesendete Artikel eingegangen ist, wird Ihnen ein Geschenkgutschein zugesandt.',
    'If the item wasn’t marked as a gift when purchased, or the gift giver had the order shipped to themselves to give to you later, we will send a refund to the gift giver and they will find out about your return.':
        'Wurde der Artikel beim Kauf nicht als Geschenk gekennzeichnet oder hat der Schenkende die Bestellung an sich selbst senden lassen, um sie Ihnen später zu geben, erstatten wir den Betrag an den Schenkenden, der dadurch von Ihrer Rückgabe erfährt.',
    'Shipping returns': 'Rücksendung',
    'To return your product, you should mail your product to: {physical address}.': 'Um Ihr Produkt zurückzugeben, senden Sie es bitte an: {physical address}.',
    'You will be responsible for paying for your own shipping costs for returning your item. Shipping costs are non-refundable. If you receive a refund, the cost of return shipping will be deducted from your refund.':
        'Sie tragen die Kosten für den Rückversand Ihres Artikels selbst. Versandkosten werden nicht erstattet. Erhalten Sie eine Erstattung, werden die Kosten für den Rückversand von Ihrer Erstattung abgezogen.',
    'Depending on where you live, the time it may take for your exchanged product to reach you may vary.': 'Je nachdem, wo Sie wohnen, kann die Zeit, bis Ihr umgetauschtes Produkt bei Ihnen ankommt, unterschiedlich lang sein.',
    'If you are returning more expensive items, you may consider using a trackable shipping service or purchasing shipping insurance. We don’t guarantee that we will receive your returned item.':
        'Wenn Sie hochwertigere Artikel zurücksenden, sollten Sie einen Versanddienst mit Sendungsverfolgung nutzen oder eine Transportversicherung abschließen. Wir garantieren nicht, dass wir Ihren zurückgesendeten Artikel erhalten.',
    'Need help?': 'Brauchen Sie Hilfe?', 'Contact us at {email} for questions related to refunds and returns.': 'Kontaktieren Sie uns unter {email} bei Fragen zu Erstattungen und Rücksendungen.',
 }),
}

# Home: ACF block data (JSON strings inside block comments). Keys are quoted JSON values.
HOME = {
    '"Out now"': '"Jetzt erhältlich"', '"Pre-order"': '"Vorbestellung"',
    '"Pre-orders are open. Secure your copy before the run is pressed."': '"Vorbestellungen sind geöffnet. Sichern Sie sich Ihr Exemplar, bevor die Auflage gepresst wird."',
    '"View release"': '"Release ansehen"', '"Pre-order now"': '"Jetzt vorbestellen"', '"All releases"': '"Alle Releases"',
    '"Two series"': '"Zwei Serien"', '"Pick your side of the map."': '"Wählen Sie Ihre Seite der Karte."',
    '"Catalogue"': '"Katalog"', '"All"': '"Alle"',
    '"For record shops \\u0026 distributors"': '"Für Plattenläden \\u0026 Vertriebe"',
    '"Stock the series in your shop."': '"Führen Sie die Serie in Ihrem Laden."',
    '"Wholesale price list, pre-order windows and shipping options on request. We ship worldwide; the buyer pays freight."':
        '"Großhandelspreisliste, Vorbestellfenster und Versandoptionen auf Anfrage. Wir liefern weltweit; die Fracht trägt der Käufer."',
    '"copies minimum for record shops"': '"Exemplare Mindestabnahme für Plattenläden"',
    '"copies minimum for distributors"': '"Exemplare Mindestabnahme für Vertriebe"',
    '"Request the wholesale list"': '"Großhandelsliste anfordern"',
}

# Titles / small replacements for pages that otherwise keep the English markup (Woo pages).
WOO = {10: ('mein-konto', 'Mein Konto', {'My account': 'Mein Konto'}), 8: ('warenkorb', 'Warenkorb', {}), 9: ('kasse', 'Kasse', {}), 7: ('shop', 'Shop', {})}
CART_EXTRA = {'aria-label="Empty record"': 'aria-label="Leere Schallplatte"'}

NODE = re.compile(r'>([^<>]+)<')


def translate(content, tmap, pid):
    left, used = [], set()

    def repl(m):
        raw = m.group(1)
        key = raw.strip()
        if not key:
            return m.group(0)
        if key in tmap:
            used.add(key)
            val = tmap[key]
            lead = '' if val[:1] == ' ' else raw[:len(raw) - len(raw.lstrip())]
            trail = '' if val[-1:] == ' ' else raw[len(raw.rstrip()):]
            return '>' + lead + val + trail + '<'
        left.append(key)
        return m.group(0)

    out = NODE.sub(repl, content)
    for a, b in LINKS.items():
        out = out.replace('href="%s"' % a, 'href="%s"' % b)
    unused = [k for k in tmap if k not in used]
    return out, unused, left


def main(dump, outdir):
    os.makedirs(outdir, exist_ok=True)
    payload = {}
    for pid, (slug, title, tmap) in PAGES.items():
        d = json.load(open(os.path.join(dump, 'p%d.json' % pid)))
        c = d['content']
        # form shortcodes → placeholders, replaced with the German CF7 form ids at deploy time
        c = c.replace('[contact-form-7 id="101"', '[contact-form-7 id="{{form:101}}"').replace('[contact-form-7 id="86"', '[contact-form-7 id="{{form:86}}"')
        out, unused, left = translate(c, tmap, pid)
        # inline markup separators that never need translating
        left = [k for k in left if k not in ('·', '&middot;', '.', ')', ',') and not re.fullmatch(r'[\W\d_]+|[\w.+-]+@[\w.-]+|@[\w.]+|7inch\.rare|My Philosophy|Lowrider Anthems|Vibetown Entertainment.*|DE\d+.*|IBAN.*|BIC.*|Harkortstr.*|Philipp Mühlen|\+49.*', k)]
        open(os.path.join(outdir, slug + '.html'), 'w').write(out)
        payload[str(pid)] = {'slug': slug, 'title': title, 'content': out}
        print('== p%d %s: unused keys=%d, untranslated nodes=%d' % (pid, slug, len(unused), len(left)))
        for k in unused: print('   UNUSED  :', k[:90])
        for k in sorted(set(left)): print('   LEFT    :', k[:110])
    # home
    d = json.load(open(os.path.join(dump, 'p33.json')))
    c = d['content']
    miss = [k for k in HOME if k not in c]
    for k, v in HOME.items(): c = c.replace(k, v)
    open(os.path.join(outdir, 'home.html'), 'w').write(c)
    payload['33'] = {'slug': 'home', 'title': 'Startseite', 'content': c}
    print('== p33 home: missing keys', miss)
    for pid, (slug, title, tmap) in WOO.items():
        d = json.load(open(os.path.join(dump, 'p%d.json' % pid)))
        c = d['content']
        for k, v in tmap.items(): c = c.replace('>' + k + '<', '>' + v + '<')
        for k, v in CART_EXTRA.items(): c = c.replace(k, v)
        payload[str(pid)] = {'slug': slug, 'title': title, 'content': c}
    json.dump(payload, open(os.path.join(dump, 'de_payload.json'), 'w'), ensure_ascii=False)
    print('payload pages:', sorted(payload, key=int))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
