const FPS = 1
function attendanceUpdate() {
    let begin = Date.now();
    $.ajax({
        type: "GET",
        url: "/ajaxAttendanceUpdate",
        cache:false,
        dataType: "json",
        success: function(resp){
            for(var itr = 0; itr<resp.length; itr++){
                var sel = document.getElementById('sel'+itr.toString());
                if(resp[itr] === "Present"){
                    sel.selectedIndex = 1;
                }
            }
        }
    });
    
    // schedule next one.
    let delay = 1000/FPS - (Date.now() - begin);
    setTimeout(attendanceUpdate, delay);
}
// schedule first one.
setTimeout(attendanceUpdate, 0);