/* WPCode snippet "Partner: body class". Location: Run everywhere (PHP).
 * Adds the body class "i7-partner" for Record shop / Distributor accounts (roles partner_shop, partner_distributor),
 * so theme JS can apply partner-only rules (e.g. bulk order minimum = pack of 10). */
add_filter( 'body_class', function ( $classes ) {
	if ( is_user_logged_in() ) {
		$roles = (array) wp_get_current_user()->roles;
		if ( array_intersect( array( 'partner_shop', 'partner_distributor' ), $roles ) ) { $classes[] = 'i7-partner'; }
	}
	return $classes;
} );
