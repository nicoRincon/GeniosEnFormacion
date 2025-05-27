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

  let updateModal = document.getElementById('activity-modal-update');
  if (updateModal) {
    updateModal.addEventListener('show.bs.modal', function (event) {
      let button = event.relatedTarget;
      let activityId = button.getAttribute('data-id');
      const url = BASE_EDIT_URL.replace('0', activityId);
      updateModal.querySelector('#edit-activity-form').setAttribute('action', url);

      $.ajax({
        url: url,
        type: 'GET',
        success: (data) => {
          updateModal.querySelector('#edit-activity-id').value = data.id;
          if (updateModal.querySelector('#edit-content-id')) {
            updateModal.querySelector('#edit-content-id').value = data.content_id;
          }
          if (updateModal.querySelector('#edit-activity-type-id')) {
            updateModal.querySelector('#edit-activity-type-id').value = data.activity_type_id;
          }
          updateModal.querySelector('#edit-content').value = data.content;
        },
        error: (error) => {
          console.error('Error al obtener la actividad: ', error);
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudo obtener la información de la actividad ' + error.message,
          });
        }
      });
    });
  }
}