// API Configuration
export let GROQ_API_KEY = localStorage.getItem('groqApiKey') || "";

export const updateAPIKey = (groqKey) => {
    GROQ_API_KEY = groqKey;
    localStorage.setItem('groqApiKey', groqKey);
};

export const getAPIUrl = () => 'https://api.groq.com/openai/v1/chat/completions';

export const DIFFICULTY_LEVELS = {
    'Easy': 'Questions based on standard textbooks like BD Chaurasia, Guyton, Harper, etc.',
    'Medium': 'NEET PG level questions covering both clinical and non-clinical topics',
    'Hard': 'Advanced NEET PG and INICET level clinical questions'
};

export const SUBJECTS = {
    'Anatomy': [
        'Complete Anatomy',
        'Upper Limb',
        'Lower Limb',
        'Histology'
    ],
    'Radiology': [
        'Radiology'
    ],
    'Biochemistry': [
        'Complete Biochemistry'
    ],
    'Pathology': [
        'Complete Pathology'
    ],
    'Pharmacology': [
        'Complete Pharmacology'
    ],
    'Microbiology': [
        'Complete Microbiology'
    ]
};