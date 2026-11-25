
const contactForm = document.getElementById("contactForm");

const submitBtn = document.getElementById("submitBtn");
const formStatus = document.getElementById("formStatus");

const attachmentInput = document.getElementById("attachments");
const fileList = document.getElementById("fileList");
const phoneInput = document.getElementById("phone");


// Allowed file extensions
const allowedExtensions = [
    "pdf",
    "doc",
    "docx",
    "xls",
    "xlsx",
    "jpg",
    "jpeg",
    "png",
    "txt",
    "csv"
];


// Attachment limits
const MAX_FILES = 10;
const MAX_FILE_SIZE = 10 * 1024 * 1024;
const MAX_TOTAL_SIZE = 100 * 1024 * 1024;


// Phone number: digits only, with optional leading +
phoneInput.addEventListener("input", function () {

    let value = phoneInput.value;

    value = value.replace(/[^0-9+]/g, "");

    // Allow + only at the beginning
    value = value.replace(/\+/g, "");

    if (phoneInput.value.startsWith("+")) {
        value = "+" + value;
    }

    // Maximum 15 digits, plus optional +
    const digits = value.replace(/\D/g, "").slice(0, 15);

    phoneInput.value =
        value.startsWith("+") ? "+" + digits : digits;

});


// Validate selected attachments
function validateFiles(files) {

    if (files.length > MAX_FILES) {
        return "You can upload a maximum of 10 files.";
    }

    let totalSize = 0;

    for (const file of files) {

        const extension = file.name
            .split(".")
            .pop()
            .toLowerCase();

        if (!allowedExtensions.includes(extension)) {
            return `File type not allowed: ${file.name}`;
        }

        if (file.size > MAX_FILE_SIZE) {
            return `${file.name} exceeds the 10 MB limit.`;
        }

        if (file.size === 0) {
            return `${file.name} is empty.`;
        }

        totalSize += file.size;

        if (totalSize > MAX_TOTAL_SIZE) {
            return "Total attachment size cannot exceed 100 MB.";
        }

    }

    return null;
}


// Display selected attachment names
attachmentInput.addEventListener("change", function () {

    fileList.innerHTML = "";
    formStatus.textContent = "";

    const files = Array.from(attachmentInput.files);

    const error = validateFiles(files);

    if (error) {

        formStatus.textContent = error;
        formStatus.style.color = "red";

        attachmentInput.value = "";
        return;

    }

    for (const file of files) {

        const listItem = document.createElement("li");

        const sizeInMB = (
            file.size / (1024 * 1024)
        ).toFixed(2);

        listItem.textContent =
            `${file.name} (${sizeInMB} MB)`;

        fileList.appendChild(listItem);

    }

});


// Submit contact form
contactForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    formStatus.textContent = "";

    // Validate phone number
    const phone = phoneInput.value.trim();

    if (!/^\+?[0-9]{10,15}$/.test(phone)) {

        formStatus.textContent =
            "Enter a valid phone number containing 10-15 digits.";

        formStatus.style.color = "red";
        return;

    }


    // Validate attachments again before submission
    const files = Array.from(attachmentInput.files);

    const fileError = validateFiles(files);

    if (fileError) {

        formStatus.textContent = fileError;
        formStatus.style.color = "red";
        return;

    }


    // Collect all form fields and attachments
    const formData = new FormData(contactForm);


    // Disable submit button
    submitBtn.disabled = true;
    submitBtn.textContent = "Submitting...";


    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/contact",
            {
                method: "POST",
                body: formData
            }
        );


        const result = await response.json();


        if (!response.ok) {

            const errorMessage = Array.isArray(result.detail)
                ? result.detail.map(error => error.msg).join(", ")
                : result.detail;

            throw new Error(
                errorMessage || "Submission failed"
            );

        }


        // Display successful submission
        formStatus.textContent =
            `Your query has been received! Your customer support number is ${result.support_number}.`;

        formStatus.style.color = "green";


        // Display email status
        if (result.email_sent) {

            formStatus.textContent +=
                " A confirmation email has been sent to your email address.";

        } else {

            formStatus.textContent +=
                " However, the confirmation email could not be sent.";

        }


        // Reset form after successful submission
        contactForm.reset();

        fileList.innerHTML = "";


    } catch (error) {

        formStatus.textContent = error.message;
        formStatus.style.color = "red";


    } finally {

        submitBtn.disabled = false;
        submitBtn.textContent = "Submit";

    }

});
