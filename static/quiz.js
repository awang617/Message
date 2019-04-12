$(document).ready(
    console.log("quiz js")
)


$(`input[type='radio']`).on('click', function() {
    $(this).siblings().find('button').removeAttr('disabled')
}) 

$('.start').click( function(event) {
    event.preventDefault()
    $(this).parent().addClass('hide')
    // debugger;
    $(this).parent().next().removeClass('hide')

})

$('.next').click( function(event) {
    event.preventDefault()
    $(this).parent().parent().parent().addClass('hide')
    // debugger;
    $(this).parent().parent().parent().next().removeClass('hide')
    $(this).attr('disabled','disabled')

})

$('.restart').click( function(event) {
    event.preventDefault()
    $(this).parent().parent().parent().addClass('hide')
    $('#first, form').removeClass('hide')
})

let result = "";
$('#quiz').submit(function(e) {
    e.preventDefault()
    $(this).children().last().addClass('hide')
    var answers = $(this).serializeArray();
    var resultNumber = 0
    for(var answer of answers){
        resultNumber += parseInt(answer.value)
    }
    result = getResults(resultNumber)
    displayResults(result)
    this.reset()
})

function getResults(num) {
    if( 8 <= num && num <= 14){
        return "cosmos"
    }else if (15 <= num && num <= 20){
        return "dogwood"
    } else if (21 <= num && num <= 26){
        return "bluebell"
    } else if (27 <= num && num <= 32){
        return "mistletoe"
    }
}

function displayResults(flower) {
    $('form').addClass('hide')
    $(`#${flower}`).removeClass('hide')

}
