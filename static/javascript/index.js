var state = 0;
var audioPlayer = new AudioPlayer();
var remaining = 5;
var hit = 0;
var time = 60;
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
    remainingBullet(remaining);
    moveFace()
    var timeId = setInterval(function(){
        time--;
        $('.time').text('00:'+('0' + time).slice(-2));
        if (time == 0) {
            clearTimeout(timeId)
        }
    },1000)
    state = 1;
}
function state1(data){
    if (remaining != 0) {
        remaining -= 1;
        audioPlayer.play("/static/Gunshot.m4a");
        if (data.hit) {
            hit++;
            $('.hit').text(hit + 'HIT');
            $('.bullet').css("display", "block");
            setTimeout(moveFace,1500);
        }
        remainingBullet(remaining)
    }
}
function moveFace(){
    y = Math.floor( Math.random() * 60 ) + "%";
    x = Math.floor( Math.random() * 65 ) + "%";
    $('.bullet').css("display", "none");
    $('.face, .bullet').css({
        top: y,
        left: x

    });
}
function reload(){
    remaining = 0;
    setTimeout(function(){
        audioPlayer.play("/static/reload.m4a");
    },2000)
    setTimeout(function(){
        remaining = 5;
        remainingBullet(remaining);
    },3500);

}
function remainingBullet(num){
    $('.remaining li').remove();
    console.log(num);
    for (var i = 0; i < 5; i++) {
        if(i < num){
            $('.remaining').append('<li class="image"><img src="/static/onbullet.jpg"></li>')
        }else{
            $('.remaining').append('<li class="image"><img src="/static/offbullet.jpg"></li>')

        }
    }
    if (num == 0) {
        reload()
    }
}
