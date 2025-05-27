window.onload = () => {
  if (ERROR) {
    Swal.fire({
      title: '¡Error!',
      text: ERROR,
      icon: 'error',
      confirmButtonText: 'Ok'
    });
  }

  if (MESSAGE) {
    Swal.fire({
      title: '¡Exito!',
      text: MESSAGE,
      icon: 'success',
      confirmButtonText: 'Ok'
    });
  }

  let updateModal = document.getElementById('content-modal-update');
  if (updateModal) {
    updateModal.addEventListener('show.bs.modal', function (event) {
      let button = event.relatedTarget;
      let contentId = button.getAttribute('data-id');
      const url = BASE_EDIT_URL.replace('0', contentId);
      updateModal.querySelector('#edit-content-form').setAttribute('action', url);

      $.ajax({
        url: url,
        type: 'GET',
        success: (data) => {
          updateModal.querySelector('#edit-content-id').value = data.id;
          updateModal.querySelector('#edit-content-name').value = data.content_name;
          updateModal.querySelector('#edit-content-description').value = data.content_description;
          updateModal.querySelector('#edit-grade-level').value = data.grade_level;
          if (updateModal.querySelector('#edit-topic-id')) {
            updateModal.querySelector('#edit-topic-id').value = data.topic_id;
          }
        },
        error: (error) => {
          console.error('Error al obtener el contenido: ', error);
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudo obtener la información del contenido ' + error.message,
          });
        }
      });
    });
  }
}