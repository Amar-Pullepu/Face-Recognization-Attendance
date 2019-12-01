function StudentAttendance(id){
    var myTag = "<a id='x' " + "href='getAttendance' hidden><\a>";
    var inputTag = "<input name='userID' " + "value='"+(id-1).toString+"'"  + " hidden>";
    document.body.innerHTML +=  myTag+ inputTag;
    document.getElementById("x").click();
}