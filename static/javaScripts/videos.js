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

if( supports['facingMode'] === true ) {
  flipBtn.disabled = false;
  
  canvasJQ.width = 600;
  canvasJQ.height = 900;
  $(".booth").width(495);
  $(".booth").height(745);
}
else{
  console.log("Faceing mode" + supports['facingMode']);
}
let stream = null;

function capture() {
  defaultsOpts.video = { facingMode: shouldFaceUser ? 'user' : 'environment' }
  navigator.mediaDevices.getUserMedia(defaultsOpts)
    .then(function(_stream) {
      stream  = _stream;
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