$(document).ready(function() {

    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function() {
  
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
  
    });

    $(".delete").click(function() {
        $(this).parent().remove()
    })

    $('.subscribe').click(function(e) {
        e.preventDefault()
        // debugger;
        if($("#subscribeEmail").is(':valid')) {
            $('#subscribeModal').modal('show');
            console.log($('#subscriberEmail'))
            // debugger;
            $(this).closest("form")[0].reset(); 
          }
    })

  });