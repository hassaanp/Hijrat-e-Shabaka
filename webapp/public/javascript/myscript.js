var selected=0;
var list=[];
var popo;
$(document).ready(function(){
	$('#login').mouseenter(function(){
		$('#login').fadeTo('fast',0.8);
	});
	$('#login').mouseleave(function(){
		$('#login').fadeTo('fast',1);
	});
	$('#mig').css('height', $('#mig').height());
	$('#scroller').css('height', $('#scroller').height());
    $('#scroller li').click(function(){
		var temp = $(this).text()
		$('#mig').append('<li name="mig1" id="mig1">'+temp+'</li>');		
		$(this).remove();
        list[list.length]=temp;
		if(selected==0){
			$('#button').css('visibility','visible');
			selected =1;		
		}
	});
	$('#button').mouseenter(function(){
		$('#button').fadeTo('fast',0.8);
	});
	$('#button').mouseleave(function(){
		$('#button').fadeTo('fast',1);
	}); 
	$('#button').click(function(){
		$('#button').fadeTo('fast',1);
		$.post("/migrate", { "name": document.getElementsByName("mig")[0].innerHTML});
	});   
});
