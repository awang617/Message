$(document).ready(
    console.log("quiz js")
)

$(`input[type='radio']`).on('click', function() {
    console.log("keyup")
    $(this).siblings('button').removeClass('hide')
}) 


$('.next').click( function(event) {
    event.preventDefault()
    console.log("clicked")
    $(this).parent().addClass('hide')
    $(this).parent().next().removeClass('hide')

})

let result = "";
$('#quiz').submit(function(e) {
    e.preventDefault()
    var answers = $(this).serializeArray();
    console.log(answers)

    var resultNumber = 0
    for(var answer of answers){
        console.log(answer.value)
        resultNumber += parseInt(answer.value)
    }
    console.log(resultNumber)
    result = getResults(resultNumber)
    console.log(result)
    displayResults(result)
})

function getResults(num) {
    console.log('here')
    if( 0 < num && num <= 4){
        return "bay leaf"
    }else if (5 < num && num <= 8) {
        return "azalea"
    } else if (8 < num && num <= 12) {
        console.log(num)
        return "bluebell"
    } else if (13 < num && num <= 16){
        return "mistletoe"
    }
}

function displayResults(flower) {
    $('form').addClass('hide')
    $(`#${flower}`).removeClass('hide')

}
