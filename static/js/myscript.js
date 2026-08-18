// ============================================================
// توابع سبد خرید و علاقه‌مندی (اصلاح‌شده)
// ============================================================

//-------------------------------------------------------------------
// تابع برای افزودن کالا به سبد خرید
function addToCart(productId) {
    // گرفتن تعداد از input اگر وجود داشته باشد
    var qty = 1;
    var qtyInput = document.getElementById('product-quantity');
    if (qtyInput) {
        qty = qtyInput.value;
    }
    
    $.ajax({
        type: "GET",
        url: "/orders/add_to_shop_cart/",
        data: {
            product_id: productId,
            qty: qty
        },
        success: function(res) {
            alert("✅ کالا با موفقیت به سبد خرید اضافه شد");
            status_of_shop_cart();
            // به‌روزرسانی تعداد در نوار
            updateNavCartCount();
        },
        error: function(xhr, status, error) {
            console.error("Error in addToCart:", error);
            alert("❌ خطا در افزودن به سبد خرید");
        }
    });
}

//-------------------------------------------------------------------
// تابع برای اضافه کردن به علاقه‌مندی‌ها
function addToFavorites(productId) {
    $.ajax({
        type: "GET",
        url: "/csf/add_to_favorite/",
        data: {
            productId: productId
        },
        success: function(res) {
            alert("❤️ محصول به علاقه‌مندی‌ها اضافه شد");
            // تغییر آیکون قلب
            var buttons = document.querySelectorAll('button[onclick*="addToFavorites(' + productId + ')"]');
            buttons.forEach(function(btn) {
                var icon = btn.querySelector('i');
                if (icon) {
                    icon.className = 'fa fa-heart';
                    icon.style.color = '#e94560';
                }
            });
            status_of_favorite_list();
        },
        error: function(xhr, status, error) {
            console.error("Error in addToFavorites:", error);
            if (xhr.status === 401) {
                alert("❌ لطفاً ابتدا وارد شوید");
            } else {
                alert("❌ خطا در افزودن به علاقه‌مندی‌ها");
            }
        }
    });
}

//-------------------------------------------------------------------
// تابع برای افزودن به لیست مقایسه
function addToCompareList(productId) {
    $.ajax({
        type: "GET",
        url: "/products/add-to-compare-list/",
        data: {
            productId: productId
        },
        success: function(res) {
            alert("⚖️ محصول به لیست مقایسه اضافه شد");
            status_of_compare_list();
        },
        error: function(xhr, status, error) {
            console.error("Error in addToCompareList:", error);
            alert("❌ خطا در افزودن به لیست مقایسه");
        }
    });
}

//-------------------------------------------------------------------
// تابع برای حذف از لیست مقایسه
function deleteFormCompareList(productId) {
    $.ajax({
        type: "GET",
        url: "/products/delete_from_compare_list/",
        data: {
            productId: productId
        },
        success: function(res) {
            alert("✅ حذف با موفقیت انجام شد");
            $("#compare_list").html(res);
            status_of_compare_list();
        },
        error: function(xhr, status, error) {
            console.error("Error in deleteFormCompareList:", error);
            alert("❌ خطا در حذف از لیست مقایسه");
        }
    });
}

//-------------------------------------------------------------------
// تابع به‌روزرسانی تعداد سبد خرید
function status_of_shop_cart() {
    $.ajax({
        type: "GET",
        url: "/orders/status_of_shop_cart/",
        success: function(res) {
            $(".indicator__value, #indicator__value").text(res);
            // به‌روزرسانی در نوار
            var cartBadge = document.getElementById('cartCount');
            if (cartBadge) {
                cartBadge.textContent = res || '0';
            }
        },
        error: function(xhr, status, error) {
            console.error("Error in status_of_shop_cart:", error);
        }
    });
}

//-------------------------------------------------------------------
// تابع به‌روزرسانی تعداد علاقه‌مندی‌ها
function status_of_favorite_list() {
    $.ajax({
        type: "GET",
        url: "/products/status_of_favorite_list/",
        success: function(res) {
            var favBadge = document.getElementById('favoriteCount');
            if (favBadge) {
                favBadge.textContent = res || '0';
            }
        },
        error: function(xhr, status, error) {
            console.error("Error in status_of_favorite_list:", error);
        }
    });
}

//-------------------------------------------------------------------
// تابع به‌روزرسانی تعداد مقایسه
function status_of_compare_list() {
    $.ajax({
        type: "GET",
        url: "/products/status-of-compare-list/",
        success: function(res) {
            if (Number(res) === 0) {
                $("#compare_count_icon").hide();
            } else {
                $("#compare_count_icon").show();
                $("#compare_count").text(res);
            }
            var compareBadge = document.getElementById('compareCount');
            if (compareBadge) {
                compareBadge.textContent = res || '0';
            }
        },
        error: function(xhr, status, error) {
            console.error("Error in status_of_compare_list:", error);
        }
    });
}

//-------------------------------------------------------------------
// تابع کمکی برای به‌روزرسانی تعداد در نوار
function updateNavCartCount() {
    var cartBadge = document.getElementById('cartCount');
    if (cartBadge) {
        $.ajax({
            type: "GET",
            url: "/orders/status_of_shop_cart/",
            success: function(res) {
                cartBadge.textContent = res || '0';
            }
        });
    }
}

// ============================================================
// اجرا در زمان بارگذاری صفحه
// ============================================================
$(document).ready(function() {
    status_of_shop_cart();
    status_of_favorite_list();
    status_of_compare_list();
});