
let dropZone = document.getElementById('drop_zone');
let dropZoneIcon = document.getElementById('drop_zone_icon');
let toast = document.getElementById('toast');

dropZone.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add('dragover');
    dropZoneIcon.textContent = '📂';
});

dropZone.addEventListener('dragleave', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('dragover');
    dropZoneIcon.textContent = '📁';
});

dropZone.addEventListener('drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('dragover');
    dropZoneIcon.textContent = '📁';
    
    let files = e.dataTransfer.files;
    let formData = new FormData();

    for (let i = 0; i < files.length; i++) {
        formData.append('file', files[i]);
    }

    let xhr = new XMLHttpRequest();
    xhr.open('POST', "./upload", true);

    xhr.onload = function() {
        if (xhr.status === 200) {
            window.alert("Archivos subidos correctamente");
            showToast('Archivo recibido correctamente');
            location.reload();
        } else {
            window.alert("Error al pasar los archivos");
            showToast('Error al subir el archivo.');
        }
    };

    xhr.send(formData);
});

function showToast(message) {
    toast.textContent = message;
    toast.className = 'show';
    setTimeout(function() { toast.className = toast.className.replace('show', ''); }, 3000);
}

function filterFiles() {
    const input = document.getElementById('file-search-input').value.toLowerCase();
    const fileList = document.getElementById('file-list');
    const files = fileList.getElementsByClassName('file-button');

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (file.textContent.toLowerCase().includes(input)) {
            file.style.display = "";
        } else {
            file.style.display = "none";
        }
    }
}