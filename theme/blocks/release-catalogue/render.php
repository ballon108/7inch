<?php
/** Release catalogue with series filter. */
$terms = get_terms( array( 'taxonomy' => 'product_cat', 'hide_empty' => true, 'meta_key' => 'panel_order', 'orderby' => 'meta_value_num', 'order' => 'ASC' ) );
$releases = i7_releases();
?>
<section id="releases" class="wp-block-group band"><div class="wp-block-group wrap">
	<div class="wp-block-group head">
		<div class="wp-block-group">
			<p class="eyebrow"><?php echo esc_html( i7_field( 'eyebrow', 'Catalogue' ) ); ?></p>
			<h2 class="wp-block-heading"><?php echo esc_html( i7_field( 'heading', 'All releases' ) ); ?></h2>
		</div>
		<div class="wp-block-buttons filters">
			<div class="wp-block-button filter f-all is-active"><a class="wp-block-button__link wp-element-button" href="#"><?php echo esc_html( i7_field( 'filter_all', 'All' ) ); ?></a></div>
			<?php if ( ! is_wp_error( $terms ) ) foreach ( $terms as $t ) : ?>
				<div class="wp-block-button filter f-<?php echo esc_attr( i7_accent( $t ) ); ?>"><a class="wp-block-button__link wp-element-button" href="#"><?php echo esc_html( $t->name ); ?></a></div>
			<?php endforeach; ?>
		</div>
	</div>
	<div class="wp-block-group grid">
	<?php foreach ( $releases as $r ) { echo i7_card( $r ); } // phpcs:ignore ?>
	</div>
</div></section>
