<?php
/**
 * 7inch — child theme of Twenty Twenty-Five.
 */
add_action( 'wp_enqueue_scripts', function () {
	$dir = get_stylesheet_directory();
	$uri = get_stylesheet_directory_uri();
	wp_enqueue_style( '7inch-style', get_stylesheet_uri(), array(), filemtime( $dir . '/style.css' ) );
	wp_enqueue_script( '7inch-site', $uri . '/assets/js/site.js', array(), filemtime( $dir . '/assets/js/site.js' ), array( 'in_footer' => true, 'strategy' => 'defer' ) );
	if ( function_exists( 'is_product' ) && is_product() ) {
		wp_enqueue_script( '7inch-product', $uri . '/assets/js/product.js', array(), filemtime( $dir . '/assets/js/product.js' ), array( 'in_footer' => true, 'strategy' => 'defer' ) );
		wp_enqueue_script_module( '7inch-viewer', $uri . '/assets/js/record-viewer.js', array(), filemtime( $dir . '/assets/js/record-viewer.js' ) );
	}
} );

add_action( 'wp_head', function () {
	$f = get_stylesheet_directory_uri() . '/assets/fonts/';
	foreach ( array( 'inter-latin-400', 'inter-latin-500' ) as $font ) {
		echo '<link rel="preload" href="' . esc_url( $f . $font . '.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
	}
	// Apply saved Day/Night choice before first paint.
	echo '<script>try{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}catch(e){}</script>' . "\n";
}, 1 );

/* ── SCF / ACF integration ─────────────────────────────────────────
 * Data model (post type "release", taxonomy "series", field groups) lives in
 * /acf-json and is loaded by Secure Custom Fields as Local JSON.
 * Interface blocks live in /blocks (block.json + render.php, rendered by SCF). */
require_once get_stylesheet_directory() . '/inc/helpers.php';
require_once get_stylesheet_directory() . '/inc/account-verification.php';
require_once get_stylesheet_directory() . '/inc/partners.php';
require_once get_stylesheet_directory() . '/inc/shipping.php';
require_once get_stylesheet_directory() . '/inc/checkout-fields.php';
require_once get_stylesheet_directory() . '/inc/images.php';

add_filter( 'acf/settings/save_json', fn() => get_stylesheet_directory() . '/acf-json' );
add_filter( 'acf/settings/load_json', function ( $paths ) { $paths[] = get_stylesheet_directory() . '/acf-json'; return $paths; } );

add_action( 'init', function () {
	foreach ( glob( get_stylesheet_directory() . '/blocks/*/block.json' ) as $file ) {
		register_block_type( dirname( $file ) );
	}
} );

add_action( 'after_setup_theme', function () {
	add_theme_support( 'editor-styles' );
	add_editor_style( 'style.css' );
} );

/* ── Partner application (Contact Form 7) ───────────────────────────
 * The header's "For partners" button links to the /partners/ page, which holds
 * the CF7 form (created by tools/partner_form.py, id in option _7inch_partner_form). */
add_filter( 'wpcf7_load_css', '__return_false' );          // styled in style.css
add_filter( 'wpcf7_autop_or_not', '__return_false' );      // keep our markup as written

/* [i7_partner_login] — login form for partners; a short notice when already logged in. */
add_shortcode( 'i7_partner_login', function () {
	if ( is_user_logged_in() ) {
		return '<p class="pp-note">You are logged in. <a href="' . esc_url( wc_get_page_permalink( 'myaccount' ) ) . '">Go to My account</a> &middot; <a href="' . esc_url( wp_logout_url( get_permalink() ) ) . '">Log out</a></p>';
	}
	ob_start();
	woocommerce_login_form( array( 'redirect' => wc_get_page_permalink( 'myaccount' ) ) );
	return '<div class="woocommerce">' . ob_get_clean() . '</div>';
} );

/* Hide the WordPress admin bar for customer accounts (B2B shop / distributor, retail customers). */
add_filter( 'show_admin_bar', function ( $show ) {
	if ( ! is_user_logged_in() ) { return $show; }
	$user = wp_get_current_user();
	if ( array_intersect( array( 'partner_shop', 'partner_distributor', 'customer' ), (array) $user->roles ) && ! current_user_can( 'edit_posts' ) ) {
		return false;
	}
	return $show;
} );

/* Header "Partners" button → "Account" (straight to My account) when a customer is logged in. */
add_filter( 'render_block', function ( $html, $block ) {
	if ( ! is_user_logged_in() || false === strpos( $html, 'href="/partners/"' ) ) { return $html; }
	if ( false === strpos( $html, 'partner-btn' ) && false === strpos( $html, 'nav-partners' ) ) { return $html; }
	$account = esc_url( function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'myaccount' ) : home_url( '/my-account/' ) );
	return str_replace( array( 'href="/partners/">Partners<' ), array( 'href="' . $account . '">Account<' ), $html );
}, 10, 2 );

/* My account: hide "Subaccounts" (B2BKing) and "Downloads" from the account navigation. */
add_filter( 'woocommerce_account_menu_items', function ( $items ) {
	unset( $items['downloads'], $items['subaccounts'] );
	return $items;
}, 999 );

/* Old partner page URL → /partners/ */
add_action( 'template_redirect', function () {
	if ( is_404() && isset( $_SERVER['REQUEST_URI'] ) && 0 === strpos( wp_parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH ), '/for-partners' ) ) {
		wp_safe_redirect( home_url( '/partners/' ), 301 );
		exit;
	}
} );
