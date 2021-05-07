var ctx = document.getElementById('myChart').getContext('2d');
var graphData = {
    type: 'line',
    data: {

        labels: [0 , 1 , 2 , 3, 4, 5, 6 , 7, 8, 9 , 10,11,12,13,14,15,16,17,18,19,20],
        datasets: [{
            label: 'Des valeurs aléatoires en fonction du temps',
            data: [12, 19, 3, 5, 2, 3 , 7,6,2,3,4,6,5,7,9,8,7,6,7,5],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
            ],
            
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
    
};
var myChart = new Chart(ctx,graphData );

ctx.fillText("My x axis label", 0, 0);

var socket = new WebSocket("ws://localhost:8000/ws/graph/");
socket.onmessage =function(e){
    var djangoData = JSON.parse(e.data);
    var newData = graphData.data.datasets[0].data;
    var newData2 = graphData.data.labels;
    newData2.shift();
    newData2.push(newData2[newData2.length -1] +1 )
    newData.shift();
    newData.push(djangoData.value)
    myChart.update()

    console.log('h' + typeof(djangoData.value) + djangoData);
    
};