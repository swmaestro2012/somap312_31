chrome.extension.onRequest.addListener(function(request, sender, callback)
{
    if (request.action == 'getImagePath') {
    	var min_width = 380;	// minimum width value (px)
    	var min_height = 30;	// minimum height value (px)
        var images = $('img');  // using jquery
    	//var images = document.getElementsByTagName('img');   // non-jquery
    	var count = 0;
        // var process = 'complete';

        var list = [];

    	for (i=0; i<images.length; i++) {
            (function(img,i){
        		if ((img.width > min_width) && (img.height > min_height) && img.src) {
                    $.ajax({
                        type: 'get',
                        url: 'http://61.43.139.108/lot_search.php?url='+img.src,
                        success: function(data, text, k) {
                            var response = data.trim();
                            var json = $.parseJSON(response);

                            // if video data are on serv.
                            if (json.status == 'exist') {
                                // everything was done here
                                var $img = $(img);
                                var offset = $img.offset();
                                var left = offset.left;
                                var top = offset.top;
                                var width = img.width;


                                // add object to body
                                $('body').append("<div id='i2t_badge_" + i + "' style='position:absolute; width: "+width+"px; height: 65px; left: "+left+"px; top: "+top+"px;'>"
                                    +"<div style='padding:5px 10px; float:left; margin-left: 5px; margin-top:5px; background-color: white;"
                                    +"border: 1px solid gray;"
                                    +"'><a href='"+json.video[0].url+"'>"
                                    +"<table style='font-size: 9pt;'>"
                                    
                                    +"<tr>"
                                    +"<td>"
                                    +"<img src='http://www.iconfinder.com/ajax/download/png/?id=49400&s=16' style='border:0px;'>"
                                    +"</td>"
                                    +"<td style='padding-left: 10px;'>"
                                    +json.video[0].title
                                    +"</td>"
                                    +"</tr>"

                                    +"<tr>"
                                    +"<td>"
                                    +"<img src='http://www.iconfinder.com/ajax/download/png/?id=32381&s=16' style='border:0px;'>"
                                    +"</td>"
                                    +"<td style='padding-left: 10px;'>"
                                    +json.video[0].position
                                    +"</td>"
                                    +"</tr>"

                                    +"</table>"
                                    +"</a>"
                                    +"</div><div style='clear:both;'></div></div>");
                                var badge = $('#i2t_badge_' + i);

                                // submit to global array
                                list.push({
                                    img: img,
                                    badge: badge
                                });
                            }

                            else {
                                //alert('none!');
                            }
                        }
                        //, error: function(request, status, err) {}
                    });
                    
        		}
             })(images[i],i);
    	}

        // sensative to browser resizing
        $(window).resize(function() {
            for(var i in list)
            {

                var img = list[i].img;
                var badge = list[i].badge;

                var $img = $(img);
                var offset = $img.offset();
                var left = offset.left;
                var top = offset.top;

                badge.css('left',left);
            }
        });



        //callback(process);    // return to parse.js
    }
});