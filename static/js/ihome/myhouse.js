//获取用户信息，判断是否进行过实名认证
$.get('/house/auth_myhouse/',function (data) {
    console.log(data)
    if(data.code== '200'){
        //已经完成实名认证
        alert('200')
        $('#houses-list').show();
        $('#auth-warn').hide();
        var html=template('house_list',{hlist:data.house_list});
        $('#houses-list').append(html);
    }else{
        //未实名认证
        $('#auth-warn').show();
    }
});
