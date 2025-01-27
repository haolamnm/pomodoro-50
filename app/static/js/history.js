document.addEventListener("DOMContentLoaded", function () {
	const searchInput = document.getElementById("search-input");
	const tableBody = document.getElementById("pomodoro-table-body");
	const rows = tableBody.getElementsByTagName("tr");

	// Add event listener to the search input
	searchInput.addEventListener("input", function () {
		const searchTerm = searchInput.value.toLowerCase();

		// Loop through all rows and hide those that don't match the search term
		for (let row of rows) {
			const cells = row.getElementsByTagName("td");
			let shouldShow = false;

			// Check each cell in the row (except the Status cell)
			for (let i = 0; i < cells.length; i++) {
				if (i !== 3) { // Skip the Status cell (index 3)
					const cellText = cells[i].textContent.toLowerCase();
					if (cellText.includes(searchTerm)) {
						shouldShow = true;
						break;
					}
				}
			}

			// Show or hide the row based on the search result
			row.style.display = shouldShow ? "" : "none";
		}
	});
});
