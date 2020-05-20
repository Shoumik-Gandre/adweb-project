let adnames = [];
let adclicks = [];
let adviews = [];
let colorlist = [];

ads.forEach(element => {
    adnames.push(element.fields.name);
});

var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
        labels: adnames,
        datasets: [{
            label: 'Clicks',
            data: alog_click_count,
            backgroundColor: 'rgba(51, 102, 255, 0.2)',
            borderColor: 'rgba(51, 102, 255, 1)',
            borderWidth: 1
        },
        {
			label: 'Total Views',
            backgroundColor: 'rgba(255, 204, 0, 0.2)',
            borderColor: 'rgba(255, 204, 0, 1)',
            data: alog_view_count,
            borderWidth: 1
		}
    ]
    },
    options: {
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                },
                //stacked: true,
            }],
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Clicks',
                },
                ticks: {
                    beginAtZero: true,
                    callback: function (value) { if (Number.isInteger(value)) { return value; } },
                    stepSize: 1
                },
            }]
        }
    }
});