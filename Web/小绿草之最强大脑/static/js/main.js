$(function() {
	$("input[type='password'][data-eye]").each(function(i) {
		var $this = $(this);

		$this.wrap($("<div/>", {
			style: 'position:relative'
		}));
		$this.css({
			paddingRight: 60
		});
		$this.after($("<div/>", {
			html: 'Show',
			class: 'btn btn-info btn-sm',
			id: 'passeye-toggle-'+i,
			style: 'position:absolute;right:10px;top:50%;transform:translate(0,-50%);-webkit-transform:translate(0,-50%);-o-transform:translate(0,-50%);padding: 2px 7px;font-size:12px;cursor:pointer;'
		}));
		$this.after($("<input/>", {
			type: 'hidden',
			id: 'passeye-' + i
		}));
		$this.on("keyup paste", function() {
			$("#passeye-"+i).val($(this).val());
		});
		$("#passeye-toggle-"+i).on("click", function() {
			if($this.hasClass("show")) {
				$this.attr('type', 'password');
				$this.removeClass("show");
				$(this).removeClass("btn-outline-primary");
			}else{
				$this.attr('type', 'text');
				$this.val($("#passeye-"+i).val());				
				$this.addClass("show");
				$(this).addClass("btn-outline-primary");
			}
		});
	});
});

function add_article(){
	$.post('api.php?action=add_article',{'title':$('#title').val(),'content':$('#content').val()},function(data){
		alert(data['msg']);
	});
}

function report(){
	$.post('api.php?action=report',{'url':$('#url').val(),'code':$('#code').val()},function(data){
		alert(data['msg']);
	});
}

function usr_info(data){
	$('.role').html(data['role']);
}

function article_list(data){
	for(var i=0;i<data.length;i++){
		$('#article_list').append('\
		<a href="detail.php?id='+data[i]['id']+'" class="card fat col-md-5 article-card">\
			<div class="card-body">\
			<b class="text-info article">id:</b>'+data[i]['id']+'<br/>\
			<b class="text-info article">title:</b>'+data[i]['title']+'\
			</div>\
		</a>');
	}
}

function detail(data){
	$('.detail .card-title').html(data['title']);
	$('.detail .card-body').html(data['content']);
}

$('#report').click(report);
$('#add_article').click(add_article);