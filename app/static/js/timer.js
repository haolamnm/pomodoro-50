document.addEventListener("DOMContentLoaded", function () {
	let timer;
	const timerDisplay = document.getElementById("timer-display");
	const pomodoroTitle = document.getElementById("pomodoro-title");

	function convertTimeToSeconds(time) {
		const [minutes, seconds] = time.split(":");
		return parseInt(minutes) * 60 + parseInt(seconds);
	}

	let remainingTime = convertTimeToSeconds(timerDisplay.textContent);
	let isRunning = false;

	const startButton = document.getElementById("start-button");
	const pauseButton = document.getElementById("pause-button");

	function formatTime(seconds) {
		const minutes = Math.floor(seconds / 60).toString().padStart(2, "0");
		const secs = (seconds % 60).toString().padStart(2, "0");
		return `${minutes}:${secs}`;
	}

	function updateDisplay() {
		timerDisplay.textContent = formatTime(remainingTime);
	}

	function startTimer() {
		if (!isRunning && remainingTime > 0 && pomodoroTitle.value !== '') {
			isRunning = true;
			startButton.classList.add("d-none");
			pauseButton.classList.remove("d-none");

			timer = setInterval(() => {
				if (remainingTime > 0) {
					remainingTime -= 1;
					updateDisplay();
				} else {
					clearInterval(timer);
					isRunning = false;
					alert("Time's up!"); // TODO: Update database
					startButton.classList.remove("d-none");
					pauseButton.classList.add("d-none");

					// TODO: Fetch from database
					// Like document.getElementById("custom-pomodoro-time");
					// const customPomodoroTime = 50 * 60;
				}
			}, 1000);
		}
	}

	function pauseTimer() {
		if (isRunning) {
			isRunning = false;
			clearInterval(timer);
			startButton.classList.remove("d-none");
			pauseButton.classList.add("d-none");
		}
	}

	startButton.addEventListener("click", startTimer);
	pauseButton.addEventListener("click", pauseTimer);

	const stopModal = new bootstrap.Modal(document.getElementById("stop-modal"));
	const confirmStop = document.getElementById("confirm-stop");

	pauseButton.addEventListener("click", () => {
		stopModal.show();
	});

	confirmStop.addEventListener("click", () => {
		stopModal.hide();
		pauseTimer();
		remainingTime = convertTimeToSeconds(timerDisplay.textContent); // Reset timer
		updateDisplay();
	});
});
