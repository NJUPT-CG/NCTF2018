<?php

include 'upload.php';
include 'user.php';
session_start();
if(!isset($_SESSION['user']) || $_SESSION['user'] !== 'admin' )	die('plz_login||maybe_u_r_not_admin');
//var_dump($_SERVER['REMOTE_ADDR']);
$user = $_SESSION['user'];
$secret_key = $_SESSION['secret'];
$dir = 'tmp/'.md5($secret_key.$_SESSION['IP']).'/';
if(!is_dir($dir)){
	mkdir($dir,0777);
	chmod($dir,0777);
}
ini_set("open_basedir", $dir);

if(isset($_POST['upload'])){
	$parts = pathinfo($_FILES['upfile']['name']);
	$ext = $parts['extension'];
	$name = Filter::check_emoji_name($_POST['name_of_emoji']).'.'.$ext;
	$file = $dir.$name;
	//var_dump($file);
	if(is_file($file)) unlink($file);
	$upload = new Upload($_FILES, $dir, $name, 'jpg');
	if($upload->save()) {
		echo "<script>alert('upload success');window.location('index.php')</script>";
	}else{
		echo 'something_error';
	}
}









?>



<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<html>
<head>
<title>图片上传</title>
<style type="text/css">
<!--
body
{
     font-size: 9pt;
}
input
{
     background-color: #66CCFF;
     border: 1px inset #CCCCCC;
}
-->
</style>
</head>
 
<body>
<form enctype="multipart/form-data" method="post" name="upform">
  上传文件:
  <input name="upfile" type="file">
  <input type="text" name="name_of_emoji" placeholder="表情的名字">
  <input type="submit" name="upload" value="上传"><br>
</form>
 
