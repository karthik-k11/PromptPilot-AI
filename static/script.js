const optimizeButton = document.getElementById("optimizeBtn");

const promptInput = document.getElementById("userPrompt");

const platformSelect = document.getElementById("platform");

const promptTypeSelect = document.getElementById("promptType");

const outputBox = document.getElementById("optimizedPrompt");

const scoreValue = document.getElementById("scoreValue");

const scoreText = document.getElementById("scoreText");

const improvementList = document.getElementById("improvementList");

const copyButton = document.getElementById("copyBtn");


optimizeButton.addEventListener("click", async () => {

    const prompt = promptInput.value.trim();

    if (prompt === "") {

        alert("Please enter a prompt.");

        return;

    }

    outputBox.textContent = "Optimizing prompt...";

    scoreValue.textContent = "...";

    scoreText.textContent = "Analyzing prompt...";

    improvementList.innerHTML =
        "<li>Analyzing your prompt...</li>";

    optimizeButton.disabled = true;

    optimizeButton.textContent = "Optimizing...";

    try {

        const response = await fetch("/optimize", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                prompt: prompt,

                platform: platformSelect.value,

                prompt_type: promptTypeSelect.value

            })

        });

        const data = await response.json();

        if (data.success) {

            outputBox.textContent = data.optimized_prompt;

            scoreValue.textContent = data.score;

            scoreText.textContent = data.level;

            improvementList.innerHTML = "";

            data.improvements.forEach((item) => {

                const li = document.createElement("li");

                li.textContent = item;

                improvementList.appendChild(li);

            });

        }

        else {

            outputBox.textContent = data.message;

        }

    }

    catch (error) {

        outputBox.textContent = "Something went wrong.";

        console.error(error);

    }

    finally {

        optimizeButton.disabled = false;

        optimizeButton.textContent = "Optimize Prompt";

    }

});


copyButton.addEventListener("click", async () => {

    const text = outputBox.textContent.trim();

    if (
        text === "" ||
        text === "Your optimized prompt will appear here..." ||
        text === "Optimizing prompt..."
    ) {
        return;
    }

    try {

        await navigator.clipboard.writeText(text);

        copyButton.textContent = "Copied!";

        setTimeout(() => {

            copyButton.textContent = "Copy";

        }, 2000);

    }

    catch (error) {

        console.error(error);

    }

});