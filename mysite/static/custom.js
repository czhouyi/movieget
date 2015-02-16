$(document).ready(function () {
	var animations = ['moveup','movedown','osci1'];
    var btns = [['#btnnews','#btnblog'],
                ['#btnnews1','#btnblog1'],
                '#btnreturn'];

    button_up = function() {
		var a = $(btns[0][0]);
		var b = $(btns[0][1]);
		var a1 = $(btns[1][0]);
		var b1 = $(btns[1][1]);
		var animation = animations[0];

		a.addClass(animation);
		b.addClass(animation);

		setTimeout(function(){
			a.removeClass(animation);
			b.removeClass(animation);
            $(btns[2]).show();
			a.hide();a1.show();
			b.hide();b1.show();
			//window.location.href="/main/";
		}, 200);
    }

    button_down = function() {
		var a = $(btns[0][0]);
		var b = $(btns[0][1]);
		var a1 = $(btns[1][0]);
		var b1 = $(btns[1][1]);
		var animation = animations[1];

		a1.addClass(animation);
		b1.addClass(animation);

		setTimeout(function(){
			a1.removeClass(animation);
			b1.removeClass(animation);
            $(btns[2]).hide();
			a.show();a1.hide();
			b.show();b1.hide();
			//window.location.href="/index/";
		}, 200);
    }

    loadPreview = function() {
        var data = ['/static/images/facebook.jpeg','/static/images/google.jpg',
                    '/static/images/sap.jpg','/static/images/youtube.jpg'];
        $('.preview').children().remove();
        data.forEach(appendDiv);
        $('.preview').show();
    }

    appendDiv = function(value, index, ar) {
        var pv = $('.preview');
        x = 0; y = 0; z = 0;
        if (index>=0 && index <=1){
            x = x-index*450;y = y+index*15;
            var topdiv = $("<div class='playout1'><img class='pimg' src='"+value+"'/></div>");
            topdiv.attr('id','pimg'+index);
            //topdiv.css({'-webkit-transform':transform(x,y,z),
              //          '-webkit-animation':osci(x,y,z)+Math.random()*20+"s infinite linear"});
            topdiv.addClass("pn"+(index+1));topdiv.addClass("osci"+(index+1));
            pv.append(topdiv);
        }
        else if(index >= 2 && index <=5){
            var secdiv = $("<div class='playout2'><img class='pimg' src='"+value+"'/></div>");
            secdiv.attr('id','pimg'+index);
            secdiv.addClass("pn"+(index+1));secdiv.addClass("osci"+(index+1));
            pv.append(secdiv);
        }
    }

    showList = function(){
        var data = ['/static/images/facebook.jpeg','/static/images/google.jpg',
                    '/static/images/sap.jpg','/static/images/youtube.jpg'];
        
    }

    osci = function(index){
        var rd = Math.round(Math.random()*2);
        return "{"+
               "0%{ -webkit-transform: rotateX(66deg) rotateY(-1deg) rotateZ(-25deg) translate3d("+x+"px,"+y+"px,"+z+"px);}"+
               "12%{ -webkit-transform: rotateX(66deg) rotateY(-1deg) rotateZ(-25deg) translate3d("+(x-rd*15*1)+"px,"+(y+rd*1*1)+"px,"+z+"px);}"+
               "25%{ -webkit-transform: rotateX(66deg) rotateY(-1deg) rotateZ(-25deg) translate3d("+(x-rd*15*2)+"px,"+(y+rd*1*2)+"px,"+z+"px);}"+
               "37%{ -webkit-transform: rotateX(66deg) rotateY(-1deg) rotateZ(-25deg) translate3d("+(x-rd*15*3)+"px,"+(y+rd*1*3)+"px,"+z+"px);}"+
               "50%{ -webkit-transform: rotateX(66deg) rotateY(-1deg) rotateZ(-25deg) translate3d("+(x-rd*15*4)+"px,"+(y+rd*1*4)+"px,"+z+"px);}"+
               "62%{ -webkit-transform: rotateX(66deg) rotateY(-1deg) rotateZ(-25deg) translate3d("+(x-rd*15*3)+"px,"+(y+rd*1*3)+"px,"+z+"px);}"+
               "75%{ -webkit-transform: rotateX(66deg) rotateY(-1deg) rotateZ(-25deg) translate3d("+(x-rd*15*2)+"px,"+(y+rd*1*2)+"px,"+z+"px);}"+
               "87%{ -webkit-transform: rotateX(66deg) rotateY(-1deg) rotateZ(-25deg) translate3d("+(x-rd*15*1)+"px,"+(y+rd*1*1)+"px,"+z+"px);}"+
               "100%{ -webkit-transform: rotateX(66deg) rotateY(-1deg) rotateZ(-25deg) translate3d("+(x-rd*15*0)+"px,"+(y+rd*1*0)+"px,"+z+"px);}"+
               "} ";
    }

    transform = function(x,y,z){
        return "rotateX(66deg) rotateY(-1deg) rotateZ(-25deg) translate3d("+x+"px,"+y+"px,"+z+"px)";
    }
    
	$('#btnnews').on('click', button_up);
	$('#btnnews').on('click', showList);
	$('#btnnews').on('mouseover', loadPreview);
	$('#btnblog').on('click', button_up);
	$('#btnreturn').on('click', button_down);
    $("#btnnews").mouseover(function(){
        var a = $(".preview");
        a.show();
    }); 
    $("#btnnews").mouseout(function(){
        var a = $(".preview");
        a.hide();
    }); 

    var defaults={
        cont:'',
        prev:'.prev',
        next:'.next',
        time:1000,
        distance:null,
        auto: false,
        autoDelay:"3000"
    };

    $.fn.slider=function(options){
        var o = $.extend({}, defaults, options||{}),self=this;
        var jqCont = $(o.cont, self);
        var jqContWidth = jqCont.width();
        var dist=0,maxDist=jqContWidth-o.distance;
        var setint;
        clearInterval(setint);

        $(o.prev,self).bind('click',function(){
            if(dist>=0) return;
            dist += o.distance;
            if(dist>=0) dist=0;
            jqCont.stop().animate({left:dist},o.time);
        });
        $(o.next,self).bind('click',function(){
            if(Math.abs(dist)>=maxDist) return;
            dist += -o.distance;
            if(Math.abs(dist)>=jqContWidth) dist=-maxDist;
            jqCont.stop().animate({left:dist},o.time);
        });

        self.bind({
            'mouseenter':function(){
                clearInterval(setint);
            },
            'mouseleave':function(){
                setint=setInterval(function(){
                    $(o.next,self).trigger('click');
                }, o.autoDelay);
            }
        });
        if(o.auto){
            self.trigger("mouseleave");
        }
    };

});

function search(keyword) {
    location.assign('https://www.google.com/search?q=' + encodeURIComponent(keyword) + '+site%3A' + location.hostname);
    return false;
}
