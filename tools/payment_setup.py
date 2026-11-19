#!/usr/bin/env python3
"""Interim payment setup: SEPA bank transfer (BACS gateway) as the only payment method until Mollie goes live.
Re-run after Mollie is installed with --off to disable it again."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__)); import deploy

ENABLE = "--off" not in sys.argv
print(deploy.php(r"""
$enable = %s;
$gw = WC()->payment_gateways()->payment_gateways();
$out = [];
if ($enable) {
  update_option('woocommerce_bacs_settings', [
    'enabled' => 'yes',
    'title' => 'Bank transfer (SEPA)',
    'description' => 'Pay by bank transfer. We ship as soon as the payment has arrived. Please use your order number as the payment reference.',
    'instructions' => 'Please transfer the total amount to the account below, using your order number as the reference. Your order will be shipped once the payment has been received.',
  ]);
  update_option('woocommerce_bacs_accounts', [[
    'account_name' => '7inch', 'bank_name' => '', 'account_number' => '',
    'sort_code' => '', 'iban' => 'DE20 4005 0150 0000 0725 46', 'bic' => 'WELADED1MST',
  ]]);
  update_option('woocommerce_default_gateway', 'bacs');
  // make bank transfer the only method (cheque / COD off; Mollie methods are left alone if installed)
  foreach (['cheque','cod'] as $id) {
    $s = get_option("woocommerce_{$id}_settings", []); $s['enabled'] = 'no'; update_option("woocommerce_{$id}_settings", $s);
  }
} else {
  $s = get_option('woocommerce_bacs_settings', []); $s['enabled'] = 'no'; update_option('woocommerce_bacs_settings', $s);
}
foreach (WC()->payment_gateways()->get_available_payment_gateways() as $id => $g) $out[] = $id;
return ['available' => $out, 'accounts' => get_option('woocommerce_bacs_accounts')];
""" % ("true" if ENABLE else "false")))
