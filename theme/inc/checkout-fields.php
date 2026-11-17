<?php
/**
 * Optional "EU VAT number" field in the block checkout (WooCommerce Additional Checkout Fields API).
 * Shown once under "Contact information" (location 'address' would repeat it in both the billing and the shipping form),
 * saved on the order and visible in admin and e-mails.
 * It is only stored and format-checked here; VAT/reverse-charge handling comes with the invoicing/B2B setup.
 */
add_action( 'woocommerce_init', function () {
	if ( ! function_exists( 'woocommerce_register_additional_checkout_field' ) ) { return; }
	woocommerce_register_additional_checkout_field( array(
		'id'            => 'i7/vat_number',
		'label'         => 'EU VAT number (optional)',
		'optionalLabel' => 'EU VAT number (optional)',
		'location'      => 'contact',
		'type'          => 'text',
		'required'      => false,
		'attributes'    => array( 'autocomplete' => 'off', 'maxLength' => '20', 'data-i7-vat' => '1' ),
	) );
} );

/** Normalise: uppercase, no spaces/dots/dashes (e.g. "de 207.201-101" → "DE207201101"). */
add_filter( 'woocommerce_sanitize_additional_field', function ( $value, $key ) {
	if ( 'i7/vat_number' === $key ) {
		$value = strtoupper( preg_replace( '/[\s.\-]+/', '', (string) $value ) );
	}
	return $value;
}, 10, 2 );

/** Light format check (country prefix + 2–12 letters/digits); empty is fine. */
add_action( 'woocommerce_validate_additional_field', function ( $errors, $key, $value ) {
	if ( 'i7/vat_number' === $key && '' !== $value && ! preg_match( '/^[A-Z]{2}[A-Z0-9]{2,12}$/', $value ) ) {
		$errors->add( 'i7_invalid_vat', 'Please enter the VAT number with its country prefix, e.g. DE123456789.' );
	}
	return $errors;
}, 10, 3 );
