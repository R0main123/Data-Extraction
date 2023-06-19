let areMatricesVisible = {};


document.querySelector('#search-input').addEventListener('input', function(e) {
    const searchTerm = e.target.value;
    const wafers = Array.from(document.querySelectorAll('.wafer-block'));  // You have used the 'wafer-block' class in your HTML. Let's try selecting that.
    console.log(wafers);  // Let's print the wafers we've selected to check if it's correct.

    wafers.forEach(function(wafer) {
        const waferId = wafer.querySelector('.wafer-id').textContent;
        if (waferId.includes(searchTerm)) {
            wafer.style.display = '';
        } else {
            wafer.style.display = 'none';
        }
    });

    const visibleWafers = wafers.filter(wafer => wafer.style.display !== 'none');
    console.log('Total Wafers:', wafers.length);  // Print the total number of wafers.
    console.log('Visible Wafers:', visibleWafers.length);  // Print the number of visible wafers.

    const noResults = document.querySelector('#no-results');
    if (visibleWafers.length === 0) {
        noResults.style.display = '';
    } else {
        noResults.style.display = 'none';
    }
});

document.querySelectorAll('.excel-action-button').forEach((button) => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const waferId = e.target.parentElement.querySelector('.wafer-id').textContent;

        if (getSelectedStructures().length > 0) {
        // Demander le nom du fichier à l'utilisateur
        let fileName = prompt("Please enter the file name");

        // Faire une requête fetch à la nouvelle route Python
        fetch(`/excel_structure/${waferId}/${getSelectedStructures()}/${fileName}`)
            .then(res => {console.log(res); return res; })
            .then(response => response.json())
            //.then(data => console.log(data))
            .catch(error => console.error('Error:', error));
    } else {
        // Faire une requête fetch à l'ancienne route Python
        fetch(`/write_excel/${waferId}`)
            .then(response => response.json())
            //.then(data => console.log(data))
            .catch(error => console.error('Error:', error));
    }
    });
});

document.querySelectorAll('.powerpoint-action-button').forEach((button) => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const waferId = e.target.parentElement.querySelector('.wafer-id').textContent;

        if (getSelectedStructures().length > 0) {
        // Demander le nom du fichier à l'utilisateur
        let fileName = prompt("Please enter the file name");

        // Faire une requête fetch à la nouvelle route Python
        fetch(`/ppt_structure/${waferId}/${getSelectedStructures()}/${fileName}`)
            .then(res => {console.log(res); return res; })
            .then(response => response.json())
            //.then(data => console.log(data))
            .catch(error => console.error('Error:', error));
    } else {
        // Faire une requête fetch à l'ancienne route Python
        fetch(`/write_ppt/${waferId}`)
            .then(response => response.json())
            //.then(data => console.log(data))
            .catch(error => console.error('Error:', error));
    }
    });
});

document.querySelectorAll('.delete-action-button').forEach((button) => {
    button.addEventListener('click', function(e) {
        const waferId = e.target.parentElement.querySelector('.wafer-id').textContent;
        fetch('/delete_wafer/' + waferId, {
            method: 'DELETE',
        })
        .then(res => res.json())
        .then(data => {
            if (data.result === 'success') {
                // Remove the wafer element from the DOM
                e.target.parentElement.remove();
            } else {
                // Handle error
            }
        });
    });
});


function updateStructuresDisplaycoords(waferId, selectedMeasurements){

    fetch(`/filter_by_Coords/${waferId}`, {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ coords: selectedMeasurements }),
    })
        .then(response => response.json())
        .then(structuresToShow => {
            document.querySelectorAll('.structure-block').forEach(function (structure){
                structure.style.display = 'none';
            });

            setTimeout(() =>{
                structuresToShow.forEach(function (structureId){
                const structureElement = document.querySelector('.structure-block[data-structure-id="' + structureId + '"]');
                if(structureElement){
                    structureElement.style.display = '';
                }
            });
        }, 1000);
    });
}


function updateStructuresDisplaymeas(waferId, selectedMeasurements){
    fetch(`/filter_by_Meas/${waferId}/${selectedMeasurements.join(',')}`)
        .then(response => response.json())
        .then(structuresToShow => {
            document.querySelectorAll('.structure-block').forEach(function (structure){
                structure.style.display = 'none';
            });

            setTimeout(() =>{
                structuresToShow.forEach(function (structureId){
                const structureElement = document.querySelector('.structure-block[data-structure-id="' + structureId + '"]');
                if(structureElement){
                    structureElement.style.display = '';
                }
            });
        }, 1000);
    });
}


function updateStructuresDisplaytemp(waferId, selectedMeasurements){
    fetch(`/filter_by_Temps/${waferId}/${selectedMeasurements.join(',')}`)
        .then(response => response.json())
        .then(structuresToShow => {
            document.querySelectorAll('.structure-block').forEach(function (structure){
                structure.style.display = 'none';
            });

            setTimeout(() =>{
                structuresToShow.forEach(function (structureId){
                const structureElement = document.querySelector('.structure-block[data-structure-id="' + structureId + '"]');
                if(structureElement){
                    structureElement.style.display = '';
                }
            });
        }, 1000);
    });
}


function updateStructuresDisplayfiles(waferId, selectedMeasurements){
    fetch(`/filter_by_Filenames/${waferId}/${selectedMeasurements.join(',')}`)
        .then(response => response.json())
        .then(structuresToShow => {
            document.querySelectorAll('.structure-block').forEach(function (structure){
                structure.style.display = 'none';
            });

            setTimeout(() =>{
                structuresToShow.forEach(function (structureId){
                const structureElement = document.querySelector('.structure-block[data-structure-id="' + structureId + '"]');
                if(structureElement){
                    structureElement.style.display = '';
                }
            });
        }, 1000);
    });
}

function getSelectedStructures() {
  // Select all checked checkboxes
  const checkedCheckboxes = document.querySelectorAll('.structure-checkbox:checked');

  // Get the structure IDs from the checked checkboxes
  const selectedStructureIds = Array.from(checkedCheckboxes).map(checkbox => checkbox.dataset.structureId);

  // Return the selected structure IDs
  return selectedStructureIds;
}


document.querySelectorAll('.wafer-action-button').forEach((button) => {

    const structureList = document.createElement('ul');  // Create structure list
    button.dataset.showingStructures = "false";
    const filterMenu = document.createElement("div");
    button.addEventListener('click', function (e) {
        let areStructuresVisible = (this.dataset.showingStructures ==='true');  // Keep track of current state
        const waferId = e.target.parentElement.querySelector('.wafer-id').textContent;

        if (areStructuresVisible) {
            // If structures are visible, remove them
            structureList.innerHTML = '';
            filterMenu.innerHTML = '';

            this.dataset.showingStructures = 'false';
        } else {

            const waferId = e.target.parentElement.querySelector(".wafer-id").textContent;


            filterMenu.id = 'filter-menu';
            filterMenu.innerHTML = `
                <a href='#' id='reset-filters'>Reset filters</a>
                <div class='menu-parent'>
                    <a href='#' class='filter-by'>Filter by</a>
                    <ul class='filter-select'>
                        <li><a href='#' data-filter='measurement'>Type of Measurements</a><ul class='sous-menu'></ul></li>
                        <li><a href='#' data-filter='temperature'>Temperature</a><ul class='sous-menu'></ul></li>
                        <li><a href='#' data-filter='file-name'>Name of file</a><ul class='sous-menu'></ul></li>
                        <li><a href='#' data-filter='coordinates'>Coordinates</a><ul class='sous-menu'></ul></li>
                    </ul>
                </div>`;
            button.parentElement.appendChild(filterMenu);

            document.querySelector('#reset-filters').addEventListener('click', function(e) {
                e.preventDefault();

                // Désélectionner tous les filtres
                document.querySelectorAll('.sous-menu a.selected').forEach(function(a) {
                    a.classList.remove('selected');
                    a.textContent = a.textContent.replace(' ✔︎', '');
                });

                // Vider la liste selectedMeasurements
                selectedMeasurements = [];

                // Mettre à jour l'affichage des structures
                updateStructuresDisplay(waferId, selectedMeasurements);
            });


            let selectedMeasurements = [];

            filterMenu.querySelector("[data-filter='measurement']").addEventListener('mouseenter', function (e){
                const submenu = this.nextSibling;

                fetch(`/get_all_types/${waferId}`)
                    .then(response => response.json())
                    .then(measureTypes => {
                        console.log(measureTypes);
                        submenu.innerHTML='';

                        measureTypes.forEach(type => {
                            const li = document.createElement('li');
                            const a = document.createElement('a');
                            a.href="#";
                            a.dataset.filter = type;
                            a.textContent = type;

                            if (selectedMeasurements.includes(type)){
                                a.classList.add('selected');
                                a.textContent += " \u2714"
                            }

                            li.appendChild(a);
                            submenu.appendChild(li);
                        });

                       filterMenu.querySelectorAll('.sous-menu a').forEach((a)=>{
                            a.addEventListener('click', function (e){
                                e.preventDefault();
                                const filterValue = this.dataset.filter;

                                if (this.classList.contains('selected')){
                                    this.classList.remove('selected');
                                    this.textContent = this.textContent.replace("\u2714", "");

                                    const index = selectedMeasurements.indexOf(filterValue);
                                    if(index > -1){
                                        selectedMeasurements.splice(index, 1)
                                    }
                                } else {
                                    this.classList.add('selected');

                                    this.textContent += ("\u2714");

                                    selectedMeasurements.push(filterValue);
                                }

                                console.log("Selected filters: ", selectedMeasurements);

                                updateStructuresDisplaymeas(waferId, selectedMeasurements);
                            });
                        });
                    });
            });

            filterMenu.querySelector("[data-filter='temperature']").addEventListener('mouseenter', function (e){
                const submenu = this.nextSibling;

                fetch(`/get_all_temps/${waferId}`)
                    .then(response => response.json())
                    .then(measureTypes => {
                        console.log(measureTypes);
                        submenu.innerHTML='';

                        measureTypes.forEach(type => {
                            const li = document.createElement('li');
                            const a = document.createElement('a');
                            a.href="#";
                            a.dataset.filter = type;
                            a.textContent = type;

                            if (selectedMeasurements.includes(type)){
                                a.classList.add('selected');
                                a.textContent += " \u2714"
                            }

                            li.appendChild(a);
                            submenu.appendChild(li);
                        });

                        filterMenu.querySelectorAll('.sous-menu a').forEach((a)=>{
                            a.addEventListener('click', function (e){
                                e.preventDefault();
                                const filterValue = this.dataset.filter;

                                if (this.classList.contains('selected')){
                                    this.classList.remove('selected');
                                    this.textContent = this.textContent.replace("\u2714", "");

                                    const index = selectedMeasurements.indexOf(filterValue);
                                    if(index > -1){
                                        selectedMeasurements.splice(index, 1)
                                    }
                                } else {
                                    this.classList.add('selected');

                                    this.textContent += ("\u2714");

                                    selectedMeasurements.push(filterValue);
                                }

                                console.log("Selected filters: ", selectedMeasurements);

                                updateStructuresDisplaytemp(waferId, selectedMeasurements);
                            });
                        });
                    });
            });

            filterMenu.querySelector("[data-filter='file-name']").addEventListener('mouseenter', function (e){
                const submenu = this.nextSibling;

                fetch(`/get_all_filenames/${waferId}`)
                    .then(response => response.json())
                    .then(measureTypes => {
                        console.log(measureTypes);
                        submenu.innerHTML='';

                        measureTypes.forEach(type => {
                            const li = document.createElement('li');
                            const a = document.createElement('a');
                            a.href="#";
                            a.dataset.filter = type;
                            a.textContent = type;

                            if (selectedMeasurements.includes(type)){
                                a.classList.add('selected');
                                a.textContent += " \u2714"
                            }

                            li.appendChild(a);
                            submenu.appendChild(li);
                        });

                        filterMenu.querySelectorAll('.sous-menu a').forEach((a)=>{
                            a.addEventListener('click', function (e){
                                e.preventDefault();
                                const filterValue = this.dataset.filter;

                                if (this.classList.contains('selected')){
                                    this.classList.remove('selected');
                                    this.textContent = this.textContent.replace("\u2714", "");

                                    const index = selectedMeasurements.indexOf(filterValue);
                                    if(index > -1){
                                        selectedMeasurements.splice(index, 1)
                                    }
                                } else {
                                    this.classList.add('selected');

                                    this.textContent += ("\u2714");

                                    selectedMeasurements.push(filterValue);
                                }

                                console.log("Selected filters: ", selectedMeasurements);

                                updateStructuresDisplayfiles(waferId, selectedMeasurements);
                            });
                        });
                    });
            });

            filterMenu.querySelector("[data-filter='coordinates']").addEventListener('mouseenter', function (e){
                const submenu = this.nextSibling;

                fetch(`/get_all_coords/${waferId}`)
                    .then(response => response.json())
                    .then(measureTypes => {
                        console.log(measureTypes);
                        submenu.innerHTML='';

                        measureTypes.forEach(type => {
                            const li = document.createElement('li');
                            const a = document.createElement('a');
                            a.href="#";
                            a.dataset.filter = type;
                            a.textContent = type;

                            if (selectedMeasurements.includes(type)){
                                a.classList.add('selected');
                                a.textContent += " \u2714"
                            }

                            li.appendChild(a);
                            submenu.appendChild(li);
                        });

                        filterMenu.querySelectorAll('.sous-menu a').forEach((a)=>{
                            a.addEventListener('click', function (e){
                                e.preventDefault();
                                const filterValue = this.dataset.filter;

                                if (this.classList.contains('selected')){
                                    this.classList.remove('selected');
                                    this.textContent = this.textContent.replace("\u2714", "");

                                    const index = selectedMeasurements.indexOf(filterValue);
                                    if(index > -1){
                                        selectedMeasurements.splice(index, 1)
                                    }
                                } else {
                                    this.classList.add('selected');

                                    this.textContent += ("\u2714");

                                    selectedMeasurements.push(filterValue);
                                }

                                console.log("Selected filters: ", selectedMeasurements);

                                updateStructuresDisplaycoords(waferId, selectedMeasurements);
                            });
                        });
                    });
            });

            const selectAllButton = document.createElement('button');
            selectAllButton.textContent = "Select All";
            selectAllButton.id = 'select-all';
            selectAllButton.className='select-all';

            filterMenu.appendChild(selectAllButton); // Ajoutez le bouton sous le menu de filtres

            // Ajoutez un écouteur d'événements pour le bouton "Select All"
            selectAllButton.addEventListener('click', function(e) {
                e.preventDefault();
                const checkboxes = document.querySelectorAll('.structure-checkbox');
                // Vérifie si toutes les cases sont cochées
                const allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked);
                // Coche ou décoche toutes les cases en fonction de leur état actuel
                checkboxes.forEach(checkbox => {
                    checkbox.checked = !allChecked;
                });
            });

            // Si les structures ne sont pas visibles, les récupérer et les afficher
            fetch('/get_structures/' + waferId)
                .then(res => res.json())
                .then(data => {
                    // Clear any existing structures
                    structureList.innerHTML = '';

                    // Add each structure to the DOM
                    data.forEach((structure) => {
                        const structureElement = document.createElement('li');
                        structureElement.className = "structure-block";
                        structureElement.dataset.structureId = structure.structure_id;
                        structureElement.style.listStyleType = "decimal";
                        areMatricesVisible[structure.structure_id] = false;

                        // Create checkbox for each structure
                        const structureCheckbox = document.createElement('input');
                        structureCheckbox.type = 'checkbox';
                        structureCheckbox.classList.add('structure-checkbox');
                        structureCheckbox.dataset.structureId = structure.structure_id; // Add structure ID as data attribute
                        structureCheckbox.checked = true;

            // Append the checkbox to the structureElement
            structureElement.appendChild(structureCheckbox);

            const textElement = document.createElement('span');
            textElement.textContent = structure.structure_id;
            textElement.className = 'structure-id'; // So we can select it later
            structureElement.appendChild(textElement);

            const arrowElement = document.createElement('span');
            arrowElement.textContent = ' ▶';
            arrowElement.className = 'structure-arrow'; // So we can select it later
            structureElement.appendChild(arrowElement);

            const matrixList = document.createElement('ul');
            matrixList.className = 'matrix-list';
            structureElement.appendChild(matrixList);

            structureList.appendChild(structureElement);
        });

                    // Ici, ajoutez les gestionnaires d'événements pour chaque structure
                    document.querySelectorAll('.structure-block').forEach(function (structure) {
                        structure.addEventListener('click', async function () {
                            const structureId = this.dataset.structureId;
                            const matrixList = this.querySelector('.matrix-list');
                            const arrowElement = this.querySelector('.structure-arrow');

                            if (areMatricesVisible[structureId]) {
                                matrixList.innerHTML = '';
                                arrowElement.textContent = ' ▶';
                            } else {
                                const waferId = this.closest('.wafer-block').dataset.waferId;
                                const response = await fetch(`/get_matrices/${waferId}/${structureId}`);
                                const matrices = await response.json();

                                matrixList.innerHTML = '';

                                for (let matrix of matrices) {
                                    const matrixBlock = document.createElement('li');
                                    matrixBlock.className = 'matrix-block';
                                    matrixBlock.textContent = `(${matrix.coordinates.x},${matrix.coordinates.y})`;
                                    matrixBlock.style.listStyleType = "decimal";
                                    matrixBlock.addEventListener('click', function(e){
                                        if(e.target && e.target.nodeName == 'LI'){
                                            const matrixId = e.target.dataset.matrixId;
                                            showPlots(`${waferId}`,`${matrixBlock.textContent}`)
                                            //window.open(`/plot_matrix/${waferId}/${matrixId}`)
                                        }
                                    })
                                    matrixList.appendChild(matrixBlock);
                                }

                                arrowElement.textContent = ' ▼';
                            }

                            areMatricesVisible[structureId] = !areMatricesVisible[structureId];
                        });
                    });
                });

            // Toggle state
            this.dataset.showingStructures = 'true';
        };

        // Add structure list to wafer block
        button.parentElement.appendChild(structureList);
    });
});



var modal = document.createElement('div');
modal.id = 'myModal';
modal.className = 'modal';

var modalContent = document.createElement('div');
modalContent.className = 'modal-content';

var span = document.createElement('span');
span.className = 'close';
span.textContent = '\u00D7'; // Code du caractère 'x'


modalContent.appendChild(span);
modal.appendChild(modalContent);

document.body.appendChild(modal);

span.onclick = function() {
  modal.style.display = 'none';
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = 'none';
  }
}

function showModalWithImage(imgSrc) {
  // Créer l'élément img
  var img = document.createElement('img');
  img.src = imgSrc;

  modalContent.appendChild(img);

  modal.style.display = 'block';
}

function showPlots(waferId, coordinates) {
    fetch(`/plot_matrix/${waferId}/${coordinates}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        // Ajoute chaque nouveau plot à la nouvelle fenêtre
        data.forEach((pngBase64) => {
            const img = document.createElement('img');
            showModalWithImage(`data:image/png;base64,${pngBase64}`);
        })
    });
}
