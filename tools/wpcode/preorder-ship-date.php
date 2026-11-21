<?php
/**
 * WPCode snippet: "Pre-order dispatch date".
 * Location: Run everywhere.
 *
 * Adds a "Dispatch date" field (Product data → Inventory) to every product and shows it next to "Available on backorder":
 *   EN "Available on backorder · Ships approx. 15 March 2027"   DE "Vorbestellbar · Versand ca. 15. März 2027"
 * Accepted values: 2027-03-15 (day), 2027-03 (month) or any free text. Enter it on the English product; the German one reads it from there
 * (a value typed on the German product wins). Empty field = no change to the current output.
 */
add_action( 'woocommerce_product_options_inventory_product_data', function () {
	woocommerce_wp_text_input( array(
		'id'          => '_i7_ship_date',
		'label'       => 'Dispatch date (pre-order)',
		'description' => 'YYYY-MM-DD or YYYY-MM, shown on the product page when the product is on backorder. Enter on the English product.',
		'desc_tip'    => true,
	) );
} );
add_action( 'woocommerce_admin_process_product_object', function ( $product ) {
	if ( isset( $_POST['_i7_ship_date'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification
		$product->update_meta_data( '_i7_ship_date', sanitize_text_field( wp_unslash( $_POST['_i7_ship_date'] ) ) ); // phpcs:ignore WordPress.Security.NonceVerification
	}
} );

/** Localised "Ships approx. …" phrase for a product, or '' when there is no date. */
function i7_ship_phrase( $product ) {
	$id  = $product->get_id();
	$raw = trim( (string) get_post_meta( $id, '_i7_ship_date', true ) );
	if ( '' === $raw && function_exists( 'pll_get_post' ) && function_exists( 'pll_default_language' ) ) {
		$orig = pll_get_post( $id, pll_default_language() );
		if ( $orig ) { $raw = trim( (string) get_post_meta( $orig, '_i7_ship_date', true ) ); }
	}
	if ( '' === $raw ) { return ''; }
	$de = 0 === strpos( determine_locale(), 'de' );
	if ( preg_match( '/^\d{4}-\d{2}-\d{2}$/', $raw ) ) {
		$when = wp_date( $de ? 'j. F Y' : 'j F Y', strtotime( $raw . ' 12:00:00' ) );
	} elseif ( preg_match( '/^\d{4}-\d{2}$/', $raw ) ) {
		$when = wp_date( 'F Y', strtotime( $raw . '-15 12:00:00' ) );
	} else {
		$when = $raw;
	}
	return ( $de ? 'Versand ca. ' : 'Ships approx. ' ) . $when;
}

add_filter( 'woocommerce_get_availability_text', function ( $text, $product ) {
	if ( ! $product || 'onbackorder' !== $product->get_stock_status() ) { return $text; }
	$phrase = i7_ship_phrase( $product );
	if ( '' === $phrase ) { return $text; }
	$de = 0 === strpos( determine_locale(), 'de' );
	return ( $de ? 'Vorbestellbar' : 'Available on backorder' ) . ' · ' . $phrase;
}, 20, 2 );
