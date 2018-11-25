$(document).ready(function() {
    $("#vk_auth").click(function() {
        window.open("https://oauth.vk.com/authorize?client_id=6760377&display=popup&redirect_uri=" + redirect_uri + "&scope=status&response_type=code")
        console.log("click");
    });
});
