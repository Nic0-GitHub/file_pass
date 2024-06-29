
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

    var files = e.dataTransfer.files;
    var formData = new FormData();

    for (var i = 0; i < files.length; i++) {
        formData.append('file', files[i]);
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', "{{ url_for('upload_file') }}", true);

    xhr.onload = function() {
        if (xhr.status === 200) {
            showToast('Archivo recibido correctamente');
            location.reload();
        } else {
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
