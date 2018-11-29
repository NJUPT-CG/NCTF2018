<?php


if (!session_id()) session_start();
error_reporting(0);
if(isset($_SESSION['count'])){
if(!isset($_POST['input'])||strlen($_POST['input'])<22||!is_numeric($_POST['input'])||intval($_POST['input'])<=0){
	session_destroy();
	echo '
	<script language="javascript">  
	alert("请输入一个位数大于21的数!!!");  
	window.history.back(-1);  </script>';
	}
}
if(preg_match("/[a-zA-Z]+/",$_POST['input'])||preg_match("/[a-zA-Z]+/",$_POST['ans'])){
	echo '
	<script language="javascript">  
	alert("请不要输入字母!!!");  
	window.history.back(-1);  </script>';
}
if(!isset($_SESSION['count']))
$_SESSION['count']=0;
if(isset($_SESSION['ans']) && isset($_POST['ans'])){
	if(($_SESSION['ans'])+intval($_POST['input'])!=$_POST['ans']){
		session_destroy();
		echo '
		<script language="javascript">  
		alert("怎么没算对呢？");  
		window.history.back(-1);  </script>';
	}
	else{
		if(intval(time())-$_SESSION['time']<1){
			session_destroy();
			echo '
			<script language="javascript">  
			alert("你手速太快啦，服务器承受不住!!!");  
			window.history.back(-1); </script> ';
		}
		if(intval(time())-$_SESSION['time']>2){
			session_destroy();
			echo '
			<script language="javascript">  
			alert("你算的太慢了少年！");  
			window.history.back(-1); </script> ';
		}
		echo '
		<script language="javascript">  
		alert("tql，算对了！！");  
	     </script> ';
		$_SESSION['count']++;
	}
}



if($_SESSION['count']>=5){
	session_destroy();
	die('nctf{Y0u_ar3_th3_sTr0ng3st_br41n}');
}
$num1=rand(0,10000000);
$num2=rand(0,10000000);
$num3=rand(0,10000000);
$num4=rand(0,10000000);
$num5=rand(0,10000000);
$num6=rand(0,10000000);
$num7=rand(0,10000000);
$num8=rand(0,10000000);
$num9=rand(0,10000000);
$mark=rand(0,3);

switch($mark){
case 0:
	$_SESSION['ans']=$num1+$num2*$num3+$num4-$num5+$num6*$num7-$num8*$num9;
	break;
case 1:
	$_SESSION['ans']=$num1-$num2+$num3-$num4+$num5+$num6-$num7+$num8-$num9;
	break;
case 2:
	$_SESSION['ans']=$num1*$num2-$num3+$num4+$num5*$num6+$num7-$num8*$num9;
	break;
case 3:
	$_SESSION['ans']=$num1+$num2+$num3*$num4-$num5-$num6+$num7*$num8+$num9;
	break;
}
$_SESSION['time']=intval(time());

?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="author" content="Kodinger">
	<meta name="viewport" content="width=device-width,initial-scale=1">
	<title>最强大脑</title>
	<link rel="stylesheet" type="text/css" href="./static/bootstrap/css/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="./static/css/main.css">
</head>
<body class="my-login-page">
    <div class="d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom box-shadow">
      <h5 class="my-0 mr-md-auto font-weight-normal">小绿草之最强大脑</h5>
    </div>
	<section class="h h-100">
		<div class="container h-100">
			<h1 class="articles">目前平台的问题：钱不够、bug多、程序员跑路...</h1>

			<div id="article_list" class="row justify-content-md-center">
                        
                        <a href="#" class="card fat col-md-5 article-card">
			    <div class="card-body">
			     <b class="text-info article">tip:</b>请输入一个位数大于21的正数加入式子进行计算出"正确结果"并提交。
			    </div>
		        </a>
                        
                        <a href="#" class="card fat col-md-5 article-card">
			    <div class="card-body">
			     <b class="text-info article">tip:</b>他是黑客！他能口算md5，XSS自己打自己，CSRF帮别人支付账单...
			    </div>
		        </a>
<p  align="right">现在已经连续答对了<?php echo $_SESSION['count'];?>次</p>
		        
                    <form action="" method="post">
					 <input type="text" name="input"><div  style="display:inline;">+</div>
					<?php
					$sentence="";

					switch($mark){
					case 0:
						$sentence="$num1+$num2*$num3+$num4-$num5+$num6*$num7-$num8*$num9=";
						break;
					case 1:
						$sentence="$num1-$num2+$num3-$num4+$num5+$num6-$num7+$num8-$num9=";
						break;
					case 2:
						$sentence="$num1*$num2-$num3+$num4+$num5*$num6+$num7-$num8*$num9=";
						break;
					case 3:
						$sentence="$num1+$num2+$num3*$num4-$num5-$num6+$num7*$num8+$num9=";
						break;
					}
					for($i=0;$i<strlen($sentence);$i++){
						echo "<div style=\"display:inline;\">".$sentence[$i]."</div>";
					}
					?>

					<input type="text" name="ans">
					<input type="submit" value="验证答案">
					</form>    
			</div>
			
		</div>
	</section>
<!--源码泄露了解一下？-->
	<script src="./static/js/jquery.min.js"></script>
	<script src="./static/js/main.js"></script>
</body>
</html>





