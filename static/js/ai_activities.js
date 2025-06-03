$(document).ready(function() {
    // URLs para las peticiones AJAX
    const GENERATE_ACTIVITIES_URL = "recommended_activity_by_user";
    const SUBMIT_ACTIVITY_URL = "submit_ai_activity";

    // Cargar actividades al iniciar la página
    loadExistingActivities();

    // Event listener para generar nuevas actividades
    $('#generate-activities-btn').on('click', function() {
        generateActivities();
    });

    function loadExistingActivities() {
        // Aquí podrías cargar actividades existentes si las tienes guardadas
        // Por ahora mostraremos el empty state
        showEmptyState();
    }

    function generateActivities() {
        showLoading();
        hideEmptyState();

        $.ajax({
            url: GENERATE_ACTIVITIES_URL,
            method: 'GET',
            dataType: 'json',
            timeout: 30000, // 30 segundos timeout
            success: function(data) {
                hideLoading();
                if (data.success && data.contents_with_activities) {
                    renderActivities(data.contents_with_activities);
                } else {
                    showError('No se pudieron generar actividades: ' + (data.error || 'Error desconocido'));
                }
            },
            error: function(xhr, status, error) {
                hideLoading();
                console.error('Error generando actividades:', error);
                showError('Error al conectar con el servidor. Por favor, intenta de nuevo.');
            }
        });
    }

    function renderActivities(activitiesData) {
        const container = $('#activities-container');
        container.empty();

        if (!activitiesData || activitiesData.length === 0) {
            showEmptyState();
            return;
        }

        activitiesData.forEach((item, index) => {
            const activityHtml = createActivityCard(item, index);
            container.append(activityHtml);
        });

        // Agregar event listeners después de crear las actividades
        attachActivityEventListeners();
    }

    function createActivityCard(item, index) {
        const activities = item.activities_suggested;
        const contentInfo = activities.content_info;
        const questions = activities.activity_data_json || [];

        const successPercentage = Math.round(item.prob_aprobar * 100);
        const scorePercentage = Math.round(item.score * 100);

        let questionsHtml = '';
        questions.forEach((question, qIndex) => {
            questionsHtml += createQuestionHtml(question, qIndex + 1, index);
        });

        return `
        <div class="activity-recommendation-card" data-content-id="${item.id_contenido}" data-activity-index="${index}">
            <div class="recommendation-header">
                <div class="recommendation-title">
                    📚 ${contentInfo.titulo}
                </div>
                <div class="d-flex flex-wrap gap-2 mb-2">
                    <span class="badge bg-light text-dark">${contentInfo.materia}</span>
                    <span class="badge bg-light text-dark">${contentInfo.tema}</span>
                    <span class="badge bg-light text-dark">Grado ${contentInfo.nivel_grado}</span>
                </div>
                <p class="mb-0 opacity-90">${contentInfo.contenido}</p>
                
                <div class="recommendation-stats">
                    <div class="stat-item">
                        <span class="stat-value">${successPercentage}%</span>
                        <div class="stat-label">Probabilidad de éxito</div>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">${item.nivel_grado}</span>
                        <div class="stat-label">Nivel recomendado</div>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">${scorePercentage}%</span>
                        <div class="stat-label">Puntuación IA</div>
                    </div>
                </div>
            </div>
            
            <div class="activity-content">
                <form class="activity-form" data-activity-index="${index}">
                    ${questionsHtml}
                </form>
            </div>
            
            <div class="activity-actions">
                <button type="button" class="btn btn-ai-primary me-3 submit-activity-btn" data-activity-index="${index}">
                    <i class="fas fa-paper-plane me-2"></i>
                    Enviar Respuestas
                </button>
                <button type="button" class="btn btn-ai-secondary reset-activity-btn" data-activity-index="${index}">
                    <i class="fas fa-redo me-2"></i>
                    Reiniciar
                </button>
            </div>
            
            <div class="activity-result" id="result-${index}">
                <!-- Los resultados se mostrarán aquí -->
            </div>
        </div>
        `;
    }

    function createQuestionHtml(question, questionNumber, activityIndex) {
        const questionId = `activity_${activityIndex}_question_${questionNumber}`;
        
        let questionHtml = `
        <div class="question-card" data-question-type="${question.type}">
            <span class="question-type-badge ${question.type}">${question.type === 'multiple' ? 'Selección Múltiple' : 'Respuesta Abierta'}</span>
            <div class="d-flex align-items-start">
                <span class="question-number">${questionNumber}</span>
                <div class="flex-grow-1">
                    <h5 class="question-title">${question.question}</h5>
        `;

        if (question.type === 'multiple') {
            questionHtml += '<div class="options-container">';
            question.options.forEach((option, optIndex) => {
                const optionId = `${questionId}_option_${optIndex}`;
                const optionLetter = String.fromCharCode(65 + optIndex); // A, B, C, D
                
                questionHtml += `
                <div class="option-item" data-option-value="${option}">
                    <input type="radio" 
                           id="${optionId}" 
                           name="${questionId}" 
                           value="${option}"
                           data-correct="${question.correct_answer.includes(option)}"
                           style="display: none;">
                    <label for="${optionId}" class="w-100 d-flex align-items-center m-0 cursor-pointer">
                        <span class="option-letter">${optionLetter}</span>
                        <span class="option-text">${option}</span>
                        <span class="option-feedback">
                            <i class="fas fa-check"></i>
                            <i class="fas fa-times"></i>
                        </span>
                    </label>
                </div>
                `;
            });
            questionHtml += '</div>';
            
            // Agregar explicación
            if (question.explanation) {
                questionHtml += `
                <div class="explanation-box" id="explanation_${questionId}">
                    <div class="explanation-content">
                        <strong>Explicación:</strong><br>
                        ${question.explanation}
                    </div>
                </div>
                `;
            }
        } else if (question.type === 'open') {
            questionHtml += `
            <div class="open-question-container">
                <textarea 
                    id="${questionId}"
                    name="${questionId}"
                    class="open-question-area"
                    placeholder="Escribe tu respuesta aquí..."
                    rows="4"></textarea>
                <small class="text-muted mt-2 d-block">
                    <i class="fas fa-lightbulb me-1"></i>
                    ${question.evaluation_criteria || 'Explica tu respuesta con detalles y ejemplos.'}
                </small>
            </div>
            `;
            
            // Mostrar respuesta esperada como guía
            if (question.sample_answer) {
                questionHtml += `
                <div class="explanation-box" id="explanation_${questionId}">
                    <div class="explanation-content">
                        <strong>Ejemplo de respuesta esperada:</strong><br>
                        ${question.sample_answer}
                    </div>
                </div>
                `;
            }
        }

        questionHtml += `
                </div>
            </div>
        </div>
        `;

        return questionHtml;
    }

    function attachActivityEventListeners() {
        // Event listeners para seleccionar opciones
        $('.option-item').off('click').on('click', function() {
            const radio = $(this).find('input[type="radio"]');
            radio.prop('checked', true);
            
            // Remover selección anterior de otras opciones del mismo grupo
            $(`input[name="${radio.attr('name')}"]`).parent().removeClass('selected');
            $(this).addClass('selected');
        });

        // Event listeners para enviar actividades
        $('.submit-activity-btn').off('click').on('click', function() {
            const activityIndex = $(this).data('activity-index');
            submitActivity(activityIndex);
        });

        // Event listeners para reiniciar actividades
        $('.reset-activity-btn').off('click').on('click', function() {
            const activityIndex = $(this).data('activity-index');
            resetActivity(activityIndex);
        });
    }

    function submitActivity(activityIndex) {
        const form = $(`.activity-form[data-activity-index="${activityIndex}"]`);
        const formData = collectFormData(form);
        const contentId = $(`.activity-recommendation-card[data-activity-index="${activityIndex}"]`).data('content-id');

        // Evaluar respuestas localmente
        const evaluation = evaluateAnswers(form);
        
        // Mostrar resultados
        showActivityResults(activityIndex, evaluation);

        // Opcional: Enviar al servidor para guardar progreso
        $.ajax({
            url: SUBMIT_ACTIVITY_URL,
            method: 'POST',
            data: JSON.stringify({
                content_id: contentId,
                answers: formData,
                evaluation: evaluation
            }),
            contentType: 'application/json',
            success: function(data) {
                console.log('Actividad guardada correctamente:', data);
            },
            error: function(xhr, status, error) {
                console.warn('No se pudo guardar la actividad:', error);
                // No mostramos error al usuario, ya que la evaluación local funciona
            }
        });
    }

    function collectFormData(form) {
        const formData = {};
        
        // Recopilar respuestas de opción múltiple
        form.find('input[type="radio"]:checked').each(function() {
            const name = $(this).attr('name');
            const value = $(this).val();
            formData[name] = value;
        });

        // Recopilar respuestas abiertas
        form.find('textarea').each(function() {
            const name = $(this).attr('name');
            const value = $(this).val().trim();
            if (value) {
                formData[name] = value;
            }
        });

        return formData;
    }

    function evaluateAnswers(form) {
        let totalQuestions = 0;
        let correctAnswers = 0;
        const results = [];

        // Evaluar preguntas de opción múltiple
        form.find('.question-card[data-question-type="multiple"]').each(function() {
            totalQuestions++;
            const questionCard = $(this);
            const selectedOption = questionCard.find('input[type="radio"]:checked');
            
            if (selectedOption.length > 0) {
                const isCorrect = selectedOption.data('correct') === true;
                if (isCorrect) {
                    correctAnswers++;
                    selectedOption.closest('.option-item').removeClass('incorrect').addClass('correct');
                } else {
                    selectedOption.closest('.option-item').removeClass('correct').addClass('incorrect');
                }

                // Mostrar explicación si existe
                const explanationBox = questionCard.find('.explanation-box');
                if (explanationBox.length > 0) {
                    explanationBox.addClass('show');
                }

                results.push({
                    type: 'multiple',
                    correct: isCorrect,
                    selected: selectedOption.val()
                });
            } else {
                results.push({
                    type: 'multiple',
                    correct: false,
                    selected: null
                });
            }
        });

        // Para preguntas abiertas, simplemente las marcamos como respondidas
        form.find('.question-card[data-question-type="open"]').each(function() {
            totalQuestions++;
            const textarea = $(this).find('textarea');
            const hasAnswer = textarea.val().trim().length > 0;
            
            if (hasAnswer) {
                correctAnswers++; // Asumimos que cualquier respuesta abierta es válida
            }

            // Mostrar ejemplo de respuesta
            const explanationBox = $(this).find('.explanation-box');
            if (explanationBox.length > 0) {
                explanationBox.addClass('show');
            }

            results.push({
                type: 'open',
                correct: hasAnswer,
                answer: textarea.val()
            });
        });

        const percentage = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0;

        return {
            total: totalQuestions,
            correct: correctAnswers,
            percentage: percentage,
            results: results
        };
    }

    function showActivityResults(activityIndex, evaluation) {
        const resultContainer = $(`#result-${activityIndex}`);
        
        let resultClass = 'result-success';
        let resultIcon = 'trophy';
        let resultTitle = '¡Excelente trabajo!';
        let resultMessage = '¡Has demostrado un gran conocimiento!';

        if (evaluation.percentage < 60) {
            resultClass = 'result-danger';
            resultIcon = 'times-circle';
            resultTitle = 'Sigue practicando';
            resultMessage = 'No te desanimes, la práctica hace al maestro.';
        } else if (evaluation.percentage < 80) {
            resultClass = 'result-warning';
            resultIcon = 'star-half-alt';
            resultTitle = '¡Buen trabajo!';
            resultMessage = 'Vas por buen camino, sigue así.';
        }

        const progressDegrees = (evaluation.percentage / 100) * 360;

        const resultHtml = `
        <div class="${resultClass}">
            <div class="text-center">
                <div class="progress-circle" style="background: conic-gradient(var(--${resultClass.split('-')[1]}-color) ${progressDegrees}deg, #e9ecef ${progressDegrees}deg);">
                    <div class="progress-text">${evaluation.percentage}%</div>
                </div>
                <h4><i class="fas fa-${resultIcon} me-2"></i>${resultTitle}</h4>
                <p class="mb-3">${resultMessage}</p>
                <div class="d-flex justify-content-center gap-3">
                    <div class="text-center">
                        <strong>${evaluation.correct}</strong><br>
                        <small>Correctas</small>
                    </div>
                    <div class="text-center">
                        <strong>${evaluation.total}</strong><br>
                        <small>Total</small>
                    </div>
                    <div class="text-center">
                        <strong>${evaluation.percentage}%</strong><br>
                        <small>Puntuación</small>
                    </div>
                </div>
            </div>
        </div>
        `;

        resultContainer.html(resultHtml).fadeIn();

        // Scroll suave hasta los resultados
        $('html, body').animate({
            scrollTop: resultContainer.offset().top - 100
        }, 500);
    }

    function resetActivity(activityIndex) {
        const form = $(`.activity-form[data-activity-index="${activityIndex}"]`);
        
        // Limpiar selecciones
        form.find('input[type="radio"]').prop('checked', false);
        form.find('.option-item').removeClass('selected correct incorrect');
        form.find('textarea').val('');
        form.find('.explanation-box').removeClass('show');
        
        // Ocultar resultados
        $(`#result-${activityIndex}`).fadeOut();

        Swal.fire({
            title: '¡Actividad reiniciada!',
            text: 'Puedes volver a intentarlo.',
            icon: 'info',
            timer: 2000,
            showConfirmButton: false
        });
    }

    function showLoading() {
        $('#loading-spinner').fadeIn();
        $('#activities-container').fadeOut();
    }

    function hideLoading() {
        $('#loading-spinner').fadeOut();
        $('#activities-container').fadeIn();
    }

    function showEmptyState() {
        $('#empty-state').fadeIn();
        $('#activities-container').fadeOut();
    }

    function hideEmptyState() {
        $('#empty-state').fadeOut();
    }

    function showError(message) {
        Swal.fire({
            title: 'Error',
            text: message,
            icon: 'error',
            confirmButtonText: 'Entendido'
        });
        showEmptyState();
    }

    // Función global para generar actividades (para usar desde botones)
    window.generateActivities = generateActivities;
});