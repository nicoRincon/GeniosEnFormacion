window.onload = () => {

    document.getElementById('register_btn').addEventListener('click', (event) => {
        const password = document.getElementById('password_register').value;
        const confirmPassword = document.getElementById('confirm_password_register').value;

        if (password !== confirmPassword) {
            event.preventDefault();
            Swal.fire({
                title: '¡Error!',
                text: 'Las contraseñas no coinciden',
                icon: 'error',
                confirmButtonText: 'Ok'
            });
        }
    });
}

function setActiveClass(element = 'login') {
    let buttonNav = document.getElementById('tab-login');
    if (element === 'register') {
        buttonNav = document.getElementById('tab-register');
    }
    const activeClass = 'active';
    const elements = document.getElementsByClassName('nav-link');
    for (const eachNavLink of elements) {
        if (eachNavLink === buttonNav) {
            eachNavLink.classList.add(activeClass);
        } else {
            eachNavLink.classList.remove(activeClass);
        }
    }
}

function changeLoginPages(element = 'login') {
    setActiveClass(element);
    if (element === 'login') {
        document.getElementById('pills-login').classList.add('show');
        document.getElementById('pills-login').classList.add('active');
        document.getElementById('pills-register').classList.remove('show');
        document.getElementById('pills-register').classList.remove('active');
    } else if (element === 'register') {
        document.getElementById('pills-register').classList.add('show');
        document.getElementById('pills-register').classList.add('active');
        document.getElementById('pills-login').classList.remove('show');
        document.getElementById('pills-login').classList.remove('active');
    }
}