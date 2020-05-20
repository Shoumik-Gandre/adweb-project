const adclicks = [];
const adviews = [];
const hourlist = [];
const adview_hourlist = [];
const colorlist = [];
const borderColorList = [];
const obj = {};
const adview_obj = {};

function fill_chart_lists() {
    let color, borderColor, redValue, greenValue, blueValue, d, index_d;
    // This function fills adclicks and hourlist with corresponding values
    click_log.forEach(click_data => {
        d = date_calc(new Date(click_data.fields.click_date));

        /*
        // Color Related
        redValue = Math.ceil(Math.random()*255 + 1);
        greenValue = Math.ceil(Math.random()*255 + 1);
        blueValue = Math.ceil(Math.random()*255 + 1);
        color = 'rgba(' + redValue + ', ' + greenValue + ', ' + blueValue + ', ' + 0.2 +')';
        borderColor = 'rgba(' + redValue + ', ' + greenValue + ', ' + blueValue + ', ' + 1 +')';
        colorlist.push(color);
        borderColorList.push(borderColor);
        */

        // filling hourlist, obj
        index_d = hourlist.indexOf(d);
        if (index_d===-1) {
            if(click_data.fields.is_clicked === true) {
                hourlist.push(d);
                obj[hourlist[hourlist.length - 1]] = 1;
            }
        } else{
            obj[d] += 1;
        }
        index_d = adview_hourlist.indexOf(d);
        if (index_d===-1) {
            adview_hourlist.push(d);
            adview_obj[adview_hourlist[adview_hourlist.length - 1]] = 1;
        } else{
            adview_obj[d] += 1
        }
    });
    
    hourlist.forEach(key => {
        adclicks.push(obj[key]);
    });

    adview_hourlist.forEach(key =>{
        adviews.push(adview_obj[key]);
    });
    
    function time_calc(in_date) {
        return (in_date.getHours() > 12 ? in_date.getHours()-12 + "PM" : in_date.getHours() + "AM");
    }

    function date_calc(in_date) {
        return in_date.getFullYear() + '/' + (parseInt(in_date.getMonth()) + 1).toString() + '/' + in_date.getDate();
    }
}

fill_chart_lists()



const ctx = document.getElementById('detail-click-chart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
        labels: hourlist,
        datasets: [{
            label: 'Clicks',
            data: adclicks,
            backgroundColor: 'rgba(153, 51, 255, 0.2)',
            borderColor: 'rgba(153, 51, 255, 1)',
            borderWidth: 1
        },
        {
            label: 'Views',
            data: adviews,
            backgroundColor: 'rgba(255, 204, 0, 0.2)',
            borderColor: 'rgba(255, 204, 0, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Clicks and Views',
                    barThickness: 10,
                },
                ticks: {
                    beginAtZero: true,
                    callback: function (value) { if (Number.isInteger(value)) { return value; } },
                    stepSize: 1
                }
            }],
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Date',
                    barThickness: 10
                },
            }]
        }
    }
});