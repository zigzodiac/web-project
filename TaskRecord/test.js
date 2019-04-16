$(function () {
    $('.tab ul li').mouseover(function () {
        $(this).addClass('active').siblings().removeClass('active');
        $('.tab-content>div:eq(' + $(this).index() + ')').css('display', 'block').siblings().css('display', 'none');
    });
    $('#agree').change(function () {
        // console.log(!$(this).attr('ch?ecked'));
        $('#nextstep').prop('disabled',!$(this).prop('checked'));//说明在chrome浏览器中，不能用click事件来修改disabled属性值，要不在浏览器中不能呈现效果。
    });
})