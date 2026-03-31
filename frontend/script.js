async function generateRecipes() {
    const isVegetarian = document.getElementById("vegetarian").value === "true";
    const ingredientsInput = document.getElementById("ingredients").value;

    const ingredients = ingredientsInput
        .split(",")
        .map(i => i.trim())
        .filter(i => i !== "");

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "Generating...";

    const response = await fetch("http://127.0.0.1:8000/ai-recipes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            is_vegetarian: isVegetarian,
            ingredients: ingredients
        })
    });

    const data = await response.json();

    resultDiv.innerHTML = "";

    data.recipes.forEach(recipe => {
        const div = document.createElement("div");
        div.className = "recipe-card";

        div.innerHTML = `
            <h2>${recipe.title}</h2>
            <p>${recipe.description}</p>

            <p><b>Ingredients:</b></p>
            <ul>
                ${recipe.ingredients.map(i => `<li>${i}</li>`).join("")}
            </ul>

            <p><b>Instructions:</b></p>
            <p>${recipe.instructions}</p>

            <p><b>Cook time:</b> ${recipe.cook_time_minutes} min</p>
            <p><b>Difficulty:</b> ${recipe.difficulty}</p>
        `;

        resultDiv.appendChild(div);
    });
}