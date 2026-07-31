// NORMAH AGRO FARM — quote & enquiry form handling.
//
// Attaches to any <form data-normah-form="quote"> or [data-normah-form="contact"].
// Both the buyer request-a-quote form (/buyers.html) and the general
// enquiry form (/contact.html) use this one script.
//
// REQUIRED SETUP — see README.md "Wiring the form" section:
// Set window.NORMAH_FORM_ENDPOINT (in a small inline <script> before this
// file loads, or by editing the constant below) to your submission
// endpoint. Two supported shapes:
//   1. A hosted form service (e.g. Formspree-style) — POST JSON, expects
//      a 2xx response.
//   2. /assets/php/send-quote.php on cPanel/Apache shared hosting — see
//      assets/php/send-quote.php.example for a working starting point.
// No form on this site posts anywhere without that endpoint being set.
(function () {
  var DEFAULT_ENDPOINT = window.NORMAH_FORM_ENDPOINT || "/assets/php/send-quote.php";

  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function showError(field, message) {
    field.classList.add("has-error");
    var errorEl = field.querySelector(".error");
    if (errorEl) errorEl.textContent = message;
  }

  function clearError(field) {
    field.classList.remove("has-error");
  }

  function validate(form) {
    var valid = true;
    var firstInvalid = null;
    var fields = form.querySelectorAll("[data-field]");

    fields.forEach(function (field) {
      clearError(field);
      var input = field.querySelector("input, select, textarea");
      var required = field.hasAttribute("data-required");
      var type = field.getAttribute("data-field");

      if (type === "crops") {
        var checked = field.querySelectorAll("input[type=checkbox]:checked");
        if (required && checked.length === 0) {
          showError(field, "Choose at least one crop.");
          valid = false;
          firstInvalid = firstInvalid || field;
        }
        return;
      }

      if (!input) return;
      var value = input.value.trim();

      if (required && !value) {
        showError(field, "This field is required.");
        valid = false;
        firstInvalid = firstInvalid || input;
        return;
      }
      if (type === "email" && value && !EMAIL_RE.test(value)) {
        showError(field, "Enter a valid email address.");
        valid = false;
        firstInvalid = firstInvalid || input;
        return;
      }
      if (type === "number" && value && (isNaN(Number(value)) || Number(value) <= 0)) {
        showError(field, "Enter a number greater than zero.");
        valid = false;
        firstInvalid = firstInvalid || input;
      }
    });

    if (firstInvalid) firstInvalid.focus();
    return valid;
  }

  function serialize(form) {
    var data = {};
    new FormData(form).forEach(function (value, key) {
      if (data[key] !== undefined) {
        data[key] = Array.isArray(data[key]) ? data[key].concat(value) : [data[key], value];
      } else {
        data[key] = value;
      }
    });
    return data;
  }

  function setStatus(statusEl, kind, message) {
    statusEl.className = "form-status is-visible form-status--" + kind;
    statusEl.textContent = message;
    statusEl.setAttribute("role", kind === "error" ? "alert" : "status");
  }

  document.querySelectorAll("form[data-normah-form]").forEach(function (form) {
    var statusEl = form.querySelector(".form-status");
    var submitBtn = form.querySelector("[type=submit]");
    var successMessage = form.getAttribute("data-success-message") || "Request sent.";
    var endpoint = form.getAttribute("data-endpoint") || DEFAULT_ENDPOINT;

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validate(form)) {
        if (statusEl) setStatus(statusEl, "error", "Check the highlighted fields and try again.");
        return;
      }

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.dataset.originalText = submitBtn.textContent;
        submitBtn.textContent = "Sending…";
      }

      var payload = serialize(form);

      fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then(function (res) {
          if (!res.ok) throw new Error("Request failed with status " + res.status);
          form.reset();
          form.hidden = true;
          if (statusEl) {
            statusEl.hidden = false;
            setStatus(statusEl, "success", successMessage);
          }
        })
        .catch(function () {
          if (statusEl) {
            setStatus(
              statusEl,
              "error",
              "Something went wrong sending this — please email us directly at info@normahfarms.co.ug or try again."
            );
          }
        })
        .finally(function () {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = submitBtn.dataset.originalText;
          }
        });
    });
  });
})();
