(function($){ 
  
  $.fn.jslider = function(options){
    
    var defaults = {
      width: '610px',
      height: '225px',
      slider_height: '24px',
      content_height: '180px',
      block_width: '590px',
      block_padding: '10px',
      animation_time: 300,
      animation_type: 'linear'
    };
    var options = $.extend(defaults, options);
    
    return this.each(function() {
      
      // get handle to jslider wrapper div
      var t = $(this);
      
      // initialize final html
      var html = '';
      var slider_html = '';
      var content_html = '';
      var content_blocks = t.children('div').size();
      var content_width = parseInt(options.width)*content_blocks+"px";
      
      t.children('div').each(function() {
        var index = t.children('div').index(this); // 0, 1, 2, ...
        var title = $(this).children('input').val();
        var description = $(this).children('div').html();
        
        // prepare slider
        if(index == 0) {
          slider_html += '<h2>'+title+'</h2>';
          slider_html += '<ul>';
          slider_html += '  <li class="selected">'+(index+1)+'</li>';
          content_html += '<div class="block" style="visibility:visible">';
        }
        else {
          slider_html += '  <li>'+(index+1)+'</li>';
          content_html += '<div class="block">';
        }
        
        content_html += ' <input type="hidden" value="'+title+'"/>';
        content_html += ' '+description;
        content_html += '</div>';
      });
      
      // prepare final html's
      slider_html += '  <div class="clear"></div>';
      slider_html += '</ul>';
      slider_html = '<div class="slider">'+slider_html+'</div>';
      content_html = '<div class="content">'+content_html+'</div>';
      html = slider_html+content_html;
      
      // populate final html
      t.html(html);
      
      // set some css properties
      t.css('width', options.width);
      t.css('height', options.height);
      t.children('div.slider').css('height', options.slider_height);
      t.children('div.content').css('height', options.content_height);
      t.children('div.content').css('width', content_width);
      t.children('div.content').children('div.block').css('width', options.block_width);
      t.children('div.content').children('div.block').css('padding', options.block_padding);
      
      // add onclick event handler on slider
      var li = t.children('div.slider').children('ul').children('li');
      li.click(function() {
        var slider_index = $(this).parent('ul').children('li').index(this)+1; // 0, 1, 2, ...
        var slider_heading = $(this).parent('ul').parent('div.slider').parent('div').children('div.content').children('div.block:nth-child('+slider_index+')').children('input').val();
        var contentslider_width = parseInt(t.width());
        var content_pos_left = 0;
        if($.browser.msie) content_pos_left = (-contentslider_width+20)*(slider_index-1);
        else content_pos_left = (-contentslider_width)*(slider_index-1);
        content_pos_left += "px";
        
        $(this).parent('ul').parent('div.slider').children('h2').html(slider_heading);
        $(this).parent('ul').children('li').removeClass('selected');
        $(this).parent('ul').parent('div.slider').parent('div').children('div.content').animate({
          "left": content_pos_left
        }, options.animation_time, options.animation_type, function(){
          $(this).children('div.block').css('visibility','hidden');
          $(this).children('div.block:nth-child('+slider_index+')').css('visibility','visible');
        });
        $(this).addClass('selected');
      });
      
      // return true
      return true;
      
    });
    
  };
  
})(jQuery);
