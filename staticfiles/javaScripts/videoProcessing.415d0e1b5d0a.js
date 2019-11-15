var canvasFrame = document.getElementById("canvasInput"); // canvasFrame is the id of <canvas>
var context = canvasFrame.getContext("2d");
const FPS = 1;
var el = document.getElementsByName("csrfmiddlewaretoken");
var csrf_value = el[0].getAttribute("value");
function processVideo() {
    let begin = Date.now();
    context.drawImage(video, 0, 0);
    var dataURL = canvasFrame.toDataURL();
    $.ajax({
        type: "POST",
        url: "/ajaxCanvas",
        cache:false,
        dataType: "json",
        data:{
            imageBase64: dataURL, 
            csrfmiddlewaretoken: csrf_value
        },
        success: function(resp){
            console.log("resp: "+resp.Status);
            if(resp.Status === "Closed"){
                window.location = "attendanceClosed";
            }
            else if(resp.Status === "True"){
                window.location = "attendanceRecorded";
            }
        }
    });
    
    // schedule next one.
    let delay = 1000/FPS - (Date.now() - begin);
    setTimeout(processVideo, delay);
}
// schedule first one.
setTimeout(processVideo, 0);