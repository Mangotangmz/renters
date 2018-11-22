function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$('#form-avatar').submit(
    function () {
            $('.error-msg').hide();
            $(this).ajaxSubmit(
                {
                    url: '/user/profile/',
                    type: 'put',
                    dataType: 'json',
                    success: function (data) {
                        if (data.code == '200') {
                            $('#user-avatar').attr('src', data.url);
                        }
                        else {
                            $('#error_msg1').show()
                        }
                    }
                }
            );
            return fasle
        }
    )

$('#form-name').submit(function () {
    $('.error-msg2').hide();
    $.ajax({
        url: '/user/user_name/',
        type: "put",
        data: {'name': $('#user-name').val()},
        success: function (data) {
            if (data.code == '200') {
                alert('保存成功')
            }
            else {
                $('.error-msg2').html('<i class="fa fa-exclamation-circle"></i>' + data.msg)
                $('.error-msg2').show()
            }

        }
    });
    return false
})
