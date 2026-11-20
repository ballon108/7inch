/* WPCode snippet "Media: convert uploaded JPG/PNG to WebP".
 * Every JPG/PNG added to the Media Library (upload, drag & drop, sideload/import) is converted to WebP right after
 * upload: the original file is replaced, so the attachment, all thumbnails and the full-size image are WebP.
 * PNG transparency is kept (WebP supports an alpha channel). Quality 82 (set in the theme: inc/images.php). */
function i7_webp_convert_upload( $upload ) {
	if ( ! empty( $upload['error'] ) || empty( $upload['file'] ) || empty( $upload['type'] ) ) { return $upload; }
	if ( ! in_array( $upload['type'], array( 'image/jpeg', 'image/png' ), true ) ) { return $upload; }
	if ( ! apply_filters( 'i7_convert_upload_to_webp', true, $upload ) ) { return $upload; }

	$editor = wp_get_image_editor( $upload['file'] );
	if ( is_wp_error( $editor ) || ! method_exists( $editor, 'save' ) ) { return $upload; }

	$dir  = dirname( $upload['file'] );
	$name = wp_unique_filename( $dir, preg_replace( '/\.(jpe?g|png)$/i', '', basename( $upload['file'] ) ) . '.webp' );
	$new  = $dir . '/' . $name;
	$editor->set_quality( 82 );
	$saved = $editor->save( $new, 'image/webp' );
	if ( is_wp_error( $saved ) || empty( $saved['path'] ) || ! file_exists( $saved['path'] ) || filesize( $saved['path'] ) < 100 ) { return $upload; }

	@unlink( $upload['file'] );
	$upload['file'] = $saved['path'];
	$upload['url']  = trailingslashit( dirname( $upload['url'] ) ) . basename( $saved['path'] );
	$upload['type'] = 'image/webp';
	return $upload;
}
add_filter( 'wp_handle_upload', 'i7_webp_convert_upload', 20 );
add_filter( 'wp_handle_sideload', 'i7_webp_convert_upload', 20 );
