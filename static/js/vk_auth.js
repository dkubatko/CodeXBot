$(document).ready(function() {
    $("#vk_auth").click(function() {
        window.open("https://oauth.vk.com/authorize?client_id=6760377&display=popup&redirect_uri=http://127.0.0.1:5000/vk&scope=status&response_type=code")
        console.log("click");
    });
});
