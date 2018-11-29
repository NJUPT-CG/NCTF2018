<?php
error_reporting(0);
include 'getip.php';
ini_set('open_basedir','.');
if(isset($_POST['viewsource'])){
	highlight_file(__FILE__);
	die();
}

mt_srand(mktime()+$seed);

function de_code($value){
	$value = base64_decode($value);
	$result = '';
	for($i=0;$i<strlen($value);$i++){
		$result .= chr(ord($value[$i])-$i*2);
	}
	return $result;
}

if(!(getip() === '127.0.0.1' && file_get_contents($_GET['9527']) === 'nctf_is_good' && mt_rand(1,10000) === intval($_GET['go_Lakers']))){
	header('location:https://bbs.hupu.com/24483652.html?share_from=kqapp');
}else{
	echo 'great';
}

echo file_get_contents(de_code($_GET['file_']));

?>

<!DOCTYPE html>
<html>
<head>
	<title>嘻嘻嘻</title>
</head>
<body>
<h3>题目在哪呢</h3>
</body>
</html>>

























































































































<!-- post me viewsource -->
