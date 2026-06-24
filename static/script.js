const optimizeButton = document.getElementById("optimizeBtn");

const promptInput = document.getElementById("userPrompt");

const platformSelect = document.getElementById("platform");

const promptTypeSelect = document.getElementById("promptType");

const outputBox = document.getElementById("optimizedPrompt");

const copyButton = document.getElementById("copyBtn");

const originalScore = document.getElementById("originalScore");

const originalLevel = document.getElementById("originalLevel");

const optimizedScore = document.getElementById("optimizedScore");

const optimizedLevel = document.getElementById("optimizedLevel");

const scoreImprovement = document.getElementById("scoreImprovement");

const improvementList = document.getElementById("improvementList");



let isOptimizing = false;



async function optimizePrompt() {

    if (isOptimizing) {

        return;

    }

    const prompt = promptInput.value.trim();

    if (prompt === "") {

        outputBox.textContent = "Please enter a prompt before optimizing.";

        outputBox.classList.remove("fade-in");

        void outputBox.offsetWidth;

        outputBox.classList.add("fade-in");

        return;

    }

    isOptimizing = true;

    optimizeButton.disabled = true;

    copyButton.disabled = true;

    document.body.style.cursor = "wait";

    optimizeButton.innerHTML = "⏳ Optimizing...";

    outputBox.textContent = "Generating an optimized prompt using Gemini AI...";

    outputBox.classList.remove("fade-in");

    originalScore.textContent = "...";
    originalLevel.textContent = "Analyzing";

    optimizedScore.textContent = "...";
    optimizedLevel.textContent = "Waiting";

    scoreImprovement.textContent = "...";

    improvementList.innerHTML = "<li>Analyzing your prompt...</li>";

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

        if (!response.ok || !data.success) {

            throw new Error(data.message);

        }

        outputBox.textContent = data.optimized_prompt;

        outputBox.classList.remove("fade-in");

        void outputBox.offsetWidth;

        outputBox.classList.add("fade-in");

        originalScore.textContent = data.original_score;

        originalLevel.textContent = data.original_level;

        optimizedScore.textContent = data.optimized_score;

        optimizedLevel.textContent = data.optimized_level;

        const improvement = data.score_improvement;

        scoreImprovement.textContent =
            improvement >= 0 ? `+${improvement}` : improvement;

        improvementList.innerHTML = "";

        data.improvements.forEach(item => {

            const li = document.createElement("li");

            li.textContent = item;

            improvementList.appendChild(li);

        });

        optimizeButton.innerHTML = "✔ Optimized";

    }

    catch (error) {

        outputBox.textContent =
            "Unable to optimize the prompt.\n\nPossible reasons:\n\n• Gemini API is temporarily busy.\n• Internet connection issue.\n• Invalid API key.\n\nPlease try again.";

        console.error(error);

        optimizeButton.innerHTML = "Try Again";

    }

    finally {

        isOptimizing = false;

        document.body.style.cursor = "default";

        copyButton.disabled = false;

        setTimeout(() => {

            optimizeButton.disabled = false;

            optimizeButton.innerHTML = "Optimize Prompt";

        }, 1500);

    }

}



optimizeButton.addEventListener("click", optimizePrompt);



promptInput.addEventListener("keydown", function (event) {

    if (event.ctrlKey && event.key === "Enter") {

        event.preventDefault();

        optimizePrompt();

    }

});



copyButton.addEventListener("click", async () => {

    const text = outputBox.textContent.trim();

    if (

        text === "" ||

        text === "Your optimized prompt will appear here..." ||

        text === "Generating an optimized prompt using Gemini AI..." ||

        text === "Please enter a prompt before optimizing."

    ) {

        return;

    }

    try {

        await navigator.clipboard.writeText(text);

        copyButton.innerHTML = "✔ Copied";

        copyButton.disabled = true;

        setTimeout(() => {

            copyButton.innerHTML = "Copy";

            copyButton.disabled = false;

        }, 2000);

    }

    catch (error) {

        console.error(error);

    }

});