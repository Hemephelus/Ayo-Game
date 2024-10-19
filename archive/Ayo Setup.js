function selectStartingPosition() {
  for (let i = 0; i < 2; i++) {
    let Pots = selectAll(sideDiv[i]);

    for (let j = 0; j < Pots.length; j++) {
      Pots[j].mousePressed(function () {
        let startingPosition = [i, j];

        gameStatesHistory[gameStatesHistory.length - 1]['startingPosition'] = startingPosition[1];
        let startingValue =
          gameStatesHistory[gameStatesHistory.length - 1]['ayoBoard'][i][j];
        let stopPosition = startingPosition[1] + startingValue;
        gameStatesHistory[gameStatesHistory.length - 1]['currentPlayer'] = (selectedPot%2)+1
        if(selectedPot%2 === 1){
          gameStatesHistory[gameStatesHistory.length - 1]['timesPlayed2']++
        }else{
          gameStatesHistory[gameStatesHistory.length - 1]['timesPlayed1']++
          
        }
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

          if(tempAyoState['currentPlayer'] === 2 && side === 0 && i === stopPosition-1){
            latestGameState = gameStatesHistory[gameStatesHistory.length-1]
            tempAyoState = JSON.parse(
              JSON.stringify(latestGameState)
              );
              tempAyoState['ayoBoard'][side][currentPot] = 0;
              tempAyoState['playerScore1'] += 4
              gameStatesHistory.push(tempAyoState);
            continue
          }

          if(tempAyoState['currentPlayer'] === 1 && side === 1 && i === stopPosition-1){
            latestGameState = gameStatesHistory[gameStatesHistory.length-1]
            tempAyoState = JSON.parse(
              JSON.stringify(latestGameState)
              );
              tempAyoState['ayoBoard'][side][currentPot] = 0;
              tempAyoState['playerScore0'] += 4
              gameStatesHistory.push(tempAyoState);
            continue
          }

          latestGameState = gameStatesHistory[gameStatesHistory.length-1]
          tempAyoState = JSON.parse(
            JSON.stringify(latestGameState)
            );
            tempAyoState['ayoBoard'][side][currentPot] = 0;
            tempAyoState['playerScore'+side] += 4
            gameStatesHistory.push(tempAyoState);
          }
          
  }


console.log(tempAyoState)
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
  
  // Reset Button
  select("#reset").mousePressed(function () {
    resetGame = true;
    if (resetGame) {
      pauseGame = true;
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
      frameR += 4;
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

// Renders the stats values on the page.
function renderStats(){
  let currentPlayerNum = gameStatesHistory[a]['currentPlayer']
  select(".game_state>span").elt.innerText = a;
  select(".current_player>span").elt.innerText = currentPlayerNum;
  select(`.player.${W2N[currentPlayerNum]}`).addClass('current_style')
  select(`.player.${W2N[(currentPlayerNum%2)+1]}`).removeClass('current_style')
  select('.player.one .score >span').elt.innerText = gameStatesHistory[a]['playerScore0']
  select('.player.two .score >span').elt.innerText = gameStatesHistory[a]['playerScore1']
  select('.player.one .times_played >span').elt.innerText = gameStatesHistory[a]['timesPlayed1']
  select('.player.two .times_played >span').elt.innerText = gameStatesHistory[a]['timesPlayed2']

  if(gameStatesHistory[a]['playerScore0'] > gameStatesHistory[a]['playerScore1']){
    select('.winning_player >span').elt.innerText = 'Player 1'
    select('.losing_player >span').elt.innerText = 'Player 2'
  }else if(gameStatesHistory[a]['playerScore0'] < gameStatesHistory[a]['playerScore1']){
    select('.winning_player >span').elt.innerText = 'Player 2'
    select('.losing_player >span').elt.innerText = 'Player 1'
  }else{
    select('.winning_player >span').elt.innerText = 'Draw'
    select('.losing_player >span').elt.innerText = 'Draw'

  }
}