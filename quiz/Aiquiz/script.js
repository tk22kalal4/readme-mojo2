import { QuizUI } from './js/ui.js';
import { updateAPIKey, getGroqAPIKey } from './js/config.js';

// Initialize the quiz application
document.addEventListener('DOMContentLoaded', () => {
    const quizUI = new QuizUI();
    
    // Handle API key setup
    const saveApiKeysBtn = document.getElementById('save-api-keys');
    const groqApiKeyInput = document.getElementById('groq-api-key');

    // Load saved API key on page load
    const savedGroqKey = getGroqAPIKey();
    if (groqApiKeyInput && savedGroqKey) {
        groqApiKeyInput.value = savedGroqKey;
    }

    if (saveApiKeysBtn) {
        saveApiKeysBtn.addEventListener('click', () => {
            const groqKey = groqApiKeyInput.value.trim();
            
            if (groqKey) {
                updateAPIKey(groqKey);
                alert('Groq API key saved successfully!');
            } else {
                alert('Please enter your Groq API key.');
            }
        });
    }
});
