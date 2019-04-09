$(document).ready(
    console.log("quiz js")
)


$(`input[type='radio']`).on('click', function() {
    $(this).siblings('button').removeClass('hide')
}) 

$('.start').click( function(event) {
    event.preventDefault()
    $(this).parent().addClass('hide')
    // debugger;
    $(this).parent().next().removeClass('hide')

})

$('.next').click( function(event) {
    event.preventDefault()
    $(this).parent().parent().addClass('hide')
    // debugger;
    $(this).parent().parent().next().removeClass('hide')
    $(this).addClass('hide')

})

$('.restart').click( function(event) {
    event.preventDefault()
    $(this).parent().parent().addClass('hide')
    $('#first, form').removeClass('hide')
})

let result = "";
$('#quiz').submit(function(e) {
    e.preventDefault()
    $(this).children().last().addClass('hide')
    var answers = $(this).serializeArray();
    console.log(answers)
    var resultNumber = 0
    for(var answer of answers){
        resultNumber += parseInt(answer.value)
    }
    console.log(resultNumber)
    result = getResults(resultNumber)
    console.log(result)
    displayResults(result)
    this.reset()
})

function getResults(num) {
    console.log('here')
    if( 8 < num && num <= 13){
        return "cosmos"
    }else if (14 < num && num <= 19){
        return "dogwood"
    } else if (20 < num && num <= 25){
        return "bluebell"
    } else if (26 < num && num <= 32){
        return "mistletoe"
    }
}

function displayResults(flower) {
    $('form').addClass('hide')
    $(`#${flower}`).removeClass('hide')

}
