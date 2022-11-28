class AyoBids {
    constructor(
    Pots,
      x,
      y,
      r
  
    ) {
      this.Pots = BidsPerPot.length;
      this.x = x
        this.y = y
        this.r = r
  
  
    }
  
  
   DrawBids(BidsPerPot) {
    fill(196);
    textSize(16);
    for (let i = this.Pots - 1; i >= 0; i--) {
      if (i < 6) {
        
        text(BidsPerPot[i], i * 70 + 115, 320);
        // console.log("      "+BidsPerPot[0])
        for (let j = 0; j < BidsPerPot[i]; j++) {
          // console.log("      "+BidsPerPot[i])
          circle(this.x, this.y, 10);
        }
      } else {
        for (let j = 0; j < BidsPerPot[i]; j++) {
          circle(this.x, this.y, 10);
        }
        text(BidsPerPot[i], 70 * (6 - i) + 465, 130);
      }
    }
  }
  
    
  DrawBoard() {
    fill(198, 100, 0);
    rect(75, 150, 450, 70, 90);
    rect(75, height/2, 450, 70, 90);
  }
    
  
    DrawPots() {
    fill(158, 80, 0);
    for (let i = 0; i < this.Pots; i++) {
      if (i < 6) {
       
        circle(70 * i + 125, 185, 55);
       
      } else { if(i == 7){
          fill(100,0,0)
        }
        circle(70 * (i - 6) + 125, 255, 55);
               fill(158, 80, 0);
      }
    }
  }
    
  }  