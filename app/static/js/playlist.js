$(document).ready(function () {

    let content = {}


    if ($(".video").length === 0) {
        $("#no-videos").show()
    }

    if ($(".song").length === 0) {
        $("#no-songs").show()
    }

    $("#playlist-title").hover(function () {
            $(this).find(".edit-btn").show()
            
        }, function () {
            $(this).find(".edit-btn").hide()
        }
    )

    $("#playlist-description").hover(function () {
        $(this).find(".edit-btn").show()
        
        }, function () {
            $(this).find(".edit-btn").hide()
        }
    )

    $("#playlist-title").on("click", function() {
        $("#playlist-info").hide()
        $("#title").val($(".playlist-title").text())
        $("#update-playlist-form").css("display", "flex")
    })

    $("#playlist-description").on("click", function() {
        $("#playlist-info").hide()
        $("#title").val($(".playlist-title").text())
        $("#update-playlist-form").css("display", "flex")
    })

    $("#update-btn").on("click", async function(e) {
        e.preventDefault()
        if ($.trim($("#title").val()).length > 0) {
            let info = {
                id: $(".playlist-title").attr('id'),
                name: $("#title").val(),
                description: $("#description").val()
            }
            await axios.post("/update-playlist", info)
            $(".playlist-title").text($("#title").val())
            $(".playlist-description").text($("#description").val())
            $("#description").text($("#description").val())
        }

        $("#update-playlist-form").hide()
        $("#playlist-info").show()
    })

    $("#cancel-btn").on("click", function(e) {
        e.preventDefault()
        $("#update-playlist-form").hide()
        $("#update-playlist-form").trigger('reset')
        $("#playlist-info").show()
    })
    

    $(".action-tab").on("click", function(e) {
        e.preventDefault()

        let type = ""
        if ($(this).parent().parent().parent().parent().hasClass("video")) {
            type = "video"
        }
        else if ($(this).parent().parent().parent().parent().hasClass("song")) {
            type = "song"
        }
        content["playlistId"] = $(".playlist-title").attr('id')
        content["id"] = $(this).parent().parent().parent().parent().attr('id')
        content["type"] = type


        let offset = $(this).offset()
        let left = offset.left

        if (offset.left + $("#actions").width() > screen.width) {
            left = offset.left - $("#actions").width() + $(this).width()
        }


        $("#actions").show()
        $("#actions").offset({top: offset.top + $(this).height(), left: left})

        $('.section').css("overflow-x", "hidden")
    })

    $("#yt-export").on("click", () => {
        $("#backdrop").show()
    })

    $("#spot-export").on("click", () => {
        $("#backdrop").show()
    })

    $("#del-btn").on("click", () => {
        $("#backdrop").show()
    })

    $("#delete-action").on("click", async function() {

        await axios.post("/remove", content)

        $(`#${content["id"]}`).remove()

        Object.keys(content).forEach((k) => { delete content[k] })

        if ($(".video").length === 0) {
            $("#no-videos").show()
        }

        if ($(".song").length === 0) {
            $("#no-songs").show()
        }

        if ($(".video").length === 0 && $(".song").length === 0) {
            $("#platform-btns").hide()
        }
    })

    $(document).on("click", function(e) {
        if ($(e.target).hasClass("action-tab")) {}
        else {
            $("#actions").hide()
            $('.section').css("overflow-x", "scroll")
        }
    })

    $(window).resize(function() {
        $("#actions").hide()
    })


});