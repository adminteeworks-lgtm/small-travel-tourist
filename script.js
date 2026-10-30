
// ======================================
// TRAVEL AGENCY WEBSITE
// JavaScript Functionality
// ======================================

// 1. Mobile Navigation Menu
const menuBtn = document.querySelector(".menu-btn");
const navLinks = document.querySelector(".nav-links");

if (menuBtn && navLinks) {
    menuBtn.addEventListener("click", () => {
        navLinks.classList.toggle("active");
    });
}

// 2. Search Destinations
const searchInput = document.querySelector("#searchInput");
const destinationCards = document.querySelectorAll(".destination-card");

if (searchInput) {
    searchInput.addEventListener("input", function () {
        const searchValue = this.value.toLowerCase();

        destinationCards.forEach(card => {
            const destination = card.textContent.toLowerCase();

            card.style.display = destination.includes(searchValue)
                ? "block"
                : "none";
        });
    });
}

// 3. Filter Destinations
const filterButtons = document.querySelectorAll(".filter-btn");

filterButtons.forEach(button => {
    button.addEventListener("click", () => {
        const category = button.dataset.category;

        destinationCards.forEach(card => {
            const cardCategory = card.dataset.category;

            card.style.display =
                category === "all" || category === cardCategory
                ? "block"
                : "none";
        });

        filterButtons.forEach(btn =>
            btn.classList.remove("active")
        );

        button.classList.add("active");
    });
});

// 4. Tour Booking System
const bookingForm = document.querySelector("#bookingForm");

if (bookingForm) {
    bookingForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const name = document.querySelector("#customerName").value;
        const destination = document.querySelector("#destination").value;
        const date = document.querySelector("#travelDate").value;
        const travelers = document.querySelector("#travelers").value;

        if (!name || !destination || !date || !travelers) {
            alert("Please fill in all booking details.");
            return;
        }

        alert(
            "BOOKING REQUEST SUCCESSFUL!\n\n" +
            "Customer: " + name +
            "\nDestination: " + destination +
            "\nTravel Date: " + date +
            "\nTravelers: " + travelers
        );

        bookingForm.reset();
    });
}

// 5. Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", function (event) {
        const target = document.querySelector(
            this.getAttribute("href")
        );

        if (target) {
            event.preventDefault();

            target.scrollIntoView({
                behavior: "smooth"
            });
        }
    });
});

// 6. Automatic Current Year
const yearElement = document.querySelector("#currentYear");

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}

// 7. Website Loading Message
document.addEventListener("DOMContentLoaded", () => {
    console.log("Welcome to our Travel Agency!");
    console.log("JavaScript is working successfully.");
});
              
