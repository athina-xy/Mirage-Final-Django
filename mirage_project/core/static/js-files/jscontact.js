// Character limits
const NAME_MAX = 50;
const EMAIL_MAX = 100;
const SUBJECT_MAX = 80;
const MESSAGE_MAX = 500;

// Basic email validation helper 
function isValidEmail(email) {
    //pattern: something@something.something
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(email);
}

// Validate contact form 
function validateContactForm(name, email, subject, message) {
    const errors = [];

    // Name
    if (!name) {
        errors.push("Name is required.");
    } else if (name.length > NAME_MAX) {
        errors.push(`Name must be at most ${NAME_MAX} characters.`);
    }

    // Email
    if (!email) {
        errors.push("Email is required.");
    } else if (email.length > EMAIL_MAX) {
        errors.push(`Email must be at most ${EMAIL_MAX} characters.`);
    } else if (!isValidEmail(email)) {
        errors.push("Please enter a valid email address.");
    }

    // Subject
    if (!subject) {
        errors.push("Subject is required.");
    } else if (subject.length > SUBJECT_MAX) {
        errors.push(`Subject must be at most ${SUBJECT_MAX} characters.`);
    }

    // Message
    if (!message) {
        errors.push("Message is required.");
    } else if (message.length > MESSAGE_MAX) {
        errors.push(`Message must be at most ${MESSAGE_MAX} characters.`);
    }

    if (errors.length > 0) {
        alert(errors.join("\n"));
        return false;
    }

    return true;
}

// When Send button is clicked
$("#sendBtn").on("click", function () {
    let name = $("#contactName").val().trim();
    let email = $("#contactEmail").val().trim();
    let subject = $("#contactSubject").val().trim();
    let message = $("#contactMessage").val().trim();

    // Calling the validation
    if (!validateContactForm(name, email, subject, message)) {
        return;
    }

    // Pop up display
    alert(
        `Message Sent!\n` +
        `Name: ${name}\n` +
        `Email: ${email}\n` +
        `Subject: ${subject}\n` +
        `Message: ${message}`
    );

    // Clear fields after sent
    $("#contactName, #contactEmail, #contactSubject, #contactMessage").val("");
});

// Pre-Order Pop-Up
$("#preorderBtn").on("click", function () {
    alert("Pre-Order Confirmed!\nThank you for supporting Mirage.");
});
