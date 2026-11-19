<?php
/**
 * VAT rules (see "podatki.md").
 *
 * Prices are gross (VAT included) and identical worldwide: 19.99 / 26.99 €.
 * Rates live in WooCommerce → Settings → Tax → Standard rates (editable); outside the EU there is a 0 % catch-all row.
 *
 *  - DE customer: 19 %.
 *  - EU consumer: 19 % (DE) or destination rate (OSS), switch in Settings → Tax ("Charge destination VAT (OSS)").
 *  - EU business with a valid VAT ID (checked in VIES), not DE: 0 % (intra-community supply).
 *  - Outside the EU: 0 % (export).
 *  - UK consumers: switched off until UK VAT registration (switch "Sell to UK consumers", then 20 %). UK partners: 0 %.
 *  - Shipping: same rate as the goods (shipping costs are entered gross for consumers).
 */

const I7_EU = array( 'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE' );
const I7_SELLER_VAT = 'DE207201101';

/** Prices are gross and the same in every country: never convert them through the shop's base rate. */
add_filter( 'woocommerce_adjust_non_base_location_prices', '__return_false' );

/* ── Settings (Tax tab) ─────────────────────────────────────────────── */
add_filter( 'woocommerce_tax_settings', function ( $settings ) {
	foreach ( $settings as $s ) { if ( ( $s['id'] ?? '' ) === 'i7_oss_enabled' ) { return $settings; } }
	$extra = array(
		array( 'title' => '7inch.rare VAT switches', 'type' => 'title', 'id' => 'i7_tax_options' ),
		array(
			'title' => 'Charge destination VAT (OSS)', 'id' => 'i7_oss_enabled', 'type' => 'checkbox', 'default' => 'no',
			'desc'  => 'EU consumers outside Germany pay the VAT rate of their country (One-Stop-Shop). Off = 19 % German VAT for all EU consumers.',
		),
		array(
			'title' => 'Sell to UK consumers', 'id' => 'i7_uk_retail', 'type' => 'checkbox', 'default' => 'no',
			'desc'  => 'Off until UK VAT registration. On = consumers in the UK can order and pay 20 % UK VAT (rate in the table below).',
		),
		array( 'type' => 'sectionend', 'id' => 'i7_tax_options' ),
	);
	return array_merge( $settings, $extra );
} );

/** OSS switch off → every EU consumer pays the German rate. */
add_filter( 'woocommerce_find_rates', function ( $matched, $args ) {
	static $busy = false;
	if ( $busy || 'yes' === get_option( 'i7_oss_enabled', 'no' ) ) { return $matched; }
	$country = $args['country'] ?? '';
	if ( 'DE' === $country || ! in_array( $country, I7_EU, true ) ) { return $matched; }
	$busy = true;
	$de   = WC_Tax::find_rates( array_merge( $args, array( 'country' => 'DE', 'state' => '', 'postcode' => '', 'city' => '' ) ) );
	$busy = false;
	return $de ? $de : $matched;
}, 10, 2 );

/* ── Posted checkout data (works for the live order-review AJAX and the final submit) ── */
function i7_posted( $key ) {
	if ( isset( $_POST[ $key ] ) ) { return wc_clean( wp_unslash( $_POST[ $key ] ) ); } // phpcs:ignore
	if ( ! empty( $_POST['post_data'] ) ) { // phpcs:ignore
		parse_str( wp_unslash( $_POST['post_data'] ), $d ); // phpcs:ignore
		if ( isset( $d[ $key ] ) ) { return wc_clean( $d[ $key ] ); }
	}
	return null;
}

function i7_billing_country() {
	$c = i7_posted( 'billing_country' );
	if ( null === $c && function_exists( 'WC' ) && WC()->customer ) { $c = WC()->customer->get_billing_country( 'edit' ); }
	return strtoupper( (string) $c );
}

function i7_billing_vat() {
	$v = i7_posted( 'billing_vat_number' );
	if ( null === $v && is_user_logged_in() ) { $v = get_user_meta( get_current_user_id(), 'billing_vat_number', true ); }
	return strtoupper( preg_replace( '/[\s.\-]+/', '', (string) $v ) );
}

/** VIES check, cached for a day. Unreachable service = not valid (VAT is charged). */
function i7_vies_valid( $country, $vat ) {
	$prefix = 'GR' === $country ? 'EL' : $country;
	if ( 0 !== strpos( $vat, $prefix ) ) { return false; }
	$num = substr( $vat, strlen( $prefix ) );
	if ( ! preg_match( '/^[A-Z0-9]{2,12}$/', $num ) ) { return false; }
	$key = 'i7_vies_' . md5( $prefix . $num );
	$hit = get_transient( $key );
	if ( false !== $hit ) { return 'ok' === $hit; }
	$res = wp_remote_get( 'https://ec.europa.eu/taxation_customs/vies/rest-api/ms/' . rawurlencode( $prefix ) . '/vat/' . rawurlencode( $num ), array( 'timeout' => 6 ) );
	if ( is_wp_error( $res ) || 200 !== wp_remote_retrieve_response_code( $res ) ) { return false; }
	$json  = json_decode( wp_remote_retrieve_body( $res ), true );
	$valid = ! empty( $json['isValid'] ) || ! empty( $json['valid'] );
	set_transient( $key, $valid ? 'ok' : 'no', DAY_IN_SECONDS );
	return $valid;
}

/** EU business with a valid VAT ID, outside Germany, or a partner (business) outside the EU. */
function i7_is_vat_exempt() {
	static $cache = array();
	$country = i7_billing_country();
	$vat     = i7_billing_vat();
	$partner = function_exists( 'i7_partner_type' ) && i7_partner_type();
	$k       = $country . '|' . $vat . '|' . (int) $partner;
	if ( isset( $cache[ $k ] ) ) { return $cache[ $k ]; }
	$exempt = false;
	$ni = 'GB' === $country && i7_is_ni( $country, (string) i7_posted( 'billing_postcode' ) );
	if ( $ni && 0 === strpos( $vat, 'XI' ) ) {
		$exempt = i7_vies_valid( 'XI', $vat );
	} elseif ( $country && ! in_array( $country, I7_EU, true ) ) {
		$exempt = $partner;                                   // consumers outside the EU already hit the 0 % row; UK consumers get 20 %
	} elseif ( $country && 'DE' !== $country && $vat ) {
		$exempt = i7_vies_valid( $country, $vat );
	}
	return $cache[ $k ] = $exempt;
}

/** WooCommerce reads a plain property here, so set it before every totals calculation (cart, checkout refresh, submit). */
add_action( 'woocommerce_before_calculate_totals', function () {
	if ( ! function_exists( 'WC' ) || ! WC()->customer ) { return; }
	$manual = is_user_logged_in() && 'yes' === get_user_meta( get_current_user_id(), 'is_vat_exempt', true ); // exemption set by hand in the user profile
	WC()->customer->set_is_vat_exempt( $manual || i7_is_vat_exempt() );
}, 1 );

/* ── UK consumers: off until UK VAT registration ────────────────────── */
add_action( 'woocommerce_after_checkout_validation', function ( $data, $errors ) {
	if ( 'yes' === get_option( 'i7_uk_retail', 'no' ) ) { return; }
	if ( i7_is_ni( $data['billing_country'] ?? '', $data['billing_postcode'] ?? '' ) ) { return; }
	$gb = 'GB' === ( $data['billing_country'] ?? '' ) || ( ! empty( $data['ship_to_different_address'] ) && 'GB' === ( $data['shipping_country'] ?? '' ) );
	if ( $gb && ! ( function_exists( 'i7_partner_type' ) && i7_partner_type() ) ) {
		$errors->add( 'uk_closed', 'Sorry, we cannot deliver to consumers in the United Kingdom at the moment. Record shops and distributors: please log in with your partner account.' );
	}
}, 10, 2 );

/* ── Note for the invoice when no VAT is charged ────────────────────── */
function i7_vat_note_for( $order ) {
	if ( (float) $order->get_total_tax() > 0 ) { return ''; }
	$country = $order->get_billing_country();
	if ( ! in_array( $country, I7_EU, true ) ) { return 'Steuerfreie Ausfuhrlieferung (tax-free export).'; }
	$vat = $order->get_meta( '_billing_vat_number' );
	return 'Steuerfreie innergemeinschaftliche Lieferung (tax-free intra-community supply). Seller VAT ID: ' . I7_SELLER_VAT . ( $vat ? ' · Buyer VAT ID: ' . $vat : '' );
}

add_action( 'woocommerce_checkout_order_processed', function ( $order_id ) {
	$order = wc_get_order( $order_id );
	if ( ! $order ) { return; }
	$order->update_meta_data( '_i7_vat_note', i7_vat_note_for( $order ) );
	$order->save_meta_data();
}, 20 );

add_action( 'woocommerce_email_after_order_table', function ( $order ) {
	$n = $order->get_meta( '_i7_vat_note' );
	if ( $n ) { echo '<p><strong>VAT:</strong> ' . esc_html( $n ) . '</p>'; }
} );
add_action( 'woocommerce_order_details_after_order_table', function ( $order ) {
	$n = $order->get_meta( '_i7_vat_note' );
	if ( $n ) { echo '<p class="pp-note"><strong>VAT:</strong> ' . esc_html( $n ) . '</p>'; }
} );
add_action( 'woocommerce_admin_order_data_after_billing_address', function ( $order ) {
	$n = $order->get_meta( '_i7_vat_note' );
	if ( $n ) { echo '<p><strong>VAT note:</strong> ' . esc_html( $n ) . '</p>'; }
} );

/* ── Partners: prices are NET (VAT added on top; 0 % for EU reverse charge / export) ── */
add_filter( 'woocommerce_prices_include_tax', function ( $incl ) {
	return ( function_exists( 'i7_partner_type' ) && i7_partner_type() ) ? false : $incl;
} );
foreach ( array( 'shop', 'cart' ) as $i7_ctx ) {
	add_filter( 'option_woocommerce_tax_display_' . $i7_ctx, function ( $v ) {
		return ( function_exists( 'i7_partner_type' ) && i7_partner_type() ) ? 'excl' : $v;
	} );
}

/* ── Northern Ireland (postcode BT…) is treated like the EU: German rate, EU business with an "XI" VAT ID is exempt ── */
function i7_is_ni( $country, $postcode ) {
	return 'GB' === strtoupper( (string) $country ) && 0 === stripos( trim( (string) $postcode ), 'BT' );
}
add_filter( 'woocommerce_find_rates', function ( $matched, $args ) {
	static $busy = false;
	if ( $busy || ! i7_is_ni( $args['country'] ?? '', $args['postcode'] ?? '' ) ) { return $matched; }
	$busy = true;
	$de   = WC_Tax::find_rates( array_merge( $args, array( 'country' => 'DE', 'state' => '', 'postcode' => '', 'city' => '' ) ) );
	$busy = false;
	return $de ? $de : $matched;
}, 5, 2 );

/* UK consumers off (until further notice): no shipping rates for GB, so neither the normal checkout nor wallet buttons can complete an order. Partners and Northern Ireland (BT…) are not affected. */
add_filter( 'woocommerce_package_rates', function ( $rates, $package ) {
	if ( 'yes' === get_option( 'i7_uk_retail', 'no' ) ) { return $rates; }
	$d = $package['destination'] ?? array();
	if ( 'GB' !== ( $d['country'] ?? '' ) || i7_is_ni( 'GB', $d['postcode'] ?? '' ) ) { return $rates; }
	if ( function_exists( 'i7_partner_type' ) && i7_partner_type() ) { return $rates; }
	return array();
}, 100, 2 );
add_filter( 'woocommerce_no_shipping_available_html', function ( $html ) {
	if ( 'GB' === ( function_exists( 'WC' ) && WC()->customer ? WC()->customer->get_shipping_country() : '' ) && 'yes' !== get_option( 'i7_uk_retail', 'no' ) && ! ( function_exists( 'i7_partner_type' ) && i7_partner_type() ) ) {
		return '<p>Sorry, we cannot deliver to consumers in the United Kingdom at the moment. Record shops and distributors: please log in with your partner account.</p>';
	}
	return $html;
} );
