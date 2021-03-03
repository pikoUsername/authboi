(function init() {
    let loginPanel = document.querySelector('#login-panel');
    let form = document.querySelector('#login-form');
    let errorMsg = document.querySelector('#error-message');

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        let url = form.getAttribute('action');
        let data = {
            'username': form.username.value,
            'password': form.password.value
        };
        ajaxRequest(url, data, onSuccess, onError);
    });

    function ajaxRequest(url, data, successCallback, errorCallback) {
        let xhr = new XMLHttpRequest();

        xhr.open('POST', url);
        xhr.setRequestHeader('Content-type', 'application/json');

        xhr.onload = () => {
            if (xhr.status === 200) {
                successCallback(xhr);
            } else {
                let response = JSON.parse(xhr.responseText);
                errorCallback(response.error);
            }
        };
        xhr.onerror = () => {
            errorCallback('Connection error. Try again later');
        };

        xhr.send(JSON.stringify(data));
    }

    function onSuccess(xhr) {
        let response = JSON.parse(xhr.responseText);
        let token = xhr.getResponseHeader('X-Token');
        errorMsg.innerHTML = '';
        window.localStorage.setItem('aiohttp_admin_token', token);
        window.location = response['location'];
    }

    function onError(message) {
        errorMsg.innerHTML = message;
        loginPanel.classList.remove('animate');
        void loginPanel.offsetWidth;   // triggering reflow /* The actual magic */
        loginPanel.classList.add('animate');
    }
})();
