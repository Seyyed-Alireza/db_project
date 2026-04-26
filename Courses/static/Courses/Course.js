const createExamButton = document.getElementById('show-form-btn')
const cancelCreate = document.getElementById('cancel-btn')
const formContainer = document.getElementById('form-container');

createExamButton.addEventListener('click', () => {
    // exam_from.style.display = 'flex';
    // notification('سلام عزیز');
    setTimeout(() => {
        const idInput = document.getElementById('id_title');
        if (idInput) {
            idInput.focus();
        }
    }, 300);
    formContainer.classList.add('show');
    // for (const exam of window.examsStatus) {
    //     console.log(exam.title, exam.status, exam.id);
    // }
});



const errorSpans = document.querySelectorAll('.error-span');
const fromInputs = document.querySelectorAll('.form-input');
const examForm = document.getElementById('exam-form')
cancelCreate.addEventListener('click', () => {
    // exam_from.style.display = 'none';
    formContainer.classList.remove('show');
    errorSpans.forEach(errorSpan => errorSpan.textContent = '');
    examForm.reset();
    // fromInputs.forEach(forInput => forInput.textContent = '');
    // titleError.style.display = 'none';
});

function addNewExam(examData) {
    let exams = window.examsStatus;
    let insertIndex = -1;
    
    for (let i = 0; i < exams.length; i++) {
        let currentOrder = order(exams[i].status);
        let newOrder = order(examData.status);
        
        if (newOrder < currentOrder) {
            insertIndex = i;
            break;
        } else if (newOrder == currentOrder) {
            if (newOrder == 1) {
                if (examData.end_time < exams[i].end_time) {
                    insertIndex = i;
                    break
                } 
            } else {
                if (examData.start_time < exams[i].start_time) {
                    insertIndex = i;
                    break
                }
            }
            // break;
        }
    }

    if (insertIndex === -1) {
        exams.push(examData);
        appendExamElement(examData);
    } else {
        exams.splice(insertIndex, 0, examData);
        insertExamElement(examData, insertIndex);
    }
}

function createExamElement(examData) {
    const div = document.createElement('div');
    div.className = 'exam-bow-wrapper';
    const innerDiv = document.createElement('div');
    innerDiv.className = 'exam-box';
    innerDiv.id = `exam-box-${examData.id}`;
    
    let statusText = '';
    if (examData.status === 'inprogress') {
        statusText = 'درحال برگزاری';
    } else if (examData.status === 'ended') {
        statusText = 'تمام شده';
    } else if (examData.status === 'waiting') {
        statusText = 'منتظر شروع';
    } else {
        statusText = 'وضعیت نامعلوم';
    }
    courseId = window.course_id
    let buttonsHTML = `
        <button type="button" class="btn" id="enter-exam-${examData.id}"
            onclick="location.href='/exams/exam_page/${courseId}/${examData.id}/'"
        >
            ورود به آزمون
        </button>
        <button type="button" class="btn"
            onclick="location.href='/exams/edit_exam/${courseId}/${examData.id}/'"
        >
            ویرایش آزمون
        </button>
        <button type="button" class="btn btn--secondary"
            onclick="deleteExam(${courseId}, ${examData.id}, ${examData.id})"
        >
            حذف آزمون
        </button>
    `;
    
    
    innerDiv.innerHTML = `
        <p>${examData.title}</p>
        ${statusText}
        <br>
        <div class="exam-options">
            ${buttonsHTML}
        </div>
    `;
    div.appendChild(innerDiv);
    // div.innerHTML = `${innerDiv}`;
    
    return div;
}

function appendExamElement(examData) {
    const container = document.getElementById('exams-container');
    const element = createExamElement(examData);
    container.appendChild(element);
}

function insertExamElement(examData, index) {
    const container = document.getElementById('exams-container');
    const children = container.children;
    const element = createExamElement(examData);
    if (index >= children.length) {
        container.appendChild(element);
    } else {
        container.insertBefore(element, children[index]);
    }
}

function order(status) {
    if (status == 'inprogress') return 1;
    else if (status == 'waiting') return 2;
    else if (status == 'ended') return 3;
    else return 4;
}

examForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const submitBtn = document.getElementById('submit-btn');

    const csrftoken = examForm.querySelector('[name=csrfmiddlewaretoken]').value;
    
    const formData = new FormData(examForm);
    
    errorSpans.forEach(errorSpan => errorSpan.textContent = '');
    submitBtn.disabled = true;
    submitBtn.textContent = 'در حال ارسال...';
    
    fetch(examForm.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            examForm.reset();
            new_exam = data.new_exam;
            submitBtn.textContent = 'در حال ایجاد...';
            addNewExam(new_exam);
            formContainer.classList.remove('show');
            notification(data.message, 'success');
        } else {
            if (data.errors) {
                for (const [field, messages] of Object.entries(data.errors)) {
                    if (field == '__all__') {
                        notification(messages[0], type='error');
                    } else {
                        const errorSpan = document.getElementById(`${field}-error`);
                        if (errorSpan) {
                            errorSpan.textContent = messages[0];
                            // errorSpan.style.display = 'block';
                        }
                    }
                }
            }
        }
    })
    .catch(error => {
        // console.error('Error:', error);
    })
    .finally(() => {
        submitBtn.disabled = false;
        submitBtn.textContent = 'ثبت آزمون';
    });
});


function deleteExam(course_id, exam_id, id) {
    if (!confirm('آیا از حذف آزمون اطمینان دارید؟')) {
        return;
    }
    data = JSON.stringify({
        exam_id: exam_id,
    })
    url = `/delete-exam/${course_id}/`
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data
    })
    .then(response => response.json())
    .then(data => {
        if (data.status == 'success') {
            const idd = `exam-box-${id}`;
            const element = document.getElementById(idd);
            const animationTime = 600;
            element.style.animation = `smallOut ${animationTime}ms ease forwards`;
            const height = element.offsetHeight;
            element.style.setProperty('--element-height', height + 'px');
            notification(data.message, 'success');
            setTimeout(() => {
                element.remove();
            }, animationTime);
        } else {
            alert('خطا: '+ data.message);
        }
    })
}

function createExam() {

}
