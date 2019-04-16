
window.onload=function () {
    $("#date").dateRangePicker(configObject);
    function myFunction()
    {
        x=document.getElementById("js")// 找到元素

        x.style.color="#0c2cff";          // 改变样式
    }
    var
        js = document.getElementById('js'),
        list = document.getElementById('list');
    list.appendChild(js);
    myFunction();


};