var state = 0;
var audioPlayer = new AudioPlayer();
ws = new WebSocket("ws://" + window.location.hostname +":"+ window.location.port + "/index");
ws.onmessage = function(msg) {
    var data = JSON.parse(msg.data);
    switch (state) {
        case 0:
            state0(data);
            break;
        case 1:
            state1(data);
            break;
        default:
            break;

    }

};


function state0(data){
    $(".qr img").css("display", "none");
    $("body,html").css("background-color", "black");
    $("body,html").css("background-color", "black");
    $(".face").css("display", "block");
    moveFace()
    state = 1;
}
function state1(data){
    audioPlayer.play("/static/Gunshot.m4a")
    if (data.hit) {
        $('.bullet').css("display", "block");
    }
}
moveFace();
function moveFace(){
    y = Math.floor( Math.random() * 60 ) + "%";
    x = Math.floor( Math.random() * 75 ) + "%";
    $('.face, .bullet').css({
        top: y,
        left: x

    });
}
