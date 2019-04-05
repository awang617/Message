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
    function add(a,b){
        return a+b
    }

    function onSuccess(response) {
        console.log(response)
        let ratings= []
        let str = response.replace(/[\[\]']+/g, '')
        str = str.replace(/\s/g, '')
        let part = str.split(',')
        for(var i=0; i< part.length; i++){
            ratings.push(parseInt(part[i]))
        }
        console.log(ratings)
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: ['5', '4', '3', '2', '1'],
                datasets: [{
                    label: 'Reviews ('+ ratings.reduce(add) +')',
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
