<?php
$pid = i7_pid( $context ?? array(), $post_id ?? 0 ); $t = i7_series_of( $pid );
$ed = (int) get_field( 'edition', $pid ); $cat = get_field( 'cat_no', $pid );
$rows = array_filter( array(
	'Format' => '7" vinyl',
	'Edition' => $ed ? $ed . ' copies' : '',
	'Year' => get_field( 'year', $pid ),
	'Cat. no.' => $cat,
	'Pressed in' => get_field( 'pressed_in', $pid ),
) );
?>
<dl class="facts"><?php foreach ( $rows as $k => $v ) : ?><div><dt><?php echo esc_html( $k ); ?></dt><dd><?php echo esc_html( $v ); ?></dd></div><?php endforeach; ?></dl>
