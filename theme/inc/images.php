<?php
/**
 * Automatic WebP: resized copies of uploaded JPEG/PNG images (thumbnails, medium, large …)
 * are generated as WebP. The original upload stays untouched (used e.g. by the 3D record viewer).
 * Existing media keeps its current files until regenerated ("Regenerate Thumbnails").
 */
add_filter( 'image_editor_output_format', function ( $formats ) {
	$formats['image/jpeg'] = 'image/webp';
	$formats['image/png']  = 'image/webp';
	return $formats;
}, 20 );

add_filter( 'wp_editor_set_quality', function ( $quality, $mime ) {
	return 'image/webp' === $mime ? 82 : $quality;
}, 10, 2 );
