
// Chapter loading and management
const ChapterManager = {
  async loadChapters() {
    try {
      // Show loading indicator
      this.showLoading(true);

      // Get the manifest file for the selected platform
      const manifest = await this.getManifest();
      const chapters = manifest[QuizState.selectedSubject] || [];

      // Get all files in the subject directory
      const directoryFiles = await this.getDirectoryFiles();

      // Match chapters from the manifest with actual files
      const matchedChapters = this.matchChapters(chapters, directoryFiles);

      // Display the chapters in the correct order
      this.displayChapters(matchedChapters);
    } catch (error) {
      console.error('Error loading chapters:', error);
      // Display an error message to the user
      const chapterList = document.getElementById('chapter-list');
      chapterList.innerHTML = '<p>Error loading chapters. Please try again later.</p>';
    } finally {
      // Hide loading indicator
      this.showLoading(false);
    }
  },

  async getManifest() {
    try {
      const response = await fetch(`quiz/${QuizState.selectedPlatform}/manifest.json`);
      if (!response.ok) {
        throw new Error(`Failed to load manifest for ${QuizState.selectedPlatform}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching manifest:', error);
      return {}; // Return empty object on error
    }
  },

  async getDirectoryFiles() {
    try {
      // This is a placeholder for an API endpoint that lists files in a directory.
      // You will need to implement this on your server.
      // For now, we will simulate this by fetching all files from the project listing.
      const response = await fetch('/files.json'); // This should be your server endpoint
      if (!response.ok) {
        throw new Error('Failed to load directory files');
      }
      const allFiles = await response.json();

      // Filter files for the current platform and subject
      const prefix = `quiz/${QuizState.selectedPlatform}/${QuizState.selectedSubject}/`;
      return allFiles
        .filter(file => file.startsWith(prefix))
        .map(file => file.substring(prefix.length));

    } catch (error) {
      console.error('Error fetching directory files:', error);
      return []; // Return empty array on error
    }
  },

  matchChapters(chapters, directoryFiles) {
    return chapters.map(chapter => {
      const manifestFile = chapter.file;
      let matchedFile = this.findBestMatch(manifestFile, directoryFiles);
      return {
        name: chapter.name,
        filename: matchedFile || manifestFile, // Fallback to manifest file if no match found
        available: !!matchedFile // Flag to indicate if the file is available
      };
    });
  },

  // Fuzzy matching to find the best file match
  findBestMatch(manifestFile, directoryFiles) {
    if (directoryFiles.includes(manifestFile)) {
      return manifestFile;
    }

    let bestMatch = null;
    let highestScore = 0;

    for (const dirFile of directoryFiles) {
      const score = this.calculateSimilarity(manifestFile, dirFile);
      if (score > highestScore) {
        highestScore = score;
        bestMatch = dirFile;
      }
    }

    // You can set a threshold for the match score
    return highestScore > 0.7 ? bestMatch : null;
  },

  // Simple string similarity calculation (Jaro-Winkler distance)
  calculateSimilarity(s1, s2) {
      let m = 0;
      const range = Math.floor(Math.max(s1.length, s2.length) / 2) - 1;
      const s1Matches = new Array(s1.length).fill(false);
      const s2Matches = new Array(s2.length).fill(false);

      for (let i = 0; i < s1.length; i++) {
          const start = Math.max(0, i - range);
          const end = Math.min(i + range + 1, s2.length);
          for (let j = start; j < end; j++) {
              if (!s2Matches[j] && s1[i] === s2[j]) {
                  s1Matches[i] = true;
                  s2Matches[j] = true;
                  m++;
                  break;
              }
          }
      }

      if (m === 0) return 0;

      let t = 0;
      let k = 0;
      for (let i = 0; i < s1.length; i++) {
          if (s1Matches[i]) {
              while (!s2Matches[k]) k++;
              if (s1[i] !== s2[k]) t++;
              k++;
          }
      }
      t /= 2;

      const jaro = (m / s1.length + m / s2.length + (m - t) / m) / 3;

      // Winkler modification
      let p = 0;
      const l = Math.min(s1.length, s2.length);
      while (p < l && s1[p] === s2[p]) p++;

      return jaro + p * 0.1 * (1 - jaro);
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
      if (chapter.available) {
        button.onclick = () => this.selectChapter(chapter.filename, chapter.name);
      } else {
        button.disabled = true;
        button.title = "Chapter not available";
      }
      chapterList.appendChild(button);
    });
  },

  async selectChapter(filename, chapterName) {
    QuizState.selectedChapter = filename;
    
    try {
      this.showLoading(true);
      const response = await fetch(`quiz/${QuizState.selectedPlatform}/${QuizState.selectedSubject}/${filename}`);
      if (!response.ok) {
        throw new Error('Failed to load chapter data');
      }
      
      const data = await response.json();
      QuizState.questions = data.questions || [];
      
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
    } finally {
        this.showLoading(false);
    }
  },
  
  showLoading(isLoading) {
      const loadingIndicator = document.getElementById('loading-indicator'); // You'll need to add this to your HTML
      if (loadingIndicator) {
          loadingIndicator.style.display = isLoading ? 'block' : 'none';
      }
  }
};

// Export for global access
window.ChapterManager = ChapterManager;
