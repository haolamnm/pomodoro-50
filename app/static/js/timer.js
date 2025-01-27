// import { showFlashMessage } from "./utils/flash";

function showFlashMessage(message, category) {
	const flashMessageContainer = document.getElementById("flash-message");

    // Remove all existing child elements from the container
    while (flashMessageContainer.firstChild) {
        flashMessageContainer.removeChild(flashMessageContainer.firstChild);
    }

	const flashMessage = document.createElement("div");
	flashMessage.classList.add("alert", `alert-${category}`, "alert-dismissible", "mb-0", "text-center", "fade", "show");
	flashMessage.role = "alert";
	flashMessage.textContent = message;

	const closeButton = document.createElement("button");
	closeButton.type = "button";
	closeButton.classList.add("btn-close");
	closeButton.setAttribute("data-bs-dismiss", "alert");
	flashMessage.setAttribute("aria-label", "Close");

	flashMessageContainer.appendChild(flashMessage);
	flashMessage.appendChild(closeButton);
}


document.addEventListener("DOMContentLoaded", function () {
	const timerDisplay = document.getElementById("timer-display");
	const pomodoroTitle = document.getElementById("pomodoro-title");
	const startButton = document.getElementById("start-button");
	const pauseButton = document.getElementById("pause-button");
	const pomodoroTime = document.getElementById("pomodoro-time");
	const stopModal = new bootstrap.Modal(document.getElementById("stop-modal"));

	const clickSound = new Audio("/static/audio/click.wav");
	const finishSound = new Audio("/static/audio/finish.wav");

	let remainingTime = convertTimeToSeconds(timerDisplay.textContent);
	let isRunning = false;
	let timer;

	function convertTimeToSeconds(time) {
		const [minutes, seconds] = time.split(":");
		return parseInt(minutes) * 60 + parseInt(seconds);
	}

	function formatTime(seconds) {
		const minutes = Math.floor(seconds / 60).toString().padStart(2, "0");
		const secs = (seconds % 60).toString().padStart(2, "0");
		return `${minutes}:${secs}`;
	}

	function updateDisplay() {
		timerDisplay.textContent = formatTime(remainingTime);
	}

	function resetDisplay() {
		remainingTime = convertTimeToSeconds(pomodoroTime.value);
		updateDisplay();
	}

	async function createCompletedPomodoro() {
		try {
			const response = await fetch("/core/add/pomodoro", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					title: pomodoroTitle.value.toLowerCase().trim(),
					duration: convertTimeToSeconds(pomodoroTime.value),
					start_at: new Date(Date.now() - convertTimeToSeconds(pomodoroTime.value) * 1000).toISOString(),
					end_at: new Date().toISOString(),
					is_completed: true,
					reason: "completed",
				}),
			});

			if (!response.ok) {
				const error = await response.json();
				console.error("Error creating Pomodoro:", error);
				return;
			}

			const data = await response.json();
			// console.log("Pomodoro created:", data);

		} catch (error) {
			console.error("Unexpected error:", error);
		}
	};

	async function createStoppedPomodoro(reason, remainingTime) {
		try {
			const response = await fetch("/core/add/pomodoro", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					title: pomodoroTitle.value.toLowerCase().trim(),
					duration: convertTimeToSeconds(pomodoroTime.value) - remainingTime,
					start_at: new Date(Date.now() - convertTimeToSeconds(pomodoroTime.value) * 1000 + remainingTime * 1000).toISOString(),
					end_at: new Date().toISOString(),
					is_completed: false,
					reason: reason.toLowerCase().trim(),
				}),
			});

			if (!response.ok) {
				const error = await response.json();
				console.error("Error creating Pomodoro:", error);
				return;
			}

			const data = await response.json();
			// console.log("Pomodoro created:", data);
		} catch (error) {
			console.error("Unexpected error:", error);
		}
	}

	async function storeInvalidReason(reason) {
		try {
			const response = await fetch("/core/add/invalid-reason", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					reason: reason.toLowerCase().trim(),
				}),
			});

			if (!response.ok) {
				const error = await response.json();
				console.error("Error storing invalid reason:", error);
				return;
			}

			const data = await response.json();
			console.log("Invalid reason stored:", data);
		} catch (error) {
			console.error("Unexpected error:", error);
		}
	}

	function startTimer() {
		// If the user has not entered a title for the Pomodoro
		if (pomodoroTitle.value === '') {
			showFlashMessage("Please enter a title for the Pomodoro", "info");
			return;
		}

		// If the timer is not running and there is time remaining
		if (!isRunning && remainingTime > 0) {
			isRunning = true;
			pomodoroTitle.setAttribute("disabled", "true");
			startButton.classList.add("d-none");
			pauseButton.classList.remove("d-none");

			// Start the timer
			timer = setInterval(() => {
				if (remainingTime > 0) {
					remainingTime -= 1;
					updateDisplay();
				} else {
					clearInterval(timer);
					isRunning = false;
					pomodoroTitle.removeAttribute("disabled");
					startButton.classList.remove("d-none");
					pauseButton.classList.add("d-none");
					createCompletedPomodoro();
					showFlashMessage("Pomodoro completed", "success");
					resetDisplay();
					finishSound.play();
				}
			}, 1000);
		}
	}

	function pauseTimer() {
		// If the timer is running
		if (isRunning) {
			isRunning = false;
			clearInterval(timer);
			startButton.classList.remove("d-none");
			pauseButton.classList.add("d-none");
		}
	}

	startButton.addEventListener("click", () => {
		stopModal.hide();
		startTimer();
		clickSound.play();
	});
	pauseButton.addEventListener("click", () => {
		stopModal.show();
		pauseTimer();
		clickSound.play();
	});

	async function handleSendReason() {
		const stopReasonTextarea = document.getElementById("stop-reason");
		const reason = stopReasonTextarea.value;
		const infoDisplay = document.getElementById("info-display");

		infoDisplay.innerHTML = '';

		if (!reason) {
			infoDisplay.innerHTML = `
				<div class="alert alert-warning alert-dismissible fade show" role="alert">
					Please provide a reason for stopping the timer.
					<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>
			`;
			return;
		}

		try {
			infoDisplay.innerHTML = `
				<div class="spinner-border text-primary" role="status">
					<span class="visually-hidden">Loading...</span>
				</div>
			`;
			stopReasonTextarea.setAttribute("disabled", "true");

			// Get the buttons to disable them
			const closeButton = document.getElementById("close-button");
			const sendReasonButton = document.getElementById("send-reason-button");

			// Disable the buttons
			closeButton.setAttribute("disabled", "true");
			sendReasonButton.setAttribute("disabled", "true");

			const response = await fetch("/core/check/reason", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					reason: reason,
					remain: formatTime(remainingTime),
					total: pomodoroTime.value,
					title: pomodoroTitle.value
				}),
			});
			// console.log(response);

			const aiResponse = await response.json();
			// console.log(aiResponse);

			const adviceDisplay = document.getElementById("advice-display");
			const modalFooter = document.querySelector(".modal-footer");

			// Clear the processing spinner
			infoDisplay.innerHTML = '';

			adviceDisplay.textContent = aiResponse.advice;

			if (aiResponse.status === 'invalid') {
				infoDisplay.innerHTML = `
					<div class="alert alert-warning alert-dismissible fade show" role="alert">
						PomoPal declined your reason!
						<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
					</div>
				`;

				modalFooter.innerHTML = `
					<button type="button" class="btn btn-secondary" id="close-button" data-bs-dismiss="modal">
						<i class="fas fa-x"></i>
					</button>
					<button type="button" class="btn btn-primary" id="continue-timer-button">
						<i class="fas fa-play"></i> <span id="countdown">30</span>s
					</button>
				`;

				let countdown = 30;
				const continueTimerButton = document.getElementById("continue-timer-button");
				const countdownSpan = document.getElementById("countdown");
				const closeButton = document.getElementById("close-button");
				const countdownInterval = setInterval(() => {
					countdown -= 1;
					countdownSpan.textContent = countdown;
					if (countdown === 0) {
						clearInterval(countdownInterval);
						storeInvalidReason(aiResponse.reason);
						stopModal.hide();
						startTimer();
					}
				}, 1000);

				continueTimerButton.addEventListener("click", () => {
					clearInterval(countdownInterval);
					storeInvalidReason(aiResponse.reason);
					stopModal.hide();
					startTimer();
					clickSound.play();
				});

				closeButton.addEventListener("click", () => {
					storeInvalidReason(aiResponse.reason);
					stopModal.hide();
					startTimer();
					clickSound.play();
				});

			} else {
				infoDisplay.innerHTML = `
					<div class="alert alert-success alert-dismissible fade show" role="alert">
						PomoPal accepted your reason!
						<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
					</div>
				`;

				modalFooter.innerHTML = `
					<button type="button" class="btn btn-secondary" id="close-button" data-bs-dismiss="modal">
						<i class="fas fa-x"></i>
					</button>
					<button type="button" class="btn btn-danger" id="stop-completely-button">
						<i class="fas fa-stop"></i>
					</button>
				`;

				const stopCompletelyButton = document.getElementById("stop-completely-button");
				const closeButton = document.getElementById("close-button");

				stopCompletelyButton.addEventListener("click", () => {
					pomodoroTitle.removeAttribute("disabled");
					stopModal.hide();
					pauseTimer();
					// console.log(pomodoroTime.value, remainingTime, aiResponse.reason);
					createStoppedPomodoro(aiResponse.reason, remainingTime);
					showFlashMessage("Pomodoro stopped", "info");
					resetDisplay();
					clickSound.play();
				});

				closeButton.addEventListener("click", () => {
					stopModal.hide();
					pauseTimer();
					createStoppedPomodoro(aiResponse.reason, remainingTime);
					showFlashMessage("Pomodoro stopped", "info");
					resetDisplay();
					clickSound.play();
				});
			}
		} catch (error) {
			console.error(error);
			infoDisplay.innerHTML = `
				<div class="alert alert-danger alert-dismissible fade show" role="alert">
					An error occurred. Please try again.
					<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
				</div>
			`;
		}
	}

	document.querySelector(".modal-footer").addEventListener("click", (event) => {
		if (event.target.id === "send-reason-button") {
			handleSendReason();
			clickSound.play();
		} else if (event.target.id === "close-button") {
			stopModal.hide();
			startTimer();
			clickSound.play();
		}
	});

	document.getElementById("stop-modal").addEventListener("hidden.bs.modal", () => {
		const stopReasonTextarea = document.getElementById("stop-reason");
		stopReasonTextarea.value = '';
		stopReasonTextarea.removeAttribute("disabled");

		const infoDisplay = document.getElementById("info-display");
		infoDisplay.innerHTML = '';

		const adviceDisplay = document.getElementById("advice-display");
		adviceDisplay.textContent = '';

		const modalFooter = document.querySelector(".modal-footer");
		modalFooter.innerHTML = `
			<button type="button" class="btn btn-secondary" id="close-button" data-bs-dismiss="modal">
				<i class="fas fa-x"></i>
			</button>
			<button type="button" class="btn btn-primary" id="send-reason-button">
				<i class="fas fa-paper-plane"></i>
			</button>
		`;

		const closeButton = document.getElementById("close-button");
		closeButton.addEventListener("click", () => {
			stopModal.hide();
			startTimer();
			clickSound.play();
		});
	});
});
