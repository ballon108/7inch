<?php
$pid = i7_pid( $context ?? array(), $post_id ?? 0 );
$t = i7_series_of( $pid ); $s = i7_accent( $t );
?>
<p class="badge has-<?php echo esc_attr( $s ); ?>-color has-text-color"><?php echo esc_html( ( $t ? $t->name : '' ) . ' · ' . i7_status_label( i7_status( $pid ) ) ); ?></p>
