<?php
/**
 * "DHL" shipping method for retail orders (rates from the User Journey brief).
 * Cost depends on the number of records: 1–3 (small parcel) or 4+ (DHL Paket).
 * Partners (shops / distributors) get delivery included, except ex-works countries (DE, BR).
 * Rates are editable per shipping zone in WooCommerce → Settings → Shipping.
 */
add_action( 'woocommerce_shipping_init', function () {
	if ( class_exists( 'I7_Shipping_DHL' ) ) { return; }

	class I7_Shipping_DHL extends WC_Shipping_Method {
		public function __construct( $instance_id = 0 ) {
			$this->id                 = 'i7_dhl';
			$this->instance_id        = absint( $instance_id );
			$this->method_title       = 'DHL';
			$this->method_description = 'DHL shipping priced by number of records (1–3 / 4+).';
			$this->supports           = array( 'shipping-zones', 'instance-settings' );
			$this->instance_form_fields = array(
				'title'       => array( 'title' => 'Method title', 'type' => 'text', 'default' => 'DHL' ),
				'cost_small'  => array( 'title' => 'Cost, 1–3 records (€)', 'type' => 'price', 'default' => '0' ),
				'cost_large'  => array( 'title' => 'Cost, 4+ records (€)', 'type' => 'price', 'default' => '0' ),
				'small_label' => array( 'title' => 'Label, 1–3 records', 'type' => 'text', 'default' => 'DHL Päckchen XS' ),
				'large_label' => array( 'title' => 'Label, 4+ records', 'type' => 'text', 'default' => 'DHL Paket' ),
			);
			$this->title = $this->get_option( 'title', 'DHL' );
			add_action( 'woocommerce_update_options_shipping_' . $this->id, array( $this, 'process_admin_options' ) );
		}

		public function calculate_shipping( $package = array() ) {
			$qty = 0;
			foreach ( $package['contents'] as $item ) { $qty += (int) $item['quantity']; }
			$country = $package['destination']['country'] ?? '';
			$large   = $qty > 3;
			$cost    = (float) $this->get_option( $large ? 'cost_large' : 'cost_small', 0 );
			$label   = $this->get_option( $large ? 'large_label' : 'small_label', 'DHL' );
			if ( function_exists( 'i7_partner_type' ) && i7_partner_type() && ! in_array( $country, array( 'DE', 'BR' ), true ) ) {
				$cost  = 0;
				$label = 'delivery included';
			}
			$this->add_rate( array(
				'id'    => $this->get_rate_id(),
				'label' => 'DHL – ' . $label,
				'cost'  => $cost,
			) );
		}
	}
} );

add_filter( 'woocommerce_shipping_methods', function ( $methods ) {
	$methods['i7_dhl'] = 'I7_Shipping_DHL';
	return $methods;
} );
