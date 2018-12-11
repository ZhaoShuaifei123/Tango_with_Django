$(document).ready(function() {

    $('#likes').click(function(){
    console.log("wojinleajaxla...............")
    var catid;
    catid = $(this).attr("data-catid");
    $.get('/rango/like/',{category_id: catid},function (data) {
        console.log("222222222wojinleajaxla...............");
        $('#like_count').html(data);
        $('#likes').hide();
        });
    });

    $('#suggestion').keyup(function () {
        var query;
        query = $(this).val();
        $.get('/rango/suggestion/',{suggestion:query},function (data) {
            $('#cats').html(data);
        });
        });

});

