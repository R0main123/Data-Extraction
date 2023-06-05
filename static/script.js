function changeMessage(){
    document.getElementById('welcome-message').textContent="Le message a changé!";
}

function handleFileSelect(evt){
    evt.stopPropagation();
    evt.preventDefault();

    var files = evt.dataTransfer.files;

    for(var i=0, f; f=files[i]; i++){
        formData.append('file[]',f,f.name);
    }

    fetch('/upload',{
        method: "POST",
        body:formData
    }).then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.text();
    }).then(data => {
        console.log(data);
    }).catch(e=>{
        console.log('There was a problem with the fetch operation: '+e.message);
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





