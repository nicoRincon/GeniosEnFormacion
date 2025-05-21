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

  let updateModal = document.getElementById('role-modal-update');
  if (updateModal) {
    updateModal.addEventListener('show.bs.modal', function (event) {
      let button = event.relatedTarget;
      let roleId = button.getAttribute('data-id');
      const url = BASE_EDIT_URL.replace('0', roleId);
      updateModal.querySelector('#edit-role-form').setAttribute(
        'action', url
      );

      $.ajax({
        url: url,
        type: 'GET',
        success: (data) => {
          updateModal.querySelector('#edit-role-id').value = data.id;
          updateModal.querySelector('#edit-role-name').value = data.role_name;
        },
        error: (error) => {
          console.error('Error al obtener el rol: ', error);
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudo obtener la información del rol ' + error.message,
          });
        }
      });
    });
  }
}