export class APIKeyManager {
    constructor() {
        this.container = document.getElementById('api-key-container');
        this.groqInput = document.getElementById('groq-api-key');
        this.saveButton = document.getElementById('save-api-keys');
        
        this.setupEventListeners();
        this.loadSavedKey();
    }

    setupEventListeners() {
        if (this.saveButton) {
            this.saveButton.addEventListener('click', () => this.saveKey());
        }
    }

    loadSavedKey() {
        const savedGroqKey = localStorage.getItem('groqApiKey');
        
        if (this.groqInput && savedGroqKey) {
            this.groqInput.value = savedGroqKey;
        }
    }

    saveKey() {
        if (!this.groqInput) return;

        const groqKey = this.groqInput.value.trim();
        
        if (groqKey) {
            localStorage.setItem('groqApiKey', groqKey);
            alert('Groq API key saved successfully!');
        } else {
            alert('Please enter your Groq API key.');
        }
    }
}