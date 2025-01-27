document.addEventListener("DOMContentLoaded", function () {
	const currentDate = new Date();
	const clickSound = new Audio("/static/audio/click.wav");
	const calHeatmapDataStr = document.getElementById("cal-heatmap-data").value;
	const calHeatmapDataJSON = calHeatmapDataStr.replace(/'/g, '"');
	const calHeatmapDataObj = JSON.parse(calHeatmapDataJSON);
	let currentMonth = currentDate.getMonth();
	let currentYear = currentDate.getFullYear();

	// Determine the initial start date
	let startDate;
	if (currentMonth < 6) {
		startDate = new Date(currentYear, 0);
	} else {
		startDate = new Date(currentYear, 6);
	}

	const currentDateRangeContainer = document.getElementById("current-date-range");

	function updateDateRange(start) {
		const options = { year: "numeric", month: "short" };
		const startDate = new Date(start);
		const endDate = new Date(start);
		startDate.setMonth(start.getMonth());
		endDate.setMonth(start.getMonth() + range - 1); // Adjust for range

		const rangeText = `${startDate.toLocaleDateString("en-US", options)} - ${endDate.toLocaleDateString("en-US", options)}`;

		currentDateRangeContainer.textContent = rangeText;
	}


	// Determine the range based on screen size
	let range = window.innerWidth >= 768 ? 6 : 4;

	// Function to clear and repaint the calendar
	function paintCalendar(start) {
		const calContainer = document.getElementById("cal-heatmap");
		// Clear previous content
		calContainer.innerHTML = "";

		// Update the date range text
		updateDateRange(start);

		// Reinitialize CalHeatmap instance
		const cal = new CalHeatmap();
		const displayDate = new Date(start);
		displayDate.setMonth(start.getMonth() + 1);
		cal.paint({
			animationDuration: 250,
			theme: 'dark',
			data: {
				source: calHeatmapDataObj,
				type: 'json',
				x: 'date',
				y: (d) => d.value,
				groupY: 'max',
			},
			date: { start: displayDate },
			range: range,
			scale: {
				color: {
					type: 'threshold',
					range: ['#14432a', '#166b34', '#37a446', '#4dd05a'],
					domain: [2, 4, 6, 8, 10],
				},
			},
			domain: {
				type: 'month',
				gutter: 3,
				label: { text: 'MMM', textAlign: 'start', position: 'top' },
			},
			subDomain: { type: 'ghDay', radius: 3, width: 15, height: 15, gutter: 3 },
		});
	}

	// Initial render
	paintCalendar(startDate);

	// Add event listeners for navigation buttons
	const prevButton = document.getElementById("prev-button");
	const nextButton = document.getElementById("next-button");

	prevButton.addEventListener("click", function () {
		// Move back by the current range
		currentMonth -= range;
		if (currentMonth < 0) {
			currentMonth += 12;
			currentYear -= 1;
		}
		startDate = new Date(currentYear, currentMonth);
		paintCalendar(startDate);
		clickSound.play();
	});

	nextButton.addEventListener("click", function () {
		// Move forward by the current range
		currentMonth += range;
		if (currentMonth > 11) {
			currentMonth -= 12;
			currentYear += 1;
		}
		startDate = new Date(currentYear, currentMonth);
		paintCalendar(startDate);
		clickSound.play();
	});

	// Adjust range on screen resize
	window.addEventListener("resize", function () {
		const newRange = window.innerWidth >= 768 ? 6 : 4;
		if (newRange !== range) {
			range = newRange;
			paintCalendar(startDate);
		}
	});
});
