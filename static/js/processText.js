function processText() {
    const textInput = document.getElementById('textInput').value;
    const processedTextElement = document.getElementById('processedText');
    processedTextElement.innerText = "Elio is working...";
    processedTextElement.parentNode.classList.add('working'); // Add the effect to the parent of the processed text

    fetch('/process_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({text: textInput}),
    })
    .then(response => response.json())
    .then(data => {
        processedTextElement.innerText = data.processed_text;
        processedTextElement.parentNode.classList.remove('working'); // Remove the effect
    })
    .catch((error) => {
        console.error('Error:', error);
        processedTextElement.parentNode.classList.remove('working'); // Ensure the effect is removed on error as well
    });
}

