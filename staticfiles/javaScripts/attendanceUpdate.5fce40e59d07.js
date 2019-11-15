const FPS = 1
function attendanceUpdate() {
    let begin = Date.now();
    $.ajax({
        type: "GET",
        url: "/ajaxAttendanceUpdate",
        cache:false,
        dataType: "json",
        success: function(resp){
            for(int itr = 0; itr<resp.length; itr++){
                var sel = document.getElementById('sel'+Integer.toString(itr));
                if(resp[itr] === "Absent"){
                    sel.selectedIndex = 0;
                }
                else{
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