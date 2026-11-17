<?php
/** Series panels — built from the "product_cat" taxonomy. */
$terms = get_terms( array( 'taxonomy' => 'product_cat', 'hide_empty' => false, 'meta_key' => 'panel_order', 'orderby' => 'meta_value_num', 'order' => 'ASC' ) );
if ( is_wp_error( $terms ) || ! $terms ) { echo '<p class="i7-empty">Add terms to the Product categories.</p>'; return; }
?>
<section id="series" class="wp-block-group band"><div class="wp-block-group wrap">
	<div class="wp-block-group head"><div class="wp-block-group">
		<p class="eyebrow"><?php echo esc_html( i7_field( 'eyebrow', 'Two series' ) ); ?></p>
		<h2 class="wp-block-heading"><?php echo esc_html( i7_field( 'heading', 'Pick your side of the map.' ) ); ?></h2>
	</div></div>
	<div class="wp-block-group series">
	<?php foreach ( $terms as $t ) :
		$s = i7_accent( $t );
		$logo = get_field( 'panel_logo', $t ); $bg = get_field( 'panel_image', $t );
	?>
		<div class="wp-block-group panel <?php echo esc_attr( $s ); ?>">
			<?php echo $bg ? i7_img( $bg, $t->name, 'bgimg' ) : ''; // phpcs:ignore ?>
			<?php echo $logo ? i7_img( $logo, $t->name, 'logo-big' ) : ''; // phpcs:ignore ?>
			<p class="eyebrow <?php echo 'mp' === $s ? 'ep' : 'el'; ?>"><?php echo esc_html( get_field( 'eyebrow', $t ) ); ?></p>
			<h3 class="wp-block-heading"><?php echo esc_html( $t->name ); ?></h3>
			<p><?php echo esc_html( get_field( 'blurb', $t ) ); ?></p>
			<p class="go"><?php echo esc_html( get_field( 'cta', $t ) ?: 'Explore ' . $t->name ); ?></p>
		</div>
	<?php endforeach; ?>
	</div>
</div></section>
