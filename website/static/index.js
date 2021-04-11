function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/úkoly";
    });
}

function hello(num) {
    leguan = num * 2
    console.log("HEllo world! " + "2 * " + num + " = " + leguan);
}

function playsound(number) {
    var sound = document.getElementById('file' + number);
    sound.play();
}