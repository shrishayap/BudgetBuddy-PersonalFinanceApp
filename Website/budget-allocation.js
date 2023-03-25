const bucketInputs = document.querySelectorAll('input[name^="bucket"]');
const totalBudgetInput = document.getElementById('total-budget');

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

function submittedBudget() {
    let budget = {};
    let categories = ["Education", "Food And Drink", "Health And Fitness", "Recreation", "Fashion And Beauty", "Entertainment", "Home And Vehicle", "Grocery", "Travel", "Miscellaneous"];
    budget.totalBudget = document.getElementById("total-budget").value;
    budget.buckets = {};

    let i = 0;
    document.querySelectorAll('input[name^="bucket"]').forEach(input => {
        budget.buckets[categories[i]] = (parseFloat(input.value) || 0);
        i++;
    });
    console.log(budget);
    return budget;
}
