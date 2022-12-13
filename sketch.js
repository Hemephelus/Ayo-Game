let BidsPerPot = [4, 4];
let BoardInfo = [];
let StartingPosition = 2;
let StartingValue = BidsPerPot[StartingPosition];
let RestPot = StartingPosition + StartingValue;
let Player1Pt = 0;
let Player2Pt = 0;
let i = 0;
let Ayo;
let sideDiv = [".Side.one > .pot", ".Side.two > .pot"];
frameR = 1;
let ayoBoard = [
  [4, 4, 4, 4, 4, 4],
  [4, 4, 4, 4, 4, 4],
];
let a= [0,0]
let gameStatesHistory = [ayoBoard]

function setup() {
  let cnv = createCanvas(windowWidth, windowHeight);
  cnv.position(0, 0);
  cnv.style("z-index", -1);
  MakeObject(BidsPerPot);
  selectStartingPosition()
}

function selectStartingPosition() {
  for (let i = 0; i < 2; i++) {
    let Pots = selectAll(sideDiv[i]);

    for (let j = 0; j < Pots.length; j++) {
      Pots[j].mousePressed(function () {
       let startingPosition = [i, j] ;
       let startingValue = ayoBoard[i][j]
       playGame(startingPosition,startingValue)
       b++
      });
    }
  }
}

function playGame(startingPosition,startingValue){
  for(let i = 0; i < startingValue; i++ ){
    tempAyoBoard = JSON.parse(JSON.stringify(gameStatesHistory[gameStatesHistory.length-1]));
    tempAyoBoard[0][i+1] += 1
    gameStatesHistory.push(tempAyoBoard)
  }
}
a = 0
b = 0

function draw() {
  //MakeObject(BidsPerPot)
  frameRate(frameR);
  // background(28);
  
  console.log(gameStatesHistory[a])
  for (let i = 0; i < gameStatesHistory[a].length; i++) {
    let btns = selectAll(sideDiv[i]);
    for (let j = 0; j < gameStatesHistory[a][i].length; j++) {
      btns[j].elt.innerText = gameStatesHistory[a][i][j];
    }
  }

  if(b > 0 && b < 4){
    a++
  }else{
    noLoop
  }
 
  // frameR++
}

// function getall









































function MakeObject(BidsPerPot) {
  fill(196);
  textSize(16);
  for (let i = BidsPerPot.length - 1; i >= 0; i--) {
    if (i < 6)
      for (let j = 0; j < BidsPerPot[i]; j++) {
        let x = 70 * i + 100 + random(15, 35);
        let y = 225 + random(15, 35);
        let Pots = BidsPerPot.length;
        let r = random(10, 11);
        Ayo = new AyoBids(Pots, x, y, r);
        BoardInfo.push(Ayo);
      }
    else {
      for (let j = 0; j < BidsPerPot[i]; j++) {
        let x = 70 * (6 - i) + 445 + random(15, 35);
        let y = 155 + random(15, 35);
        let Pots = BidsPerPot.length;
        let r = random(10, 11);

        Ayo = new AyoBids(Pots, x, y, r);
        BoardInfo.push(Ayo);
      }
    }
  }
}

















function MoveBids(BidsPerPot, StartingPosition, StartingValue, RestPot) {
  if (StartingValue != 0) {
    for (
      StartingPosition = StartingPosition;
      StartingPosition < RestPot;
      StartingPosition++
    ) {
      BoardInfo.pop();
      BidsPerPot[(StartingPosition + 1) % 12] =
        BidsPerPot[(StartingPosition + 1) % 12] + 1;

      if (BidsPerPot[(StartingPosition + 1) % 12] == 4) {
        if ((StartingPosition + 1) % 12 < 6) {
          Player1Pt = Player1Pt + 4; //Add 4 to player 1
        } else {
          Player2Pt = Player2Pt + 4; //Add 4 to player 2
        }

        BidsPerPot[(StartingPosition + 1) % 12] = 0;
      }
    }

    //     if (BidsPerPot[(StartingPosition + 0) % 12] == 0) {

    //       if (Path[DepthLevel] < 6 && (StartingPosition % 12) > 5) {//Player1

    //         Player1Pt = Player1Pt + 4
    //         Player2Pt = Player2Pt - 4 //Add 4 to player 1

    //       } else if (Path[DepthLevel] > 5 && (StartingPosition % 12) < 6) {//Player2

    //         Player1Pt = Player1Pt - 4
    //         Player2Pt = Player2Pt + 4

    //       }
    //     }

    let ZeroPosition = StartingPosition - StartingValue;
    BidsPerPot[ZeroPosition % 12] = 0;
    StartingValue = BidsPerPot[StartingPosition % 12];
    RestPot = StartingPosition + StartingValue;

    if (StartingValue > 1) {
      MoveBids(BidsPerPot, StartingPosition, StartingValue, RestPot);
    }

    return BidsPerPot;
  }

  return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
}
