document.addEventListener("DOMContentLoaded", function() {
    // Generate CAPTCHA
    function generateCaptcha(elementId) {
        const captchaContainer = document.getElementById(elementId);
        captchaContainer.innerHTML = ""; // Clear previous CAPTCHA
        const charsArray = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@!#$%^&*";
        const lengthOtp = 6;
        let captcha = [];
        for (let i = 0; i < lengthOtp; i++) {
            const index = Math.floor(Math.random() * charsArray.length);
            captcha.push(charsArray[index]);
        }
        const canv = document.createElement("canvas");
        canv.id = "captcha";
        canv.width = 100;
        canv.height = 50;
        const ctx = canv.getContext("2d");
        ctx.font = "25px Arial";
        ctx.strokeText(captcha.join(""), 0, 30);
        captchaContainer.appendChild(canv);
        captchaContainer.captchaCode = captcha.join("");
    }

    // Validate CAPTCHA
    window.validateCaptcha = function(inputId, captchaId) {
        const inputElement = document.getElementById(inputId);
        const captchaContainer = document.getElementById(captchaId);
        if (inputElement.value === captchaContainer.captchaCode) {
            return true;
        } else {
            alert("Invalid CAPTCHA. Please try again.");
            return false;
        }
    }

    // Generate CAPTCHA on page load
    generateCaptcha("studentCaptcha");
    generateCaptcha("employerCaptcha");
});