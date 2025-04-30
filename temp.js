function setup() {
    createCanvas(400, 400);
    background(255);
    fill(160, 82, 45);
    ellipse(200, 200, 150, 150); // head
    ellipse(150, 180, 50, 50);   // left ear
    ellipse(250, 180, 50, 50);   // right ear
    fill(0);
    ellipse(185, 190, 10, 10);   // left eye
    ellipse(215, 190, 10, 10);   // right eye
    stroke(0);
    noFill();
    arc(200, 220, 40, 20, 0, PI); // smile
  }
setup()  