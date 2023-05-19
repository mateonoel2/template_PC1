function login() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var data = { "username": username, "password": password };

    fetch('/login', {
        method: 'POST',
        body: JSON.stringify(data),
        headers:{
            'Content-Type': 'application/json'
        }
    })   
    .then(response => response.text())
    .then(text =>   {
                        if (text === "SUCCESS") {
                            window.location.href = "/game_menu?username=" + data.username;
                        }
                        else {
                            document.body.innerHTML = text;
                        }
                    }
    )
}