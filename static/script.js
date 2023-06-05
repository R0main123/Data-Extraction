function changeMessage(){
    document.getElementById('welcome-message').textContent="Le message a changé!";
}

document.addEventListener("DOMContentLoaded", function() {
    function handleFileSelect(evt){
    evt.stopPropagation();
    evt.preventDefault();

    var files = evt.dataTransfer.files;
    var formData = new FormData();  // N'oubliez pas de définir formData

    for(var i=0, f; f=files[i]; i++){
        formData.append('file[]',f,f.name);
    }

    fetch('/upload', {
    method: "POST",
    body: formData,
}).then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.text();
}).then(url => {
    window.location.href = url;  // Redirige vers l'URL renvoyée par le serveur
}).catch(e => {
    console.log('There was a problem with the fetch operation: ' + e.message);
});

}


    function handleDragOver(evt){
        evt.preventDefault();
        evt.stopPropagation();
        evt.dataTransfer.dropEffect='send';
    }

    var dropZone = document.getElementById("drop_zone");
    dropZone.addEventListener("dragover", handleDragOver,false)
    dropZone.addEventListener("drop", handleFileSelect,false)
});




