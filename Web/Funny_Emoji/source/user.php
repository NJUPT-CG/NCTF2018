<?php
class User{
	var $conn = null;

	public function __construct(){
		 $this->conn = mysql_connect('127.0.0.1','root','toor');
         if(!$this->conn)   die('connect database error');
         mysql_select_db('nctf',$this->conn);
	}

	public function reg_user($username,$password){
		 $query = "insert into users (`username`,`password`) values ('$username','$password')";
         mysql_query($query,$this->conn);
         if(!mysql_insert_id()) die('insert error');
         return 1;
	}

	public function log_user($username,$password){
		 $query = "select * from users where username='$username'";
		 //echo $query;
		 $result = mysql_query($query,$this->conn);
		 $row = mysql_fetch_array($result, MYSQL_ASSOC);
		 //var_dump($row);
		 if($row['password'] === $password){
		 	return $row['username'];
		 }else{
		 	return false;
		 }
	}

	public function check($username){
		 $query = "select * from users where username='$username' limit 1";
         $result = mysql_query($query,$this->conn);
         $row = mysql_fetch_array($result, MYSQL_ASSOC);
         if($row){
             die("<script>alert('This username has been used');window.location.href='index.php'</script>");
        }
        return 1;
	}

	public function __destruct(){
         mysql_close($this->conn);
     }

}

class Filter{
	public function check($value){
		if(preg_match('/[^a-zA-Z0-9]/i', $value))	
			die("<script>alert('[a-zA-Z0-9]{1,9}');window.location.href='login.php'</script>");

		return addslashes($value);
	}

	public function sqli_check($value){
		$black = '/order|limit|by|#|\s|>|=|<|;|substr|mid|chr|union|all|sleep|from|load_file|outfile|into|lpad|rpad|left|right|if|select/i';
		if(preg_match($black, $value)){
			die('illegal_thing');
		}
		return $value;
	}

	function check_emoji_name($value){
		if(!preg_match('/[a-zA-Z0-9]{1,20}/', $value))	die('illegal_name');
		return $value;
	}
}

function rand_str($length=16){
	$li = 'qazwsxedcrfvtgbyhnujmiklop0987654321';
	srand(time(NULL));
	$s = '';
	for($i=0;$i<$length;$i++){
		$s .= $li[rand(0,strlen($li)-1)];
	}
	return $s;
}

	



?>
