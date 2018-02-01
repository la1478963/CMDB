/**
 * Created by Administrator on 2017/11/8.
 */
 $(function () {
    $('.item-title').click(function () {
        if($(this).next().hasClass('hide')){
            $(this).next().removeClass('hide')
        }else{
            $(this).next().addClass('hide')
        }
    })


});