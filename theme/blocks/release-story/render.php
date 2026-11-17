<?php
/** Series story + both labels. */
$pid = i7_pid( $context ?? array(), $post_id ?? 0 ); $t = i7_series_of( $pid ); $s = i7_accent( $t ); $title = get_the_title( $pid );
?>
<section class="wp-block-group band"><div class="wp-block-group wrap story">
	<div class="wp-block-group">
		<p class="eyebrow has-<?php echo esc_attr( $s ); ?>-color has-text-color"><?php echo esc_html( $t ? $t->name : '' ); ?></p>
		<h2 class="wp-block-heading"><?php echo esc_html( $t ? get_field( 'story_heading', $t ) : '' ); ?></h2>
		<p style="margin-top:var(--wp--preset--spacing--40)"><?php echo esc_html( $t ? get_field( 'story_text', $t ) : '' ); ?></p>
	</div>
	<div class="wp-block-group labels">
		<?php foreach ( array( 'a' => 'Side A', 'b' => 'Side B' ) as $k => $L ) : $img = get_field( 'label_' . $k, $pid ); if ( ! $img ) { continue; } ?>
			<figure><?php echo i7_img( $img, $title . ' ' . strtolower( $L ) . ' label' ); // phpcs:ignore ?><figcaption><?php echo esc_html( $L . ' · ' . get_field( 'side_' . $k, $pid ) ); ?></figcaption></figure>
		<?php endforeach; ?>
	</div>
</div></section>
