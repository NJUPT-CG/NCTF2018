<?php
session_start();
$flag = 1;
if(!isset($_SESSION['user']))
	$flag = 0;
?>

<?php
function show_option(){
    $dir = 'images';
    $files = scandir($dir);
    for($i=2;$i<count($files);$i++){
        $filename = explode('.', $files[$i])[0];
        echo '<option value="'.$filename.'">'.$filename.'</option>';
    }

    if($_SESSION['user'] === 'admin'){
        $secret_key = $_SESSION['secret'];
        $d = 'tmp/'.md5($secret_key.$_SESSION['IP']);
        if(!is_dir($d)){
		mkdir($d,0777);
		chmod($d,0777);
	}
	//var_dump($_SESSION);
	
        $admin_dir = dir($d);
        while(false !== ($filename=$admin_dir->read())){
            if($filename === '.' || $filename === '..')   continue;
            $filename = explode('.', $filename)[0];
            echo '<option value="'.$filename.'">'.$filename.'</option>';
        }
    }
}

?>

<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="">
        <meta name="author" content="">
        <link rel="shortcut icon" type="image/png" href="./images/rabbit.jpg">
        <title>ccc</title>

        <!-- CSS -->
        <link href="./public/css/bootstrap.css" rel="stylesheet">
        <link href="./public/css/main.css" rel="stylesheet">
        
        <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
        <![endif]-->
<style>
.animatedSearch {
    width: 50%;
    border: 1px solid #ccc;
    font-size: 1.2rem;
    border-radius: 5px;
    padding: 5px 8px;
    color: #333;
    transition: width 0.4s ease-in-out;
}

/**/
.animatedSearch:focus {
    width: 90%;
}
</style>
        <script src="./public/js/jquery-1.10.2.min.js"></script>
        <script src="./public/js/bootstrap.min.js"></script>
        <script src="./public/js/angular.js" type="text/javascript"></script>
        <script src="./public/js/angular-resource.js" type="text/javascript"></script>
        <script src="./public/js/angular-route.js" type="text/javascript"></script>
        <script src="./public/js/services.js" type="text/javascript"></script>
            </head>

    <body>

        

<div ng-controller="">
    <div class="navbar navbar-fixed-top navbar-inverse" role="navigation">
        <div class="container">
            <div class="navbar-header">
                <a class="navbar-brand" href="#">ccc</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                                    <li class="dropdown">
                                        <a href="login.php" class="dropdown-toggle" data-toggle="dropdown">登陆 </a>
                                    </li>
                                    <li class="dropdown">
                                        <a href="register.php" class="dropdown-toggle" data-toggle="dropdown">注册 </a>
                                    </li>
                                    <li class="dropdown">
                                        <a href="index.php" class="dropdown-toggle" data-toggle="dropdown">emoji </a>
                                    </li>
                                    <li class="dropdown">
                                        <a href="logout.php" class="dropdown-toggle" data-toggle="dropdown">Logout </a>
                                    </li>
                                </ul> 
                <form class="navbar-form navbar-right" role="form" method="get" action="/">
                
                </form>
            </div>
        </div>
    </div>
    <div class="cpsbg">
        <div class="container">
            <div class="row">
                <div class="col-md-2">
                </div>
                <div class="col-md-8 whitebg">
                    <ul class="list-group">
                        <div style="text-align: center;">
                        <h1>emoji</h1>
                    <select onChange="get_images()" id='sel' >
<?php 
if($flag) show_option();
else die('<script>alert(\'not login\');window.location=\'login.php\'</script>');
?>
</select>
<br />
<br />
<img src="images/rabbit.jpg" id='ima' />
<!-- php动态生成option -->
<!-- js来控制图片的显示 -->
<br />
<h1>get_emoji</h1>
<br />
<textarea rows="5" cols="35" id="text" >
xixixi
</textarea>
<button onclick="get_my_image()">generate</button>
<br />
    <img src="" id="ima2" />

                        </div>
                    </ul>
                    <table class="table table-hover">


</table>

                </div>
                <div class="col-md-2">
                </div>
            </div>
        </div>
    </div>

</div>
<script type="text/javascript">
    eval(function(p,a,c,k,e,d){e=function(c){return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)d[e(c)]=k[c]||e(c);k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p;}('5 m(s){9=\'\';x(i=0;i<s.e;i++){9+=v.w(s.c(i)^8.c(i%8.e))}h y(9)}1 8=\'u\';5 k(s){h s.p(\'\\n\',\'%r\')}1 j=q;5 z(){1 s=2.3(\'f\');1 i=2.3(\'H\');1 4=s.b;i.o="G/"+s.d[4].7+".J"}5 F(){1 s=2.3(\'f\');1 i=2.3(\'B\');1 t=2.3(\'E\');1 4=s.b;1 g=s.d[4].7;1 l=t.7;1 6=m(j("D"));1 a=k(l);i.o="C.A?I="+g+"&a="+a+"&6="+6}',46,46,'|var|document|getElementById|index|function|ptl|value|key|flag|data|selectedIndex|charCodeAt|options|length|sel|im_name|return||enccccrypt|hold_data|im_text|encccccrypt||src|replace|atob|0a|||nctf23333|String|fromCharCode|for|btoa|get_images|php|ima2|image|ZGF0YTovL3RleHQvcGxhaW4s|text|get_my_image|images|ima|name|jpg'.split('|'),0,{}))

</script>
    </body>
</html>









 
