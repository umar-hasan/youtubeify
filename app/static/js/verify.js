$(document).ready(function () {
    
    if ($("#yt-verified").length) {
        $("#yt-icon").css("mix-blend-mode", "exclusion")
        $("#yt-verify-icon").css("mix-blend-mode", "soft-light")
        $("#yt-link").hover(function() {
            $("#yt-link").css("mix-blend-mode", "normal")
        })
        $("#yt-link").on("click", function(e) {
            e.preventDefault()
        })
    }

    if ($("#spot-verified").length) {
        $("#spot-icon").css("mix-blend-mode", "exclusion")
        $("#spot-verify-icon").css("mix-blend-mode", "soft-light")
        $("#spot-link").hover(function() {
            $("#spot-link").css("mix-blend-mode", "normal")
        })
        $("#spot-link").on("click", function(e) {
            e.preventDefault()
        })
    }

    if ($("#yt-verified").length && $("#spot-verified").length) {
        $("#continue").show()
    }

});