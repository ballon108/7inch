<?php
/** Side A / Side B with audio previews. */
$pid = i7_pid( $context ?? array(), $post_id ?? 0 ); $s = i7_accent( i7_series_of( $pid ) );
$play = i7_field( 'play_label', 'Play preview' ); $pause = i7_field( 'pause_label', 'Pause' );
$ico_play = '<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M4 2.5v11l9-5.5z"/></svg>';
?>
<ol class="tracks" data-series="<?php echo esc_attr( $s ); ?>" data-play="<?php echo esc_attr( $play ); ?>" data-pause="<?php echo esc_attr( $pause ); ?>">
<?php foreach ( array( 'a' => 'A', 'b' => 'B' ) as $k => $L ) :
	$name = get_field( 'side_' . $k, $pid ); if ( ! $name ) { continue; }
	$note = get_field( 'note_' . $k, $pid ); $aid = get_field( 'audio_' . $k, $pid ); $url = $aid ? wp_get_attachment_url( (int) $aid ) : '';
?>
	<li>
		<span class="side has-<?php echo esc_attr( $s ); ?>-color has-text-color"><?php echo esc_html( $L ); ?></span>
		<span class="t"><?php echo esc_html( $name ); ?><?php if ( $note ) : ?><small><?php echo esc_html( $note ); ?></small><?php endif; ?></span>
		<?php if ( $url ) : ?><button type="button" class="play" data-side="<?php echo esc_attr( $k ); ?>" data-audio="<?php echo esc_url( $url ); ?>" aria-label="<?php echo esc_attr( $play . ' – Side ' . $L ); ?>"><?php echo $ico_play; // phpcs:ignore ?><span class="ring"></span></button><?php endif; ?>
	</li>
<?php endforeach; ?>
</ol>
