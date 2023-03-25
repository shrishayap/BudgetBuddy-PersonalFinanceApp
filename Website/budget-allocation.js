const totalBudgetInput = document.querySelector("#total-budget");
const bucketInputs = document.querySelectorAll(".bucket-input");

// Add an event listener to the total budget input to check the sum of the bucket inputs
totalBudgetInput.addEventListener("input", function() {
  const totalBudget = parseFloat(totalBudgetInput.value);
  let sum = 0;
  let invalid = false;
  for (let i = 0; i < bucketInputs.length; i++) {
    const bucketValue = parseFloat(bucketInputs[i].value);
    if (isNaN(bucketValue)) {
      // If any of the bucket values are not numbers, set the input as invalid
      invalid = true;
      break;
    }
    sum += bucketValue;
    if (sum > totalBudget) {
      // If the sum of the bucket inputs is greater than the total budget, set the input as invalid
      invalid = true;
      break;
    }
  }
  if (invalid) {
    totalBudgetInput.setCustomValidity("Invalid input: The sum of the bucket inputs cannot exceed the total budget.");
  } else {
    totalBudgetInput.setCustomValidity("");
  }
});

// Add event listeners to the bucket inputs to check the sum of the bucket inputs
for (let i = 0; i < bucketInputs.length; i++) {
  bucketInputs[i].addEventListener("input", function() {
    const totalBudget = parseFloat(totalBudgetInput.value);
    let sum = 0;
    let invalid = false;
    for (let j = 0; j < bucketInputs.length; j++) {
      const bucketValue = parseFloat(bucketInputs[j].value);
      if (isNaN(bucketValue)) {
        // If any of the bucket values are not numbers, set the input as invalid
        invalid = true;
        break;
      }
      sum += bucketValue;
      if (sum > totalBudget) {
        // If the sum of the bucket inputs is greater than the total budget, set the input as invalid
        invalid = true;
        break;
      }
    }
    if (invalid) {
      document.querySelector("#bucket-input-error").textContent = "Invalid input: The sum of the bucket inputs cannot exceed the total budget.";
    } else {
      document.querySelector("#bucket-input-error").textContent = "";
    }
  });
}
