import { fetchFromAPI } from './api.js';

export async function generateQuestion(subject, difficulty, topic = '') {
    const difficultyContext = getDifficultyContext(difficulty);
    const topicContext = topic ? ` specifically about ${topic}` : '';
    const prompt = `Generate a ${difficulty.toLowerCase()} level multiple choice question about ${subject}${topicContext}. ${difficultyContext}
        Format the response exactly as follows:
        {
            "question": "The question text here",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "correctIndex": correct_option_index_here
        }`;

    try {
        const response = await fetchFromAPI(prompt);
        // Attempt to extract the JSON string from the response
        const jsonStartIndex = response.indexOf('{');
        const jsonEndIndex = response.lastIndexOf('}');
        let jsonString = response;
        if (jsonStartIndex !== -1 && jsonEndIndex !== -1 && jsonEndIndex > jsonStartIndex) {
            jsonString = response.substring(jsonStartIndex, jsonEndIndex + 1);
        } else {
            throw new Error("Could not find valid JSON in API response.");
        }
        const questionData = JSON.parse(jsonString);
        return questionData;
    } catch (error) {
        console.error('Question Generation Error:', error);
        return {
            question: 'Failed to load question. Please try again.',
            options: ['Error', 'Error', 'Error', 'Error'],
            correctIndex: 0
        };
    }
}

function getDifficultyContext(difficulty) {
    switch (difficulty) {
        case 'Easy':
            return 'Base the question on standard textbooks like BD Chaurasia, Guyton, Harper, etc.';
        case 'Medium':
            return 'Make it a NEET PG level question covering both clinical and non-clinical topics.';
        case 'Hard':
            return 'Make it an advanced NEET PG or INICET level clinical question.';
        default:
            return '';
    }
}
