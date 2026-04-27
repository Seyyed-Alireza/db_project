let exit_button_clicked = false;
let cancel_button_clicked = false;
let unloaded = false;
let blur_event = false;
let visibility_change_event = false;

// const startExamButton = document.getElementById('start-exam');
// if (startExamButton) {
//     startExamButton.addEventListener('click', () => {
//         start_exam_clicked = true;
//     })
// } else {
//     console.log('error');
// }

function sendResolution() {
    const data = JSON.stringify({
        event: 'question',
        new_width: window.innerWidth,
        new_height: window.innerHeight
    });

    fetch('/log/change-size/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data
    })
}

function updateAnswerForm(answerForm) {
    form = document.getElementById('answer-form');
    console.log(answerForm)
}

function updateQuestion(question) {
    qBox = document.getElementById('question-box');
    const qtdiv = document.createElement('div');
    qtdiv.innerHTML = `
        سؤال ${question.order}: ${question.text}
    `;
    qtdiv.className = 'question-text';
    qBox.appendChild(qtdiv);
    const imgdiv = document.createElement('img');
    imgdiv.id = 'question-image';
    imgdiv.src = question.image
    qBox.appendChild(imgdiv);
    updateAnswerForm(question.answer_form);
}

document.addEventListener('DOMContentLoaded', function() {
    const exit_button = document.getElementById('end-exam');
    if (exit_button) {
        exit_button.addEventListener('click', exitExam);
    }
});

function exitExam() {
    exit_button_clicked = true;
    if (!confirm('آیا مطمئن هستید که می‌خواهید آزمون را تمام کنید؟')) {
        exit_button_clicked = false;
        cancel_button_clicked = true;
        return;
    }

    const data = JSON.stringify({
        event: "exit_exam_with_click",
        timestamp: new Date().toISOString(),
        url: window.location.href
    });

    fetch('/exit-exam/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data
    })
    .then(response => response.json())
    .then(data => {
        unloaded = true;
        // console.log(data.status);
        if (data.status == 'ok') {
            window.location.replace(`/course/${data.course_id}`);
        } else {
            alert('خطا: '+ data.message);
        }
    })
    .catch(error => {
        console.error('Error: ', error);
        alert('خطا! دوباره تلاش کنید');
    });
}

function disableActionBtns() {
    const preQuestionBtn = document.getElementById('pre-question');
    if (preQuestionBtn) preQuestionBtn.disabled = true;
    const saveAnswerBtn = document.getElementById('save-answer');
    if (saveAnswerBtn) saveAnswerBtn.disabled = true;
    const nextQuestionBtn = document.getElementById('next-question');
    if (nextQuestionBtn) nextQuestionBtn.disabled = true;
    const endExamBtn = document.getElementById('end-exam');
    if (endExamBtn) endExamBtn.disabled = true;
}

function enableActionBtns() {
    const preQuestionBtn = document.getElementById('pre-question');
    if (preQuestionBtn) preQuestionBtn.disabled = false;
    const saveAnswerBtn = document.getElementById('save-answer');
    if (saveAnswerBtn) saveAnswerBtn.disabled = false;
    const nextQuestionBtn = document.getElementById('next-question');
    if (nextQuestionBtn) nextQuestionBtn.disabled = false;
    const endExamBtn = document.getElementById('end-exam');
    if (endExamBtn) endExamBtn.disabled = false;
}

async function saveAnswer() {
    const answerForm = document.getElementById('answer-form');
    const formData = new FormData(answerForm);
    const saveAnswerBtn = document.getElementById('save-answer');
    disableActionBtns();
    saveAnswerBtn.textContent = 'در حال ذخیره';
    try {
        const response = await fetch(answerForm.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
        const data = await response.json();
        if (data.success) {
            notification(data.message);
        } else {
            notification(data.message, 'error');
        }
    } catch (error) {
        notification('خطا در ارتباط با سرور', 'error');
    } finally {
        enableActionBtns();
        saveAnswerBtn.textContent = 'ذخیره پاسخ';
    }
}

function updateQuestionForm(data) {
    if (data.success) {
        container = document.getElementById('container');
        container.innerHTML = data.html;
        const exit_button = document.getElementById('end-exam');
        if (exit_button) {
            exit_button.addEventListener('click', exitExam);
        }
        const nextQuestionBtn = document.getElementById('next-question');
        if (nextQuestionBtn) {
            nextQuestionBtn.addEventListener('click', nextQuestion);
        }
        const preQuestionBtn = document.getElementById('pre-question');
        if (preQuestionBtn) {
            preQuestionBtn.addEventListener('click', preQuestion);
        }
        const saveAnswerBtn = document.getElementById('save-answer');
        if (saveAnswerBtn) {
            saveAnswerBtn.addEventListener('click', saveAnswer);
        }
    } else {
        console.log('failed')
    }
}

async function getQuestion(order) {
    const data_fetch = JSON.stringify({
        order: order
    })
    disableActionBtns();
    const response = await fetch('/get-question/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data_fetch
    })

    const data = await response.json();
    updateQuestionForm(data);
    enableActionBtns();
    // if (data.success) {
    //     container = document.getElementById('container');
    //     container.innerHTML = data.html;
    //     const exit_button = document.getElementById('end-exam');
    //     if (exit_button) {
    //         exit_button.addEventListener('click', exitExam);
    //     }
    //     const saveAnswerBtn = document.getElementById('save-answer');
    //     if (saveAnswerBtn) {
    //         saveAnswerBtn.addEventListener('click', saveAnswer);
    //     }
    // } else {
    //     console.log('failed')
    // }
}

async function nextQuestion() {
    disableActionBtns();
    try {
            const response = await fetch('/next-question/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
        })
        const data = await response.json();
        updateQuestionForm(data);
    } catch (error) {
        notification('خطا در ارتباط با سرور', 'error');
    } finally {
        enableActionBtns();
    }
}

async function preQuestion() {
    disableActionBtns();
    try {
        const response = await fetch('/pre-question/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
        })
        const data = await response.json();
        updateQuestionForm(data);
    } catch (error) {
        notification('خطا در ارتباط با سرور', 'error');
    } finally {
        enableActionBtns();
    }
}

document.addEventListener('DOMContentLoaded', () => getQuestion(1))
document.addEventListener('DOMContentLoaded', sendResolution)

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function visibilityHandler(event_type) {
    const data = JSON.stringify({
        event: event_type,
        // timestamp: new Date().toISOString(),
        // url: window.location.href
    });


    fetch('/log/tab-switch/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data
    });
    // .then(response => response.json())
    // .then(data => console.log('Answer: ', data))
    // .catch(error => console.error('Error: ', error));
}

function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

const blurHandler = debounce( () => {
    if (unloaded || exit_button_clicked || visibility_change_event) {
        return;
    }
    // console.log('blur')

    if (cancel_button_clicked) {
        cancel_button_clicked = false;
        return;
    }
    
    blur_event = true;
    visibilityHandler('window_blur');
}, 200);

window.addEventListener('blur', blurHandler);


window.addEventListener('focus', () => {
    if (!blur_event) {
        return;
    }
    visibilityHandler('window_focus');
    blur_event = false;
});

window.addEventListener('visibilitychange', () => {
    if (unloaded || window.start_exam_button) {
        return
    }
    if (document.hidden) {
        visibility_change_event = true;
        visibilityHandler('window_hidden');
    } else {
        visibility_change_event = false;
        visibilityHandler('window_visible');
    }
    
})


window.addEventListener('beforeunload', () => {
    if (exit_button_clicked || window.start_exam_button) {
        return;
    }
    // if (!confirm('Are you sure?')) {
    //     return;
    // }
    unloaded = true;
    const data = JSON.stringify({
        event: "exit_exam_without_click",
        timestamp: new Date().toISOString(),
        url: window.location.href
    });

    if (navigator.sendBeacon && false) {
        const blob = new Blob([data], {type: 'application/json'});
        navigator.sendBeacon('/exit-exam/', blob);
    } else {
        fetch('/exit-exam/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: data,
            keepalive: true
        });
    }
});


const resizeHandler = debounce(() => {
    // console.log('عرض صفحه سایت:', window.innerWidth);
    // console.log('عرض صفحه مرورگر:', window.outerWidth);
    // console.log('عرض صفحه مانیتور', screen.width);
    const data = JSON.stringify({
        event: "resolution_change",
        new_width: window.innerWidth,
        new_height: window.innerHeight
    });

    fetch('/log/change-size/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data
    });
}, 500);


window.addEventListener('resize', resizeHandler);


function copyPasteHandler(text) {
    console.log(text);
}

document.addEventListener('copy', copyPasteHandler('copy'));
document.addEventListener('paste', copyPasteHandler('paste'));
document.addEventListener('cut', copyPasteHandler('cut'));

