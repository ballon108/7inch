<?php
/** Hero carousel — featured releases. */
$out  = i7_field( 'badge_out', 'Out now' );
$pre  = i7_field( 'badge_pre', 'Pre-order' );
$plead = i7_field( 'pre_lead', 'Pre-orders are open. Secure your copy before the run is pressed.' );
$cv   = i7_field( 'cta_view', 'View release' );
$cp   = i7_field( 'cta_pre', 'Pre-order now' );
$ca   = i7_field( 'cta_all', 'All releases' );
$url0 = i7_field( 'cta_url', '' );

$releases = i7_releases( array(
	'meta_query' => array( array( 'key' => 'featured', 'value' => '1' ) ),
	'meta_key' => 'hero_order', 'orderby' => 'meta_value_num', 'order' => 'ASC', 'numberposts' => 4,
) );
if ( ! $releases ) { echo '<p class="i7-empty">Mark releases as “Show in hero carousel” to fill this block.</p>'; return; }
?>
<section id="home" class="wp-block-group hero"><h1 class="screen-reader-text">7inch.rare - Music Shop</h1><div class="wp-block-group wrap"><div class="wp-block-group hero-slides">
<?php foreach ( $releases as $i => $r ) :
	$term = i7_series_of( $r->ID );
	$s    = i7_accent( $term );
	$st   = i7_status( $r->ID );
	$ispre = ( 'pre' === $st );
	$a = get_field( 'side_a', $r->ID ); $b = get_field( 'side_b', $r->ID );
	$lead = ( $ispre ? $plead . ' ' : '' ) . ( $term ? get_field( 'hero_lead', $term ) : '' ) . ( $a || $b ? ' A: ' . $a . ' · B: ' . $b : '' );
	$badge = ( $ispre ? $pre : $out ) . ' · ' . ( $term ? $term->name : '' );
	$title = get_the_title( $r );
	$url   = $url0 ?: get_permalink( $r );
?>
	<div class="wp-block-group hero-slide <?php echo esc_attr( $s ); ?>" data-title="<?php echo esc_attr( $title ); ?>">
		<div class="wp-block-group htext">
			<p class="badge has-<?php echo esc_attr( $s ); ?>-color has-text-color"><?php echo esc_html( $badge ); ?></p>
			<h2 class="wp-block-heading"><?php echo esc_html( $title ); ?></h2>
			<p class="lead"><?php echo esc_html( trim( $lead ) ); ?></p>
			<div class="wp-block-buttons ctas">
				<div class="wp-block-button btn-fill"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( $url ); ?>"><?php echo esc_html( $ispre ? $cp : $cv ); ?></a></div>
				<div class="wp-block-button btn-ghost"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( $url ); ?>"><?php echo esc_html( $ca ); ?></a></div>
			</div>
			<div class="wp-block-group dots"></div>
		</div>
		<div class="wp-block-group scene <?php echo esc_attr( $s ); ?>">
			<?php if ( $ispre ) : ?><p class="pre"><?php echo esc_html( $pre ); ?></p><?php endif; ?>
			<div class="wp-block-group float">
				<div class="wp-block-group disc"><?php echo i7_img( get_field( 'label_a', $r->ID ), 'lr' === $s ? '' : $title . ' label', '', $i > 0 ); // phpcs:ignore ?></div>
				<?php if ( 'lr' === $s ) { echo i7_img( get_field( 'cover_front', $r->ID ), $title . ' cover', 'sleeve', $i > 0 ); } // phpcs:ignore ?>
			</div>
			<div class="wp-block-group pod"></div>
		</div>
	</div>
<?php endforeach; ?>
</div></div></section>
