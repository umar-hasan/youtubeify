$(document).ready(function () {


    $("#nav-top-container").height($(".navbar").height())
    $("#nav-left-container").width($(".navbar").width())

    $(".hamburger").on("click", () => {
        $("#actions").hide()
        if ($(".hamburger").hasClass("is-active")) {
            $("#main-page").animate({ marginLeft: '0'}, 1000)
            $(".hamburger").removeClass("is-active")
            $(".side-menu").removeClass("animate__slideInLeft")
            $(".side-menu").addClass("animate__slideOutLeft")
            
        }
        else {
            $("#main-page").animate({ marginLeft: `${$(".side-menu").width()}px`}, 500)
            $(".hamburger").addClass("is-active")
            $(".side-menu").removeClass("animate__slideOutLeft")
            $(".side-menu").addClass("animate__slideInLeft")
            
        }
        
        
    })

    $(".alert").delay(5000).fadeOut('slow')


    
});