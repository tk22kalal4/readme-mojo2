
// Chapter loading and management
const ChapterManager = {
  async loadChapters() {
    try {
      // Load chapters for the selected platform and subject
      const knownFiles = await this.getKnownFiles();
      this.displayChapters(knownFiles);
    } catch (error) {
      console.error('Error loading chapters:', error);
      // Fallback to known files
      const knownFiles = await this.getKnownFiles();
      this.displayChapters(knownFiles);
    }
  },

  async getKnownFiles() {
    const knownFiles = [];
    
    // Get actual files from the directory based on platform and subject
    try {
      // Try to fetch directory listing or known file patterns
      const commonPatterns = [
        '-Previous_Year_Questions.json',
        '_Previous_Year_Questions.json', 
        '-Questions.json',
        '_Questions.json'
      ];
      
      // Subject-specific chapter names that are likely to exist
      const commonChapters = await this.getSubjectChapters(QuizState.selectedSubject);
      
      for (const chapter of commonChapters) {
        for (const pattern of commonPatterns) {
          const filename = chapter + pattern;
          try {
            const response = await fetch(`quiz/${QuizState.selectedPlatform}/${QuizState.selectedSubject}/${filename}`);
            if (response.ok) {
              const data = await response.json();
              if (data.questions && data.questions.length > 0) {
                knownFiles.push({
                  name: data.chapter || chapter.replace(/_/g, ' '),
                  filename: filename
                });
              }
            }
          } catch (error) {
            // Continue to next file
          }
        }
      }
      
      // If no files found, try a few more generic patterns
      if (knownFiles.length === 0) {
        const genericFiles = [
          `${QuizState.selectedSubject}-Previous_Year_Questions.json`,
          `${QuizState.selectedSubject.charAt(0).toUpperCase() + QuizState.selectedSubject.slice(1)}-Previous_Year_Questions.json`
        ];
        
        for (const file of genericFiles) {
          try {
            const response = await fetch(`quiz/${QuizState.selectedPlatform}/${QuizState.selectedSubject}/${file}`);
            if (response.ok) {
              const data = await response.json();
              if (data.questions && data.questions.length > 0) {
                knownFiles.push({
                  name: data.chapter || file.replace('.json', ''),
                  filename: file
                });
              }
            }
          } catch (error) {
            // Continue
          }
        }
      }
      
    } catch (error) {
      console.error('Error scanning for files:', error);
    }
    
    return knownFiles;
  },

  async getSubjectChapters(subject) {
    // Define common chapters for each subject
    const subjectChapters = {
      anatomy: ['Introduction', 'Upper_Limb', 'Lower_Limb', 'Head_and_Neck', 'Thorax', 'Abdomen', 'Pelvis', 'Back', 'Neuroanatomy', 'Miscellaneous'],
      physiology: ['General_Physiology', 'Blood', 'CVS', 'Respiratory', 'Renal', 'GIT', 'Endocrine', 'Reproductive', 'Nervous_System', 'Special_Senses'],
      pathology: ['General_Pathology', 'Systemic_Pathology', 'Hematology', 'Clinical_Pathology'],
      pharmacology: ['General_Pharmacology', 'ANS', 'CVS', 'CNS', 'Respiratory', 'GIT', 'Endocrine', 'Chemotherapy'],
      microbiology: ['General_Microbiology', 'Bacteriology', 'Virology', 'Mycology', 'Parasitology', 'Immunology'],
      biochemistry: ['Proteins', 'Carbohydrates', 'Lipids', 'Enzymes', 'Vitamins', 'Minerals', 'Metabolism', 'Molecular_Biology', 'Clinical_Biochemistry', 'Oxidative_Phosphorylation'],
      anaesthesia: ['General_Anaesthesia', 'Regional_Anaesthesia', 'Pharmacology', 'Monitoring', 'Emergency_Medicine', 'Pain_Management', 'Central_Neuraxial_Blockade', 'Perioperative_Fluids', 'Anaesthesia_Circuits', 'Demonstration'],
      dermatology: ['Basic_Dermatology', 'Inflammatory_Disorders', 'Infections', 'Tumors', 'Hair_Disorders', 'Nail_Disorders', 'Blistering_Disorders'],
      ent: ['Ear', 'Nose', 'Throat', 'Head_and_Neck'],
      fmt: ['Forensic_Medicine', 'Toxicology'],
      medicine: ['Cardiology', 'Pulmonology', 'Gastroenterology', 'Nephrology', 'Endocrinology', 'Neurology', 'Hematology', 'Infectious_Diseases'],
      obgy: ['Obstetrics', 'Gynecology', 'Reproductive_Endocrinology'],
      ophthalmology: ['Basic_Ophthalmology', 'Anterior_Segment', 'Posterior_Segment', 'Glaucoma', 'Pediatric_Ophthalmology'],
      orthopedics: ['Trauma', 'Spine', 'Upper_Limb', 'Lower_Limb', 'Pediatric_Orthopedics', 'Sports_Medicine'],
      pediatrics: ['Neonatology', 'Growth_and_Development', 'Nutrition', 'Infections', 'Genetic_Disorders'],
      psm: ['Epidemiology', 'Biostatistics', 'Health_Planning', 'Environmental_Health'],
      psychiatry: ['General_Psychiatry', 'Child_Psychiatry', 'Substance_Abuse', 'Personality_Disorders'],
      radiology: ['Plain_Radiography', 'CT', 'MRI', 'Ultrasound', 'Nuclear_Medicine'],
      surgery: ['General_Surgery', 'GI_Surgery', 'Hepatobiliary_Surgery', 'Vascular_Surgery', 'Trauma_Surgery']
    };
    
    return subjectChapters[subject] || ['General', 'Basic', 'Advanced', 'Clinical'];
  },

  displayChapters(chapters) {
    const chapterList = document.getElementById('chapter-list');
    chapterList.innerHTML = '';
    
    if (chapters.length === 0) {
      chapterList.innerHTML = '<p>No chapters available for this combination.</p>';
      return;
    }
    
    chapters.forEach(chapter => {
      const button = document.createElement('button');
      button.className = 'chapter-btn';
      button.innerHTML = `<i class="fas fa-book"></i> ${chapter.name}`;
      button.onclick = () => this.selectChapter(chapter.filename, chapter.name);
      chapterList.appendChild(button);
    });
  },

  async selectChapter(filename, chapterName) {
    QuizState.selectedChapter = filename;
    
    try {
      const response = await fetch(`quiz/${QuizState.selectedPlatform}/${QuizState.selectedSubject}/${filename}`);
      if (!response.ok) {
        throw new Error('Failed to load chapter data');
      }
      
      if (filename.endsWith('.json')) {
        const data = await response.json();
        QuizState.questions = data.questions || [];
      } else {
        // Handle non-JSON files
        const text = await response.text();
        QuizState.questions = this.parseTextToQuestions(text, chapterName);
      }
      
      if (QuizState.questions.length === 0) {
        alert('No questions found in this chapter.');
        return;
      }
      
      // Initialize quiz
      QuizState.currentQuestionIndex = 0;
      QuizState.userAnswers = [];
      QuizState.score = 0;
      QuizState.isReviewMode = false;
      
      NavigationManager.showScreen('quiz-container');
      QuizManager.loadQuestion();
    } catch (error) {
      console.error('Error loading chapter:', error);
      alert('Error loading chapter. Please try again.');
    }
  },

  parseTextToQuestions(text, chapterName) {
    // Simple parser for text files - this is a basic implementation
    // You can enhance this based on the actual format of your text files
    if (text.trim() === 'fg' || text.trim() === 'q') {
      return [{
        q_no: 1,
        question: `Sample question from ${chapterName}`,
        options: {
          A: "Option A",
          B: "Option B", 
          C: "Option C",
          D: "Option D"
        },
        correct_answer: "A",
        explanation: "This is a sample question since the file contains minimal content.",
        chapter_heading: chapterName
      }];
    }
    return [];
  }
};

// Export for global access
window.ChapterManager = ChapterManager;
