let sideDiv = [".Side.one > .pot", ".Side.two > .pot"];
frameR = 1;
let pauseGame = false;
let playGame = true;
let resetGame = false;
let W2N = {
  '1': 'one',
  '2': 'two',
}
let gameState = {
  'ayoBoard': [
    [4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4],
  ],
  'playerScore0': 0,
  'playerScore1': 0,
  'currentPlayer' : 1,
  'startingPosition' : 1,
  'timesPlayed1': 0,
  'timesPlayed2': 0,
};

let gameStatesHistory = [gameState];

function setup() {
  let cnv = createCanvas(windowWidth, windowHeight);
  cnv.position(0, 0);
  cnv.style("z-index", -1);
  // MakeObject(BidsPerPot);
  selectStartingPosition();
  Control_Buttons();
}

let a = 0;
let selectedPot = 0;

function draw() {
  //MakeObject(BidsPerPot)
  frameRate(frameR);
  let currentBoardState = gameStatesHistory[a]['ayoBoard']
  for (let i = 0; i < currentBoardState.length; i++) {
    let btns = selectAll(sideDiv[i]);
    for (let j = 0; j < currentBoardState[i].length; j++) {
      btns[j].elt.innerText = currentBoardState[i][j];
    }
  }

  renderStats()
  
  if (selectedPot > 0 && a < gameStatesHistory.length - 1 && playGame === true) {
    a++;
  } else {
    noLoop();
  }
}


/**
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 */
// function getall

// function MakeObject(BidsPerPot) {
//   fill(196);
//   textSize(16);
//   for (let i = BidsPerPot.length - 1; i >= 0; i--) {
//     if (i < 6)
//       for (let j = 0; j < BidsPerPot[i]; j++) {
//         let x = 70 * i + 100 + random(15, 35);
//         let y = 225 + random(15, 35);
//         let Pots = BidsPerPot.length;
//         let r = random(10, 11);
//         Ayo = new AyoBids(Pots, x, y, r);
//         BoardInfo.push(Ayo);
//       }
//     else {
//       for (let j = 0; j < BidsPerPot[i]; j++) {
//         let x = 70 * (6 - i) + 445 + random(15, 35);
//         let y = 155 + random(15, 35);
//         let Pots = BidsPerPot.length;
//         let r = random(10, 11);

//         Ayo = new AyoBids(Pots, x, y, r);
//         BoardInfo.push(Ayo);
//       }
//     }
//   }
// }

// function MoveBids(BidsPerPot, StartingPosition, StartingValue, RestPot) {
//   if (StartingValue != 0) {
//     for (
//       StartingPosition = StartingPosition;
//       StartingPosition < RestPot;
//       StartingPosition++
//     ) {
//       BoardInfo.pop();
//       BidsPerPot[(StartingPosition + 1) % 12] =
//         BidsPerPot[(StartingPosition + 1) % 12] + 1;

//       if (BidsPerPot[(StartingPosition + 1) % 12] == 4) {
//         if ((StartingPosition + 1) % 12 < 6) {
//           Player1Pt = Player1Pt + 4; //Add 4 to player 1
//         } else {
//           Player2Pt = Player2Pt + 4; //Add 4 to player 2
//         }

//         BidsPerPot[(StartingPosition + 1) % 12] = 0;
//       }
//     }

//     //     if (BidsPerPot[(StartingPosition + 0) % 12] == 0) {

//     //       if (Path[DepthLevel] < 6 && (StartingPosition % 12) > 5) {//Player1

//     //         Player1Pt = Player1Pt + 4
//     //         Player2Pt = Player2Pt - 4 //Add 4 to player 1

//     //       } else if (Path[DepthLevel] > 5 && (StartingPosition % 12) < 6) {//Player2

//     //         Player1Pt = Player1Pt - 4
//     //         Player2Pt = Player2Pt + 4

//     //       }
//     //     }

//     let ZeroPosition = StartingPosition - StartingValue;
//     BidsPerPot[ZeroPosition % 12] = 0;
//     StartingValue = BidsPerPot[StartingPosition % 12];
//     RestPot = StartingPosition + StartingValue;

//     if (StartingValue > 1) {
//       MoveBids(BidsPerPot, StartingPosition, StartingValue, RestPot);
//     }

//     return BidsPerPot;
//   }

//   return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
// }
