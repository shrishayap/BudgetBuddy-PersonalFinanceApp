// Define an object to store account details
let account = {};

// Get form elements
const createForm = document.getElementById("create-form");
const loginForm = document.getElementById("login-form");

// Handle form submission
createForm.addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent form from refreshing the page

  // Get form values and store them in the account object
  account.firstName = document.getElementById("first-name").value;
  account.lastName = document.getElementById("last-name").value;
  account.email = document.getElementById("email").value;
  account.phone = document.getElementById("phone").value;

  // Do something with the account object, like save it to a database or display it on the page
  console.log(account);

  // Clear the form inputs
  createForm.reset();
});

