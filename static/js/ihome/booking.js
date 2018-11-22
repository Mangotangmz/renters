function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

$(document).ready(function () {
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function () {
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd) / (1000 * 3600 * 24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共" + days + "晚)");
        }
    });

    $('.submit-btn').click(function () {
        var search = document.location.search
        h_id = search.split('=')[1]
        //获取入住时间
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();
        //发起请求下订单
        $.post('/order/', {
            house_id: h_id,
            start_date: startDate,
            end_date: endDate
        }, function (data) {
            if (data.code == '200') {
                location.href = '/order/orders/';
            }
        });
    });


})


//房屋信息
$(document).ready(function () {

    var path = window.location.search
    var h_id = path.split('&')[0].split('=')[1]
    $.get('/house/getbookingbyid/' + h_id + '/', function (data) {
        $('.house-info img').attr('src', data.house.image)
        $('.house-text').html('<h3>+data.house.title+</h3><p>￥<span>' + data.house.price + '</span>/晚</p>')
    });
});

