// API Configuration
export const getGroqAPIKey = () => localStorage.getItem('groqApiKey') || "";

export const updateAPIKey = (groqKey) => {
    localStorage.setItem('groqApiKey', groqKey);
};

export const getAPIUrl = () => 'https://api.groq.com/openai/v1/chat/completions';

export const DIFFICULTY_LEVELS = {
    'Easy': 'Basic recall, non-clinical',
    'Medium': 'Applied, mixed topics',
    'Hard': 'Advanced clinical, case-based'
};

export const SUBJECTS = {
    'Anatomy': [
        'Complete Anatomy',
        'Upper Limb',
        'Lower Limb',
        'Histology'
    ],
export const SUBJECTS = {
    'Anatomy': [
        'Introduction',
        'General Embryology',
        'Histology',
        'Osteology and Arthrology',
        'Neuro Anatomy',
        'Head and Neck',
        'Back Region',
        'Thorax',
        'Upper Limb',
        'Abdomen',
        'Pelvis and Perineum',
        'Lower Limb'
    ],
    'Biochemistry': [
        'Introduction',
        'Carbohydrate Chemistry',
        'Carbohydrate Metabolism',
        'Oxidative Phosphorylation',
        'Lipid Chemistry',
        'Lipid Metabolism',
        'Amino Acids and Proteins Chemistry',
        'Amino Acid and Protein Metabolism',
        'Genetics',
        'Enzymes',
        'Heme Synthesis',
        'Vitamins'
    ],
    'Physiology': [
        'General Physiology',
        'Nerve Muscle Physiology',
        'Cardiovascular System',
        'Blood Physiology',
        'Excretory System',
        'Respiratory System',
        'Gastrointestinal System',
        'The Nervous System',
        'Endocrine and Reproductive System'
    ]
}
    
};
