#!/usr/bin/env python3
"""Build the Germanized (StoreaBill) invoice template for Vibetown Entertainment (B2B invoices, text-only layout)
and write it into the default invoice template post(s). usage: invoice_template.py"""
import deploy, base64

GREY = '#6b6b6b'

def sc(data, ph, tip='', extra=''):
    return ('<span class="document-shortcode sab-tooltip" data-tooltip="%s" data-shortcode="%s"><span class="editor-placeholder"></span>%s</span>'
            % (tip or data, data, ph))

def p(inner, attrs='', cls=''):
    return '<!-- wp:paragraph %s --><p%s>%s</p><!-- /wp:paragraph -->' % (attrs, (' class="%s"' % cls) if cls else '', inner)

def small(inner):
    return ('<!-- wp:paragraph {"fontSize":"small","style":{"color":{"text":"%s"}}} --><p class="has-text-color has-small-font-size" style="color:%s">%s</p><!-- /wp:paragraph -->' % (GREY, GREY, inner))

def col(inner, width=None):
    a = ' {"width":%s}' % width if width else ''
    st = ' style="flex-basis:%s%%"' % width if width else ''
    return '<!-- wp:column%s --><div class="wp-block-column"%s>%s</div><!-- /wp:column -->' % (a, st, inner)

def cols(*cs):
    return '<!-- wp:columns --><div class="wp-block-columns">%s</div><!-- /wp:columns -->' % ''.join(cs)

def spacer(h):
    return '<!-- wp:spacer {"height":%d} --><div style="height:%dpx" aria-hidden="true" class="wp-block-spacer"></div><!-- /wp:spacer -->' % (h, h)

def bi(key, ph):
    return sc('business_information?data=' + key, ph)

HEAD = ('<!-- wp:storeabill/header --><div class="wp-block-storeabill-header"><div class="wp-block-group__inner-container sab-header-container">'
        + cols(
            col(p('<strong>' + bi('base_company_name', 'Vibetown Entertainment') + ' – ' + bi('contact_full_name', 'Philipp Mühlen')
                  + '</strong><br>' + bi('base_address_data&amp;format=address:break:no', 'Harkortstraße 29<br />48163 Münster')
                  + '<br>VAT ID: ' + bi('vat_id', 'DE207201101') + '<br>E-mail: ' + bi('contact_email', 'contact@vibetown.de')
                  + ' · ' + bi('contact_phone', '+49 174 322 63 09'), '{"fontSize":"small"}', 'has-small-font-size'))
        )
        + '</div></div><!-- /wp:storeabill/header -->')

ADDR = ('<!-- wp:storeabill/address --><div class="wp-block-storeabill-address sab-document-address has-text-align-left"><p class="address-heading"><strong><span style="font-size:10px" class="has-inline-text-size">Invoice to</span></strong></p>'
        '<p class="address-content"><span class="placeholder-content"><span class="editor-placeholder"></span>{content}</span></p></div><!-- /wp:storeabill/address -->')
SHIP = ('<!-- wp:storeabill/shipping-address {"hideIfEqualsBilling":true} --><div class="wp-block-storeabill-shipping-address sab-document-address has-text-align-left"><p class="address-heading"><strong><span style="font-size:10px" class="has-inline-text-size">Ship to</span></strong></p>'
        '<p class="address-content"><span class="placeholder-content"><span class="editor-placeholder"></span>{content}</span></p></div><!-- /wp:storeabill/shipping-address -->')

TITLE = '<!-- wp:storeabill/document-title {"customFontSize":"25"} --><p class="has-text-align-left" style="font-size:25px"><strong>INVOICE</strong></p><!-- /wp:storeabill/document-title -->'

DETAILS = cols(
    col(p('Invoice no.: ' + sc('document?data=formatted_number', '17/2026', 'Formatted document number')
          + '<br>Order no.: ' + sc('document?data=order_number', '1234', 'Order number')
          + '<br>Payment method: ' + sc('document?data=payment_method_title', 'Mollie', 'Payment method')
          + '<br>Customer VAT ID: ' + sc('document?data=billing_vat_id', 'DE123456789', 'Customer VAT ID'))),
    col('<!-- wp:storeabill/document-date {"align":"right"} --><p class="has-text-align-right">Date: <span class="placeholder-content sab-tooltip" data-tooltip="Document Date"><span class="editor-placeholder"></span>{content}</span></p><!-- /wp:storeabill/document-date -->'
        + p('Incoterms 2020: DAP<br>Country of origin: Germany (EU)', '{"align":"right"}', 'has-text-align-right')))

def column(heading, inner, width=None, align=None):
    a = {}
    if width: a['width'] = width
    if align: a['align'] = align
    import json
    attrs = dict(a, headingTextColor='#000000', headingBackgroundColor='#e5e5e5')
    cls = 'wp-block-storeabill-item-table-column is-horizontally-aligned-%s' % (align or 'left')
    st = ' style="flex-basis:%s%%"' % width if width else ''
    return ('<!-- wp:storeabill/item-table-column %s --><div class="%s"%s><span class="item-column-heading-text"><strong>%s</strong></span>%s</div><!-- /wp:storeabill/item-table-column -->'
            % (json.dumps(attrs, separators=(',', ':')), cls, st, heading, inner))

def item(kind, attrs=''):
    return ('<!-- wp:storeabill/item-%s %s --><p class="wp-block-storeabill-item-%s sab-block-item-content"><span class="placeholder-content sab-tooltip" data-tooltip="%s"><span class="editor-placeholder"></span>{content}</span></p><!-- /wp:storeabill/item-%s -->'
            % (kind, attrs, kind, kind, kind))

TABLE = ('<!-- wp:storeabill/item-table {"className":"is-style-even","customBorderColor":"#a9a9a9","borders":["horizontal"],"headingTextColor":"black","customHeadingBackgroundColor":"#e5e5e5","showPricesIncludingTax":false,"hasDenseLayout":false} -->'
         '<div class="wp-block-storeabill-item-table is-style-even has-border-horizontal">'
         + column('Description', item('name') + '<!-- wp:storeabill/item-attributes {"customTextColor":"#a9a9a9","fontSize":"small"} /-->', 40)
         + column('HS code', '<!-- wp:storeabill/item-meta {"metaType":"hs_code"} --><p class="wp-block-storeabill-item-meta sab-block-item-content">{content}</p><!-- /wp:storeabill/item-meta -->', 16, 'center')
         + column('Qty', item('quantity'), 9, 'center')
         + column('Unit (net)', item('price', '{"showPricesIncludingTax":false}'), 17, 'center')
         + column('Total (net)', item('line-total', '{"discountTotalType":"before_discounts","showPricesIncludingTax":false}'), 18, 'right')
         + '</div><!-- /wp:storeabill/item-table -->')

def total_row(t, heading, extra=''):
    return '<!-- wp:storeabill/item-total-row {"totalType":"%s","heading":"%s"%s} /-->' % (t, heading, extra)

TOTALS = ('<!-- wp:storeabill/item-totals {"hasDenseLayout":false} --><div class="wp-block-storeabill-item-totals">'
          + total_row('line_subtotal', 'Subtotal goods (net)')
          + total_row('shipping', 'Shipping', ',"hideIfEmpty":true')
          + total_row('discount', 'Discount', ',"hideIfEmpty":true')
          + total_row('vouchers', 'Voucher', ',"hideIfEmpty":true')
          + total_row('net', 'Net total')
          + '<!-- wp:storeabill/item-total-row {"totalType":"taxes","hideIfEmpty":true,"heading":"%s"} /-->' % (
              '\\u003cspan class=\\u0022document-shortcode sab-tooltip\\u0022 data-tooltip=\\u0022Tax Rate\\u0022 data-shortcode=\\u0022document_total?data=rate\\u0026amp;total_type=taxes\\u0022\\u003e\\u003cspan class=\\u0022editor-placeholder\\u0022\\u003e\\u003c/span\\u003e19\\u003c/span\\u003e % VAT')
          + '<!-- wp:storeabill/item-total-row {"content":"\\u003cstrong\\u003e{total}\\u003c/strong\\u003e","totalType":"total","borders":["top","bottom"],"customBorderColor":"#a9a9a9","customFontSize":"16","heading":"\\u003cstrong\\u003eTOTAL INVOICE VALUE\\u003c/strong\\u003e"} /-->'
          + '</div><!-- /wp:storeabill/item-totals -->')

NOTICES = ('<!-- wp:storeabill/reverse-charge-notice --><p class="has-text-align-left">Tax-free intra-Community supply (§ 4 No. 1b i.V.m. § 6a UStG); the recipient is liable for VAT (reverse charge).</p><!-- /wp:storeabill/reverse-charge-notice -->'
           '<!-- wp:storeabill/third-country-notice --><p class="has-text-align-left">VAT-exempt export delivery – steuerfreie Ausfuhrlieferung gem. § 4 Nr. 1a i. V. m. § 6 UStG.</p><!-- /wp:storeabill/third-country-notice -->')

PAY = (spacer(10)
       + p('<strong>PAYMENT</strong><br>Payment terms: prepayment – due immediately, before dispatch<br>Account holder: ' + bi('holder', 'Philipp Mühlen')
           + '<br>IBAN / BIC: ' + bi('iban', 'DE20 4005 0150 0000 0725 46') + ' · ' + bi('bic', 'WELADED1MST')
           + '<br>Bank: ' + bi('bank_name', 'Sparkasse Münsterland Ost')
           + '<br>Reference: Invoice ' + sc('document?data=formatted_number', '17/2026'), '{"fontSize":"small"}', 'has-small-font-size')
       + p('Thank you for your order!', '{"fontSize":"small"}', 'has-small-font-size'))

FOOT = ('<!-- wp:storeabill/footer --><div class="wp-block-storeabill-footer"><div class="wp-block-group__inner-container sab-footer-container">'
        '<!-- wp:storeabill/page-number {"align":"right"} --><p class="wp-block-storeabill-page-number sab-page-number has-text-align-right">Page <span class="current-page-no-placeholder-content sab-tooltip" data-tooltip="Page number"><span class="editor-placeholder"></span>{current_page_no}</span> of <span class="total-pages-placeholder-content sab-tooltip" data-tooltip="Total pages"><span class="editor-placeholder"></span>{total_pages}</span></p><!-- /wp:storeabill/page-number -->'
        + spacer(10)
        + '<!-- wp:separator {"customColor":"#a9a9a9","className":"is-style-wide"} --><hr class="wp-block-separator has-text-color has-background is-style-wide" style="background-color:#a9a9a9;color:#a9a9a9" /><!-- /wp:separator -->'
        + cols(
            col(small('<strong>' + bi('base_company_name', 'Vibetown Entertainment') + '</strong><br>' + bi('contact_full_name', 'Philipp Mühlen')
                      + '<br>' + bi('base_address_data&amp;format=address:break:no', 'Harkortstraße 29<br />48163 Münster')), 34),
            col(small('<strong>Tax</strong><br>VAT ID: ' + bi('vat_id', 'DE207201101') + '<br>Tax no.: ' + bi('local_tax_number', '336/5143/2169')), 33),
            col(small('<strong>Contact</strong><br>' + bi('contact_email', 'contact@vibetown.de') + '<br>' + bi('contact_phone', '+49 174 322 63 09')), 33))
        + '</div></div><!-- /wp:storeabill/footer -->')

CONTENT = ('<!-- wp:storeabill/document-styles /-->' + HEAD + spacer(18)
           + cols(col(ADDR), col(SHIP)) + spacer(10) + TITLE + DETAILS + spacer(14) + TABLE + TOTALS + NOTICES + PAY + FOOT)

if __name__ == '__main__':
    b = base64.b64encode(CONTENT.encode()).decode()
    print(deploy.php("""
$c = base64_decode('%s');
$out = [];
foreach ((array) get_posts(['post_type'=>'document_template','numberposts'=>-1,'fields'=>'ids','meta_key'=>'_document_type','meta_value'=>'invoice']) as $id) {
  $r = wp_update_post(['ID'=>$id,'post_content'=>wp_slash($c)], true);
  $out[$id] = is_wp_error($r) ? $r->get_error_message() : 'ok';
}
return $out;
""" % b))
