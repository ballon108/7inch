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
	// Dark mode only.
	echo '<meta name="color-scheme" content="dark">' . "\n";
}, 1 );

/* ── SCF / ACF integration ─────────────────────────────────────────
 * Data model (post type "release", taxonomy "series", field groups) lives in
 * /acf-json and is loaded by Secure Custom Fields as Local JSON.
 * Interface blocks live in /blocks (block.json + render.php, rendered by SCF). */
require_once get_stylesheet_directory() . '/inc/helpers.php';
require_once get_stylesheet_directory() . '/inc/partners.php';
require_once get_stylesheet_directory() . '/inc/shipping.php';
require_once get_stylesheet_directory() . '/inc/checkout-fields.php';
require_once get_stylesheet_directory() . '/inc/images.php';
require_once get_stylesheet_directory() . '/inc/taxes.php';

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

/* ── Customer registration: /register/ page + "Create account" button on My account ────────────
 * WooCommerce's own handler processes the POST (nonce "woocommerce-register"); the combined
 * login/register columns stay off, so My account shows only the login form plus a button. */
add_shortcode( 'i7_register_form', function () {
	if ( is_user_logged_in() ) {
		return '<p class="pp-note">You already have an account. <a href="' . esc_url( wc_get_page_permalink( 'myaccount' ) ) . '">Go to My account</a></p>';
	}
	ob_start();
	wc_print_notices();
	?>
	<div class="woocommerce"><form method="post" class="woocommerce-form woocommerce-form-register register" action="<?php echo esc_url( get_permalink() ); ?>">
		<?php do_action( 'woocommerce_register_form_start' ); ?>
		<p class="woocommerce-form-row woocommerce-form-row--wide form-row form-row-wide">
			<label for="reg_email">Email address&nbsp;<span class="required" aria-hidden="true">*</span></label>
			<input type="email" class="woocommerce-Input woocommerce-Input--text input-text" name="email" id="reg_email" autocomplete="email" required value="<?php echo ! empty( $_POST['email'] ) ? esc_attr( wp_unslash( $_POST['email'] ) ) : ''; // phpcs:ignore ?>" />
		</p>
		<?php if ( 'no' === get_option( 'woocommerce_registration_generate_password' ) ) : ?>
		<p class="woocommerce-form-row woocommerce-form-row--wide form-row form-row-wide">
			<label for="reg_password">Password&nbsp;<span class="required" aria-hidden="true">*</span></label>
			<input type="password" class="woocommerce-Input woocommerce-Input--text input-text" name="password" id="reg_password" autocomplete="new-password" required />
		</p>
		<?php else : ?>
		<p class="pp-note">A link to set your password will be sent to your email address.</p>
		<?php endif; ?>
		<?php do_action( 'woocommerce_register_form' ); ?>
		<p class="woocommerce-form-row form-row">
			<?php wp_nonce_field( 'woocommerce-register', 'woocommerce-register-nonce' ); ?>
			<button type="submit" class="woocommerce-Button woocommerce-button button woocommerce-form-register__submit" name="register" value="Register">Create account</button>
		</p>
		<?php do_action( 'woocommerce_register_form_end' ); ?>
	</form></div>
	<?php
	return ob_get_clean();
} );

add_action( 'woocommerce_after_customer_login_form', function () {
	echo '<div class="wp-block-buttons ctas i7-create-account"><p class="pp-note">For distributors and shops</p><div class="wp-block-button btn-ghost"><a class="wp-block-button__link wp-element-button" href="' . esc_url( home_url( '/partners-register/' ) ) . '">Create account</a></div></div>';
} );


/* Dark mode only: no Day/Night switch, the theme is fixed. */
add_filter( 'language_attributes', function ( $out ) { return $out . ' data-theme="dark"'; } );


/* Partner application form: searchable country select (WooCommerce's selectWoo, same look as checkout / account). */
add_action( 'wp_enqueue_scripts', function () {
	if ( ! is_page( 'partners-register' ) || ! wp_script_is( 'selectWoo', 'registered' ) ) { return; }
	wp_enqueue_style( 'select2' );
	wp_enqueue_script( 'selectWoo' );
	wp_add_inline_script( 'selectWoo', "jQuery(function($){var s=$('.pf-form select[name=country]');if(!s.length||!$.fn.selectWoo)return;"
		. "var init=function(){s.selectWoo({width:'100%',placeholder:'Select country',dropdownParent:s.closest('.pf')});};init();"
		. "document.addEventListener('wpcf7reset',function(){s.val('').trigger('change');});});" );
}, 20 );
