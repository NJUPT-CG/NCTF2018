<?php

$seed = '2163713';
function getip(){
		if($_SERVER['HTTP_X_FORWARDED_FOR']){
   	        die('X_FORWARDED_FOR is good,but can you find another one?');
        } elseif($_SERVER['HTTP_CLIENT_IP']){
         	$ip = $_SERVER['HTTP_CLIENT_IP'];
        } else{
	        $ip = $_SERVER['REMOTE_ADDR'];
         }
       $ip  = preg_match('/^([0-9]{1,3}\.){3}[0-9]{1,3}$/',$ip) ? $ip : 'Unknown';
       return $ip;
	}

?>









































