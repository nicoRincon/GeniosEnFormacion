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

  let updateModal = document.getElementById('topic-modal-update');
  if (updateModal) {
    updateModal.addEventListener('show.bs.modal', function (event) {
      let button = event.relatedTarget;
      let topicId = button.getAttribute('data-id');
      const url = BASE_EDIT_URL.replace('0', topicId);
      updateModal.querySelector('#edit-topic-form').setAttribute('action', url);

      $.ajax({
        url: url,
        type: 'GET',
        success: (data) => {
          updateModal.querySelector('#edit-topic-id').value = data.id;
          updateModal.querySelector('#edit-topic-name').value = data.topic_name;
          updateModal.querySelector('#edit-topic-description').value = data.topic_description;
          if (updateModal.querySelector('#edit-subject-id')) {
            updateModal.querySelector('#edit-subject-id').value = data.subject_id;
          }
        },
        error: (error) => {
          console.error('Error al obtener el tema: ', error);
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudo obtener la información del tema ' + error.message,
          });
        }
      });
    });
  }
}