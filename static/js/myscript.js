// برای اینکه وقتی فیلتر کردیم بعد دوباره بخواهیم فیلتر کنیم فیلتر های قبلی پاک نشه
$(document).ready(
    function(){
    var urlparts = new URLSearchParams(Window.location.search);
    if (urlparts = ""){
        localStorage.clear();
        $("#filter_state").css("display", "none");
        } else {
            $("#filter_state").css("display", "inline_block");
        }
        $('input:checkbox').on('click', function(){
            var fav, favs = [];
            $('input:checkbox').each(function(){
                fav = { id : $(this).attr('id'), value: $(this).prop('checked')};
                favs.push(fav);
            })
            localStorage.setItem("favorites", JSON.stringify(favs)); 
        })
        var favorites = JSON.parse(localStorage.getItem('favorites'));
        for (var i = 0; i < favorites.length; i++){
            $('#' + favorites[i].id),prop('checked' , favorites[i].value);
        }
    }
);



// #---------------------------------------------------
// برای اینکه ردج قیمت را مشخص و کاما قرار دیهم 
function showVal(x){
    x = x.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
    document.getElementById('sel_price').innerText = x;

}
// #---------------------------------------------------
//##تابع برای حذف پارامترهای خط آدرس
function removeURLParameter(url, parameter) {
    var urlparts = url.split('?');
    if (urlparts.length >= 2){
        var prefix = encodeURIComponent(parameter) + '=';
        var pars = urlparts[1].split(/[&;]/g);
        for (var i = pars.length; i-- > 0;){

            if (pars[i].lastIndexOf(prefix, 0) != -1) {
                pars.splice(i, 1);
        }

        }
        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
    }
   
    return url;
}


//-------------------------------------------------------------------
//##تابع انتخاب مدل مرتب سازی محصولات 
function select_sort() {
    alert(test)
    var select_sort_value = $("#select_sort").val();
    // $("$select_sort").attr('selected', 'selected' );
    var url = removeURLParameter(window.Location.href, "sort_type");
    window.location = url + "&sort_type=" + select_sort_value;
    
}
// -------------------------shop_cart-----------------------------------
// ceate status shop_cart
status_of_shop_cart()
function status_of_shop_cart() {
    $.ajax({
        type: "GET",
        url : "/orders/status_of_shop_cart/",
        success: function(res) { 
            $("#indicator__value").text(res);
        }
    });
}
//-------------------------------------------------------------------
//##تابع برای افزودن کالا به سبد خرید
function add_to_shop_cart(product_id, qty){
    if (qty === 0) {
        qty = $("#product-quantity").val();
    }
    $.ajax({
        type: "GET",
        url : "/orders/add_to_shop_cart/",
        data :{
            product_id : product_id,
            qty :qty
        },
        success: function(res) {
            alert("کالا به سبد خرید اضافه شد");
            $("#shop_cart_list").html(res);
            status_of_shop_cart();
        }
    });
}
//-------------------------------------------------------------------
// //##تابع برای حذف کالا از سبد خرید
function delete_form_shop_cart(product_id){
    $.ajax({
        type: "GET",
        url : "/orders/delete_form_shop_cart/",
        data :{
            product_id : product_id,
        },
        success: function(res) {
            alert("کالا مورد نظر حذف شد ");
            $("#shop_cart_list").html(res);
            status_of_shop_cart();
            
        }
    });
}

 
// create function update shop_cart(به روز رسانی)
function update_shop_cart(){
    var product_id_list = []
    var qty_list = []
    $("input[id^='qty_']").each(function(index) {
        product_id_list.push($(this).attr('id').slice(4));
        qty_list.push($(this).val());
    });
    console.log(product_id_list);
    console.log(qty_list)
    $.ajax({
        type: "GET",
        url : "/orders/update_shop_cart/",
        data :{
            product_id_list : product_id_list,
            qty_list :qty_list,
        },
        success: function(res) {
  
            $("#shop_cart_list").html(res);
            status_of_shop_cart();
            
        }
    });
    
}

// ----------------------------------------------------------------

function showCreateCommentForm(productId, commentId, slug) {
     
    $.ajax({
        type: "GET",
        url: "/csf/create_comment/" + slug ,
        data: {
            productId: productId,
            commentId: commentId,

        },
        success: function(res) {
            $("#btn_" + commentId).hide();
            $("#comment_form_" + commentId).html(res);
        }
    });
}
 
 
//----------------------------------------------------------------
function addScore(score, productId){
    var starRatings = document.querySelectorAll('.fa-star');
    starRatings.forEach(element => {
        element.classList.remove('checked'); 
    });
    for (let i = 1; i <= score; i++){
        const element = document.getElementById("star_" + i);
        element.classList.add('checked');
    }
 
    $.ajax({
        type: "GET",
        url: "/csf/add_score/",
        data:{
            productId: productId,
            score: score,
        },
        success: function(res) {
            alert(res);
        }

    });
    starRatings.forEach(element => {
        element.classList.add("disable");
    });
}

//----------------------------------------------------------------
function addToFavorites(productId) {
    
    $.ajax({
        type: "GET",
        url: "/csf/add_to_favorite/",
        data:{
            productId: productId,
         
        },
        success: function(res) {
            alert(res);
        }

    });
}
//----------------------------------------------------------------
status_of_compare_list();
//----------------------------------------------------------------
function status_of_compare_list() {
    $.ajax({
        type: "GET",
        url : "/products/status_of_compare_list/",
        success: function(res) {
            if (Number(res) === 0 ) {
                $("#compare_count_icon").hide();
            } else {
                $("#compare_count_icon").show();
                $("#compare_count").text(res);
            } 
        },
    });
}

//----------------------------------------------------------------
function addToCompareList(productId, productGroupId) {
    $.ajax({
        type : "GET",
        url : "/products/add_to_compare_list/",
        data :{
            productId : productId,
            productGroupId: productGroupId,
        },
        success : function(res) {
            alert(res);
            status_of_compare_list();

        }
    });

}
//----------------------------------------------------------------
function deleteFormCompareList(productId) {
    $.ajax({
        type : "GET",
        url : "/products/delete_from_compare_list/",
        data :{
            productId: productId,
        },
        success: function(res) {
            alert('حذف با موفقیت انجام شد');
            $("#compare_list").html(res);
            status_of_compare_list();
        }
    });

}
 
 
 