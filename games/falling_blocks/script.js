// Game Configuration Constants
const GAME_CONFIG = {
    gameWidth: 600,
    playerWidth: 35,
    blockSize: 35,
    moveSpeed: 10,
    initialFallSpeed: 5,
    initialSpawnRate: 500,
    fallSpeedIncreaseInterval: 1000*3, // Increase speed 3 seconds
    spawnRateDecreaseInterval: 1000, // Decrease spawn rate every 1 seconds
    timeWarpDuration: 5000, // 5 seconds duration
    timeWarpEffect: 0.5, // Slows down time to 50%
};

// Game State
const gameState = {
    position: GAME_CONFIG.gameWidth / 2 - GAME_CONFIG.playerWidth / 2,
    score: 0,
    gameStartTime: Date.now(),
    blockFallSpeed: GAME_CONFIG.initialFallSpeed,
    spawnRate: GAME_CONFIG.initialSpawnRate,
    moveLeft: false,
    moveRight: false,
    gameOver: false,
    timeWarpActive: false,
    activeTimeWarps: 0,
};

// Game Elements
const gameArea = document.getElementById('gameArea');
const player = document.getElementById('player');
let scoreDisplay;
let shieldTimer, speedBoostTimer;

function createScoreDisplay() {
    scoreDisplay = document.createElement('div');
    configureElement(scoreDisplay, {top: '10px', right: '10px', color: 'black', position: 'absolute'});
    gameArea.appendChild(scoreDisplay);
}

function setupEventListeners() {
    document.addEventListener('keydown', event => handleKeyPress(event, true));
    document.addEventListener('keyup', event => handleKeyPress(event, false));
}

function handleKeyPress(event, isKeyDown) {
    if (event.key === 'ArrowLeft') gameState.moveLeft = isKeyDown;
    if (event.key === 'ArrowRight') gameState.moveRight = isKeyDown;
}

function updatePlayerPosition() {
    adjustPlayerPosition();
    requestAnimationFrame(updatePlayerPosition);
}

const acceleration = 0.5; // Adjust the rate of acceleration
const maxSpeed = GAME_CONFIG.moveSpeed;
let currentSpeed = 0;

function adjustPlayerPosition() {
    // Collision detection with game area boundaries
    // Left boundary
    if (gameState.position < 0) {
        gameState.position = 0;
        currentSpeed = 0; // Reset speed if colliding with boundary
    }
    // Right boundary
    if (gameState.position > GAME_CONFIG.gameWidth - GAME_CONFIG.playerWidth) {
        gameState.position = GAME_CONFIG.gameWidth - GAME_CONFIG.playerWidth;
        currentSpeed = 0; // Reset speed if colliding with boundary
    }

    if (gameState.moveLeft && gameState.position > 0) {
        currentSpeed = Math.max(currentSpeed - acceleration, -maxSpeed);
    } else if (gameState.moveRight && gameState.position < GAME_CONFIG.gameWidth - GAME_CONFIG.playerWidth) {
        currentSpeed = Math.min(currentSpeed + acceleration, maxSpeed);
    } else {
        // Decelerate to stop
        if (currentSpeed > 0) currentSpeed -= acceleration;
        else if (currentSpeed < 0) currentSpeed += acceleration;
    }
    gameState.position += currentSpeed;
    player.style.left = `${gameState.position}px`;
}



function spawnBlock() {
    if (gameState.gameOver) return;
    const block = document.createElement('div');
    configureElement(block, {width: '50px', height: '50px', backgroundColor: 'red', position: 'absolute', top: '0'});
    block.style.left = `${randomPosition()}px`;
    // add to block class
    block.classList.add('block');
    gameArea.appendChild(block);
    let blockInterval = setInterval(() => moveBlock(block, blockInterval), 50);
}

function moveBlock(block, blockInterval) {
    updateGameDifficulty();
    let blockTop = parseInt(block.style.top.replace('px', '')) + gameState.blockFallSpeed;
    block.style.top = `${blockTop}px`;
    handleBlockCollision(block, blockTop, blockInterval);
}

function updateGameDifficulty() {
    const elapsedTime = Date.now() - gameState.gameStartTime;

    if (gameState.timeWarpActive) return; // Don't update difficulty if time warp is active
    // Increase block fall speed
    gameState.blockFallSpeed = Math.floor(elapsedTime / GAME_CONFIG.fallSpeedIncreaseInterval) + GAME_CONFIG.initialFallSpeed;

    // Decrease spawn rate: make sure it doesn't go below a certain threshold
    const decreaseAmount = Math.floor(elapsedTime / GAME_CONFIG.spawnRateDecreaseInterval);
    gameState.spawnRate = Math.max(100, GAME_CONFIG.initialSpawnRate - decreaseAmount); // Assuming 100ms is the minimum spawn rate

    console.log("Spawn Rate:" + gameState.spawnRate);
    console.log("Block Fall Speed:" + gameState.blockFallSpeed);
    console.log("Elapsed Time:" + elapsedTime);
}


function handleBlockCollision(block, blockTop, blockInterval) {
    collision = checkCollision(block, blockTop);
    console.log("Collision: " + collision);
    if (collision) {
        player.classList.add('player-collision'); // Add flash effect
        setTimeout(() => player.classList.remove('player-collision'), 500); // Remove effect after animation
        //alert("Game Over!");
        clearInterval(blockInterval);
        //window.location.reload(); // Consider a more sophisticated game over handling
        showGameOverScreen();
        
    }
    if (blockTop > GAME_CONFIG.gameWidth) {
        clearInterval(blockInterval);
        gameArea.removeChild(block);
    }
}

function checkCollision(block, blockTop) {
    if (gameState.gameOver || gameState.isInvincible) return false;
    
    let blockLeft = parseInt(block.style.left.replace('px', ''));
    let blockRight = blockLeft + GAME_CONFIG.blockSize;
    
    let playerLeft = gameState.position;
    let playerRight = playerLeft + GAME_CONFIG.playerWidth;
    let playerBottom = 400 - 10; // Bottom of the game area minus player's bottom margin
    let playerTop = playerBottom - 35; // Player's height is 35px

    // Check if block and player overlap
    let collisionX = blockLeft < playerRight && blockRight > playerLeft;
    let collisionY = blockTop < playerBottom && (blockTop + GAME_CONFIG.blockSize) > playerTop;

    return collisionX && collisionY;
}



function updateScore() {
    if (gameState.gameOver) return;
    gameState.score++;
    scoreDisplay.textContent = `Score: ${gameState.score}`;
}

function gameLoop() {
    if (!gameState.gameOver) {
        
        setTimeout(() => {
            spawnBlock();
            maybeSpawnShieldPowerUp();
            maybeSpawnSpeedBoostPowerUp();
            maybeSpawnTimeWarpPowerUp();
            gameLoop();
        }, gameState.spawnRate);
    }
}

function startGameLoop() {
    updatePlayerPosition();
    gameLoop();
    setInterval(updateScore, 1000);
}

// Game Initialization and Setup
function initGame() {
    createScoreDisplay();
    createPowerUpTimers();
    setupEventListeners();
    startGameLoop();
    drawCanvasBackground();
}

function setupGameArea() {
    // Set up the game area, player, and any other initial visual elements here
    // For now, we're adding the score display to the game area
    gameArea.appendChild(scoreDisplay);
}

// Power-Up Functions
function spawnShieldPowerUp() {
    const shield = document.createElement('div');
    configureElement(shield, {width: '50px', height: '50px', backgroundColor: 'green', position: 'absolute'});
      
    
    shield.style.top = '0';
    shield.style.left = `${randomPosition()}px`;
    shield.classList.add('shield');
    gameArea.appendChild(shield);

    let shieldInterval = setInterval(() => movePowerUp(shield, shieldInterval), 50);
}

function maybeSpawnShieldPowerUp() {
    // Randomly decide to spawn a shield, e.g., 5% chance
    if (Math.random() < 0.05) {
        spawnShieldPowerUp();
    }
}

function movePowerUp(powerUp, powerUpInterval) {
    let powerUpTop = parseInt(powerUp.style.top.replace('px', '')) + 2;
    powerUp.style.top = `${powerUpTop}px`;

    if (checkPowerUpCollision(powerUp)) {
        if (powerUp.classList.contains('speed-boost')) {
            activateSpeedBoost();
        } else if (powerUp.classList.contains('shield')) {
            activateShield();
        }
        clearInterval(powerUpInterval);
        gameArea.removeChild(powerUp);
    } else if (powerUpTop > GAME_CONFIG.gameWidth) {
        clearInterval(powerUpInterval);
        gameArea.removeChild(powerUp);
    }
}


function activateShield() {
    player.classList.add('power-up-pickup'); // Add scale-up effect
    setTimeout(() => player.classList.remove('power-up-pickup'), 200); // Remove effect after animation

    gameState.isInvincible = true;
    clearInterval(shieldTimer); // Clear any existing shield timer
    shieldTimerDisplay.style.display = 'block';
    updateTimer(shieldTimerDisplay, 5); // Reset and start the shield timer
    shieldTimer = setInterval(() => {
        if (updateTimer(shieldTimerDisplay, -1) <= 0) { // Decrease timer and check if it's done
            deactivateShield();
            clearInterval(shieldTimer);
            shieldTimerDisplay.style.display = 'none';
        }
    }, 1000);
    player.classList.add('shield-active');
}

function deactivateShield() {
    gameState.isInvincible = false;
    player.classList.remove('shield-active');
}

function checkPowerUpCollision(powerUp) {
    let powerUpTop = parseInt(powerUp.style.top.replace('px', ''));
    let powerUpLeft = parseInt(powerUp.style.left.replace('px', ''));
    return powerUpTop + GAME_CONFIG.blockSize > 350 && powerUpTop < 400 &&
           powerUpLeft < gameState.position + GAME_CONFIG.playerWidth && powerUpLeft + GAME_CONFIG.blockSize > gameState.position;
}

// Speed powerup

function spawnSpeedBoostPowerUp() {
    const speedBoost = document.createElement('div');
    configureElement(speedBoost, {width: '50px', height: '50px', backgroundColor: 'orange', position: 'absolute'});
    speedBoost.style.top = '0';
    speedBoost.style.left = `${randomPosition()}px`;
    speedBoost.classList.add('speed-boost');

    gameArea.appendChild(speedBoost);

    let speedBoostInterval = setInterval(() => {
        movePowerUp(speedBoost, speedBoostInterval);
        if (checkPowerUpCollision(speedBoost)) {
            activateSpeedBoost();
            clearInterval(speedBoostInterval);
        }
    }, 50);
}

function maybeSpawnSpeedBoostPowerUp() {
    if (Math.random() < 0.05) {  // 5% Adjust probability as needed
        spawnSpeedBoostPowerUp();
    }
}

function activateSpeedBoost() {
    player.classList.add('power-up-pickup'); // Add scale-up effect
    setTimeout(() => player.classList.remove('power-up-pickup'), 200); // Remove effect after animation

    gameState.originalMoveSpeed = gameState.moveSpeed;
    gameState.moveSpeed *= 2;
    clearInterval(speedBoostTimer); // Clear any existing speed boost timer
    speedBoostTimerDisplay.style.display = 'block';
    updateTimer(speedBoostTimerDisplay, 5); // Reset and start the speed boost timer
    speedBoostTimer = setInterval(() => {
        if (updateTimer(speedBoostTimerDisplay, -1) <= 0) { // Decrease timer and check if it's done
            deactivateSpeedBoost();
            clearInterval(speedBoostTimer);
            speedBoostTimerDisplay.style.display = 'none';
        }
    }, 1000);
    player.classList.add('speed-boost-active');
}

function deactivateSpeedBoost() {
    gameState.moveSpeed = gameState.originalMoveSpeed;
    player.classList.remove('speed-boost-active');
}

function spawnTimeWarpPowerUp() {
    const timeWarp = document.createElement('div');
    configureElement(timeWarp, {width: '50px', height: '50px', backgroundColor: 'purple', position: 'absolute'});
    timeWarp.style.top = '0';
    timeWarp.style.left = `${randomPosition()}px`;
    timeWarp.classList.add('time-warp');
    gameArea.appendChild(timeWarp);
    // update timer
    updateTimer(timeWarpTimerDisplay, 5);

    let timeWarpInterval = setInterval(() => {
        movePowerUp(timeWarp, timeWarpInterval);
        if (checkPowerUpCollision(timeWarp)) {
            activateTimeWarp();
            clearInterval(timeWarpInterval);
        }
    }, 50);
}

function maybeSpawnTimeWarpPowerUp() {
    if (Math.random() < 0.03) {  // Adjust probability as needed
        spawnTimeWarpPowerUp();
    }
}

function activateTimeWarp() {
    gameState.activeTimeWarps++;

    if (gameState.activeTimeWarps === 1) { // Only apply effect if this is the first active time warp
        gameState.originalFallSpeed = gameState.blockFallSpeed;
        gameState.blockFallSpeed *= GAME_CONFIG.timeWarpEffect;
    }
    gameState.timeWarpActive = true;

    // Timer for the duration of the power-up
    setTimeout(() => {
        deactivateTimeWarp();
    }, GAME_CONFIG.timeWarpDuration);
}

function deactivateTimeWarp() {
    gameState.activeTimeWarps--;
    if (gameState.activeTimeWarps === 0) { // Only reset speed if this is the last active time warp
        gameState.blockFallSpeed = gameState.originalFallSpeed;
        gameState.timeWarpActive = false;
    }
}

// Utility Functions
function configureElement(element, styles) {
    for (const [key, value] of Object.entries(styles)) {
        element.style[key] = value;
    }
}

function randomPosition() {
    return Math.floor(Math.random() * (GAME_CONFIG.gameWidth - GAME_CONFIG.blockSize));
}

function createPowerUpTimers() {
    shieldTimerDisplay = document.createElement('div');
    speedBoostTimerDisplay = document.createElement('div');
    timeWarpTimerDisplay = document.createElement('div');

    configureElement(shieldTimerDisplay, {top: '50px', right: '10px', position: 'absolute', display: 'none', class: 'power-up-timer'});
    configureElement(speedBoostTimerDisplay, {top: '70px', right: '10px', position: 'absolute', display: 'none', class: 'power-up-timer'});
    configureElement(timeWarpTimerDisplay, {top: '90px', right: '10px', position: 'absolute', display: 'none', class: 'power-up-timer'});

    gameArea.appendChild(shieldTimerDisplay);
    gameArea.appendChild(speedBoostTimerDisplay);
    gameArea.appendChild(timeWarpTimerDisplay);
}

function updateTimer(displayElement, change) {
    let time = parseInt(displayElement.textContent.replace('s', '')) || 0;
    time += change;
    displayElement.textContent = time + 's';
    return time;
}

function createGameOverScreen() {
    const gameOverScreen = document.createElement('div');
    gameOverScreen.classList.add('game-over');
    gameOverScreen.innerHTML = `
        <h1>Game Over!</h1>
        <p>Your score: ${gameState.score}</p>
        <button id="restartButton">Restart</button>
        <button id="mainMenuButton">Main Menu</button>
    `;
    gameArea.appendChild(gameOverScreen);
    gameOverScreen.style.display = 'none';

    document.getElementById('restartButton').addEventListener('click', restartGame);
    document.getElementById('mainMenuButton').addEventListener('click', goToMainMenu);
}

function showGameOverScreen() {
    createGameOverScreen();
    document.querySelector('.game-over').style.display = 'block';
    gameState.gameOver = true; // Add this flag to the gameState
}

function restartGame() {
    location.reload(); // Simple way to restart the game
    // For a more sophisticated restart, you would reset all game state variables and start the game loop again
}

function goToMainMenu() {
    // Redirect to the main menu or change the game's state to show the main menu
    // This depends on how your game's menu system is set up


}

function drawCanvasBackground() {
    const canvas = document.createElement('canvas');
    gameArea.appendChild(canvas);
    canvas.width = gameArea.offsetWidth;
    canvas.height = gameArea.offsetHeight;

    const ctx = canvas.getContext('2d');
    // Draw your patterns here:

    // Example: Draw a grid
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 1;
    for (let i = 0; i < canvas.width; i += 50) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, canvas.height);
        ctx.stroke();
    }
    for (let i = 0; i < canvas.height; i += 50) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(canvas.width, i);
        ctx.stroke();
    }

}




initGame();
