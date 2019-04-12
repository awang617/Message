// creating a chart with an ajax call to get the review ratings for a product
$(document).ready(function() {
    console.log("working")

    $('.review-form').on('click', function(event) {
        event.preventDefault();
        $(this).siblings('.review').slideDown()

    })

    $('.cancel-review').on('click', function(event) {
        event.preventDefault();
        $(this).parents('.review').slideUp()
    })

    productid = $('[data-id]').attr('data-id')
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
        let ratings= []
        // getting rid of the brackets and white spaces
        let str = response.replace(/[\[\]']+/g, '')
        str = str.replace(/\s/g, '')
        // split based on commas to make an array of strings
        let part = str.split(',')
        // change the str to int and push to the array
        for(var i=0; i< part.length; i++){
            ratings.push(parseInt(part[i]))
        }
        // render the chart
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
