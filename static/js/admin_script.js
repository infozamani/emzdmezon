$(document).ready(function() {  
    var listOfElements = $('select[id^="id_product_features-"][id$="-feature"]');  
    $(listOfElements).on('change', function() {  
        var f_id = $(this).val();  
        var dd1 = $(this).attr('id');  
        var dd2 = dd1.replace("-feature", "-filter_value");  

        $.ajax({  
            type: "GET",  
            url: "/products/ajax_admin/?feature_id=" + f_id,  
            success: function(res) {  
                var cols = document.getElementById(dd2);  
                cols.options.length = 0;   
                Object.keys(res).forEach(function(k) {  
                    cols.options.add(new Option(k, res[k]));  
                });  
            },  
            error: function(xhr, status, error) {  
                console.error("AJAX Error: " + status + error);  
                alert("An error occurred while processing your request.");  
            },  
        });  
    });   
});