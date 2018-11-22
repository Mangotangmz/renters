function logout() {
    $.ajax({
        url:'/user/logout/',
        type:'DELETE',
        success:function(data) {
            if(data.code=='200') {
                location.href = '/house/index/';
            }
        }
    });
}

$(document).ready(function(){

    $.ajax({
        url:'/user/user/',
        type:'GET',
        dataType:'json',
        success:function(data) {
            $('#user-avatar').attr('src',data.user.avatar);
            $('#user-name').html(data.user.name);
            $('#user-mobile').text(data.user.phone);
        },
        error:function(data){

        }
    });
});