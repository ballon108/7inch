/* WPCode snippet "Partner: Legal Guarantee in My account". Location: Run everywhere (PHP).
 * Shows the EU "Legal Guarantee" label (WooCommerce Germanized) on the My account dashboard for Record shop /
 * Distributor accounts only. The label is switched off in the shop itself (Germanized > Shopmarks > Legal guarantee). */
add_action( 'woocommerce_account_dashboard', function () {
	if ( ! function_exists( 'wc_gzd_get_legal_guarantee_html' ) || ! is_user_logged_in() ) { return; }
	if ( ! array_intersect( array( 'partner_shop', 'partner_distributor' ), (array) wp_get_current_user()->roles ) ) { return; }
	echo '<div class="i7-legal-guarantee" style="margin-top:32px">' . wc_gzd_get_legal_guarantee_html( 'preview', '', 'account' ) . '</div>';
}, 20 );
