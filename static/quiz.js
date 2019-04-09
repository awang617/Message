$(document).ready(
    console.log("quiz js")
)


$(`input[type='radio']`).on('click', function() {
    $(this).siblings('button').removeClass('hide')
}) 


$('.next').click( function(event) {
    event.preventDefault()
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
        resultNumber += parseInt(answer.value)
    }
    console.log(resultNumber)
    result = getResults(resultNumber)
    displayResults(result)
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
