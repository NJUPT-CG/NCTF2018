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