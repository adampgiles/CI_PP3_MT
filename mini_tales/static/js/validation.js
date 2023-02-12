// Set input and alert elements
const registerForm = document.getElementById("register-form") 
const formAlertContainer = document.getElementById("validation-alert-container");
const formAlert = document.getElementById("validation-alerts");
const username = document.getElementById("register-username");
const password = document.getElementById("register-password");
const confirmPassword = document.getElementById("confirm-password");

// Username constrained to a minimum of 6 characters, at least one lowercase letter and no special characters.
const usernameRegex= new RegExp(/^(?=.*[a-z])\w{6,}$/);
// Password constrained to a minimum of 6 characters, at least one number, one lowercase letter, one uppercase letter and no special characters.
var passwordRegex = new RegExp(/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])\w{6,}$/);

registerForm.addEventListener("submit", (event) => {
    let alerts = [];

    // Check if input fields are EMPTY
    if(username.value == "" || password.value == "" || confirmPassword.value == ""){
        alerts.push("- Please enter details in all three text boxes.");
    }
    // Check if username field meets regex validation
    if(usernameRegex.test(username.value) != true){
        alerts.push("- Username must be a minimum of 6 characters, at least one lowercase letter and no special characters.");
    }
    // Check if password fields meets regex validation
    if(passwordRegex.test(password.value) != true || passwordRegex.test(confirmPassword.value) != true){
        alerts.push("- Password must be a minimum of 6 characters, at least one number, one lowercase letter, one uppercase letter and no special characters.");
    }
    // Check if password fields match
    if(password.value != confirmPassword.value){        
        alerts.push("- Both Password fields must match.");
    }
    // If any of the above checks fail, prevent the form from submitting and add the alerts to the formAlert message
    if(alerts.length > 0){        
        event.preventDefault();
        formAlertContainer.style.display = "block";
        formAlert.innerHTML = alerts.join('<br>');
    }
})