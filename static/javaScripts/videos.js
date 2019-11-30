// camera stream video element
let videoElm = document.querySelector('#video');
// flip button element
let flipBtn = document.querySelector('#flip-btn');

let canvasJQ = document.querySelector('#canvasInput');

// default user media options
let defaultsOpts = { audio: false, video: true }
let shouldFaceUser = true;

// check whether we can use facingMode
let supports = navigator.mediaDevices.getSupportedConstraints();


let stream = null;

function capture() {
  defaultsOpts.video = { facingMode: shouldFaceUser ? 'user' : 'environment' }
  navigator.mediaDevices.getUserMedia(defaultsOpts)
    .then(function(_stream) {
      stream  = _stream;
      document.querySelector('#console').innerHTML = stream.getVideoTracks()[0].getSettings().height +" "+ stream.getVideoTracks()[0].getSettings().width;
      canvasJQ.height = stream.getVideoTracks()[0].getSettings().height;
      canvasJQ.width = stream.getVideoTracks()[0].getSettings().width;
      $(".booth").width(canvasJQ.width);
      $(".booth").height(canvasJQ.height);
      if(canvasJQ.height > canvasJQ.width){
          flipBtn.disabled = false;
      }
      videoElm.srcObject = stream;
      videoElm.play();
    })
    .catch(function(err) {
      console.log(err)
    });
}

function flipCam(){
  console.log("Fliped");
  if( stream == null ) return
  // we need to flip, stop everything
  stream.getTracks().forEach(t => {
    t.stop();
  });
  // toggle / flip
  shouldFaceUser = !shouldFaceUser;
  capture();
}

capture();