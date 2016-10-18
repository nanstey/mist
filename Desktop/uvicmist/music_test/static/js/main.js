$(function(){
    
    $("div#id_intervals").before("<br/><div class='checkbox'><label for='selectAll'><input type='checkbox' id='selectAll'> Select All</label></div>");
    
    $("#selectAll").on('change',function() {
        $(".intervalCheckbox:checkbox").prop('checked', $(this).prop("checked"));
    });
});

