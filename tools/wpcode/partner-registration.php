/* WPCode snippet "Partner: application -> e-mail confirmation -> account". Location: Run everywhere (PHP).
 * Source of truth is kept in the 7inch repo (tools/wpcode/partner-registration.php); the live copy is the WPCode snippet.
 *
 * Flow:
 *  1. A record shop / distributor sends the application form (Contact Form 7: id 86 = EN, id 202 = DE).
 *     Contact Form 7 mails the application to shop@7inchrare.com (form setting).
 *  2. This snippet stores the application for 3 days under a one-time token and e-mails the applicant a summary
 *     of the data to verify, with a confirmation link.
 *  3. Opening the link creates the WooCommerce customer (billing address from the form), puts it into the B2BKing group
 *     (Shop 130 / Distributor 131, so group prices apply), sends the "set your password" e-mail and tells shop@7inchrare.com.
 *     The applicant can then log in to My account and sees the offer of the group.
 * Existing accounts are never touched: if the e-mail address is already registered, nothing is changed and shop@ is informed.
 * To undo: deactivate this snippet. */
if ( ! function_exists( 'i7pr_start' ) ) {

	function i7pr_forms() { return array( 86 => 'en', 202 => 'de' ); }
	function i7pr_admin_mail() { return 'shop@7inchrare.com'; }

	/** @return string[] localized texts */
	function i7pr_t( $lang ) {
		$de = ( 'de' === $lang );
		return array(
			'subject' => $de ? 'Bitte bestätigen Sie Ihre Angaben – Vibetown Entertainment' : 'Please confirm your details – Vibetown Entertainment',
			'hello'   => $de ? 'Guten Tag %s,' : 'Hello %s,',
			'intro'   => $de ? "vielen Dank für Ihre Anfrage für ein Händlerkonto (%s) bei Vibetown Entertainment (7inchrare.com).\n\nBitte prüfen Sie Ihre Angaben:" : "thank you for applying for a trade account (%s) at Vibetown Entertainment (7inchrare.com).\n\nPlease check the details you entered:",
			'confirm' => $de ? 'Wenn alles stimmt, bestätigen Sie Ihre Angaben mit diesem Link:' : 'If everything is correct, confirm your details with this link:',
			'after'   => $de ? "Nach der Bestätigung wird Ihr Konto angelegt und Sie erhalten eine weitere E-Mail mit einem Link, um Ihr Passwort festzulegen. Danach können Sie sich unter „Mein Konto“ anmelden und das Angebot für Ihr Konto sehen.\n\nDer Link ist 3 Tage gültig. Wenn Sie sich nicht beworben haben, ignorieren Sie diese Nachricht einfach." : "After you confirm, your account is created and we send you another e-mail with a link to set your password. You can then log in to My account and see the offer for your account.\n\nThe link is valid for 3 days. If you did not apply, simply ignore this message.",
			'labels'  => $de ? array( 'company' => 'Firma', 'contact' => 'Ansprechpartner', 'email' => 'E-Mail', 'phone' => 'Telefon', 'address' => 'Adresse', 'vat' => 'EU-USt-IdNr.' ) : array( 'company' => 'Company', 'contact' => 'Contact person', 'email' => 'E-mail', 'phone' => 'Phone', 'address' => 'Address', 'vat' => 'EU VAT number' ),
			'shop'    => $de ? 'Plattenladen' : 'Record shop',
			'dist'    => $de ? 'Vertrieb' : 'Distributor',
			'ok'      => $de ? 'Ihr Konto ist bestätigt. Sie können sich jetzt anmelden – legen Sie dafür zuerst über den Link in der soeben gesendeten E-Mail Ihr Passwort fest.' : 'Your account is confirmed. You can log in now – first set your password with the link in the e-mail we have just sent you.',
			'exists'  => $de ? 'Für diese E-Mail-Adresse gibt es bereits ein Konto. Bitte melden Sie sich an oder nutzen Sie „Passwort vergessen?“. Wir haben Ihre Anfrage notiert.' : 'An account with this e-mail address already exists. Please log in, or use “Lost your password?”. We have noted your application.',
			'invalid' => $de ? 'Dieser Bestätigungslink ist ungültig, abgelaufen oder wurde bereits verwendet. Falls Sie schon bestätigt haben, prüfen Sie Ihr Postfach auf die E-Mail zum Festlegen des Passworts; andernfalls bewerben Sie sich bitte erneut oder kontaktieren Sie uns.' : 'This confirmation link is invalid, expired or has already been used. If you have already confirmed, check your inbox for the e-mail to set your password; otherwise please apply again or contact us.',
			'error'   => $de ? 'Wir konnten Ihr Konto nicht automatisch anlegen. Wir haben Ihre Anfrage notiert und melden uns in Kürze.' : 'We could not create your account automatically. We have noted your application and will contact you shortly.',
		);
	}

	function i7pr_headers() {
		return array( 'Content-Type: text/plain; charset=UTF-8', 'From: Vibetown Entertainment <' . i7pr_admin_mail() . '>', 'Reply-To: ' . i7pr_admin_mail() );
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

	/** Stores the application under a one-time token and mails the applicant the confirmation link. Returns the token. */
	function i7pr_start( array $d ) {
		$token = wp_generate_password( 40, false, false );
		set_transient( 'i7pr_' . hash( 'sha256', $token ), $d, 3 * DAY_IN_SECONDS );
		$t    = i7pr_t( $d['lang'] );
		$L    = $t['labels'];
		$link = add_query_arg( 'i7_partner_verify', $token, home_url( '/' ) );
		$body = sprintf( $t['hello'], $d['contact'] ) . "\n\n" . sprintf( $t['intro'], 'distributor' === $d['type'] ? $t['dist'] : $t['shop'] ) . "\n\n"
			. $L['company'] . ': ' . $d['company'] . "\n"
			. $L['contact'] . ': ' . $d['contact'] . "\n"
			. $L['email'] . ': ' . $d['email'] . "\n"
			. ( '' !== $d['phone'] ? $L['phone'] . ': ' . $d['phone'] . "\n" : '' )
			. $L['address'] . ":\n  " . implode( "\n  ", i7pr_address_lines( $d ) ) . "\n"
			. ( '' !== $d['vat'] ? $L['vat'] . ': ' . $d['vat'] . "\n" : '' )
			. "\n" . $t['confirm'] . "\n" . $link . "\n\n" . $t['after'] . "\n\nVibetown Entertainment";
		$err = '';
		$cap = static function ( $e ) use ( &$err ) { $err = $e->get_error_message(); };
		add_action( 'wp_mail_failed', $cap );
		$sent = wp_mail( $d['email'], $t['subject'], $body, i7pr_headers() );
		remove_action( 'wp_mail_failed', $cap );
		// result of the last confirmation mail (for troubleshooting; no address stored)
		update_option( 'i7pr_last_send', array( 'time' => current_time( 'mysql' ), 'ok' => (bool) $sent, 'error' => $err, 'lang' => $d['lang'], 'domain' => substr( strrchr( $d['email'], '@' ), 1 ) ), false );
		return $token;
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

	/** Creates the customer from a confirmed application. Returns user id or WP_Error. */
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
		$uid = wc_create_new_customer( $d['email'], '', '', array( 'first_name' => $parts[0], 'last_name' => $parts[1] ?? '' ) );
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

	/** Validates the token and creates the account. Returns array( status, lang, user_id ). */
	function i7pr_process( $token ) {
		$key = 'i7pr_' . hash( 'sha256', (string) $token );
		$d   = get_transient( $key );
		if ( ! is_array( $d ) ) { return array( 'invalid', 'en', 0 ); }
		$lang   = $d['lang'];
		$d['cc']         = i7pr_country_code( $d['country'] );
		$d['state_code'] = i7pr_state_code( $d['cc'], $d['state'] );
		$locale = ( 'de' === $lang ) ? 'de_DE' : 'en_US';
		$sw     = function_exists( 'switch_to_locale' ) ? switch_to_locale( $locale ) : false;
		if ( email_exists( $d['email'] ) ) {
			delete_transient( $key );
			i7pr_notify_admin( 'Partner application: e-mail already registered (' . $d['company'] . ')', $d, 'The applicant confirmed the e-mail address, but an account with this address already exists. Nothing was changed.' );
			if ( $sw ) { restore_previous_locale(); }
			return array( 'exists', $lang, 0 );
		}
		$uid = i7pr_create_account( $d );
		if ( is_wp_error( $uid ) ) {
			update_option( 'i7pr_last_error', array( 'time' => current_time( 'mysql' ), 'code' => $uid->get_error_code(), 'message' => $uid->get_error_message() ), false ); // the token stays valid, the link can be opened again
			i7pr_notify_admin( 'Partner application: account could not be created (' . $d['company'] . ')', $d, 'Error: ' . $uid->get_error_message() );
			if ( $sw ) { restore_previous_locale(); }
			return array( 'error', $lang, 0 );
		}
		delete_transient( $key ); // one use
		i7pr_notify_admin( 'Partner account created: ' . $d['company'], $d, 'The applicant confirmed the data; the account was created automatically (group ' . ( 'distributor' === $d['type'] ? 'Distributor' : 'Shop' ) . ').' . "\nEdit: " . admin_url( 'user-edit.php?user_id=' . $uid ) );
		if ( $sw ) { restore_previous_locale(); }
		return array( 'ok', $lang, $uid );
	}

	/** Contact Form 7 -> store the application and mail the confirmation link. */
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
		i7pr_start( array(
			'type'      => ( 'Distributor' === $g( 'apply_as' ) ) ? 'distributor' : 'shop',
			'company'   => $g( 'company' ), 'first_name' => $g( 'first_name' ), 'last_name' => $g( 'last_name' ),
			'contact'   => trim( $g( 'first_name' ) . ' ' . $g( 'last_name' ) ) ?: $g( 'contact' ), 'email' => $email, 'phone' => $g( 'phone' ),
			'address_1' => $g( 'address_1' ), 'address_2' => $g( 'address_2' ), 'postcode' => $g( 'postcode' ), 'city' => $g( 'city' ),
			'state'     => $g( 'state' ), 'country' => $g( 'country' ), 'vat' => $g( 'vat' ),
			'lang'      => $forms[ $id ],
		) );
	} );

	/** Confirmation link. */
	add_action( 'template_redirect', function () {
		if ( empty( $_GET['i7_partner_verify'] ) ) { return; } // phpcs:ignore WordPress.Security.NonceVerification
		list( $status, $lang ) = i7pr_process( sanitize_text_field( wp_unslash( $_GET['i7_partner_verify'] ) ) ); // phpcs:ignore
		if ( 'invalid' === $status && function_exists( 'pll_current_language' ) && in_array( pll_current_language( 'slug' ), array( 'en', 'de' ), true ) ) {
			$lang = pll_current_language( 'slug' ); // unknown token: use the language of the URL
		}
		$t = i7pr_t( $lang );
		if ( function_exists( 'WC' ) && WC()->session ) {
			WC()->session->set_customer_session_cookie( true );
			wc_add_notice( $t[ $status ], 'ok' === $status ? 'success' : 'error' );
		}
		$page = function_exists( 'wc_get_page_id' ) ? wc_get_page_id( 'myaccount' ) : 0;
		if ( $page && function_exists( 'pll_get_post' ) ) { $page = pll_get_post( $page, $lang ) ?: $page; }
		wp_safe_redirect( $page ? get_permalink( $page ) : home_url( '/' ) );
		exit;
	} );
}
