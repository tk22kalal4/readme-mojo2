import { generateQuestion } from './questionGenerator.js';
import { fetchFromAPI } from './api.js';

export class Quiz {
    constructor() {
        this.currentQuestion = null;
        this.score = 0;
        this.timer = null;
        this.timeLimit = 0;
        this.questionLimit = 0;
        this.questionsAnswered = 0;
        this.wrongAnswers = 0;
        this.difficulty = '';
        this.subject = '';
        this.subtopic = '';
        this.topic = '';
    }

    async generateQuestion() {
        if (this.questionLimit && this.questionsAnswered >= this.questionLimit) {
            return null;
        }

        try {
            const question = await generateQuestion(this.subtopic, this.difficulty, this.topic);
            this.currentQuestion = question;
            return question;
        } catch (error) {
            console.error('Error generating question:', error);
            return {
                question: 'Failed to generate question. Please check your API keys and try again.',
                options: ['Error', 'Error', 'Error', 'Error'],
                correctIndex: 0
            };
        }
    }

    async getExplanation(question, options, correctIndex) {
        try {
            const prompt = `
                For this ${this.difficulty.toLowerCase()} level medical question:
                Question: "${question}"
                Options: ${options.map((opt, i) => `${i + 1}. ${opt}`).join(', ')}
                Correct Answer: ${options[correctIndex]}

                Please provide a detailed explanation in this format:
                CORRECT ANSWER (${options[correctIndex]}):
                • Point 1 about why it's correct
                • Point 2 about why it's correct

                WHY OTHER OPTIONS ARE INCORRECT:
                ${options.map((opt, i) => i !== correctIndex ? `${opt}:
                • Point 1 why it's wrong
                • Point 2 why it's wrong` : '').filter(Boolean).join('\n\n')}
            `;

            const explanation = await fetchFromAPI(prompt);

            return {
                text: explanation || 'Explanation not available.'
            };
        } catch (error) {
            console.error('Error getting explanation:', error);
            return {
                text: 'Failed to load explanation. Please check your API keys and try again.'
            };
        }
    }

    async getLearningObjectives(question, options, correctIndex) {
        try {
            const prompt = `
                Based on this medical question and its correct answer:
                Question: "${question}"
                Correct Answer: ${options[correctIndex]}
                
                Generate 3-5 key learning objectives that students should achieve after understanding this question. Format as bullet points.
            `;
            
            const objectives = await fetchFromAPI(prompt);
            return {
                content: `<div class="learning-objectives-list">${objectives}</div>`
            };
        } catch (error) {
            console.error('Error getting learning objectives:', error);
            return {
                content: '<p>Failed to load learning objectives. Please check your API keys and try again.</p>'
            };
        }
    }

    async askDoubt(doubt, questionContext) {
        try {
            const prompt = `
                A student has a doubt about this medical question: "${questionContext}"
                Their doubt is: "${doubt}"
                
                Please provide a clear and educational answer to address their doubt.
            `;
            
            const answer = await fetchFromAPI(prompt);
            return {
                text: answer || 'Unable to answer your doubt at this time.'
            };
        } catch (error) {
            console.error('Error answering doubt:', error);
            return {
                text: 'Failed to get answer. Please check your API keys and try again.'
            };
        }
    }

    getResults() {
        return {
            total: this.questionsAnswered,
            correct: this.score,
            wrong: this.wrongAnswers,
            percentage: this.questionsAnswered > 0 
                ? Math.round((this.score / this.questionsAnswered) * 100) 
                : 0
        };
    }
}