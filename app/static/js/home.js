$(document).ready(function () {
    
    let content = {}
    let id = ""
    let cardClass = ""
    let actionTab = $(".action-tab")
    let addAction = $("#add-action")
    let createBtn = $("#create-playlist-btn")
    let addForm = $("#add-form")
    let createForm = $("#create-form")



    actionTab.on("click", function(e) {
        e.preventDefault()
        id = $(this).parent().parent().parent().parent().attr('id')
        cardClass = $(this).parent().parent().parent().parent().attr('class')

        content["id"] = id
        content["img"] = $(this).parent().parent().siblings(".card-img-top").attr('src')
        content["title"] = $(this).siblings(".content-holder").find(".card-title").text()
        if ($(this).siblings(".content-holder").find(".card-text").hasClass("channel")) {
            content["channel"] = $(this).siblings(".content-holder").find(".channel").text()
        }
        else if ($(this).siblings(".content-holder").find(".card-text").hasClass("artist")) {
            content["artist"] = $(this).siblings(".content-holder").find(".artist").text()
        }
        content["title"] = $(this).siblings(".content-holder").find(".card-title").text()
        
        let offset = $(this).offset()
        let left = offset.left

        if (offset.left + $("#actions").width() > screen.width) {
            left = offset.left - $("#actions").width() + $(this).width()
        }
        
        $("#actions").show()
        $("#actions").offset({top: offset.top + $(this).height(), left: left})

        $('.section').css("overflow", "hidden")
        $('.col-section').css("overflow-y", "hidden")
        
    })

    addAction.on("click", function() {
        $(".modal").modal('show')
    })

    createBtn.on("click", function() {
        createForm.css("display", "flex")
        createBtn.hide()
    })

    $(".modal").on("hidden.bs.modal", () => {
        createForm.hide()
        addForm.trigger("reset")
        $("#add-btn").prop("disabled", true)
    })

    let newPLName = ""
    let checked = 0

    $(".modal").on("shown.bs.modal", () => {

        createBtn.show()
        
        $('#playlist-name').on("input", function() {
            newPLName = $('#playlist-name').val()
            if ($.trim(newPLName).length > 0 || checked > 0) {
                $("#add-btn").prop("disabled", false)
            }
            else {
                $("#add-btn").prop("disabled", true)
            }
        })
        $(".playlist-check").on("click", () => {
            checked = $(".playlist-check:checked").length
            if ($.trim(newPLName).length > 0 || checked > 0) {
                $("#add-btn").prop("disabled", false)
            }
            else {
                $("#add-btn").prop("disabled", true)
            }
        })
        
        
    })

    addForm.on("submit", async function(e) {
        e.preventDefault()
        let playlists = []
        if ($(".playlist-check:checked").length > 0) {
            $(".playlist-check:checked").each(function() {
                console.log(this.id)
                playlists.push(this.id)
            })
        }
        if ($.trim($("#playlist-name").val()).length > 0) {
            let newPlaylist = {
                name: $("#playlist-name").val(),
                description: $("#desc").val()
            }
            let newPL = await axios.post("/create-playlist", newPlaylist)

            playlists.push(newPL.data)

            $(`<div class="form-check">
                    <input class="form-check-input playlist-check" type="checkbox" value="" id=${newPL.data}>
                    <label class="form-check-label" for=${newPL.data}>
                        ${newPlaylist.name}
                    </label>
                </div>`).appendTo("#existing-playlists")

        }

        let type = ""

        if (cardClass.includes("video")) {
            type = "video"
        }
        else if (cardClass.includes("song")) {
            type = "song"
        }
        else {
            $(".modal").modal('hide')
            createForm.hide()
            return
        }

        let info = {
            content: content,
            type: type,
            playlists: playlists
        }


        await axios.post("/add", info)

        
        Object.keys(content).forEach((k) => { delete content[k] })
        cardClass = ""


        $(".modal").modal('hide')
        createForm.hide()
    })

    $(document).on("click", function(e) {
        if ($(e.target).hasClass("action-tab")) {}
        else {
            $("#actions").hide()
            $('.section').css("overflow", "scroll")
        }
    })

    $(window).resize(function() {
        $("#actions").hide()
      })

});