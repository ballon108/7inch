/**
 * WPCode snippet: "Cookie notice: standalone styling (password page)". Location: Run everywhere.
 * The ASE "Password protection" page is a bare login-style template (login_head / login_footer) that
 * does not load the theme stylesheet, so the Cookie Notice banner fell back to the plugin defaults.
 * This prints the same banner styling with its own colour tokens on that page only.
 */
add_action( 'login_head', function () {
	$base = get_theme_file_uri( 'assets/fonts/' );
	?>
<style id="i7-cookie-standalone">
@font-face{font-family:Inter;font-weight:400;font-style:normal;font-display:swap;src:url(<?php echo esc_url( $base ); ?>inter-latin-400.woff2) format("woff2")}
@font-face{font-family:Inter;font-weight:500;font-style:normal;font-display:swap;src:url(<?php echo esc_url( $base ); ?>inter-latin-500.woff2) format("woff2")}
:root{--ink:#FCFCFA;--ash:#A9B0AB;--mute:#8A928D;--mp:#FF6A2B;--halo:#2E3A2F;--line:#1E2623;--card:#0A0F0D}
#cookie-notice{font-family:Inter,system-ui,sans-serif}
#cookie-notice{left:50%!important;right:auto!important;bottom:20px!important;top:auto!important;transform:translateX(-50%);width:min(780px,calc(100% - 32px))!important;min-width:0!important;
 background:var(--card)!important;color:var(--ink)!important;border:1px solid var(--line);border-radius:16px;box-shadow:0 18px 50px rgba(0,0,0,.55);padding:0!important;font-family:inherit;z-index:99999}
#cookie-notice .cookie-notice-container{color:var(--ink)!important;display:flex;align-items:center;gap:18px 24px;flex-wrap:wrap;padding:20px 24px!important;text-align:left}
#cookie-notice .cn-text-container{flex:1 1 320px;margin:0!important;font-size:14px;line-height:1.55;color:var(--ash)}
#cookie-notice .cn-buttons-container{display:flex;flex-wrap:wrap;align-items:center;gap:10px;flex:0 0 auto;margin:0!important}
#cookie-notice .cn-button{font-family:inherit;font-size:13px;font-weight:500;letter-spacing:.01em;line-height:1;margin:0!important;padding:13px 20px!important;border-radius:999px!important;border:1px solid var(--mp)!important;background:var(--mp)!important;color:#0A0F0D!important;cursor:pointer;transition:background .15s,color .15s,border-color .15s}
#cookie-notice .cn-button:hover{filter:brightness(1.08)}
#cookie-notice #cn-refuse-cookie{background:transparent!important;color:var(--ink)!important;border-color:var(--halo)!important}
#cookie-notice #cn-refuse-cookie:hover{border-color:var(--ink)!important}
#cookie-notice .cn-more-info{background:transparent!important;border-color:transparent!important;color:var(--mute)!important;padding:13px 6px!important;text-decoration:underline;text-underline-offset:3px}
#cookie-notice .cn-more-info:hover{color:var(--ink)!important}
#cookie-notice .cn-close-icon{display:none!important}  /* closing must not count as consent */
#cookie-notice .cookie-revoke-container{color:var(--ash)!important;padding:16px 24px!important}
#cookie-notice .cookie-revoke-container .cn-text-container{font-size:14px}
@media(max-width:600px){#cookie-notice{bottom:12px!important}#cookie-notice .cookie-notice-container{padding:18px!important}#cookie-notice .cn-buttons-container{width:100%}#cookie-notice .cn-set-cookie{flex:1 1 auto;text-align:center}}
body.cookies-set #cookie-notice,#cookie-notice.cookie-notice-hidden{display:none!important}
</style>
	<?php
} );
