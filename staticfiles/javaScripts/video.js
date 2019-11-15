(function() {
    var video = document.getElementById('video'),
        vendorUrl = window.URL || window.webkitURL;
    
    navigator.getMedia = navigator.getUserMedia ||
                         navigator.webkitGetUserMedia ||
                         navigator.mozGetUserMedia ||
                         navigator.msGetUserMedia;
    
    //Capture Media
    navigator.getMedia({
        video : true,
        audio : false
    }, function(stream) {
        video.srcObject=stream;
        video.play();
    }, function(error) {
        //An Error Occured
    })
})(); 



