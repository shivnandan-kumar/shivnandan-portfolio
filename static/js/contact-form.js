"use strict";

(() => {
  const form = document.querySelector("#contact-form");
  const status = document.querySelector("#contact-status");

  if (!form || !status) return;

  const nameField = form.querySelector("#contact-name");
  const emailField = form.querySelector("#contact-email");
  const messageField = form.querySelector("#contact-message");
  const honeypot = form.querySelector('[name="website"]');
  const accessKey = form.querySelector('[name="access_key"]');
  const submitButton = form.querySelector(".contact-submit");
  const successMessage = "Thanks for reaching out. Your message has been sent.";
  const failureMessage = "Your message could not be sent right now. Please try again later.";
  let submitting = false;

  function showStatus(message, category) {
    const notice = document.createElement("p");
    notice.className = `contact-notice contact-notice-${category}`;
    notice.setAttribute("role", category === "error" ? "alert" : "status");
    notice.textContent = message;
    status.replaceChildren(notice);
    status.hidden = false;
  }

  function validateFields() {
    nameField.setCustomValidity(nameField.value.trim() ? "" : "Enter your name.");
    emailField.setCustomValidity(
      emailField.value.trim() && emailField.validity.valid ? "" : "Enter a valid email address."
    );

    const messageLength = messageField.value.trim().length;
    messageField.setCustomValidity(
      messageLength >= 20 && messageLength <= 3000
        ? ""
        : "Message must be between 20 and 3000 characters."
    );

    return form.reportValidity();
  }

  [nameField, emailField, messageField].forEach((field) => {
    field.addEventListener("input", () => field.setCustomValidity(""));
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (submitting || !validateFields()) return;

    // Discard bot submissions silently, matching the previous honeypot behavior.
    if (honeypot.value.trim()) return;

    if (!accessKey.value.trim()) {
      showStatus(failureMessage, "error");
      return;
    }

    submitting = true;
    const originalButtonText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.textContent = "Sending...";
    form.setAttribute("aria-busy", "true");
    status.hidden = true;

    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), 15000);

    try {
      const response = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          access_key: accessKey.value.trim(),
          name: nameField.value.trim(),
          email: emailField.value.trim(),
          message: messageField.value.trim(),
          subject: "New portfolio contact message",
          from_name: "Shivnandan Kumar",
        }),
        signal: controller.signal,
      });

      const result = await response.json();
      if (!response.ok || result.success !== true) throw new Error("Delivery failed");

      form.reset();
      showStatus(successMessage, "success");
    } catch (_error) {
      showStatus(failureMessage, "error");
    } finally {
      window.clearTimeout(timeoutId);
      submitting = false;
      submitButton.disabled = false;
      submitButton.textContent = originalButtonText;
      form.removeAttribute("aria-busy");
    }
  });

  // Activate native form submission only after the guarded handler is installed.
  // Without JavaScript, the button remains inert and cannot post directly to Web3Forms.
  submitButton.type = "submit";
})();
