$(document).ready(function() {

    $('.review-form').on('click', function(event) {
        event.preventDefault();
    })

    console.log("working")
    productid = $('[data-id]').attr('data-id')
    console.log(productid)
    $.ajax({
        method:"GET",
        url: "/rating_votes/"+productid,
        success: onSuccess,
        error: onError
    })

    function onSuccess(response) {
        console.log(response)
        let ratings= []
        for(var i=0; i< response.length; i++){
            if (!isNaN(response[i]) && response[i] !== " "){
                console.log(response[i])
                ratings.push(parseInt(response[i]))
            }
        }
        console.log(ratings)
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: ['5', '4', '3', '2', '1'],
                datasets: [{
                    label: 'Reviews',
                    data: ratings,
                    backgroundColor: 'gray',
                    borderColor: 'gray',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
        $('#myChart').css("height: 200px; width: 200px")
    

    }

    function onError() {
        console.log("error")
    }

    
})
