$(function() {

    $('.icon-set a').hover(
        function(event){
            $(event.target).siblings('.icon-img').addClass('icon-img-select');
            $(event.target).siblings('.icon-description').addClass('icon-desc-select');
        },
        function(event){
            $(event.target).siblings('.icon-img').removeClass('icon-img-select');
            $(event.target).siblings('.icon-description').removeClass('icon-desc-select');
    });

    $('#els-filter li').click(function() {
        $('#els-filter li.current').removeClass('current');
        $(this).addClass('current');
        
        var filterVal = $(this).text().toLowerCase().replace(' ','-'); // only works for one space, I think
                
        if(filterVal == 'all') {
            $('.icon-set.hidden').fadeIn('fast').removeClass('hidden');
        } else {
            $('.icon-set').each(function() {
                if(!$(this).hasClass('els-' + filterVal)) {
                    $(this).fadeOut('fast').addClass('hidden');
                } else {
                    $(this).fadeIn('fast').removeClass('hidden');
                }
            });
        }
        
        return false;
    });

});
