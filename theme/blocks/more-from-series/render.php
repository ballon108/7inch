<?php
$pid = i7_pid( $context ?? array(), $post_id ?? 0 ); $t = i7_series_of( $pid );
$more = $t ? i7_releases( array( 'numberposts' => 4, 'exclude' => array( $pid ), 'tax_query' => array( array( 'taxonomy' => 'product_cat', 'terms' => $t->term_id ) ) ) ) : array();
if ( ! $more ) { return; }
?>
<section class="wp-block-group band"><div class="wp-block-group wrap">
	<div class="wp-block-group head"><div class="wp-block-group">
		<p class="eyebrow"><?php echo esc_html( i7_field( 'eyebrow', 'Keep digging' ) ); ?></p>
		<h2 class="wp-block-heading"><?php echo esc_html( i7_field( 'heading', 'More from the series' ) ); ?></h2>
	</div></div>
	<div class="wp-block-group grid"><?php foreach ( $more as $r ) { echo i7_card( $r ); } // phpcs:ignore ?></div>
</div></section>
