这题其实就是几个trick。

1. `$_REQUEST` 变量虽然说是包含 `$_GET,$_POST,$_COOKIE` 这些，但实际上却存在一个覆盖的问题，就是当 get 和 post 中有一个同名变量 data 时，在 request变量数组 中只会有一个名为 data 的变量，并且获取的是 post 的值。通过这样的覆盖，从而绕过对 get 变量的值的过滤。

2. `$_SERVER['QUERY_STRING']` 这里的bypass，这个点应该是比较常见的了，`$_SERVER['QUERY_STRING']` 获取的值是未经urldecode的，所以直接编码一下就好了。

3. 数组这里，fuzz一下，很容易发现数组是可绕的（参见同类型的漏洞也容易想到）。

4. file_get_contents 这里要用伪协议其实很容易想到，但很多人似乎就想着用 `php://input` ，这里因为要去覆盖 `$_REQUEST` ，所以假如是用 post 去覆盖的话，就不能用`php://input` 了。最简单的，用 `data://` 协议就好了。

5. `preg_match('/nctfisfun$/', $_GET['nctf']) && $_GET['nctf'] !== 'nctfisfun'` 这个点，可能做起来的时候会觉得很奇怪，这里有什么好绕的？实际上，是因为出题人又双叒叕写错正则了。本来是想写 `preg_match('/^nctfisfun$/', $_GET['nctf']) && $_GET['nctf'] !== 'nctfisfun'`，然后让去看后面那个 $ 符的。。。



   payload：出题人忘了，并且不想做题，大家按着上面的点去打吧


```php+HTML
<?php
highlight_file(__FILE__);
error_reporting(0);
if($_REQUEST){
    foreach ($_REQUEST as $key => $value) {
        if(preg_match('/[a-zA-Z]/i', $value))   die('waf..');
    }
}

if($_SERVER){
    if(preg_match('/yulige|flag|nctf/i', $_SERVER['QUERY_STRING']))  die('waf..');
}

if(isset($_GET['yulige'])){
    if(!(substr($_GET['yulige'], 32) === md5($_GET['yulige']))){         //日爆md5!!!!!!
        die('waf..');
    }else{
        if(preg_match('/nctfisfun$/', $_GET['nctf']) && $_GET['nctf'] !== 'nctfisfun'){
            $getflag = file_get_contents($_GET['flag']);
        }
        if(isset($getflag) && $getflag === 'ccc_liubi'){
            include 'flag.php';
            echo $flag;
        }else die('waf..');
    }
}


?>

```

