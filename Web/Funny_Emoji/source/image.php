<?php
ini_set('open_basedir', '.:/tmp');
$x=isset($_GET['x'])?$_GET['x']:80;
$y=isset($_GET['y'])?$_GET['y']:380;

session_start();
if(!isset($_SESSION['user']))
    die('plz,login');
else{       
    if(!isset($_GET['name']) || empty($_GET['name'])){
        $dst_path = 'image/tiangou.jpg';    
    }else{
        $dst_path = getpath($_GET['name']); 
    }

    if(!isset($_GET['ptl']) || empty($_GET['ptl'])){
        $content = 'data://text/plain,小老弟你怎么回事';
    }else{
        $content = decccccrypt($_GET['ptl']).$_GET['data'];
    }    
}


generate($dst_path,$x,$y,$content);

function generate($dst_path,$x,$y,$content){
    $dst = imagecreatefromstring(file_get_contents($dst_path));
    $font = './simsun.ttc';
    $black = imagecolorallocate($dst, 0x00, 0x00, 0x00);//字体颜色
    imagefttext($dst, 20, 0, $x, $y, $black, $font, file_get_contents($content));
    //imagefttext($dst, 10, 0, 0, 440, $black, $font, $watermark);
    list($dst_w, $dst_h, $dst_type) = getimagesize($dst_path);
    //var_dump($dst_w);
    header('Content-Type: image/jpg');
    imagejpeg($dst);
    imagedestroy($dst);
}

function decccccrypt($s){
    $key = 'nctf23333';
    $s = base64_decode($s);
    $flag = '';
    for ($i=0; $i < strlen($s); $i++) {
        $flag .= chr(ord($s[$i])^ord($key[$i%9]));
    }
    return $flag;
}

function getpath($name){
    $default_dir = 'images/';
    $files = scandir($default_dir);
    for($i=0;$i<count($files);$i++){
        if($files[$i] == $name.'.jpg'){
            return $default_dir.$name.'.jpg';
        }
    }

    $user = $_SESSION['user'];
    $secret_key = $_SESSION['secret'];
    if($user === 'admin'){
        $d = 'tmp/'.md5($secret_key.$_SESSION['IP']);
        $admin_dir = dir($d);
        while(false !== ($filename=$admin_dir->read())){
            if($filename === '.' || $filename === '..')   continue;
            if($filename == $name.'.jpg'){
                return $d.'/'.$name.'.jpg';
            }
        }
    
        return 'image/tiangou.jpg';
    }
}
