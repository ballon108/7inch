#!/usr/bin/env python3
"""B2BKing registration for commercial accounts: roles "Shop" (group 130) and "Distributor" (group 131), both activated by
e-mail confirmation (see theme/inc/account-verification.php). Idempotent."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__)); import deploy
r = deploy.php(r"""
$groups = ['Shop'=>130,'Distributor'=>131]; $ids = []; $log = [];
foreach ($groups as $title => $gid) {
  $ex = get_posts(['post_type'=>'b2bking_custom_role','title'=>$title,'post_status'=>'any','numberposts'=>1]);
  $id = $ex ? $ex[0]->ID : wp_insert_post(['post_type'=>'b2bking_custom_role','post_title'=>$title,'post_status'=>'publish']);
  update_post_meta($id,'b2bking_custom_role_status','1');
  update_post_meta($id,'b2bking_custom_role_approval','manual');                       // account stays pending until the e-mail link is used
  update_post_meta($id,'b2bking_custom_role_automatic_approval_group','group_'.$gid);  // group given on confirmation
  update_post_meta($id,'_i7_email_verify','1');
  $ids[$title] = $id;
}
// retire the generic admin-approved "B2B" registration role (replaced by Shop / Distributor)
update_post_meta(118,'b2bking_custom_role_status','0');
// registration fields: show for Shop + Distributor
$val = 'role_'.$ids['Shop'].',role_'.$ids['Distributor'];
foreach (get_posts(['post_type'=>'b2bking_custom_field','numberposts'=>-1,'post_status'=>'any']) as $f) {
  update_post_meta($f->ID,'b2bking_custom_field_registration_role','multipleroles');
  update_post_meta($f->ID,'b2bking_custom_field_multiple_roles',$val);
}
update_option('b2bking_approval_pending_frontend_text_setting','Thank you for registering. We have sent you an e-mail with a confirmation link - open it to activate your account.');
return ['roles'=>$ids,'fields'=>$val,'role118_status'=>get_post_meta(118,'b2bking_custom_role_status',true)];""")
print(json.dumps(r))
