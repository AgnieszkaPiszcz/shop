console.log('hello')

$(function () {
    $("form").submit(async function(event){
        event.preventDefault();
        let form = document.getElementById('form');
        let formData = new FormData(form);
        formData.append('submit', 'submit');

        let emailDiv = document.getElementById('email-div');
        let namelDiv = document.getElementById('name-div');
        let msgDiv = document.getElementById('msg-div');
        let formMsgDiv = document.getElementById("form-message");

        while(emailDiv.firstChild){
            emailDiv.removeChild(emailDiv.firstChild)
        }

        while(namelDiv.firstChild){
            namelDiv.removeChild(namelDiv.firstChild)
        }

        while(formMsgDiv.firstChild){
            formMsgDiv.removeChild(formMsgDiv.firstChild)
        }

        while(msgDiv.firstChild){
            msgDiv.removeChild(msgDiv.firstChild)
        }

        let name = document.getElementById('name');
        let email = document.getElementById('email');
        let msg = document.getElementById('msg');
        let submit = document.getElementById('submit');
        let csrf_token = document.getElementById('csrf_token');

        let data = {
            name: name.value,
            email: email.value,
            msg: msg.value,
            submit: submit.value,
            csrf_token: csrf_token.value
        }

        try {
            let response = await fetch('/contact', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: new Headers({
                    "content-type": "application/json"
                  })
            });
            
            let responseJson = await response.json();
            console.log(responseJson);

            if(responseJson["message"]){
                console.log(responseJson["message"]);
                try {
                    let responseEmail = await fetch("/contact/send_email");
                    let responseEmailJson = await responseEmail.json();
                    if(responseEmailJson["message"]){
                        formMsgDiv.appendChild(document.createTextNode("Wysłano wiadomość."));
                        formMsgDiv.classList.add("alert-success");
                    }
            
                    } catch (errorFiles) {
                        console.log(errorFiles);
                    }

            }
            else {
                
                if(responseJson.email){
                    let emailDiv = document.getElementById('email-div');
                    for(var error of responseJson.email){
                        let errMsg = document.createTextNode(error);
                        let spanElem = document.createElement("span");
                        spanElem.appendChild(errMsg);
                        emailDiv.appendChild(spanElem);

                    }
                }
                if(responseJson.name){
                    let nameDiv = document.getElementById('name-div');
                    for(var error of responseJson.name){
                        let errMsg = document.createTextNode(error);
                        let spanElem = document.createElement("span");
                        spanElem.appendChild(errMsg);
                        nameDiv.appendChild(spanElem);

                    }
                }
                if(responseJson.msg){
                    let emailDiv = document.getElementById('name-div');
                    for(var error of responseJson.msg){
                        let errMsg = document.createTextNode(error);
                        let spanElem = document.createElement("span");
                        spanElem.appendChild(errMsg);
                        msgDiv.appendChild(spanElem);
                    }
                }
            }
            
        } catch (error) {
            console.log(error);
        }
  
    })
}) 
