<?php
/** Wholesale call-to-action. */
/* The button leads to the partner page (login + registration), in the current language. */
$partners = get_page_by_path( 'partners' );
$href     = $partners ? get_permalink( function_exists( 'pll_get_post' ) ? ( pll_get_post( $partners->ID ) ?: $partners->ID ) : $partners->ID ) : home_url( '/partners/' );
$stats = get_field( 'stats' );
if ( ! $stats ) { $stats = array( array( 'number' => '50', 'label' => 'copies minimum for record shops' ), array( 'number' => '100', 'label' => 'copies minimum for distributors' ) ); }
?>
<section id="trade" class="wp-block-group band"><div class="wp-block-group wrap trade">
	<div class="wp-block-group">
		<p class="eyebrow"><?php echo esc_html( i7_field( 'eyebrow', 'For record shops & distributors' ) ); ?></p>
		<h2 class="wp-block-heading"><?php echo esc_html( i7_field( 'heading', 'Stock the series in your shop.' ) ); ?></h2>
		<p class="lead" style="margin-top:var(--wp--preset--spacing--40)"><?php echo esc_html( i7_field( 'lead', 'Wholesale price list, pre-order windows and shipping options on request. We ship worldwide; the buyer pays freight.' ) ); ?></p>
	</div>
	<div class="wp-block-group nums">
	<?php foreach ( $stats as $row ) : ?>
		<div class="wp-block-group num"><p class="nb"><?php echo esc_html( $row['number'] ); ?></p><p class="nl"><?php echo esc_html( $row['label'] ); ?></p></div>
	<?php endforeach; ?>
	</div>
	<div class="wp-block-group ctas-row">
		<div class="wp-block-buttons ctas"><div class="wp-block-button btn-fill"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( $href ); ?>"><?php echo esc_html( i7_field( 'button_label', 'Request the wholesale list' ) ); ?></a></div></div>
	</div>
</div></section>
