<?php
/**
 * "DHL" shipping method for retail orders (rates from the User Journey brief).
 * Consumers: 1–5 records (untracked outside Germany, tracked option at the higher price) or 6+.
 * Partners: per parcel by weight (0.1 kg per record; up to 5 kg / up to 10 kg, more parcels above), net prices.
 *  * Rates are editable per shipping zone in WooCommerce → Settings → Shipping.
 */
add_action( 'woocommerce_shipping_init', function () {
	if ( class_exists( 'I7_Shipping_DHL' ) ) { return; }

	class I7_Shipping_DHL extends WC_Shipping_Method {
		public function __construct( $instance_id = 0 ) {
			$this->id                 = 'i7_dhl';
			$this->instance_id        = absint( $instance_id );
			$this->method_title       = 'DHL';
			$this->method_description = 'DHL shipping priced by number of records (1–5 / 6+).';
			$this->supports           = array( 'shipping-zones', 'instance-settings' );
			$this->instance_form_fields = array(
				'title'       => array( 'title' => 'Method title', 'type' => 'text', 'default' => 'DHL' ),
				'cost_small'  => array( 'title' => 'Consumers: 1–5 records (€, gross)', 'type' => 'price', 'default' => '0' ),
				'cost_large'  => array( 'title' => 'Consumers: 6+ records, or tracked 1–5 (€, gross)', 'type' => 'price', 'default' => '0' ),
				'small_label' => array( 'title' => 'Label, 1–5 records', 'type' => 'text', 'default' => 'untracked' ),
				'large_label' => array( 'title' => 'Label, 6+ records (tracked)', 'type' => 'text', 'default' => 'tracked' ),
				'b2b_5kg'     => array( 'title' => 'Partners: parcel up to 5 kg (€, net)', 'type' => 'price', 'default' => '0' ),
				'b2b_10kg'    => array( 'title' => 'Partners: parcel up to 10 kg (€, net)', 'type' => 'price', 'default' => '0' ),
			);
			$this->title = $this->get_option( 'title', 'DHL' );
			add_action( 'woocommerce_update_options_shipping_' . $this->id, array( $this, 'process_admin_options' ) );
		}

		public function calculate_shipping( $package = array() ) {
			$qty = 0;
			foreach ( $package['contents'] as $item ) { $qty += (int) $item['quantity']; }
			$country = $package['destination']['country'] ?? '';
			$partner = function_exists( 'i7_partner_type' ) && i7_partner_type();
			if ( $partner ) {
				// 0.1 kg per record: every full 100 records = one 10 kg parcel, the rest = one 5 kg (≤ 50) or 10 kg parcel.
				$c5 = (float) $this->get_option( 'b2b_5kg', 0 );
				$c10 = (float) $this->get_option( 'b2b_10kg', 0 );
				$full = intdiv( $qty, 100 );
				$rem  = $qty - $full * 100;
				$n    = $full + ( $rem ? 1 : 0 );
				$cost = $full * $c10 + ( $rem ? ( $rem <= 50 ? $c5 : $c10 ) : 0 );
				if ( $n < 1 || $cost <= 0 ) { return; }
				$this->add_rate( array( 'id' => $this->get_rate_id(), 'label' => 'DHL – ' . $n . ( 1 === $n ? ' parcel' : ' parcels' ), 'cost' => $cost ) );
				return;
			}
			$small = (float) $this->get_option( 'cost_small', 0 );
			$large = (float) $this->get_option( 'cost_large', 0 );
			$rates = array();
			if ( $qty > 5 ) {
				$rates[] = array( $large, $this->get_option( 'large_label', 'tracked' ), 'large' );
			} else {
				$rates[] = array( $small, $this->get_option( 'small_label', 'untracked' ), 'small' );
				if ( 'DE' !== $country && $large > $small ) { $rates[] = array( $large, $this->get_option( 'large_label', 'tracked' ), 'large' ); }
			}
			foreach ( $rates as $r ) {
				$cost = $r[0];
				// Consumer shipping costs are gross (VAT included): split the VAT out so the customer pays exactly the listed amount.
				// Germanized ("shipping costs include tax") already splits the VAT out of the cost of every method, VAT-exempt customers included;
				// doing it here as well would divide twice (7.90 → 5.58 instead of 6.64).
				$exempt = function_exists( 'i7_is_vat_exempt' ) && i7_is_vat_exempt();
				$gzd    = function_exists( 'wc_gzd_additional_costs_include_tax' ) && wc_gzd_additional_costs_include_tax();
				if ( $cost > 0 && wc_tax_enabled() && wc_prices_include_tax() && ! $gzd ) {
					$trates = $exempt ? WC_Tax::get_base_tax_rates( '' ) : WC_Tax::get_shipping_tax_rates();
					$cost  -= array_sum( WC_Tax::calc_inclusive_tax( $cost, $trates ) );
				}
				$this->add_rate( array( 'id' => $this->get_rate_id( $r[2] ), 'label' => 'DHL – ' . $r[1], 'cost' => $cost ) );
			}
		}
	}
} );

add_filter( 'woocommerce_shipping_methods', function ( $methods ) {
	$methods['i7_dhl'] = 'I7_Shipping_DHL';
	return $methods;
} );
