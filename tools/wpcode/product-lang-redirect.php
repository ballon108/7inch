<?php
/**
 * WPCode snippet: "Polylang: /de/product/<en-slug>/ → German product".
 * Location: Run everywhere (front end).
 *
 * German products have their own slugs (mp-08-2), but /de/product/mp-08/ still resolves to the English product,
 * so the page is English while the URL is German. Redirect to the translation in the language of the URL; the other way round too.
 */
add_action( 'template_redirect', function () {
	if ( ! is_singular( 'product' ) || ! function_exists( 'pll_current_language' ) || ! function_exists( 'pll_get_post' ) ) { return; }
	$cur  = pll_current_language();            // language of the URL (/de/ prefix → de).
	$id   = get_queried_object_id();
	$lang = pll_get_post_language( $id );     // language of the product that was found.
	if ( ! $cur || ! $lang || $cur === $lang ) { return; }
	$tr = pll_get_post( $id, $cur );
	if ( $tr && 'publish' === get_post_status( $tr ) ) {
		wp_safe_redirect( get_permalink( $tr ), 301 );
		exit;
	}
}, 1 );
