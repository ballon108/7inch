<?php
/** Release catalogue with series filter. */
$terms = get_terms( array( 'taxonomy' => 'product_cat', 'hide_empty' => true, 'meta_key' => 'panel_order', 'orderby' => 'meta_value_num', 'order' => 'ASC' ) );
$releases = i7_releases();
$cur  = is_tax( 'product_cat' ) ? get_queried_object() : null;          // series page → start filtered
$curk = ( $cur && ! is_wp_error( $cur ) ) ? i7_accent( $cur ) : 'all';
$gmin = i7_group_minimum();
?>
<section id="releases" class="wp-block-group band"><div class="wp-block-group wrap">
	<div class="wp-block-group head">
		<div class="wp-block-group">
			<p class="eyebrow"><?php echo esc_html( i7_field( 'eyebrow', 'Catalogue' ) ); ?></p>
			<h2 class="wp-block-heading"><?php echo esc_html( i7_field( 'heading', 'All releases' ) ); ?></h2>
		</div>
		<div class="wp-block-buttons filters">
			<div class="wp-block-button filter f-all<?php echo 'all' === $curk ? ' is-active' : ''; ?>"><a class="wp-block-button__link wp-element-button" href="#"><?php echo esc_html( i7_field( 'filter_all', 'All' ) ); ?></a></div>
			<?php if ( ! is_wp_error( $terms ) ) foreach ( $terms as $t ) : ?>
				<div class="wp-block-button filter f-<?php echo esc_attr( i7_accent( $t ) ); ?><?php echo i7_accent( $t ) === $curk ? ' is-active' : ''; ?>"><a class="wp-block-button__link wp-element-button" href="#"><?php echo esc_html( $t->name ); ?></a></div>
			<?php endforeach; ?>
		</div>
	</div>
	<?php if ( $gmin ) : ?>
	<p class="b2b-note">Minimum order for your account: <strong><?php echo (int) $gmin; ?> records</strong> in total, across all titles. Your trade prices apply automatically in the basket.</p>
	<?php endif; ?>
	<div class="wp-block-group grid">
	<?php foreach ( $releases as $r ) { echo i7_card( $r, $curk ); } // phpcs:ignore ?>
	</div>
</div></section>
