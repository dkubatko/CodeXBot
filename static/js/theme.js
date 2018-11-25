// Dark
var d_bg = "#000000";
var d_text = "#EE682A";
var d_wg = "#060809";
var d_wgshdw = "#434343";

// Light
var l_bg = "#AFBFDC";
var l_text = "#171A1C";
var l_wg = "#F9F0AF";
var l_wgshdw = "#F0A979";

$(document).ready(function() {
    $("#dark").click(function() {
        changeTheme(d_bg, d_text, d_wg, d_wgshdw);
        $("#dark").css("border", "1px solid black");
        $("#light").css("border", "1px solid white");
    });
    $("#light").click(function() {
        changeTheme(l_bg, l_text, l_wg, l_wgshdw);
        $("#light").css("border", "1px solid black");
        $("#dark").css("border", "1px solid white");
    });
});

function changeTheme(bg, text, wg, wgshdw) {
    $("body").css("background-color", bg);
    $("body").css("color", text);
    $(".widget").css("background-color", wg);
    $(".widget").css("box-shadow", "5px 5px " + wgshdw);
}