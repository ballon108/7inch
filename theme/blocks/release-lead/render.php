<?php
/* Lead text = the product's own description (Product description editor). Falls back to the series lead + edition size. */
$pid  = i7_pid( $context ?? array(), $post_id ?? 0 );
$pre  = 'pre' === i7_status( $pid ) ? 'Pre-orders are open. Secure your copy before the run is pressed. ' : '';
$desc = trim( (string) get_post_field( 'post_content', $pid ) );
if ( '' !== $desc ) {
	$html = wpautop( wp_kses_post( $desc ) );
	$html = preg_replace( '/<p(\s[^>]*)?>/', '<p class="lead">', $html );
	if ( $pre ) {
		$html = '<p class="lead">' . esc_html( trim( $pre ) ) . '</p>' . $html;
	}
	echo $html; // phpcs:ignore WordPress.Security.EscapeOutput
	return;
}
$t = i7_series_of( $pid ); $ed = (int) get_field( 'edition', $pid );
$lead = $pre . ( $t ? get_field( 'hero_lead', $t ) : '' ) . ( $ed ? sprintf( ' Limited to %d copies.', $ed ) : '' );
?>
<p class="lead"><?php echo esc_html( trim( $lead ) ); ?></p>
