<?php
/**
 * Classic checkout customisations.
 * - Billing address is the main address; shipping is an optional "Another address for shipping".
 * - Optional "EU VAT number" billing field: normalised, format-checked, saved on the order,
 *   shown in the admin billing box and in e-mails. (VAT / reverse-charge handling comes with invoicing/B2B.)
 */
add_filter( 'gettext', function ( $translated, $text, $domain ) {
	if ( 'woocommerce' === $domain && 'Ship to a different address?' === $text ) { return 'Another address for shipping'; }
	return $translated;
}, 10, 3 );

add_filter( 'woocommerce_checkout_fields', function ( $fields ) {
	$fields['billing']['billing_vat_number'] = array(
		'label'        => 'EU VAT number',
		'required'     => false,
		'class'        => array( 'form-row-wide' ),
		'priority'     => 125,
		'autocomplete' => 'off',
		'maxlength'    => 20,
	);
	return $fields;
} );

/** Uppercase, no spaces/dots/dashes ("de 207.201-101" → "DE207201101"). */
add_filter( 'woocommerce_process_checkout_field_billing_vat_number', function ( $value ) {
	return strtoupper( preg_replace( '/[\s.\-]+/', '', (string) $value ) );
} );

/** Light format check (country prefix + 2–12 letters/digits); empty is fine. */
add_action( 'woocommerce_after_checkout_validation', function ( $data, $errors ) {
	$v = $data['billing_vat_number'] ?? '';
	if ( '' !== $v && ! preg_match( '/^[A-Z]{2}[A-Z0-9]{2,12}$/', $v ) ) {
		$errors->add( 'billing_vat_number_format', '<strong>EU VAT number</strong> must start with the country code, e.g. DE123456789.' );
	}
}, 10, 2 );

add_filter( 'woocommerce_admin_billing_fields', function ( $fields ) {
	$fields['vat_number'] = array( 'label' => 'EU VAT number', 'show' => true );
	return $fields;
} );

add_filter( 'woocommerce_email_order_meta_fields', function ( $fields, $sent_to_admin, $order ) {
	$vat = $order->get_meta( '_billing_vat_number' );
	if ( $vat ) { $fields['billing_vat_number'] = array( 'label' => 'EU VAT number', 'value' => $vat ); }
	return $fields;
}, 10, 3 );

/** The same optional VAT number on My account → Addresses → Billing (stored as user meta, prefilled at checkout). */
add_filter( 'woocommerce_address_to_edit', function ( $address, $load_address ) {
	if ( 'billing' === $load_address ) {
		$address['billing_vat_number'] = array(
			'label'        => 'EU VAT number',
			'required'     => false,
			'type'         => 'text',
			'class'        => array( 'form-row-wide' ),
			'priority'     => 125,
			'autocomplete' => 'off',
			'custom_attributes' => array( 'maxlength' => 20 ),
			'value'        => get_user_meta( get_current_user_id(), 'billing_vat_number', true ),
		);
	}
	return $address;
}, 10, 2 );

add_filter( 'woocommerce_process_myaccount_field_billing_vat_number', function ( $value ) {
	return strtoupper( preg_replace( '/[\s.\-]+/', '', (string) $value ) );
} );

add_action( 'woocommerce_after_save_address_validation', function ( $user_id, $load_address, $address ) {
	if ( 'billing' !== $load_address ) { return; }
	$v = strtoupper( preg_replace( '/[\s.\-]+/', '', (string) wp_unslash( $_POST['billing_vat_number'] ?? '' ) ) );
	if ( '' !== $v && ! preg_match( '/^[A-Z]{2}[A-Z0-9]{2,12}$/', $v ) ) {
		wc_add_notice( '<strong>EU VAT number</strong> must start with the country code, e.g. DE123456789.', 'error' );
	}
}, 10, 3 );

/** Company name on top of the billing form (checkout + My account). Visibility option: woocommerce_checkout_company_field = optional. */
add_filter( 'woocommerce_billing_fields', function ( $fields ) {
	if ( isset( $fields['billing_company'] ) ) {
		$fields['billing_company']['label']    = 'Company name';
		$fields['billing_company']['priority'] = 5;
		$fields['billing_company']['class']    = array( 'form-row-wide' );
	}
	return $fields;
}, 20 );

/** Our customers must confirm their e-mail before they can log in, so WooCommerce's "Confirm email to check for past orders" prompt is redundant. */
add_filter( 'woocommerce_customer_email_verification_should_show_prompt', '__return_false' );

add_filter( 'woocommerce_order_button_text', function () { return 'Order with obligation to pay'; } );
