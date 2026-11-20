/* WPCode snippet "Partner: application -> account + welcome e-mail". Location: Run everywhere (PHP).
 * Source of truth is kept in the 7inch repo (tools/wpcode/partner-registration.php); the live copy is the WPCode snippet.
 *
 * Flow:
 *  1. A record shop / distributor sends the application form (Contact Form 7: id 86 = EN, id 202 = DE).
 *     Contact Form 7 mails the application to shop@7inchrare.com (form setting).
 *  2. This snippet immediately creates the WooCommerce customer (billing address from the form), puts it into the B2BKing
 *     group (Shop 130 / Distributor 131, so group prices apply) and sends ONE welcome e-mail (the WooCommerce "new account"
 *     e-mail with a welcome subject / text) containing the link to set the password. Only the owner of the mailbox can set
 *     the password, so this also confirms the address. shop@7inchrare.com gets a "Partner account created" notice.
 *  3. After setting the password the partner logs in to My account and sees the offer of the group.
 * Existing accounts are never touched: if the e-mail address is already registered, nothing is changed, the applicant gets a
 * short "you already have an account" e-mail and shop@ is informed.
 * To undo: deactivate this snippet. */
if ( ! function_exists( 'i7pr_register' ) ) {

	function i7pr_forms() { return array( 86 => 'en', 202 => 'de' ); }
	function i7pr_admin_mail() { return 'shop@7inchrare.com'; }

	/** @return string[] localized texts */
	function i7pr_t( $lang ) {
		$de = ( 'de' === $lang );
		return array(
			'shop'          => $de ? 'Plattenladen' : 'Record shop',
			'dist'          => $de ? 'Vertrieb' : 'Distributor',
			'wel_subject'   => $de ? 'Willkommen bei Vibetown Entertainment – Passwort festlegen' : 'Welcome to Vibetown Entertainment – set your password',
			'wel_heading'   => $de ? 'Willkommen bei Vibetown Entertainment' : 'Welcome to Vibetown Entertainment',
			'wel_text'      => $de ? 'Dein Händlerkonto (%s) ist angelegt. Lege mit dem Link oben dein Passwort fest. Danach meldest du dich unter „Mein Konto“ an und siehst das Angebot und die Preise für dein Konto.' : 'Your trade account (%s) is ready. Set your password with the link above, then log in to My account to see the offer and prices for your account.',
			'ex_subject'    => $de ? 'Ihr Konto bei Vibetown Entertainment' : 'Your account at Vibetown Entertainment',
			'ex_body'       => $de ? "Hallo %s,\n\nvielen Dank für deine Anfrage. Für diese E-Mail-Adresse gibt es bereits ein Konto.\n\nAnmelden: %s\nPasswort vergessen? %s\n\nVibetown Entertainment" : "Hello %s,\n\nthank you for your application. An account with this e-mail address already exists.\n\nLog in: %s\nForgot your password? %s\n\nVibetown Entertainment",
		);
	}

	function i7pr_address_lines( $d ) {
		$l   = array();
		$l[] = $d['address_1'];
		if ( '' !== $d['address_2'] ) { $l[] = $d['address_2']; }
		$l[] = trim( $d['postcode'] . ' ' . $d['city'] );
		if ( '' !== $d['state'] ) { $l[] = $d['state']; }
		$l[] = $d['country'];
		return $l;
	}

	/** Country name (as submitted: English) -> ISO code, independent of the current locale. */
	function i7pr_country_code( $name ) {
		$lists = array( WC()->countries->get_countries() );
		$sw    = function_exists( 'switch_to_locale' ) ? switch_to_locale( 'en_US' ) : false;
		$file  = WC()->plugin_path() . '/i18n/countries.php';
		if ( file_exists( $file ) ) { $lists[] = include $file; }
		if ( $sw ) { restore_previous_locale(); }
		foreach ( $lists as $list ) {
			if ( ! is_array( $list ) ) { continue; }
			foreach ( $list as $k => $v ) { if ( 0 === strcasecmp( (string) $v, (string) $name ) ) { return $k; } }
		}
		return '';
	}

	function i7pr_state_code( $country, $state ) {
		if ( '' === $state || '' === $country ) { return $state; }
		$states = WC()->countries->get_states( $country );
		if ( empty( $states ) ) { return $state; }
		if ( isset( $states[ $state ] ) ) { return $state; }
		foreach ( $states as $k => $v ) { if ( 0 === strcasecmp( $v, $state ) ) { return $k; } }
		return '';
	}

	/** Welcome wording for the WooCommerce "new account" e-mail, only while this snippet creates an account. */
	add_filter( 'woocommerce_email_subject_customer_new_account', function ( $s ) {
		$w = $GLOBALS['i7pr_welcome'] ?? null;
		return $w ? i7pr_t( $w['lang'] )['wel_subject'] : $s;
	}, 20 );
	add_filter( 'woocommerce_email_heading_customer_new_account', function ( $s ) {
		$w = $GLOBALS['i7pr_welcome'] ?? null;
		return $w ? i7pr_t( $w['lang'] )['wel_heading'] : $s;
	}, 20 );
	add_filter( 'woocommerce_email_additional_content_customer_new_account', function ( $c ) {
		$w = $GLOBALS['i7pr_welcome'] ?? null;
		if ( ! $w ) { return $c; }
		$t = i7pr_t( $w['lang'] );
		return sprintf( $t['wel_text'], 'distributor' === $w['type'] ? $t['dist'] : $t['shop'] );
	}, 20 );

	/** Creates the customer from an application. Returns user id or WP_Error. */
	function i7pr_create_account( array $d ) {
		$parts = array( $d['first_name'] ?? '', $d['last_name'] ?? '' );
		if ( '' === $parts[0] ) { $parts = preg_split( '/\s+/', trim( $d['contact'] ), 2 ); } // fallback: single "contact" value
		$yes   = static function () { return 'yes'; };
		add_filter( 'pre_option_woocommerce_registration_generate_password', $yes );
		add_filter( 'pre_option_woocommerce_registration_generate_username', $yes );
		$off = array( 'woocommerce_email_enabled_b2bking_new_customer_email', 'woocommerce_email_enabled_b2bking_new_customer_requires_approval_email' );
		foreach ( $off as $f ) { add_filter( $f, '__return_false' ); }
		// The human check (Turnstile) was passed on the application form; this server-side step has no widget token,
		// so validation errors of other plugins on the registration are ignored here.
		$ignore = static function () { return new WP_Error(); };
		add_filter( 'woocommerce_registration_errors', $ignore, 9999 );
		$GLOBALS['i7pr_welcome'] = $d; // welcome wording for the "new account" e-mail
		$uid = wc_create_new_customer( $d['email'], '', '', array( 'first_name' => $parts[0], 'last_name' => $parts[1] ?? '' ) );
		unset( $GLOBALS['i7pr_welcome'] );
		remove_filter( 'woocommerce_registration_errors', $ignore, 9999 );
		foreach ( $off as $f ) { remove_filter( $f, '__return_false' ); }
		remove_filter( 'pre_option_woocommerce_registration_generate_password', $yes );
		remove_filter( 'pre_option_woocommerce_registration_generate_username', $yes );
		if ( is_wp_error( $uid ) ) { return $uid; }

		$cc    = $d['cc'] ?? i7pr_country_code( $d['country'] );
		$state = $d['state_code'] ?? i7pr_state_code( $cc, $d['state'] );
		$vat   = strtoupper( preg_replace( '/[\s.\-]+/', '', $d['vat'] ) );
		$bill  = array(
			'first_name' => $parts[0], 'last_name' => $parts[1] ?? '', 'company' => $d['company'],
			'address_1' => $d['address_1'], 'address_2' => $d['address_2'], 'postcode' => $d['postcode'], 'city' => $d['city'],
			'state' => $state, 'country' => $cc, 'email' => $d['email'], 'phone' => $d['phone'],
		);
		foreach ( $bill as $k => $v ) { update_user_meta( $uid, 'billing_' . $k, $v ); }
		if ( '' !== $vat ) { update_user_meta( $uid, 'billing_vat_number', $vat ); }

		$dist = ( 'distributor' === $d['type'] );
		update_user_meta( $uid, 'b2bking_registration_role', 'role_' . ( $dist ? 141 : 140 ) );
		update_user_meta( $uid, 'b2bking_account_approved', 'yes' );
		update_user_meta( $uid, 'b2bking_b2buser', 'yes' );
		if ( function_exists( 'b2bking' ) ) { b2bking()->update_user_group( $uid, $dist ? 131 : 130 ); }
		return $uid;
	}

	function i7pr_notify_admin( $subject, array $d, $extra = '' ) {
		$body = $extra . "\n\nType: " . $d['type'] . "\nCompany: " . $d['company'] . "\nContact person: " . $d['contact'] . "\nE-mail: " . $d['email'] . "\nPhone: " . $d['phone'] . "\nAddress:\n  " . implode( "\n  ", i7pr_address_lines( $d ) ) . "\nEU VAT number: " . $d['vat'] . "\nLanguage: " . $d['lang'];
		wp_mail( i7pr_admin_mail(), $subject, $body, array( 'Content-Type: text/plain; charset=UTF-8' ) );
	}

	/** Application -> account + welcome e-mail. Returns array( status, user_id ): created | exists | error. */
	function i7pr_register( array $d ) {
		$lang            = $d['lang'];
		$d['cc']         = i7pr_country_code( $d['country'] );
		$d['state_code'] = i7pr_state_code( $d['cc'], $d['state'] );
		$sw              = function_exists( 'switch_to_locale' ) ? switch_to_locale( 'de' === $lang ? 'de_DE' : 'en_US' ) : false;
		$uid             = 0;
		if ( email_exists( $d['email'] ) ) {
			$status = 'exists';
			$t      = i7pr_t( $lang );
			$my     = function_exists( 'wc_get_page_id' ) ? wc_get_page_id( 'myaccount' ) : 0;
			if ( $my && function_exists( 'pll_get_post' ) ) { $my = pll_get_post( $my, $lang ) ?: $my; }
			$login = $my ? get_permalink( $my ) : home_url( '/' );
			wp_mail( $d['email'], $t['ex_subject'], sprintf( $t['ex_body'], $d['first_name'] ?: $d['contact'], $login, trailingslashit( $login ) . 'lost-password/' ), array( 'Content-Type: text/plain; charset=UTF-8' ) );
			i7pr_notify_admin( 'Partner application: e-mail already registered (' . $d['company'] . ')', $d, 'An account with this address already exists. Nothing was changed; the applicant was e-mailed the login / password reset links.' );
		} else {
			$uid = i7pr_create_account( $d );
			if ( is_wp_error( $uid ) ) {
				$status = 'error';
				update_option( 'i7pr_last_error', array( 'time' => current_time( 'mysql' ), 'code' => $uid->get_error_code(), 'message' => $uid->get_error_message() ), false );
				i7pr_notify_admin( 'Partner application: account could not be created (' . $d['company'] . ')', $d, 'Error: ' . $uid->get_error_message() );
				$uid = 0;
			} else {
				$status = 'created';
				i7pr_notify_admin( 'Partner account created: ' . $d['company'], $d, 'The account was created automatically (group ' . ( 'distributor' === $d['type'] ? 'Distributor' : 'Shop' ) . ') and the applicant received the welcome e-mail with the link to set the password.' . "\nEdit: " . admin_url( 'user-edit.php?user_id=' . $uid ) );
			}
		}
		if ( $sw ) { restore_previous_locale(); }
		// result of the last application (for troubleshooting; no address stored)
		update_option( 'i7pr_last_result', array( 'time' => current_time( 'mysql' ), 'status' => $status, 'lang' => $lang, 'domain' => substr( strrchr( $d['email'], '@' ), 1 ) ), false );
		return array( $status, $uid );
	}

	/** Contact Form 7 -> create the account and send the welcome e-mail. */
	add_action( 'wpcf7_mail_sent', function ( $form ) {
		$forms = i7pr_forms();
		$id    = (int) $form->id();
		if ( ! isset( $forms[ $id ] ) ) { return; }
		$sub = WPCF7_Submission::get_instance();
		if ( ! $sub ) { return; }
		$p = $sub->get_posted_data();
		$g = static function ( $k ) use ( $p ) {
			$v = $p[ $k ] ?? '';
			if ( is_array( $v ) ) { $v = reset( $v ); }
			return sanitize_text_field( (string) $v );
		};
		$email = sanitize_email( $g( 'your-email' ) );
		if ( ! is_email( $email ) ) { return; }
		i7pr_register( array(
			'type'      => ( 'Distributor' === $g( 'apply_as' ) ) ? 'distributor' : 'shop',
			'company'   => $g( 'company' ), 'first_name' => $g( 'first_name' ), 'last_name' => $g( 'last_name' ),
			'contact'   => trim( $g( 'first_name' ) . ' ' . $g( 'last_name' ) ) ?: $g( 'contact' ), 'email' => $email, 'phone' => $g( 'phone' ),
			'address_1' => $g( 'address_1' ), 'address_2' => $g( 'address_2' ), 'postcode' => $g( 'postcode' ), 'city' => $g( 'city' ),
			'state'     => $g( 'state' ), 'country' => $g( 'country' ), 'vat' => $g( 'vat' ),
			'lang'      => $forms[ $id ],
		) );
	} );
}
