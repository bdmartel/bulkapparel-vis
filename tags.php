<?php
// Tags for the color browser, kept on the server so they match on every device.
// Only for someone signed in with the shared benmartel.com sign-in; anyone else gets 401 and the page
// keeps its tags in that browser only. The data lives outside the web root (DATA below), never in the repo.
//   GET               {ok, tags:{slug:[tag,...]}, bought:{slug:[{d,n,order},...]}}
//   POST {set:{slug:[tag,...]}}   replaces the tags of each slug given (an empty list clears it)
session_name('bm_sess');
session_set_cookie_params(['lifetime' => 7776000, 'path' => '/', 'domain' => '.benmartel.com', 'secure' => true, 'httponly' => true, 'samesite' => 'Lax']);
session_start();
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex, nofollow');
$signedIn = !empty($_SESSION['ok']);
session_write_close();
if (!$signedIn) {
  http_response_code(401);
  echo json_encode(['ok' => false, 'login' => 'https://claude.benmartel.com/?next=' . rawurlencode('https://bulkapparel.benmartel.com/')]);
  exit;
}

const DATA = '/var/www/bulkapparel-data';
$tagsFile = DATA . '/tags.json';
$boughtFile = DATA . '/bought.json';
function jread(string $f) { return is_file($f) ? (json_decode((string)file_get_contents($f), true) ?: []) : []; }

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  // same-site only: a JSON body from this page
  $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
  if ($origin !== 'https://bulkapparel.benmartel.com' || stripos($_SERVER['CONTENT_TYPE'] ?? '', 'application/json') !== 0) {
    http_response_code(403); echo json_encode(['ok' => false, 'error' => 'bad origin']); exit;
  }
  $in = json_decode((string)file_get_contents('php://input', false, null, 0, 200000), true);
  if (!is_array($in) || !is_array($in['set'] ?? null)) { http_response_code(400); echo json_encode(['ok' => false]); exit; }
  $fh = fopen("$tagsFile.lock", 'c'); flock($fh, LOCK_EX);
  $tags = jread($tagsFile);
  foreach ($in['set'] as $slug => $list) {
    if (!preg_match('/^[a-z0-9-]{1,60}$/', (string)$slug) || !is_array($list)) continue;
    $clean = [];
    foreach ($list as $t) {
      $t = trim(mb_strtolower(preg_replace('/\s+/', ' ', (string)$t)));
      if ($t !== '' && mb_strlen($t) <= 40 && !in_array($t, $clean, true)) $clean[] = $t;
    }
    if ($clean) $tags[$slug] = array_slice($clean, 0, 30); else unset($tags[$slug]);
  }
  ksort($tags);
  file_put_contents("$tagsFile.tmp", json_encode($tags, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
  rename("$tagsFile.tmp", $tagsFile);
  flock($fh, LOCK_UN);
  echo json_encode(['ok' => true, 'tags' => $tags]);
  exit;
}

echo json_encode(['ok' => true, 'tags' => (object)jread($tagsFile), 'bought' => (object)jread($boughtFile)]);
