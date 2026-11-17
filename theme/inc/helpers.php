<?php
/** Rendering helpers shared by the SCF blocks (WooCommerce products = releases). */

function i7_img( $id, $alt = '', $cls = '', $lazy = true ) {
	if ( ! $id ) { return ''; }
	$img = wp_get_attachment_image( (int) $id, 'full', false, array( 'alt' => $alt, 'loading' => $lazy ? 'lazy' : 'eager', 'decoding' => 'async' ) );
	return '<figure class="wp-block-image size-full' . ( $cls ? ' ' . esc_attr( $cls ) : '' ) . '">' . $img . '</figure>';
}

/** The product's series = its (non-default) product category. */
function i7_series_of( $post_id ) {
	$terms = get_the_terms( $post_id, 'product_cat' );
	if ( ! $terms || is_wp_error( $terms ) ) { return null; }
	foreach ( $terms as $t ) { if ( 'uncategorized' !== $t->slug ) { return $t; } }
	return null;
}

function i7_accent( $term ) {
	$a = $term ? get_field( 'accent', $term ) : '';
	return in_array( $a, array( 'mp', 'lr' ), true ) ? $a : 'mp';
}

function i7_field( $name, $default = '' ) {
	$v = get_field( $name );
	return ( $v === null || $v === false || $v === '' ) ? $default : $v;
}

/** Block's product ID: current product on the front end / template context in the editor. */
function i7_pid( $context = array(), $post_id = 0 ) {
	$id = get_the_ID();
	if ( ! $id && ! empty( $context['postId'] ) ) { $id = (int) $context['postId']; }
	return $id ?: (int) $post_id;
}

/** in | out | pre — derived from the WooCommerce stock status. */
function i7_status( $product_id ) {
	$p = wc_get_product( $product_id );
	if ( ! $p ) { return 'in'; }
	$s = $p->get_stock_status();
	return 'outofstock' === $s ? 'out' : ( 'onbackorder' === $s ? 'pre' : 'in' );
}

function i7_status_label( $st ) {
	$map = array( 'in' => 'In stock', 'out' => 'Sold out', 'pre' => 'Pre-order' );
	return $map[ $st ] ?? $map['in'];
}

function i7_releases( $args = array() ) {
	return get_posts( array_merge( array( 'post_type' => 'product', 'numberposts' => -1, 'post_status' => 'publish', 'orderby' => 'menu_order title', 'order' => 'ASC' ), $args ) );
}

/** Catalogue card (also used by "More from the series"). */
function i7_card( $r ) {
	$t = i7_series_of( $r->ID ); $s = i7_accent( $t ); $st = i7_status( $r->ID ); $title = get_the_title( $r );
	$thumb = get_post_thumbnail_id( $r->ID );
	$art = ( 'lr' === $s ) ? i7_img( $thumb, $title . ' cover' ) : '<div class="wp-block-group v">' . i7_img( $thumb, $title . ' label' ) . '</div>';
	ob_start(); ?>
	<a class="wp-block-group card rel-<?php echo esc_attr( $s ); ?>" href="<?php echo esc_url( get_permalink( $r ) ); ?>">
		<div class="wp-block-group art"><?php echo $art; // phpcs:ignore ?></div>
		<p class="eyebrow has-<?php echo esc_attr( $s ); ?>-color has-text-color"><?php echo esc_html( $t ? $t->name : '' ); ?></p>
		<p class="ct"><?php echo esc_html( $title ); ?></p>
		<p class="st<?php echo 'out' === $st ? ' out has-mute-color' : ' has-' . esc_attr( $s ) . '-color'; ?> has-text-color"><?php echo esc_html( i7_status_label( $st ) ); ?></p>
	</a>
	<?php
	return ob_get_clean();
}

/* Add-to-cart wording from the mockup. */
add_filter( 'woocommerce_product_single_add_to_cart_text', function ( $text, $product ) {
	return 'onbackorder' === $product->get_stock_status() ? 'Pre-order now' : 'Add to cart';
}, 10, 2 );
add_filter( 'woocommerce_product_add_to_cart_text', function ( $text, $product ) {
	return 'onbackorder' === $product->get_stock_status() ? 'Pre-order now' : ( 'outofstock' === $product->get_stock_status() ? 'Sold out' : 'Add to cart' );
}, 10, 2 );
