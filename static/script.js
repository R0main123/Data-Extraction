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
        for (let i = 0; i < files.length; i++) {
            formData.append('file', files[i]);
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
