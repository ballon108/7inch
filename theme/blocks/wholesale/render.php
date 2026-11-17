<?php
/** Wholesale call-to-action. */
$email = i7_field( 'email', 'peet@7inchrare.com' );
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
		<div class="wp-block-buttons ctas"><div class="wp-block-button btn-fill"><a class="wp-block-button__link wp-element-button" href="mailto:<?php echo esc_attr( antispambot( $email ) ); ?>"><?php echo esc_html( i7_field( 'button_label', 'Request the wholesale list' ) ); ?></a></div></div>
		<p class="mail"><?php echo esc_html( $email ); ?></p>
	</div>
</div></section>
