document.addEventListener('DOMContentLoaded', function() {
	const weeklyDurations = document.getElementById('weekly-durations').value;
	const durations = JSON.parse(weeklyDurations);

	const ctx = document.getElementById('durationsChart').getContext('2d');
	const durationsChart = new Chart(ctx, {
		type: 'bar',
		data: {
			labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
			datasets: [{
				label: 'Minutes spent',
				data: durations,
				backgroundColor: [
					'rgba(75, 192, 192, 0.5)',
					'rgba(54, 162, 235, 0.5)',
					'rgba(255, 206, 86, 0.5)',
					'rgba(153, 102, 255, 0.5)',
					'rgba(255, 99, 132, 0.5)',
					'rgba(201, 203, 207, 0.5)',
					'rgba(255, 159, 64, 0.5)'
				],
				borderColor: [
					'rgba(75, 192, 192, 1)',
					'rgba(54, 162, 235, 1)',
					'rgba(255, 206, 86, 1)',
					'rgba(153, 102, 255, 1)',
					'rgba(255, 99, 132, 1)',
					'rgba(201, 203, 207, 1)',
					'rgba(255, 159, 64, 1)'
				],
				borderWidth: 1
			}]
		},
		options: {
			responsive: true,
			scales: {
				y: {
					beginAtZero: true,
					title: {
						display: true,
						text: 'Minutes'
					}
				},
				x: {
					title: {
						display: true,
						text: 'Day of the Week'
					}
				}
			},
			plugins: {
				legend: {
					display: true,
					position: 'top'
				}
			}
		}
	});
});
