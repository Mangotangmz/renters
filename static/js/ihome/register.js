function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

$(document).ready(function() {

    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });
    $(".form-register").submit(function(){
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        passwd2 = $("#password2").val();

        $.ajax({
            url:'/user/register/',
            type:'POST',
            dataType:'json',
            data:{'mobile':mobile, 'password':passwd, 'password2':passwd2},
            success: function(msg){
                alert(msg.msg);
                if(msg.code == '200'){
                    location.href='/user/login/';
                }
            },
            error: function(msg){
                console.log(msg)
            }
        });
    });
})


