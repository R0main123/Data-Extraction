document.addEventListener('DOMContentLoaded', function() {
    let dropZone = document.getElementById('drop_zone');

    // Prevent default behavior when file is dragged over drop zone
    dropZone.ondragover = function(event) {
        event.preventDefault();
    };

    // Handle dropped files
    dropZone.ondrop = function(event) {
        event.preventDefault();

        let files = event.dataTransfer.files;

        let formData = new FormData();
        let processedFiles = [];
        for (let i = 0; i < files.length; i++) {
            let file = files[i];
            let filename = file.name;

            let temperature = prompt('Please enter the temperature for file ' + filename);

            // Si le nom du fichier ne commence pas par "AL", demandez à l'utilisateur d'entrer lot_id et wafer_id
            if (!filename.startsWith('AL')) {
                let lot_id = prompt('Please enter the lot ID for file ' + filename);
                let wafer_id = prompt('Please enter the wafer ID for file ' + filename);

                // Ajoutez lot_id et wafer_id à formData pour les envoyer au serveur
                formData.append('lot_id', lot_id);
                formData.append('wafer_id', wafer_id);

                // Changez le nom du fichier pour lot_idwafer_id.extension
                let extension = filename.split('.').pop();
                filename = filename.substring(0, filename.lastIndexOf(".")) + '@@@' +lot_id + '_' +wafer_id + "_" + temperature + '.' + extension;
                let newFile = new File([file], filename, {type: file.type});

                processedFiles.push(newFile);
            } else {
                // Pour les fichiers commençant par "AL", ajoutez simplement la température
                let extension = filename.split('.').pop();
                let nameWithoutExtension = filename.substring(0, filename.lastIndexOf("."));
                filename = nameWithoutExtension + "_" + temperature + '.' + extension;
                let newFile = new File([file], filename, {type: file.type});

                processedFiles.push(newFile);
            }
        }

        for (let i = 0; i < processedFiles.length; i++) {
            formData.append('file', processedFiles[i]);
        }

        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                window.location = "/options";
            } else {
                console.error('Upload failed');
            }
        });
    };
});





