<?php
include 'user.php';

session_start();
$user = new User;

if(!isset($_SESSION['user'])){
	if(isset($_POST['register'])){
	$username = Filter::check($_POST['username']);
	$password = Filter::check($_POST['password']);
	if($user->check($username) && $user->reg_user($username,$password)){
		$html = 'register success';
		//echo 'success_html here';
		}
	}else{
		$html = '<form action="register.php" method="POST" />
			<input type="text" name="username" value="" /><br /><br />
			<input type="password" name="password" value="" /><br /><br />
			<input type="submit" name="register" value="Submit" />
			</form>';
		}
}else{
	header("location:index.php");
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
                        <h1>世界上更好看的注册框</h1>
                    <?php echo $html;?>


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
    </body>
</html>
