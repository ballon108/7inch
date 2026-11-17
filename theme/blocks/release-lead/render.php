<?php
$pid = i7_pid( $context ?? array(), $post_id ?? 0 );
$t = i7_series_of( $pid ); $ed = (int) get_field( 'edition', $pid );
$lead = ( 'pre' === i7_status( $pid ) ? 'Pre-orders are open. Secure your copy before the run is pressed. ' : '' ) . ( $t ? get_field( 'hero_lead', $t ) : '' ) . ( $ed ? sprintf( ' Limited to %d copies.', $ed ) : '' );
?>
<p class="lead"><?php echo esc_html( trim( $lead ) ); ?></p>
