document.addEventListener("DOMContentLoaded", () => {
  let storyId = null;
  let decisionCount = 0;

  const generateBtn = document.getElementById("generate");
  const promptInput = document.getElementById("prompt");

  const storySection = document.getElementById("storySection");
  const chatSection = document.getElementById("chatSection");

  const titleElem = document.getElementById("title");
  const charactersElem = document.getElementById("characters");
  const storyElem = document.getElementById("story");
  const optionsElem = document.getElementById("options");

  const characterSelect = document.getElementById("characterSelect");
  const questionInput = document.getElementById("characterQuestion");
  const askButton = document.getElementById("askCharacter");
  const characterReply = document.getElementById("characterReply");

  generateBtn.addEventListener("click", async () => {
    const inputText = promptInput.value.trim();
    if (!inputText) {
      alert("¡Escribe algo primero! 😊");
      return;
    }

    storyElem.textContent = "Generando historia mágica... 🧠✨";
    storySection.classList.remove("hidden");
    chatSection.classList.add("hidden");
    optionsElem.innerHTML = "";
    characterReply.textContent = "";
    characterReply.classList.add("hidden");
    decisionCount = 0;

    try {
      const response = await fetch(
        "https://us-central1-cuenta-cuentos-463600.cloudfunctions.net/create-story",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt: inputText })
        }
      );

      const data = await response.json();
      storyId = data.id;
      updateStoryUI(data);
    } catch (error) {
      storyElem.textContent = "¡Uy! Ocurrió un error. 😢";
      console.error("Error al generar la historia:", error);
    }
  });

  function updateStoryUI(data) {
    titleElem.textContent = `Título: ${data.title}`;
    charactersElem.textContent = `Personajes: ${data.characters.join(", ")}`;
    storyElem.textContent = data.story;
    optionsElem.innerHTML = "";
    chatSection.classList.remove("hidden");

    if (data.continuations) {
      data.continuations.forEach((option, index) => {
        const container = document.createElement("div");

        const div = document.createElement("div");
        div.textContent = option;
        div.className =
          "bg-white border border-gray-200 rounded-xl p-4 shadow hover:shadow-md hover:bg-orange-50 transition cursor-pointer";
        div.addEventListener("click", () => handleContinue(option));

        container.appendChild(div);

        // Separador menos después de la última opción
        if (index < data.continuations.length - 1) {
          const hr = document.createElement("hr");
          hr.className = "my-2 border-gray-300";
          container.appendChild(hr);
        }

        optionsElem.appendChild(container);
      });
    } else {
      const endMessage = document.createElement("div");
      endMessage.className = "mt-4 text-green-700 font-bold text-center";
      endMessage.textContent = "🎉 ¡Fin de la historia! Esperamos que te haya gustado.";
      optionsElem.appendChild(endMessage);
    }

    characterSelect.innerHTML = `<option value="">Selecciona un personaje</option>`;
    data.characters.forEach((char) => {
      const option = document.createElement("option");
      option.value = char;
      option.textContent = char;
      characterSelect.appendChild(option);
    });
  }

  async function handleContinue(selectedOption) {
    if (!storyId) return;

    storyElem.textContent =
      decisionCount < 4
        ? "Continuando la historia... 🌱"
        : "Concluyendo la historia... 🌟";
    optionsElem.innerHTML = "";
    characterReply.classList.add("hidden");

    try {
      let endpoint = "";
      let body = {};

      if (decisionCount < 4) {
        endpoint =
          "https://us-central1-cuenta-cuentos-463600.cloudfunctions.net/continue-story";
        body = { id: storyId, prompt: selectedOption };
        decisionCount++;
      } else {
        endpoint =
          "https://us-central1-cuenta-cuentos-463600.cloudfunctions.net/end-story";
        body = { id: storyId };
        decisionCount++;
      }

      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });

      const data = await response.json();
      storyId = data.id;
      updateStoryUI(data);
    } catch (error) {
      storyElem.textContent = "Error al continuar la historia 😢";
      console.error("Error al continuar:", error);
    }
  }

  askButton.addEventListener("click", async () => {
    const character = characterSelect.value;
    const question = questionInput.value.trim();

    if (!storyId || !character || !question) {
      alert("Selecciona un personaje y escribe una pregunta.");
      return;
    }

    characterReply.textContent = "Preguntando...";
    characterReply.classList.remove("hidden");

    try {
      const response = await fetch(
        "https://us-central1-cuenta-cuentos-463600.cloudfunctions.net/characters-chat",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            id: storyId,
            character: character,
            question: question
          })
        }
      );

      const data = await response.json();
      characterReply.textContent = `🗣️ ${data.reply}`;
    } catch (error) {
      characterReply.textContent = "Error al obtener respuesta 😢";
      console.error("Error al preguntar al personaje:", error);
    }
  });
});
