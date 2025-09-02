// API Configuration
export const getGroqAPIKey = () => localStorage.getItem('groqApiKey') || "";

export const updateAPIKey = (groqKey) => {
    localStorage.setItem('groqApiKey', groqKey);
};

export const getAPIUrl = () => 'https://api.groq.com/openai/v1/chat/completions';

export const DIFFICULTY_LEVELS = {
    'Easy': 'Diverse non-clinical NEET PG questions ranging from simple recall, definitions, and surface-level facts to slightly deeper concepts, ensuring variety (non-repetitive) while testing broad coverage of fundamentals',
    'Medium': 'Diverse NEET PG level questions covering both clinical and non-clinical topics, ensuring variety (non-repetitive) with a balance of case-based, applied, and concept-testing questions across multiple subjects for broad coverage',
    'Hard': 'Diverse advanced NEET PG and INICET level clinical questions, ensuring variety (non-repetitive) with challenging, case-based, integrative, and multi-step reasoning questions that cover broad and complex topics across specialties'
};

export const SUBJECTS = {
    'Anatomy': [
        'Complete Anatomy',
        'Upper Limb',
        'Lower Limb',
        'Histology'
    ],
    'Pediatrics': [
    'Acyanotic Congenital Heart Diseases',
    'Apgar Score And Neonatal Resuscitation',
    'Basics Of Neonatology And Routine Newborn Care',
    'Childhood Respiratory Disorders',
    'Chromosomal Disorders',
    'Congenital Adrenal Hyperplasia And Related Diso',
    'Cyanotic Congenital Heart Diseases',
    'Deficiency Of Fat Soluble Vitamins',
    'Deficiency Of Water Soluble Vitamins Trace El',
    'Developmental Milestones',
    'Diseases In Neonates Requiring Special Care',
    'Disorders Of Newborn',
    'Disorders Of Puberty',
    'Disorders Of Thyroid',
    'Disorders Of The Liver',
    'Disorders Of The Nervous System',
    'Disorders Of The Pituitary Gland',
    'Facets Of Growth And Development',
    'Fetal Circulation',
    'Fluid And Electrolyte Disorders',
    'Measles Mumps Rubella And Other Viral Infections',
    'Medical Gi Disorders',
    'Mendelian And Non Mendelian Disorders',
    'Metabolic Disorders Of Amino Acids',
    'Metabolic Disorders Of Urea Cycle Complex Mole',
    'Musculoskeletal Disorders',
    'Neonatal Respiratory Disorders',
    'Nutrition And Breastfeeding',
    'Paediatric Hemato Oncology',
    'Paediatric Rheumatology',
    'Pediatric Anemias',
    'Pediatric Bacterial And Parasitic Infections',
    'Pediatric Hematology Introduction Bleeding',
    'Pediatric Nephrology',
    'Pediatric Urology',
    'Polio And Aids',
    'Protein Energy Malnutrition',
    'Solid Neoplasms Of Childhood',
    'Surgical Gi Disorders'
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
