<?php
/** 3D record viewer — front/back sleeve + both labels of the current product. */
$pid = i7_pid( $context ?? array(), $post_id ?? 0 );
$term = i7_series_of( $pid ); $s = i7_accent( $term ); $title = get_the_title( $pid );
$u = fn( $f ) => ( $id = get_field( $f, $pid ) ) ? wp_get_attachment_image_url( (int) $id, 'full' ) : '';
$front = $u( 'cover_front' ); $back = $u( 'cover_back' ); $la = $u( 'label_a' ); $lb = $u( 'label_b' );
$views = 'lr' === $s ? array( 'front' => 'Front', 'back' => 'Back', 'out' => 'Pull out the record', 'spin' => 'Spin' ) : array( 'a' => 'Side A', 'b' => 'Side B', 'spin' => 'Spin' );
?>
<div class="wp-block-group rec-viewer">
	<div class="stage" id="stage" tabindex="0" role="img" aria-label="3D view of the record. Drag to rotate, pinch to zoom, double-click to reset."
		data-mode="<?php echo esc_attr( $s ); ?>" data-front="<?php echo esc_url( $front ); ?>" data-back="<?php echo esc_url( $back ); ?>" data-label-a="<?php echo esc_url( $la ); ?>" data-label-b="<?php echo esc_url( $lb ); ?>">
		<canvas id="c"></canvas>
		<img class="fallback" src="<?php echo esc_url( 'lr' === $s ? $front : $la ); ?>" alt="<?php echo esc_attr( $title ); ?>">
		<p class="hint" id="hint">Drag to turn · pinch to zoom · double-click to reset</p>
	</div>
	<div class="views" role="group" aria-label="View" id="views">
		<?php $i = 0; foreach ( $views as $v => $label ) : ?>
			<button type="button" data-v="<?php echo esc_attr( $v ); ?>" aria-pressed="<?php echo 0 === $i++ ? 'true' : 'false'; ?>"><?php echo esc_html( $label ); ?></button>
		<?php endforeach; ?>
	</div>
</div>
