
const contactForm = document.getElementById("contactForm");

contactForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const submitBtn = document.getElementById("submitBtn");
    const formStatus = document.getElementById("formStatus");

   const contactData = {
    name: document.getElementById("name").value.trim(),
    phone: document.getElementById("phone").value.trim(),
    email: document.getElementById("email").value.trim(),
    subject: document.getElementById("subject").value,
    message: document.getElementById("message").value.trim()
    };

    submitBtn.disabled = true;
    submitBtn.textContent = "Submitting...";
    formStatus.textContent = "";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/contact",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(contactData)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Submission failed");
        }

        formStatus.textContent = "Your message was submitted successfully!";
        formStatus.style.color = "green";

        contactForm.reset();

    } catch (error) {

        formStatus.textContent = error.message;
        formStatus.style.color = "red";

    } finally {

        submitBtn.disabled = false;
        submitBtn.textContent = "Submit";

    }

});
