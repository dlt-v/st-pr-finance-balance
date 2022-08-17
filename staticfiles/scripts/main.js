const labels = ['January', 'February', 'March', 'April', 'May', 'June'];

const data = {
    labels: labels,
    datasets: [
        {
            label: 'My First dataset',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45],
            color: '#fff',
        },
    ],
};

const config = {
    type: 'bar',
    data: data,
    options: {
        color: '#fff',
        backgroundColor: '#fff',
        scales: {
            color: 'rgba(0, 0, 0, 0.4)',
            y: {
                beginAtZero: true,
                ticks: {
                    // Include a dollar sign in the ticks
                    callback: function (value, index, ticks) {
                        return '$' + value;
                    },

                    color: 'white',
                },
                color: 'white',
            },
        },
    },
};
const myChart = new Chart(document.getElementById('myChart'), config);
