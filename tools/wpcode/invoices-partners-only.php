/* WPCode snippet "Invoices: automatic only for shops and distributors".
 * Germanized Pro creates invoices automatically (timing: when a transactional e-mail is sent, PDF attached);
 * this limits the automation to orders of partner accounts (roles partner_shop / partner_distributor).
 * Consumers get no automatic invoice; an invoice can still be created by hand in the order screen. */
add_filter( 'storeabill_woo_auto_sync_order_invoices', function ( $sync, $order_id, $order ) {
	if ( ! $sync ) { return false; }
	$wc_order = wc_get_order( $order_id );
	$user     = $wc_order && $wc_order->get_customer_id() ? get_userdata( $wc_order->get_customer_id() ) : false;
	return $user && array_intersect( array( 'partner_shop', 'partner_distributor' ), (array) $user->roles ) ? $sync : false;
}, 10, 3 );
