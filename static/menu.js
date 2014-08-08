$(function() {
    $('#contacts').hide();
    $('#escapepad').click(function(){
        if ( $("#contacts").is(":hidden") ) {
            $('#contacts').slideDown("slow");
        } else {
            $('#contacts').slideUp();
        }
    });
});
