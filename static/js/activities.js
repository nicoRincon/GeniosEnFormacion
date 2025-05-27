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
      title: '¡Éxito!',
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
          updateModal.querySelector('#edit-content-id').value = data.content_id;

          if (data.questions_json) {
            loadQuestionsFromJson('update', data.questions_json);
          }
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

  // Para crear
  initQuestionsForm('create');
  // Para editar
  initQuestionsForm('update');

  function initQuestionsForm(formPrefix) {
    const questionsList = document.getElementById(`questions-list-${formPrefix}`);
    const addQuestionBtn = document.getElementById(`add-question-${formPrefix}`);
    const questionTemplate = document.getElementById(`question-template-${formPrefix}`).content;
    // Inicializa con una pregunta
    addQuestion(true);

    function createOptionItem(value = '') {
      const div = document.createElement('div');
      div.className = 'input-group mb-2 option-item';
      div.innerHTML = `
            <input type="text" class="form-control option-input" placeholder="Opción" value="${value}" required>
            <button type="button" class="btn btn-outline-danger remove-option" title="Eliminar opción">&times;</button>
        `;
      return div;
    }

    function updateCorrectOptions(questionCard) {
      const optionsList = questionCard.querySelector('.options-list');
      const correctOptionsList = questionCard.querySelector('.correct-options-list');
      correctOptionsList.innerHTML = '';
      const optionInputs = optionsList.querySelectorAll('.option-input');
      optionInputs.forEach((input, _) => {
        const value = input.value;
        const id = 'correct-option-' + Math.random().toString(36).slice(2, 11);
        const div = document.createElement('div');
        div.className = 'form-check';
        div.innerHTML = `
                <input class="form-check-input" type="checkbox" value="${value}" id="${id}" name="correct_options">
                <label class="form-check-label" for="${id}">${value || '(vacío)'}</label>
            `;
        correctOptionsList.appendChild(div);
      });
    }

    function addQuestion(initial = false) {
      const questionCard = document.importNode(questionTemplate, true).children[0];

      // Asigna un name único a los radios de tipo de pregunta
      const radios = questionCard.querySelectorAll('.type-question-radio');
      const radioName = 'type_question_' + Math.random().toString(36).slice(2, 11);
      radios.forEach(radio => radio.name = radioName);

      // Opciones
      const optionsList = questionCard.querySelector('.options-list');
      const addOptionBtn = questionCard.querySelector('.add-option');
      const optionsContainer = questionCard.querySelector('.options-container');
      const correctOptionsContainer = questionCard.querySelector('.correct-options-container');
      const openEndedContainer = questionCard.querySelector('.correct-text');

      // Inicializa con 3 opciones
      for (let i = 0; i < 3; i++) {
        optionsList.appendChild(createOptionItem());
      }
      updateCorrectOptions(questionCard);

      optionsList.addEventListener('input', () => updateCorrectOptions(questionCard));
      optionsList.addEventListener('change', () => updateCorrectOptions(questionCard));
      optionsList.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-option')) {
          e.target.closest('.option-item').remove();
          updateCorrectOptions(questionCard);
        }
      });
      addOptionBtn.addEventListener('click', function () {
        optionsList.appendChild(createOptionItem());
        updateCorrectOptions(questionCard);
      });

      // Mostrar/ocultar según tipo de pregunta
      function updateVisibility() {
        const selected = questionCard.querySelector('.type-question-radio:checked').value;
        if (selected === 'open') {
          optionsContainer.style.display = 'none';
          correctOptionsContainer.style.display = 'none';
          openEndedContainer.style.display = '';
        } else {
          optionsContainer.style.display = '';
          correctOptionsContainer.style.display = '';
          openEndedContainer.style.display = 'none';
        }
      }
      radios.forEach(radio => {
        radio.addEventListener('change', updateVisibility);
      });
      updateVisibility();

      // Eliminar pregunta
      questionCard.querySelector('.remove-question').addEventListener('click', function () {
        questionCard.remove();
      });

      questionsList.appendChild(questionCard);
    }

    addQuestionBtn.addEventListener('click', function () {
      addQuestion();
    });

    const btnSave = document.getElementsByClassName('save-data-modal');
    if (btnSave) {
      for (const element of btnSave) {
        element.addEventListener('click', async (event) => {
          event.preventDefault();
          await createJsonData();
          event.target.closest('.modal').querySelector('form').submit();
        });
      }
    }

    async function createJsonData() {
      const questions = [];
      questionsList.querySelectorAll('.question-item').forEach(questionCard => {
        const title = questionCard.querySelector('.question-title').value;
        const type = questionCard.querySelector('.type-question-radio:checked').value;
        let options = [];
        let correctOptions = [];
        let openEndedResponse = '';
        let isMultipleSelection = false;
        let canBeOpenEnded = false;

        if (type === 'multiple' || type === 'single') {
          options = Array.from(questionCard.querySelectorAll('.option-input')).map(i => i.value).filter(Boolean);
          correctOptions = Array.from(
            questionCard.querySelectorAll('.correct-options-list input[type=checkbox]:checked')
          ).map(i => i.value);
          isMultipleSelection = (type === 'multiple');
        }
        if (type === 'open') {
          openEndedResponse = questionCard.querySelector('.open-ended-response input').value;
          canBeOpenEnded = true;
        }

        questions.push({
          title,
          options,
          correct_options: correctOptions,
          is_multiple_selection: isMultipleSelection,
          can_be_open_ended: canBeOpenEnded,
          open_ended_response: openEndedResponse
        });
      });
      const jsonString = JSON.stringify(questions, null, 2);

      const questionsJsonInput = document.getElementById(`questions-json-${formPrefix}`);
      questionsJsonInput.value = jsonString;
    }
  }
}

function loadQuestionsFromJson(formPrefix, questionsJson) {
  const questionsList = document.getElementById(`questions-list-${formPrefix}`);
  const questionTemplate = document.getElementById(`question-template-${formPrefix}`).content;

  // Limpia preguntas existentes
  questionsList.innerHTML = '';

  if (!questionsJson) return;

  let questions;
  try {
    questions = typeof questionsJson === 'string' ? JSON.parse(questionsJson) : questionsJson;
  } catch (e) {
    console.error('JSON inválido:', e);
    return;
  }

  questions.forEach(q => {
    const questionCard = document.importNode(questionTemplate, true).children[0];

    // Asigna un nombre único a los radios
    const radios = questionCard.querySelectorAll('.type-question-radio');
    const radioName = 'type_question_' + Math.random().toString(36).slice(2, 11);
    radios.forEach(radio => radio.name = radioName);

    // Título
    questionCard.querySelector('.question-title').value = q.title || '';

    // Tipo de pregunta
    if (q.can_be_open_ended) {
      questionCard.querySelector('.type-question-radio[value="open"]').checked = true;
    } else if (q.is_multiple_selection) {
      questionCard.querySelector('.type-question-radio[value="multiple"]').checked = true;
    } else {
      questionCard.querySelector('.type-question-radio[value="single"]').checked = true;
    }

    // Opciones
    const optionsList = questionCard.querySelector('.options-list');
    optionsList.innerHTML = '';
    if (q.options && q.options.length) {
      q.options.forEach(opt => {
        const div = document.createElement('div');
        div.className = 'input-group mb-2 option-item';
        div.innerHTML = `
          <input type="text" class="form-control option-input" placeholder="Opción" value="${opt}" required>
          <button type="button" class="btn btn-outline-danger remove-option" title="Eliminar opción">&times;</button>
        `;
        optionsList.appendChild(div);
      });
    } else {
      // Si no hay opciones, agrega 3 vacías por defecto
      for (let i = 0; i < 3; i++) {
        const div = document.createElement('div');
        div.className = 'input-group mb-2 option-item';
        div.innerHTML = `
          <input type="text" class="form-control option-input" placeholder="Opción" value="" required>
          <button type="button" class="btn btn-outline-danger remove-option" title="Eliminar opción">&times;</button>
        `;
        optionsList.appendChild(div);
      }
    }

    // Opciones correctas
    const correctOptionsList = questionCard.querySelector('.correct-options-list');
    correctOptionsList.innerHTML = '';
    if (q.options && q.options.length) {
      q.options.forEach(opt => {
        const id = 'correct-option-' + Math.random().toString(36).slice(2, 11);
        const checked = q.correct_options && q.correct_options.includes(opt) ? 'checked' : '';
        const div = document.createElement('div');
        div.className = 'form-check';
        div.innerHTML = `
          <input class="form-check-input" type="checkbox" value="${opt}" id="${id}" name="correct_options" ${checked}>
          <label class="form-check-label" for="${id}">${opt || '(vacío)'}</label>
        `;
        correctOptionsList.appendChild(div);
      });
    }

    // Respuesta abierta
    questionCard.querySelector('.open-ended-response input').value = q.open_ended_response || '';

    // Mostrar/ocultar según tipo
    function updateVisibility() {
      const selected = questionCard.querySelector('.type-question-radio:checked').value;
      const optionsContainer = questionCard.querySelector('.options-container');
      const correctOptionsContainer = questionCard.querySelector('.correct-options-container');
      const openEndedContainer = questionCard.querySelector('.correct-text');
      if (selected === 'open') {
        optionsContainer.style.display = 'none';
        correctOptionsContainer.style.display = 'none';
        openEndedContainer.style.display = '';
      } else {
        optionsContainer.style.display = '';
        correctOptionsContainer.style.display = '';
        openEndedContainer.style.display = 'none';
      }
    }
    radios.forEach(radio => {
      radio.addEventListener('change', updateVisibility);
    });
    updateVisibility();

    // Listeners para opciones dinámicas
    optionsList.addEventListener('input', () => {
      // Actualiza las opciones correctas al cambiar las opciones
      correctOptionsList.innerHTML = '';
      Array.from(optionsList.querySelectorAll('.option-input')).forEach(input => {
        const value = input.value;
        const id = 'correct-option-' + Math.random().toString(36).slice(2, 11);
        const checked = q.correct_options && q.correct_options.includes(value) ? 'checked' : '';
        const div = document.createElement('div');
        div.className = 'form-check';
        div.innerHTML = `
          <input class="form-check-input" type="checkbox" value="${value}" id="${id}" name="correct_options" ${checked}>
          <label class="form-check-label" for="${id}">${value || '(vacío)'}</label>
        `;
        correctOptionsList.appendChild(div);
      });
    });

    optionsList.addEventListener('click', function (e) {
      if (e.target.classList.contains('remove-option')) {
        e.target.closest('.option-item').remove();
        // Actualiza las opciones correctas al eliminar
        correctOptionsList.innerHTML = '';
        Array.from(optionsList.querySelectorAll('.option-input')).forEach(input => {
          const value = input.value;
          const id = 'correct-option-' + Math.random().toString(36).slice(2, 11);
          const checked = q.correct_options && q.correct_options.includes(value) ? 'checked' : '';
          const div = document.createElement('div');
          div.className = 'form-check';
          div.innerHTML = `
            <input class="form-check-input" type="checkbox" value="${value}" id="${id}" name="correct_options" ${checked}>
            <label class="form-check-label" for="${id}">${value || '(vacío)'}</label>
          `;
          correctOptionsList.appendChild(div);
        });
      }
    });

    questionCard.querySelector('.add-option').addEventListener('click', function () {
      const div = document.createElement('div');
      div.className = 'input-group mb-2 option-item';
      div.innerHTML = `
        <input type="text" class="form-control option-input" placeholder="Opción" value="" required>
        <button type="button" class="btn btn-outline-danger remove-option" title="Eliminar opción">&times;</button>
      `;
      optionsList.appendChild(div);
      // Actualiza las opciones correctas al agregar
      correctOptionsList.innerHTML = '';
      Array.from(optionsList.querySelectorAll('.option-input')).forEach(input => {
        const value = input.value;
        const id = 'correct-option-' + Math.random().toString(36).slice(2, 11);
        const checked = q.correct_options && q.correct_options.includes(value) ? 'checked' : '';
        const div = document.createElement('div');
        div.className = 'form-check';
        div.innerHTML = `
          <input class="form-check-input" type="checkbox" value="${value}" id="${id}" name="correct_options" ${checked}>
          <label class="form-check-label" for="${id}">${value || '(vacío)'}</label>
        `;
        correctOptionsList.appendChild(div);
      });
    });

    // Eliminar pregunta
    questionCard.querySelector('.remove-question').addEventListener('click', function () {
      questionCard.remove();
    });

    questionsList.appendChild(questionCard);
  });
}