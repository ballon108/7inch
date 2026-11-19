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

/** Cart-level minimum order quantity (B2BKing "minimum order" rule) for the current customer's group; 0 = none. */
function i7_group_minimum() {
	if ( ! is_user_logged_in() ) { return 0; }
	$gid = get_user_meta( get_current_user_id(), 'b2bking_customergroup', true );
	if ( ! $gid ) { return 0; }
	static $cache = array();
	if ( isset( $cache[ $gid ] ) ) { return $cache[ $gid ]; }
	$cache[ $gid ] = 0;
	$rules = get_posts( array( 'post_type' => 'b2bking_rule', 'numberposts' => -1, 'post_status' => 'publish', 'meta_query' => array( array( 'key' => 'b2bking_rule_what', 'value' => 'minimum_order' ) ) ) );
	foreach ( $rules as $r ) {
		if ( 'group_' . $gid === get_post_meta( $r->ID, 'b2bking_rule_who', true ) && 'quantity' === get_post_meta( $r->ID, 'b2bking_rule_quantity_value', true ) ) {
			$cache[ $gid ] = (int) get_post_meta( $r->ID, 'b2bking_rule_howmuch', true );
			break;
		}
	}
	return $cache[ $gid ];
}

/** Catalogue card (also used by "More from the series"). */
function i7_card( $r, $filter = 'all' ) {
	$t = i7_series_of( $r->ID ); $s = i7_accent( $t ); $st = i7_status( $r->ID ); $title = get_the_title( $r );
	$thumb = get_post_thumbnail_id( $r->ID );
	$art = ( 'lr' === $s ) ? i7_img( $thumb, $title . ' cover' ) : '<div class="wp-block-group v">' . i7_img( $thumb, $title . ' label' ) . '</div>';
	$link = esc_url( get_permalink( $r ) );
	$prod = wc_get_product( $r->ID );
	$can  = 'out' !== $st && $prod && $prod->is_purchasable();
	$price_html = $prod ? $prod->get_price_html() : '';
	$qa   = $prod ? apply_filters( 'woocommerce_quantity_input_args', array( 'input_value' => 1, 'min_value' => 1, 'max_value' => '', 'step' => 1 ), $prod ) : array();
	$qmin = max( 1, (int) ( $qa['min_value'] ?? 1 ) ); $qstep = max( 1, (int) ( $qa['step'] ?? 1 ) );
	$qval = max( $qmin, i7_group_minimum(), (int) ( $qa['input_value'] ?? $qmin ) ); $qmax = ( isset( $qa['max_value'] ) && '' !== $qa['max_value'] && $qa['max_value'] > 0 ) ? (int) $qa['max_value'] : '';
	ob_start(); ?>
	<div class="wp-block-group card rel-<?php echo esc_attr( $s ); ?><?php echo ( 'all' !== $filter && $filter !== $s ) ? ' is-hidden' : ''; ?>">
		<div class="wp-block-group art"><?php echo $art; // phpcs:ignore ?></div>
		<p class="eyebrow has-mp-color has-text-color"><?php echo esc_html( $t ? $t->name : '' ); ?></p>
		<p class="ct"><a href="<?php echo $link; // phpcs:ignore ?>"><?php echo esc_html( $title ); ?></a></p>
		<div class="card-meta">
			<p class="st<?php echo 'out' === $st ? ' out has-mute-color' : ' has-mp-color'; ?> has-text-color"><?php echo esc_html( i7_status_label( $st ) ); ?></p>
			<?php if ( $price_html ) : ?><p class="card-price"><?php echo wp_kses_post( $price_html ); ?></p><?php endif; ?>
		</div>
		<?php if ( $can ) : ?>
		<form class="card-buy" method="post" action="<?php echo $link; // phpcs:ignore ?>">
			<div class="qty">
				<button type="button" data-step="-<?php echo (int) $qstep; ?>" aria-label="Decrease quantity">&minus;</button>
				<input type="number" name="quantity" value="<?php echo (int) $qval; ?>" min="<?php echo (int) $qmin; ?>" step="<?php echo (int) $qstep; ?>"<?php echo '' !== $qmax ? ' max="' . (int) $qmax . '"' : ''; ?> inputmode="numeric" aria-label="<?php echo esc_attr( 'Quantity: ' . $title ); ?>">
				<button type="button" data-step="<?php echo (int) $qstep; ?>" aria-label="Increase quantity">+</button>
			</div>
			<button type="submit" name="add-to-cart" value="<?php echo (int) $r->ID; ?>" class="card-add"><?php echo esc_html( 'pre' === $st ? 'Pre-order now' : 'Add to cart' ); ?></button>
		</form>
		<?php elseif ( 'out' !== $st && ! is_user_logged_in() ) : ?>
		<div class="card-buy"><a class="card-add" href="<?php echo esc_url( wc_get_page_permalink( 'myaccount' ) ); ?>">Log in to buy</a></div>
		<?php else : ?>
		<div class="card-buy"><span class="card-add is-disabled" aria-disabled="true"><?php echo esc_html( 'out' === $st ? 'Sold out' : 'Not available' ); ?></span></div>
		<?php endif; ?>
	</div>
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
