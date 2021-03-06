$(document).ready(function () {
    
    $("#add-playlist-form").on("submit", async function() {
        let newPlaylist = {
            name: $("#playlist-name").val(),
            description: $("#desc").val()
        }
        await axios.post("/create-playlist", newPlaylist)
        location.reload()
    })

});