const canvas = document.getElementById("metronome");
const ctx = canvas.getContext("2d");

function drawBeats(rhythm) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  rhythm.slice(0, rhythm.length-1).forEach((interval, i) => {

    ctx.fillStyle = 'green';

    // Controls the fading of dots over time
    ctx.globalAlpha = Math.pow((i / rhythm.length), 2);

    drawBeat(rhythm[i], rhythm[i+1]);
  });
}

function drawBeat(x, y) {
  ctx.beginPath();
  ctx.arc(x,y,10,0,Math.PI*2); // Outer circle
  ctx.fill();
}
