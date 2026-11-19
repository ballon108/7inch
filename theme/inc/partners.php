<?php
/**
 * Partner roles (Record shop / Distributor) and their link to B2BKing.
 * Wholesale prices, quantity tiers and minimum order quantities live in B2BKing
 * (groups "Shop" and "Distributor" + dynamic rules), not in the theme.
 * Assigning one of the partner roles puts the user in the matching B2BKing group.
 */

add_action( 'init', function () {
	if ( ! get_role( 'partner_shop' ) )        { add_role( 'partner_shop', 'Partner: Record shop', array( 'read' => true ) ); }
	if ( ! get_role( 'partner_distributor' ) ) { add_role( 'partner_distributor', 'Partner: Distributor', array( 'read' => true ) ); }
} );

/** 'shop' | 'distributor' | '' for the current visitor. */
function i7_partner_type() {
	if ( ! is_user_logged_in() ) { return ''; }
	$u = wp_get_current_user();
	if ( in_array( 'partner_distributor', (array) $u->roles, true ) ) { return 'distributor'; }
	if ( in_array( 'partner_shop', (array) $u->roles, true ) )        { return 'shop'; }
	return '';
}

/** B2BKing group post ID by title ("Shop" / "Distributor"), 0 if missing. */
function i7_b2bking_group_id( $title ) {
	$ids = get_posts( array( 'post_type' => 'b2bking_group', 'post_status' => 'publish', 'title' => $title, 'numberposts' => 1, 'fields' => 'ids' ) );
	return $ids ? (int) $ids[0] : 0;
}

/** Keep the B2BKing group in sync with the partner role. */
function i7_sync_partner_group( $user_id ) {
	$u = get_userdata( $user_id );
	if ( ! $u ) { return; }
	$map = array( 'partner_distributor' => 'Distributor', 'partner_shop' => 'Shop' );
	foreach ( $map as $role => $title ) {
		if ( in_array( $role, (array) $u->roles, true ) ) {
			$gid = i7_b2bking_group_id( $title );
			if ( $gid ) {
				update_user_meta( $user_id, 'b2bking_customergroup', $gid );
				update_user_meta( $user_id, 'b2bking_b2buser', 'yes' );
			}
			return;
		}
	}
	// Lost both partner roles: drop only a Shop/Distributor group assignment.
	$cur = (int) get_user_meta( $user_id, 'b2bking_customergroup', true );
	if ( $cur && in_array( $cur, array( i7_b2bking_group_id( 'Shop' ), i7_b2bking_group_id( 'Distributor' ) ), true ) ) {
		delete_user_meta( $user_id, 'b2bking_customergroup' );
		delete_user_meta( $user_id, 'b2bking_b2buser' );
	}
}
add_action( 'user_register',  'i7_sync_partner_group', 20 );
add_action( 'set_user_role',  function ( $uid ) { i7_sync_partner_group( $uid ); }, 20 );
add_action( 'add_user_role',  function ( $uid ) { i7_sync_partner_group( $uid ); }, 20 );
add_action( 'remove_user_role', function ( $uid ) { i7_sync_partner_group( $uid ); }, 20 );
