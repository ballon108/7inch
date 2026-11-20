#!/usr/bin/env python3
"""Convert existing Media Library JPG/PNG attachments to WebP (one-off; new uploads are converted by the WPCode snippet).
Usage: webp_convert.py all | webp_convert.py 14,87,88 [--dry]
For each attachment: backup of the old original + sizes to uploads/_webp-backup/, new WebP original (quality 82, alpha kept),
attachment meta/mime/guid updated, thumbnails regenerated (WebP), old files deleted, and every reference to the old
file names (post content, post meta, options - serialize-safe) rewritten to the .webp names. Attachment IDs do not change."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__)); import deploy
arg = sys.argv[1] if len(sys.argv) > 1 else "all"
dry = "--dry" in sys.argv
limit = 10
ids = "all" if arg == "all" else [int(x) for x in arg.split(",")]
code = r"""
$want = json_decode('%IDS%', true); $dry = %DRY%; $limit = %LIMIT%;
require_once ABSPATH . 'wp-admin/includes/image.php'; require_once ABSPATH . 'wp-admin/includes/file.php';
global $wpdb; $up = wp_upload_dir(); $base = $up['basedir']; $bk = $base . '/_webp-backup'; $out = [];
if ('all' === $want) {
  $want = $wpdb->get_col("select ID from {$wpdb->posts} where post_type='attachment' and post_mime_type in ('image/jpeg','image/png') order by ID");
  $want = array_slice($want, 0, $limit);
}
function i7_deep_replace($v, $re, $to) {
  if (is_string($v)) { return preg_replace($re, $to, $v); }
  if (is_array($v)) { foreach ($v as $k => $x) { $v[$k] = i7_deep_replace($x, $re, $to); } return $v; }
  if (is_object($v)) { foreach (get_object_vars($v) as $k => $x) { $v->$k = i7_deep_replace($x, $re, $to); } return $v; }
  return $v;
}
function i7_alpha($file) {
  if (!class_exists('Imagick')) { return null; }
  try { $im = new Imagick($file); if (!$im->getImageAlphaChannel()) { return 'none'; }
    $m = $im->getImageChannelMean(Imagick::CHANNEL_ALPHA); $q = $im->getQuantum(); return round(1 - $m['mean'] / $q, 3); } catch (\Throwable $e) { return 'err'; }
}
foreach ($want as $id) {
  $id = (int) $id; $post = get_post($id);
  if (!$post || !in_array($post->post_mime_type, ['image/jpeg', 'image/png'], true)) { $out[] = [$id, 'skip (not jpg/png)']; continue; }
  $file = get_attached_file($id); $rel = get_post_meta($id, '_wp_attached_file', true);
  if (!$file || !file_exists($file)) { $out[] = [$id, 'skip (file missing)']; continue; }
  $meta = wp_get_attachment_metadata($id); $olds = [$file];
  foreach ((array) ($meta['sizes'] ?? []) as $s) { $olds[] = dirname($file) . '/' . $s['file']; }
  if (!empty($meta['original_image'])) { $olds[] = dirname($file) . '/' . $meta['original_image']; }
  $olds = array_values(array_unique(array_filter($olds, 'file_exists')));
  $row = [$id, basename($file), round(filesize($file) / 1024) . ' KB', 'alpha_before' => i7_alpha($file)];
  if ($dry) { $out[] = $row; continue; }
  foreach ($olds as $f) { $dst = $bk . '/' . ltrim(substr($f, strlen($base)), '/'); wp_mkdir_p(dirname($dst)); copy($f, $dst); }
  $ed = wp_get_image_editor($file);
  if (is_wp_error($ed)) { $row[] = 'editor error: ' . $ed->get_error_message(); $out[] = $row; continue; }
  $newrel = preg_replace('/\.(jpe?g|png)$/i', '.webp', $rel); $newfile = $base . '/' . $newrel;
  if (file_exists($newfile)) { $newfile = dirname($newfile) . '/' . wp_unique_filename(dirname($newfile), basename($newfile)); $newrel = ltrim(substr($newfile, strlen($base)), '/'); }
  $ed->set_quality(82); $s = $ed->save($newfile, 'image/webp');
  if (is_wp_error($s) || !file_exists($newfile) || filesize($newfile) < 100) { $row[] = 'save failed'; $out[] = $row; continue; }
  $oldbase = preg_replace('/\.(jpe?g|png)$/i', '', $rel);
  update_attached_file($id, $newfile);
  wp_update_post(['ID' => $id, 'post_mime_type' => 'image/webp', 'guid' => $up['baseurl'] . '/' . $newrel]);
  foreach ($olds as $f) { if ($f !== $newfile && file_exists($f)) { @unlink($f); } }
  delete_post_meta($id, '_wp_attachment_backup_sizes');
  $newmeta = wp_generate_attachment_metadata($id, $newfile); wp_update_attachment_metadata($id, $newmeta);
  // rewrite references to the old file names
  $re = '#(' . preg_quote($oldbase, '#') . ')(-\d+x\d+)?\.(jpe?g|png)#i'; $to = '$1$2.webp'; $n = 0; $like = '%' . $wpdb->esc_like($oldbase) . '%';
  foreach ($wpdb->get_results($wpdb->prepare("select ID,post_content from {$wpdb->posts} where post_type!='attachment' and post_content like %s", $like)) as $p) {
    $c = preg_replace($re, $to, $p->post_content); if ($c !== $p->post_content) { $wpdb->update($wpdb->posts, ['post_content' => $c], ['ID' => $p->ID]); $n++; } }
  foreach ($wpdb->get_results($wpdb->prepare("select meta_id,meta_value from {$wpdb->postmeta} where meta_value like %s and meta_key not in ('_wp_attached_file','_wp_attachment_metadata')", $like)) as $m) {
    $v = maybe_unserialize($m->meta_value); $nv = i7_deep_replace($v, $re, $to); if ($nv !== $v) { $wpdb->update($wpdb->postmeta, ['meta_value' => maybe_serialize($nv)], ['meta_id' => $m->meta_id]); $n++; } }
  foreach ($wpdb->get_results($wpdb->prepare("select option_id,option_name,option_value from {$wpdb->options} where option_value like %s", $like)) as $o) {
    $v = maybe_unserialize($o->option_value); $nv = i7_deep_replace($v, $re, $to); if ($nv !== $v) { $wpdb->update($wpdb->options, ['option_value' => maybe_serialize($nv)], ['option_id' => $o->option_id]); $n++; } }
  $row[] = '-> ' . basename($newfile) . ' ' . round(filesize($newfile) / 1024) . ' KB'; $row['alpha_after'] = i7_alpha($newfile); $row['sizes'] = count($newmeta['sizes'] ?? []); $row['refs_rewritten'] = $n;
  $out[] = $row;
}
wp_cache_flush();
return $out;
"""
import json
code = code.replace("%IDS%", json.dumps(ids)).replace("%DRY%", "true" if dry else "false").replace("%LIMIT%", str(limit))
for r in deploy.php(code):
    print(r)
