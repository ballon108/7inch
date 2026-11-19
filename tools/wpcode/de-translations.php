<?php
/**
 * WPCode snippet: "Polylang: German UI strings (theme)".
 * Location: Run everywhere. Source of truth is kept here; the live copy is the WPCode snippet.
 *
 * The 7inch theme has hard-coded English in block templates/parts (plain HTML), in block render.php files
 * and in a few PHP filters. This translates those strings on the German front end only (Polylang "de"),
 * so English output is untouched. WordPress / WooCommerce / B2BKing strings come from their own de_DE language packs.
 */
if ( ! function_exists( 'i7de_on' ) ) {

	/** True on the German front end (and in German AJAX requests). */
	function i7de_on() {
		static $on = null;
		if ( null !== $on ) { return $on; }
		if ( ! function_exists( 'pll_current_language' ) ) { return false; }
		$lang = pll_current_language();
		if ( ! $lang ) { return false; } // language not resolved yet: do not cache.
		return $on = ( 'de' === $lang );
	}

	/** Exact-match dictionary (source text → German). Keys are plain text (no HTML entities). */
	function i7de_dict() {
		static $d = null;
		if ( null !== $d ) { return $d; }
		$d = array(
			// Header / footer.
			'Releases' => 'Releases', 'Series' => 'Serien', 'Wholesale' => 'Großhandel', 'About' => 'Über uns',
			'Contact' => 'Kontakt', 'Partners' => 'Partner', 'Account' => 'Konto', 'Menu' => 'Menü', 'Main' => 'Hauptmenü',
			'Imprint' => 'Impressum', 'Privacy' => 'Datenschutz', 'Terms' => 'AGB', 'Withdrawal' => 'Widerruf',
			'Shipping & payment' => 'Versand & Zahlung',
			// 404.
			'Error 404' => 'Fehler 404', 'This track skipped.' => 'Dieser Track hat gesprungen.',
			'The page you are looking for doesn’t exist or has moved. Let’s put the needle back on a record that does.' => 'Die gesuchte Seite existiert nicht oder wurde verschoben. Setzen wir die Nadel zurück auf eine Platte, die es gibt.',
			'Back to home' => 'Zurück zur Startseite', 'Browse releases' => 'Releases ansehen',
			// Cart / checkout / order templates.
			'Your order' => 'Ihre Bestellung',
			// Product page.
			'Record shop or distributor?' => 'Plattenladen oder Vertrieb?', 'Login or Register' => 'Anmelden oder Registrieren',
			'Format' => 'Format', 'Edition' => 'Auflage', 'Year' => 'Jahr', 'Cat. no.' => 'Kat.-Nr.', 'Pressed in' => 'Gepresst in',
			'7" vinyl' => '7" Vinyl',
			'In stock' => 'Auf Lager', 'Sold out' => 'Ausverkauft', 'Pre-order' => 'Vorbestellung', 'Out now' => 'Jetzt erhältlich',
			'Pre-order now' => 'Jetzt vorbestellen', 'Add to cart' => 'In den Warenkorb', 'View release' => 'Release ansehen',
			'All releases' => 'Alle Releases', 'Log in to buy' => 'Zum Kauf anmelden', 'Not available' => 'Nicht verfügbar',
			'Decrease quantity' => 'Menge verringern', 'Increase quantity' => 'Menge erhöhen',
			'Play preview' => 'Vorschau abspielen', 'Pause' => 'Pause',
			'Side A' => 'Seite A', 'Side B' => 'Seite B', 'Front' => 'Vorderseite', 'Back' => 'Rückseite',
			'Pull out the record' => 'Platte herausziehen', 'Spin' => 'Drehen', 'View' => 'Ansicht',
			'3D view of the record. Drag to rotate, pinch to zoom, double-click to reset.' => '3D-Ansicht der Platte. Zum Drehen ziehen, zum Zoomen zwei Finger auseinanderziehen, zum Zurücksetzen doppelklicken.',
			'Drag to turn · pinch to zoom · double-click to reset' => 'Ziehen zum Drehen · Zwei Finger zum Zoomen · Doppelklick zum Zurücksetzen',
			// Catalogue / home blocks.
			'Catalogue' => 'Katalog', 'All' => 'Alle', 'Keep digging' => 'Weiterstöbern', 'More from the series' => 'Mehr aus der Serie',
			'Two series' => 'Zwei Serien', 'Pick your side of the map.' => 'Wählen Sie Ihre Seite der Karte.',
			'For record shops & distributors' => 'Für Plattenläden & Vertriebe',
			'Stock the series in your shop.' => 'Führen Sie die Serie in Ihrem Laden.',
			'Wholesale price list, pre-order windows and shipping options on request. We ship worldwide; the buyer pays freight.' => 'Großhandelspreisliste, Vorbestellfenster und Versandoptionen auf Anfrage. Wir liefern weltweit; die Fracht trägt der Käufer.',
			'copies minimum for record shops' => 'Exemplare Mindestabnahme für Plattenläden',
			'copies minimum for distributors' => 'Exemplare Mindestabnahme für Vertriebe',
			'Request the wholesale list' => 'Großhandelsliste anfordern',
			'Minimum order for your account:' => 'Mindestbestellmenge für Ihr Konto:',
			'in total, across all titles. Your trade prices apply automatically in the basket.' => 'insgesamt, über alle Titel. Ihre Händlerpreise werden automatisch im Warenkorb angewendet.',
			// Login / registration shortcodes and buttons.
			'You are logged in.' => 'Sie sind angemeldet.', 'You already have an account.' => 'Sie haben bereits ein Konto.',
			'Go to My account' => 'Zu Mein Konto', 'Log out' => 'Abmelden',
			'Email address' => 'E-Mail-Adresse', 'Password' => 'Passwort', 'Create account' => 'Konto erstellen',
			'A link to set your password will be sent to your email address.' => 'Ein Link zum Festlegen Ihres Passworts wird an Ihre E-Mail-Adresse gesendet.',
			'For distributors and shops' => 'Für Vertriebe und Plattenläden',
			// Checkout fields / buttons / notices (also used by filters below).
			'EU VAT number' => 'EU-USt-IdNr.', 'Company name' => 'Firmenname', 'Another address for shipping' => 'Andere Lieferadresse',
			'Order with obligation to pay' => 'Zahlungspflichtig bestellen',
			'incl. VAT, plus shipping' => 'inkl. MwSt., zzgl. Versand', 'excl. VAT, plus shipping' => 'zzgl. MwSt. und Versand',
			'Prices incl. VAT, plus shipping.' => 'Preise inkl. MwSt., zzgl. Versand.', 'Prices excl. VAT, plus shipping.' => 'Preise zzgl. MwSt. und Versand.',
			'<strong>EU VAT number</strong> must start with the country code, e.g. DE123456789.' => '<strong>EU-USt-IdNr.</strong> muss mit dem Ländercode beginnen, z. B. DE123456789.',
			'Sorry, we cannot deliver to consumers in the United Kingdom at the moment. Record shops and distributors: please log in with your partner account.' => 'Leider können wir derzeit keine Verbraucher im Vereinigten Königreich beliefern. Plattenläden und Vertriebe: Bitte melden Sie sich mit Ihrem Partnerkonto an.',
			'Thank you – your e-mail address is confirmed and your account is active. You can log in now.' => 'Vielen Dank – Ihre E-Mail-Adresse ist bestätigt und Ihr Konto ist aktiv. Sie können sich jetzt anmelden.',
			'This confirmation link is invalid or has expired. Please contact us and we will activate your account.' => 'Dieser Bestätigungslink ist ungültig oder abgelaufen. Bitte kontaktieren Sie uns, dann aktivieren wir Ihr Konto.',
		);
		return $d;
	}

	/** Plain translation (dictionary only); returns the input when unknown. */
	function i7de_plain( $s ) {
		$d = i7de_dict();
		return isset( $d[ $s ] ) ? $d[ $s ] : $s;
	}

	/**
	 * Translate one text node / attribute value (HTML-escaped in, HTML-escaped out).
	 * Leading/trailing whitespace is preserved; unknown strings are returned untouched.
	 */
	function i7de_t( $s, $attr = false ) {
		$s0 = (string) $s;
		if ( ! preg_match( '/^((?:\s|&nbsp;)*)(.*?)((?:\s|&nbsp;)*)$/us', $s0, $m ) || '' === $m[2] ) { return $s0; }
		$key = html_entity_decode( $m[2], ENT_QUOTES | ENT_HTML5, 'UTF-8' );
		$out = i7de_translate_key( $key );
		if ( $out === $key ) { return $s0; }
		return $m[1] . htmlspecialchars( $out, $attr ? ENT_QUOTES : ENT_NOQUOTES, 'UTF-8', false ) . $m[3];
	}

	/** Decoded string in → decoded German out (same string when nothing matches). */
	function i7de_translate_key( $key ) {
		$d = i7de_dict();
		if ( isset( $d[ $key ] ) ) { return $d[ $key ]; }
		$n = 0;
		$rules = array(
			'/^(Out now|Pre-order|In stock|Sold out) · (.*)$/us' => function ( $m ) { return i7de_plain( $m[1] ) . ' · ' . $m[2]; },
			'/^(.+) · (In stock|Sold out|Pre-order)$/us'          => function ( $m ) { return $m[1] . ' · ' . i7de_plain( $m[2] ); },
			'/^Side ([AB]) · (.*)$/us'                           => function ( $m ) { return 'Seite ' . $m[1] . ' · ' . $m[2]; },
			'/^(.+?) – Side ([AB])$/us'                          => function ( $m ) { return i7de_plain( $m[1] ) . ' – Seite ' . $m[2]; },
			'/^Quantity: (.+)$/us'                               => function ( $m ) { return 'Menge: ' . $m[1]; },
			'/^Explore (.+)$/us'                                 => function ( $m ) { return $m[1] . ' entdecken'; },
			'/^(\d+) copies$/u'                                  => function ( $m ) { return $m[1] . ' Exemplare'; },
			'/^(\d+) records$/u'                                 => function ( $m ) { return $m[1] . ' Schallplatten'; },
			'/^DHL – (\d+) parcels?$/u'                          => function ( $m ) { return 'DHL – ' . $m[1] . ( 1 === (int) $m[1] ? ' Paket' : ' Pakete' ); },
			'/^DHL – tracked$/u'                                 => function () { return 'DHL – mit Sendungsverfolgung'; },
			'/^DHL – untracked$/u'                               => function () { return 'DHL – ohne Sendungsverfolgung'; },
		);
		foreach ( $rules as $re => $cb ) {
			$out = preg_replace_callback( $re, $cb, $key, 1, $n );
			if ( $n ) { return $out; }
		}
		// Sentences embedded in longer text (hero / product lead).
		$subs = array(
			'Pre-orders are open. Secure your copy before the run is pressed.' => 'Vorbestellungen sind geöffnet. Sichern Sie sich Ihr Exemplar, bevor die Auflage gepresst wird.',
		);
		$out = str_replace( array_keys( $subs ), array_values( $subs ), $key );
		$out = preg_replace( '/Limited to (\d+) copies\./u', 'Limitiert auf $1 Exemplare.', $out );
		return $out;
	}

	/** Root-relative link → its German equivalent (home, anchors, translated pages); unchanged when there is none. */
	function i7de_link( $url ) {
		static $cache = array();
		if ( isset( $cache[ $url ] ) ) { return $cache[ $url ]; }
		$res = $url;
		if ( 0 !== strpos( $url, '//' ) && 0 !== strpos( $url, '/de/' ) && 0 !== strpos( $url, '/wp-' ) && false === strpos( $url, '?' ) && function_exists( 'pll_home_url' ) ) {
			$home = trailingslashit( home_url( '/de/' ) );
			if ( '/' === $url ) {
				$res = $home;
			} elseif ( 0 === strpos( $url, '/#' ) ) {
				$res = $home . substr( $url, 1 );
			} else {
				$parts = explode( '#', $url, 2 );
				$page  = get_page_by_path( trim( $parts[0], '/' ) );
				$tr    = $page ? pll_get_post( $page->ID, 'de' ) : 0;
				if ( $tr ) { $res = get_permalink( $tr ) . ( isset( $parts[1] ) ? '#' . $parts[1] : '' ); }
			}
		}
		return $cache[ $url ] = $res;
	}

	/** Whole-page filter: text nodes, selected attributes, internal links. */
	function i7de_page( $html ) {
		if ( ! is_string( $html ) || '' === $html || false === strpos( $html, '<' ) ) { return $html; }
		$parts = preg_split( '#(<script\b.*?</script>|<style\b.*?</style>)#is', $html, -1, PREG_SPLIT_DELIM_CAPTURE );
		if ( false === $parts ) { return $html; }
		foreach ( $parts as $i => $p ) {
			if ( 1 === $i % 2 ) { // script / style: only a known inline placeholder.
				$parts[ $i ] = str_replace( "placeholder:'Select country'", "placeholder:'Land auswählen'", $p );
				continue;
			}
			$p = preg_replace_callback( '/>([^<>]+)</u', function ( $m ) { return '>' . i7de_t( $m[1] ) . '<'; }, $p );
			$p = preg_replace_callback( '/\s(aria-label|placeholder|data-play|data-pause)="([^"]*)"/u', function ( $m ) { return ' ' . $m[1] . '="' . i7de_t( $m[2], true ) . '"'; }, $p );
			$p = preg_replace_callback( '/\bhref="(\/[^"]*)"/', function ( $m ) { return 'href="' . esc_url( i7de_link( $m[1] ) ) . '"'; }, $p );
			$parts[ $i ] = $p;
		}
		return implode( '', $parts );
	}

	add_action( 'template_redirect', function () {
		if ( ! i7de_on() || is_feed() || is_embed() || wp_doing_ajax() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) { return; }
		ob_start( 'i7de_page' );
	}, 0 );

	/* ── Strings produced by PHP filters / WooCommerce hooks (also reached by AJAX fragments) ── */
	$i7de_plain_filter = function ( $v ) { return ( is_string( $v ) && i7de_on() ) ? i7de_translate_key( $v ) : $v; };
	foreach ( array( 'woocommerce_order_button_text', 'woocommerce_add_error', 'woocommerce_add_success', 'woocommerce_add_notice' ) as $hook ) {
		add_filter( $hook, $i7de_plain_filter, 99 );
	}
	add_filter( 'woocommerce_product_single_add_to_cart_text', function ( $t ) { return i7de_on() ? i7de_translate_key( $t ) : $t; }, 99 );
	add_filter( 'woocommerce_product_add_to_cart_text', function ( $t ) { return i7de_on() ? i7de_translate_key( $t ) : $t; }, 99 );

	add_filter( 'gettext', function ( $translated, $text, $domain ) {
		if ( 'Another address for shipping' === $translated && i7de_on() ) { return 'Andere Lieferadresse'; }
		return $translated;
	}, 99, 3 );

	$i7de_labels = function ( $fields ) {
		if ( ! i7de_on() || ! is_array( $fields ) ) { return $fields; }
		foreach ( $fields as $k => $f ) {
			if ( is_array( $f ) && isset( $f['label'] ) && is_string( $f['label'] ) ) { $fields[ $k ]['label'] = i7de_translate_key( $f['label'] ); }
			elseif ( is_array( $f ) && ! isset( $f['label'] ) ) { // checkout fields are grouped by section.
				foreach ( $f as $k2 => $f2 ) {
					if ( is_array( $f2 ) && isset( $f2['label'] ) && is_string( $f2['label'] ) ) { $fields[ $k ][ $k2 ]['label'] = i7de_translate_key( $f2['label'] ); }
				}
			}
		}
		return $fields;
	};
	add_filter( 'woocommerce_checkout_fields', $i7de_labels, 99 );
	add_filter( 'woocommerce_billing_fields', $i7de_labels, 99 );
	add_filter( 'woocommerce_address_to_edit', $i7de_labels, 99 );

	add_filter( 'woocommerce_package_rates', function ( $rates ) {
		if ( ! i7de_on() ) { return $rates; }
		foreach ( $rates as $r ) { $r->set_label( i7de_translate_key( $r->get_label() ) ); }
		return $rates;
	}, 99 );

	/** Account confirmation e-mail (sent from account-verification.php). */
	add_filter( 'wp_mail', function ( $args ) {
		if ( ! i7de_on() || empty( $args['subject'] ) || 0 !== strpos( $args['subject'], 'Confirm your e-mail address' ) ) { return $args; }
		if ( preg_match( '#https?://\S+#', (string) $args['message'], $m ) ) {
			$args['subject'] = 'Bestätigen Sie Ihre E-Mail-Adresse – Vibetown Entertainment';
			$args['message'] = "Guten Tag,\n\nvielen Dank für Ihre Registrierung bei Vibetown Entertainment (7inchrare.com). Bitte bestätigen Sie Ihre E-Mail-Adresse, um Ihr Händlerkonto zu aktivieren:\n\n"
				. $m[0] . "\n\nDer Link ist 3 Tage gültig. Wenn Sie sich nicht registriert haben, können Sie diese Nachricht ignorieren.\n\nVibetown Entertainment";
		}
		return $args;
	} );

	/** Strings created by site.js / product.js at runtime. */
	add_action( 'wp_footer', function () {
		if ( ! i7de_on() ) { return; }
		?>
<script>(function(){var m={'Previous':'Zurück','Next':'Weiter'},t='Added ✓',tt='Hinzugefügt ✓';
function fix(n){if(n.nodeType===1){if(n.hasAttribute&&n.hasAttribute('aria-label')&&m[n.getAttribute('aria-label')])n.setAttribute('aria-label',m[n.getAttribute('aria-label')]);
if(n.querySelectorAll)n.querySelectorAll('[aria-label]').forEach(fix);}else if(n.nodeType===3&&n.nodeValue===t){n.nodeValue=tt;}}
new MutationObserver(function(rs){rs.forEach(function(r){r.addedNodes.forEach(fix);if(r.type==='characterData')fix(r.target);});}).observe(document.documentElement,{childList:true,subtree:true,characterData:true});
document.querySelectorAll('[aria-label]').forEach(fix);})();</script>
		<?php
	}, 99 );

	/* Theme blocks use get_posts() (no Polylang filtering): limit product queries to the current language,
	 * otherwise every release shows up twice (EN + DE). Runs in both languages. */
	add_action( 'pre_get_posts', function ( $q ) {
		if ( is_admin() || ! function_exists( 'pll_current_language' ) || '' !== (string) $q->get( 'lang' ) ) { return; }
		$pt = $q->get( 'post_type' );
		if ( 'product' !== $pt && ! ( is_array( $pt ) && in_array( 'product', $pt, true ) ) ) { return; }
		if ( $q->get( 'p' ) || $q->get( 'name' ) || $q->get( 'post__in' ) ) { return; }
		$lang = pll_current_language();
		if ( $lang ) { $q->set( 'lang', $lang ); }
	}, 5 );

	/* ── EN / DE language switcher in the header (before the "Partners" button) ── */
	function i7_lang_switcher() {
		if ( ! function_exists( 'pll_the_languages' ) ) { return ''; }
		$langs = pll_the_languages( array( 'raw' => 1, 'hide_if_no_translation' => 0 ) );
		if ( ! is_array( $langs ) || count( $langs ) < 2 ) { return ''; }
		$label = ( function_exists( 'pll_current_language' ) && 'de' === pll_current_language() ) ? 'Sprache' : 'Language';
		$out = '<nav class="lang-switch" aria-label="' . esc_attr( $label ) . '">';
		foreach ( $langs as $l ) {
			$cur  = ! empty( $l['current_lang'] );
			$out .= '<a href="' . esc_url( $l['url'] ) . '" lang="' . esc_attr( $l['locale'] ) . '" hreflang="' . esc_attr( $l['slug'] ) . '"' . ( $cur ? ' aria-current="true" class="is-current"' : '' ) . '>' . esc_html( strtoupper( $l['slug'] ) ) . '</a>';
		}
		return $out . '</nav>';
	}

	add_filter( 'render_block', function ( $html, $block ) {
		if ( 'core/html' !== ( $block['blockName'] ?? '' ) || false === strpos( $html, 'class="partner-btn"' ) ) { return $html; }
		return i7_lang_switcher() . $html;
	}, 20, 2 );

	add_action( 'wp_head', function () {
		echo '<style id="i7-lang-switch">.lang-switch{display:inline-flex;align-items:center;border:1px solid var(--line);border-radius:100px;padding:3px;margin-right:4px}'
			. '.lang-switch a{font:12px "Space Mono",monospace;letter-spacing:.06em;text-decoration:none;color:var(--mute);padding:6px 10px;border-radius:100px;line-height:1}'
			. '.lang-switch a:hover{color:var(--ink)}.lang-switch a.is-current{background:var(--ink);color:var(--bg)}'
			. '@media(max-width:600px){.lang-switch a{padding:6px 8px}}</style>' . "\n";
	}, 20 );
}
