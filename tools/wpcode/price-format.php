/* WPCode snippet "Prices: EN €26.99 / DE 26,99 €". WooCommerce stores one price format (comma, symbol after the amount);
 * English pages and e-mails show it the English way (€26.99), German ones keep 26,99 €. */
$i7_price_de = function () { return 0 === strpos( determine_locale(), 'de' ); };
add_filter( 'wc_get_price_decimal_separator', function ( $s ) use ( $i7_price_de ) { return $i7_price_de() ? $s : '.'; }, 99 );
add_filter( 'wc_get_price_thousand_separator', function ( $s ) use ( $i7_price_de ) { return $i7_price_de() ? $s : ','; }, 99 );
add_filter( 'woocommerce_price_format', function ( $f ) use ( $i7_price_de ) { return $i7_price_de() ? $f : '%1$s%2$s'; }, 99 );
