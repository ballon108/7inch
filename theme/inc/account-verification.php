<?php
/**
 * E-mail confirmation for commercial accounts (Shop / Distributor).
 *
 * B2BKing registration roles flagged with meta `_i7_email_verify` create the account as "pending"
 * (b2bking_account_approved = no, B2BKing logs the user out). We e-mail a one-time link; opening it
 * activates the account itself and puts the user in the customer group configured on the role
 * (`b2bking_custom_role_automatic_approval_group`). Other roles keep admin-only approval.
 */

const I7_VERIFY_META = '_i7_email_verify';
const I7_VERIFY_TTL  = 3 * DAY_IN_SECONDS;

/** Group ID the user gets after confirming, or null when this account is not e-mail-activated. */
function i7_verify_group( $user_id ) {
	$role = get_user_meta( $user_id, 'b2bking_registration_role', true );
	if ( ! is_string( $role ) || 0 !== strpos( $role, 'role_' ) ) { return null; }
	$rid = (int) substr( $role, 5 );
	if ( ! $rid || ! get_post_meta( $rid, '_i7_email_verify', true ) ) { return null; }
	$g = get_post_meta( $rid, 'b2bking_custom_role_automatic_approval_group', true );
	return preg_match( '/^group_(\d+)$/', (string) $g, $m ) ? (int) $m[1] : null;
}

function i7_send_verification( $user_id ) {
	if ( get_user_meta( $user_id, I7_VERIFY_META, true ) ) { return; }
	$user = get_userdata( $user_id );
	if ( ! $user ) { return; }
	$token = wp_generate_password( 40, false, false );
	update_user_meta( $user_id, I7_VERIFY_META, array( 'hash' => hash( 'sha256', $token ), 'exp' => time() + I7_VERIFY_TTL ) );
	$link = add_query_arg( array( 'i7_verify' => $token, 'uid' => $user_id ), home_url( '/' ) );
	$body = "Hello,\n\nthank you for registering at 7inch.rare. Please confirm your e-mail address to activate your trade account:\n\n"
		. $link . "\n\nThe link is valid for 3 days. If you did not register, you can ignore this message.\n\n7inch.rare";
	wp_mail( $user->user_email, 'Confirm your e-mail address – 7inch.rare', $body );
}

/* Registration creates the account as "pending" – send the link as soon as both facts are known (either order). */
foreach ( array( 'added_user_meta', 'updated_user_meta' ) as $i7_hook ) {
	add_action( $i7_hook, function ( $mid, $user_id, $key ) {
		if ( ! in_array( $key, array( 'b2bking_account_approved', 'b2bking_registration_role' ), true ) ) { return; }
		if ( 'no' !== get_user_meta( $user_id, 'b2bking_account_approved', true ) ) { return; }
		if ( null === i7_verify_group( $user_id ) ) { return; }
		i7_send_verification( $user_id );
	}, 10, 3 );
}

/** Validates the token and activates the account. Returns true on success. */
function i7_verify_user( $user_id, $token ) {
	$rec   = get_user_meta( $user_id, I7_VERIFY_META, true );
	$group = i7_verify_group( $user_id );
	if ( ! is_array( $rec ) || ! $group || 'no' !== get_user_meta( $user_id, 'b2bking_account_approved', true ) ) { return false; }
	if ( $rec['exp'] < time() || ! hash_equals( $rec['hash'], hash( 'sha256', (string) $token ) ) ) { return false; }
	update_user_meta( $user_id, 'b2bking_account_approved', 'yes' );
	update_user_meta( $user_id, 'b2bking_b2buser', 'yes' );
	if ( function_exists( 'b2bking' ) ) { b2bking()->update_user_group( $user_id, $group ); }
	delete_user_meta( $user_id, I7_VERIFY_META );
	return true;
}

add_action( 'template_redirect', function () {
	if ( empty( $_GET['i7_verify'] ) || empty( $_GET['uid'] ) ) { return; } // phpcs:ignore WordPress.Security.NonceVerification
	$ok = i7_verify_user( (int) $_GET['uid'], sanitize_text_field( wp_unslash( $_GET['i7_verify'] ) ) ); // phpcs:ignore
	if ( function_exists( 'WC' ) && WC()->session ) {
		WC()->session->set_customer_session_cookie( true );
		wc_add_notice( $ok ? 'Thank you – your e-mail address is confirmed and your account is active. You can log in now.' : 'This confirmation link is invalid or has expired. Please contact us and we will activate your account.', $ok ? 'success' : 'error' );
	}
	wp_safe_redirect( function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'myaccount' ) : home_url( '/' ) );
	exit;
} );
