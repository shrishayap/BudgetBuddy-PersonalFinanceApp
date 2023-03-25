let account = {};

const createForm = document.getElementById("create-form");
const loginForm = document.getElementById("login-form");

createForm.addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent form from refreshing the page

  account.firstName = document.getElementById("first-name").value;
  account.lastName = document.getElementById("last-name").value;
  account.email = document.getElementById("email").value;
  account.phone = document.getElementById("phone").value;

  console.log(account);

  createForm.reset();
});

