<?php
/**
 * TEMPORARY partner pricing display (until the B2B plugin takes over).
 * Logged-in shops / distributors see the wholesale price instead of the retail price,
 * together with the minimum order quantity it applies to.
 * Display only: it does not change cart or checkout prices.
 * Prices = "country price" for 100–249 pcs from the User Journey brief.
 */

add_action( 'init', function () {
	if ( ! get_role( 'partner_shop' ) )        { add_role( 'partner_shop', 'Partner: Record shop', array( 'read' => true ) ); }
	if ( ! get_role( 'partner_distributor' ) ) { add_role( 'partner_distributor', 'Partner: Distributor', array( 'read' => true ) ); }
} );

/** [ currency, My Philosophy, Lowrider Anthems ] by ISO country; '*' = EU default. */
function i7_partner_price_table() {
	$eu  = array( 'EUR', 9.00, 10.50 );
	$usd = array( 'USD', 10.00, 12.00 );
	return array(
		'*' => $eu, 'DE' => $eu, 'FR' => $eu, 'ES' => $eu, 'IT' => $eu, 'NL' => $eu, 'BE' => $eu,
		'PL' => array( 'EUR', 8.00, 9.50 ),
		'GB' => array( 'EUR', 9.50, 11.00 ),
		'BR' => array( 'EUR', 7.50, 9.00 ),
		'US' => $usd, 'MX' => $usd, 'CA' => $usd, 'AU' => $usd, 'NZ' => $usd,
		'JP' => array( 'USD', 9.50, 11.00 ),
	);
}

/** 'shop' | 'distributor' | '' for the current visitor. */
function i7_partner_type() {
	if ( ! is_user_logged_in() ) { return ''; }
	$u = wp_get_current_user();
	if ( in_array( 'partner_distributor', (array) $u->roles, true ) ) { return 'distributor'; }
	if ( in_array( 'partner_shop', (array) $u->roles, true ) )        { return 'shop'; }
	return '';
}

add_filter( 'woocommerce_get_price_html', function ( $html, $product ) {
	$type = i7_partner_type();
	if ( ! $type ) { return $html; }
	$uid     = get_current_user_id();
	$country = strtoupper( (string) get_user_meta( $uid, 'billing_country', true ) );
	if ( $country === 'RU' ) { return ''; }
	$table = i7_partner_price_table();
	$row   = $table[ $country ] ?? $table['*'];
	$col   = has_term( 'lowrider-anthems', 'product_cat', $product->get_id() ) ? 2 : 1;
	$price = (float) $row[ $col ];
	$min   = $type === 'distributor' ? 100 : 50;
	if ( $type === 'shop' ) { $price += 1.00; } // 50–99 pcs tier: country price + 1.00
	$sym  = $row[0] === 'USD' ? '$' : '€';
	$fmt  = $row[0] === 'USD' ? number_format( $price, 2, '.', ',' ) : number_format( $price, 2, ',', '.' );
	$amt  = $row[0] === 'USD' ? $sym . $fmt : $fmt . ' ' . $sym;
	$ship = in_array( $country, array( 'DE', 'BR' ), true ) ? esc_html__( 'Ex works, shipping paid by the buyer.', '7inch' ) : esc_html__( 'Delivery included.', '7inch' );
	return '<span class="partner-price">' . esc_html( $amt ) . '</span> <span class="partner-note">' .
		sprintf( /* translators: %d: minimum copies */ esc_html__( 'Price at the minimum order of %d copies (all titles combined).', '7inch' ), $min ) . ' ' . $ship . '</span>';
}, 20, 2 );
