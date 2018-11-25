var socket = io.connect(base_uri);
socket.on('connect', function() {
    socket.emit('update', {username: '{{ username }}}'});
    speak("Connected", 'en');
});
socket.on('ask', function(data) {
    console.log(data);
    var list = document.getElementById('demo');
    var entry = document.createElement('p');
    entry.appendChild(document.createTextNode(data.message));
    list.appendChild(entry);
    speak(data.message, data.lang);
});
socket.on('giveaway', function(data) {
    console.log(data);
    var list = document.getElementById('events');
    var entry = document.createElement('p');
    entry.appendChild(document.createTextNode(data.message));
    list.appendChild(entry);
    speak(data.message, data.lang);
});
socket.on('vk_auth', function(data) {
    console.log(data);
    $("#vk_auth").text("VK Connected!")
    $("#vk_auth").prop("disabled", true)
    // var list = document.getElementById('events');
    // var entry = document.createElement('li');
    // entry.appendChild(document.createTextNode(data.message));
    // list.appendChild(entry);
    // speak(data.message, data.lang);
});
socket.on('audio', function(data) {
    console.log(data);
    $("#audio").css('visibility', 'visible');
    $("#current_track").text(data.audio)
    // var list = document.getElementById('events');
    // var entry = document.createElement('li');
    // entry.appendChild(document.createTextNode(data.message));
    // list.appendChild(entry);
    // speak(data.message, data.lang);
});