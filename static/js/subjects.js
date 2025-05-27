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

  let updateModal = document.getElementById('subject-modal-update');
  if (updateModal) {
    updateModal.addEventListener('show.bs.modal', function (event) {
      let button = event.relatedTarget;
      let subjectId = button.getAttribute('data-id');
      const url = BASE_EDIT_URL.replace('0', subjectId);
      updateModal.querySelector('#edit-subject-form').setAttribute('action', url);

      $.ajax({
        url: url,
        type: 'GET',
        success: (data) => {
          updateModal.querySelector('#edit-subject-id').value = data.id;
          updateModal.querySelector('#edit-subject-name').value = data.subject_name;
          updateModal.querySelector('#edit-subject-description').value = data.subject_description;
        },
        error: (error) => {
          console.error('Error al obtener la materia: ', error);
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudo obtener la información de la materia ' + error.message,
          });
        }
      });
    });
  }
}