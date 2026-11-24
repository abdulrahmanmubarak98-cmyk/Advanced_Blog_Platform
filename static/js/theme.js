// Reference the HTML document.
const root = document.documentElement;

// Define the localStorage key.
const storageKey = "blog-theme";

// Retrieve the saved theme.
const savedTheme = localStorage.getItem(storageKey);

// Check the visitor's system preference.
const systemPrefersDark = window.matchMedia(
    "(prefers-color-scheme: dark)"
).matches;

// Validate the saved theme and determine the initial theme.
const initialTheme =
    savedTheme === "dark" || savedTheme === "light"
        ? savedTheme
        : (systemPrefersDark ? "dark" : "light");

// Apply the selected theme.
function applyTheme(theme) {
    root.setAttribute("data-theme", theme);

    const darkModeEnabled = theme === "dark";

    // Update the button icon.
    const themeToggleIcon = document.getElementById("themeToggleIcon");

    if (themeToggleIcon) {
        themeToggleIcon.className = darkModeEnabled
            ? "bi bi-sun-fill"
            : "bi bi-moon-stars-fill";
    }

    // Update the accessible label and button state.
    const themeToggle = document.getElementById("themeToggle");
    const themeToggleLabel = document.getElementById("themeToggleLabel");

    if (themeToggle) {
        const accessibleLabel = darkModeEnabled
            ? "Switch to light mode"
            : "Switch to dark mode";

        themeToggle.setAttribute("aria-label", accessibleLabel);
        themeToggle.setAttribute("title", accessibleLabel);
        themeToggle.setAttribute("aria-pressed", String(darkModeEnabled));

        if (themeToggleLabel) {
            themeToggleLabel.textContent = accessibleLabel;
        }
    }
}

//  Restore the initial theme.
applyTheme(initialTheme);

// Locate the theme-toggle button.
const themeToggle = document.getElementById("themeToggle");

// Listen for clicks if the button exists.
if (themeToggle) {
    themeToggle.addEventListener("click", function () {

        const currentTheme = root.getAttribute("data-theme");

        const nextTheme =
            currentTheme === "dark" ? "light" : "dark";

        // Apply the new theme.
        applyTheme(nextTheme);

        // Save the user's selection.
        localStorage.setItem(storageKey, nextTheme);
    });
}