const bucketInputs = document.querySelectorAll('input[name^="bucket"]');
const totalBudgetInput = document.getElementById('total-budget');
const submitButton = document.getElementById('submit-button');
var budgetMap;

function updateTotalBudget() {
  let total = 0;
  bucketInputs.forEach(input => {
    total += parseFloat(input.value) || 0;
  });
  totalBudgetInput.value = total.toFixed(2);
}

bucketInputs.forEach(input => {
  input.addEventListener('input', updateTotalBudget);
});
