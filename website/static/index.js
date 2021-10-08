function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/úkoly";
    });
}

function deleteSched(schedId) {
    fetch("/delete-sched", {
        method: "POST",
        body: JSON.stringify({ schedId: schedId }),
    }).then((_res) => {
        window.location.href = "/admin";
    });
}

function playsound(number) {
    var sound = document.getElementById('file' + number);
    sound.play();
}
var d = new Date();
document.getElementById('date').innerHTML = "Today is: " + d.getDate() + "." + d.getMonth() + ".";
document.getElementById('col').onclick = function change_col() {
    const color = "#FFFFFF"
    fetch("/change-color", {
        method: "POST",
        body: JSON.stringify({ color }),
    }).then((_res) => {
        window.location.href = "/";
    });
};