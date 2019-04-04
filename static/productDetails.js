$(document).ready(function() {
    console.log("working")

    $('.review-form').on('click', function(event) {
        event.preventDefault();
        // $(this).siblings('.review').removeClass('hidden')
        $(this).siblings('.review').slideDown()

    })

    $('.cancel-review').on('click', function(event) {
        event.preventDefault();
        $(this).parents('.review').slideUp()
    })

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
                    xAxes:[{
                        ticks: {
                            beginAtZero: true
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    

    }

    function onError() {
        console.log("error")
    }

    
})
