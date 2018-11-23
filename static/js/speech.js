var rate = document.getElementById("rate");
var pitch = document.getElementById("pitch");
var volume = document.getElementById("volume");
var rate_o = document.getElementById("rate_o");
var pitch_o = document.getElementById("pitch_o");
var volume_o = document.getElementById("volume_o");

rate_o.innerHTML = rate.value; // Display the default slider value
// Update the current slider value (each time you drag the slider handle)
rate.oninput = function() {
    rate_o.innerHTML = this.value;
}

pitch_o.innerHTML = pitch.value; // Display the default slider value
// Update the current slider value (each time you drag the slider handle)
pitch.oninput = function() {
    pitch_o.innerHTML = this.value;
}

volume_o.innerHTML = volume.value; // Display the default slider value
// Update the current slider value (each time you drag the slider handle)
volume.oninput = function() {
    volume_o.innerHTML = this.value;
}

var voiceReady = false;
var synth = window.speechSynthesis;
window.speechSynthesis.onvoiceschanged = function() {
    console.log("Voices ready")
    // only start upon voices loaded
    voiceReady = true;
    var voices = window.speechSynthesis.getVoices();
    console.log(voices);
};
function speak(message, lang) {
    var voices = window.speechSynthesis.getVoices();
    if (voiceReady) {
        var utterThis = new SpeechSynthesisUtterance(message);           
        utterThis.rate = rate.value;
        utterThis.pitch = pitch.value;
        utterThis.volume = volume.value;
        // CHANGE FROM HARDCODED
        console.log(lang);
        console.log(message);
        switch (lang) {
            case 'ru':
                utterThis.voice = synth.getVoices()[17];
                break;
            case 'en':
                utterThis.voice = synth.getVoices()[3];
            break;
            default:
                utterThis.voice = synth.getVoices()[3];
                break;
        }
        synth.speak(utterThis);
    }
}