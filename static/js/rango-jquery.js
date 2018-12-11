//使用 jQuery 选择文档对象（$(document)），然后调用 ready() 函数。
// 浏览器把页面完全加载完后，执行 function() { }表示的匿名函数。
// $(document).ready(function() {
// 写Jquery代码
// });
$(document).ready(function() {

    $("#about-btn").click( function(event) {
    msgstr = $("#msg").html()
    msgstr = msgstr + "ooo"
    $("#msg").html(msgstr)});

});