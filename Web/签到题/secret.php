<?php
   setcookie("nctf2018","where is flag?"); 
   $ch = curl_init(); 
   curl_setopt($ch, CURLOPT_URL, "https://www.baidu.com"); 
   curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
   curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); //这个是重点,规避ssl的证书检查。
   curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, FALSE); // 跳过host验证
   $output = curl_exec($ch); 
   echo $output;
   curl_close($ch);      
