

  萌新难度的题，可能是因为 viewsource 那个参数放的太底下了，一开始很多人都没看到。题目的点其实很明显，就是 header() 函数没有exit的话，后面的代码并不会结束而会继续执行的。所以下面那个读文件的地方就可以直接传入参数调用了（抓包来看返回的结果）。再看 de_code() 函数，就是减了一下下标然后base64编码了一次，这个python写一下就出来了。

```python

```



  似乎有的萌新因为经验不足，没有发现有flag.php，然后把getip.php给读了，甚至把我瞎写的随机数也给日下来了。。。

```php+HTML
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
。
。
。
<!-- post me viewsource -->

```

