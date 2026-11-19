/* WPCode snippet "Emails: German footer". Order e-mails are sent in the order's language (Polylang for WooCommerce
 * switches the locale); the footer text is stored in English, so German e-mails get the German version here. */
add_filter( 'option_woocommerce_email_footer_text', function ( $text ) {
	if ( 0 !== strpos( determine_locale(), 'de' ) ) { return $text; }
	return 'Vibetown Entertainment (7inch.rare) · Inhaber: Philipp Mühlen · Harkortstr. 29 · 48163 Münster · Deutschland · USt-IdNr. DE207201101'
		. '<br><a href="' . esc_url( home_url( '/de/agb/' ) ) . '">AGB</a> · <a href="' . esc_url( home_url( '/de/widerrufsbelehrung/' ) ) . '">Widerruf</a>';
} );
