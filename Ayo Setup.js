function selectStartingPosition() {
  for (let i = 0; i < 2; i++) {
    let Pots = selectAll(sideDiv[i]);

    for (let j = 0; j < Pots.length; j++) {
      Pots[j].mousePressed(function () {
        let startingPosition = [i, j];
        let startingValue =
          gameStatesHistory[gameStatesHistory.length - 1]['ayoBoard'][i][j];
        let stopPosition = startingPosition[1] + startingValue;
        gameStatesHistory[gameStatesHistory.length - 1]['currentPlayer'] = (selectedPot%2)+1
        selectedPot++
        playAyoGameSession(startingPosition, startingValue, stopPosition);
      });
    }
  }
}

function playAyoGameSession(startingPosition, startingValue, stopPosition){
  latestGameState = gameStatesHistory[gameStatesHistory.length-1]
  startingPosition= playAyoGame(startingPosition, stopPosition,latestGameState)
  latestGameState = gameStatesHistory[gameStatesHistory.length-1]
  let [side,pot]= startingPosition
  startingValue = latestGameState['ayoBoard'][side][pot]
  stopPosition = pot+startingValue

  while(startingValue > 1){
    latestGameState = gameStatesHistory[gameStatesHistory.length-1]
    // console.log(latestGameState)
    startingPosition= playAyoGame(startingPosition, stopPosition,latestGameState)
    latestGameState = gameStatesHistory[gameStatesHistory.length-1]
    let [side,pot]= startingPosition
    startingValue = latestGameState['ayoBoard'][side][pot]
    stopPosition = pot+startingValue
  }

}

function playAyoGame(startingPosition, stopPosition,latestGameState) {
  let tempAyoState = JSON.parse(
    JSON.stringify(latestGameState)
    );
    tempAyoState['ayoBoard'][startingPosition[0]][startingPosition[1]] = 0;
    gameStatesHistory.push(tempAyoState);
    let currentPot, side;
    for (let i = startingPosition[1]; i < stopPosition; i++) {
      latestGameState = gameStatesHistory[gameStatesHistory.length-1]
      tempAyoState = JSON.parse(
        JSON.stringify(latestGameState)
        );
        side = (startingPosition[0] + (floor((i + 1) / 6) % 2)) % 2;
        currentPot = (i + 1) % 6;
        tempAyoState['ayoBoard'][side][currentPot] += 1;
        
        gameStatesHistory.push(tempAyoState);
        if(tempAyoState['ayoBoard'][side][currentPot] === 4){
          latestGameState = gameStatesHistory[gameStatesHistory.length-1]
          tempAyoState = JSON.parse(
            JSON.stringify(latestGameState)
            );
            tempAyoState['ayoBoard'][side][currentPot] = 0;
            tempAyoState['playerScore'+side] += 4
            gameStatesHistory.push(tempAyoState);
          }
          


  }

  return [side, currentPot]
}


function Control_Buttons() {
  // Pause Button
  select("#pause").mousePressed(function () {
    pauseGame = true;
    if (pauseGame) {
      playAyoGame = false;
      fastForwardGame = false;
      frameR = 1;
      noLoop();
    }
  });

  select("#reset").mousePressed(function () {
    resetGame = true;
    if (resetGame) {
      pauseGame = true;

      // playGame = false;
      a = 0;
      selectedPot = 0;
      loop();
    }
  });

  // Play Button
  select("#play_arrow").mousePressed(function () {
    playGame = true;
    if (playGame) {
      pauseGame = false;
      fastForwardGame = true;
      frameR = 1;
      loop();
    }
  });

  // Fast Forward Button
  select("#fast_forward").mousePressed(function () {
    fastForwardGame = true;
    if (playGame) {
      frameR = 10;
      loop();
    }
  });

  // Fast Forward Button
  select("#skip_next").mousePressed(function () {
    skipNextGame = true;
    if (skipNextGame) {
      playGame = false;
      a++;
      loop();
    }
    noLoop();
  });

  // Skip Previous Button
  select("#skip_previous").mousePressed(function () {
    skipPreviousGame = true;
    if (skipPreviousGame) {
      playGame = false;
      a--;
      loop();
    }
    noLoop();
  });
}