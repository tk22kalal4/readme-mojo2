import os
import re

def replace_code_in_files():
    # Define the file patterns to search
    file_patterns = [
        '.html', '.css', '.js', '.java', '.txt', 
        '.xml', '.json', '.php', '.py', '.rb', 
        '.ts', '.jsx', '.tsx', '.md'
    ]
    
    # Boundary markers
    start_marker = "function initQuiz() {function initQuiz() {
            try {
                debugLog(&quot;Initializing quiz&quot;);
                loadProgress();
                const startButton = document.getElementById(&#x27;start-test&#x27;);
                if (!startButton) {
                    throw new Error(&quot;Start test button not found&quot;);
                }
                startButton.addEventListener(&#x27;click&#x27;, startQuiz);
                debugLog(&quot;Start test button listener attached&quot;);
                document.getElementById(&#x27;previous-btn&#x27;).addEventListener(&#x27;click&#x27;, showPreviousQuestion);
                document.getElementById(&#x27;next-btn&#x27;).addEventListener(&#x27;click&#x27;, showNextQuestion);
                document.getElementById(&#x27;mark-review&#x27;).addEventListener(&#x27;click&#x27;, toggleMarkForReview);
                document.getElementById(&#x27;nav-toggle&#x27;).addEventListener(&#x27;click&#x27;, toggleNavPanel);
                document.getElementById(&#x27;submit-test&#x27;).addEventListener(&#x27;click&#x27;, showSubmitModal);
                document.getElementById(&#x27;continue-test&#x27;).addEventListener(&#x27;click&#x27;, closeExitModal);
                document.getElementById(&#x27;exit-test&#x27;).addEventListener(&#x27;click&#x27;, () =&gt; {
                    debugLog(&quot;Exiting test&quot;);
                    localStorage.removeItem(`quiz_${quizId}`);
                    window.location.reload();
                });
                document.getElementById(&#x27;cancel-submit&#x27;).addEventListener(&#x27;click&#x27;, closeSubmitModal);
                document.getElementById(&#x27;confirm-submit&#x27;).addEventListener(&#x27;click&#x27;, submitTest);
                document.getElementById(&#x27;take-again&#x27;).addEventListener(&#x27;click&#x27;, () =&gt; {
                    debugLog(&quot;Restarting test&quot;);
                    localStorage.removeItem(`quiz_${quizId}`);
                    window.location.reload();
                });
                document.getElementById(&#x27;close-nav&#x27;).addEventListener(&#x27;click&#x27;, toggleNavPanel);
                document.getElementById(&#x27;nav-filter&#x27;).addEventListener(&#x27;change&#x27;, updateNavPanel);
                document.getElementById(&#x27;prev-result&#x27;).addEventListener(&#x27;click&#x27;, showPreviousResult);
                document.getElementById(&#x27;next-result&#x27;).addEventListener(&#x27;click&#x27;, showNextResult);
                document.getElementById(&#x27;results-nav-toggle&#x27;).addEventListener(&#x27;click&#x27;, toggleResultsNavPanel);
                document.getElementById(&#x27;close-results-nav&#x27;).addEventListener(&#x27;click&#x27;, toggleResultsNavPanel);
                document.getElementById(&#x27;results-nav-filter&#x27;).addEventListener(&#x27;change&#x27;, updateResultsNavPanel);
                
                // Normal Mode event listeners
                document.getElementById(&#x27;start-normal-mode&#x27;).addEventListener(&#x27;click&#x27;, startNormalMode);
                document.getElementById(&#x27;normal-previous-btn&#x27;).addEventListener(&#x27;click&#x27;, showPreviousNormalQuestion);
                document.getElementById(&#x27;normal-next-btn&#x27;).addEventListener(&#x27;click&#x27;, showNextNormalQuestion);
                document.getElementById('normal-nav-toggle').addEventListener('click', function() {
                  toggleNavPanel('normal');
                });
                document.getElementById('normal-results-nav-toggle').addEventListener('click', function() {
                  toggleResultsNavPanel('normal');
                });                
                debugLog(&quot;Quiz initialized successfully&quot;);
            } catch (e) {
                console.error(&quot;Failed to initialize quiz:&quot;, e);
                debugLog(&quot;Failed to initialize quiz: &quot; + e.message);
                document.getElementById(&#x27;error-message&#x27;).innerHTML = &quot;Error initializing quiz. Please check the console for details or contact support.&quot;;
                document.getElementById(&#x27;normal-nav-toggle&#x27;).onclick = function() {
                  toggleNavPanel(&#x27;normal&#x27;);
                };
                document.getElementById(&#x27;normal-results-nav-toggle&#x27;).onclick = function() {
                  toggleResultsNavPanel(&#x27;normal&#x27;);
                };            
            }
        }

        // Start quiz
        function startQuiz() {
            try {
                currentMode = 'quiz'; // Set mode to quiz
                debugLog(&quot;Starting quiz&quot;);
                document.getElementById(&#x27;instructions&#x27;).classList.add(&#x27;hidden&#x27;);
                document.getElementById(&#x27;quiz&#x27;).classList.remove(&#x27;hidden&#x27;);
                showQuestion(currentQuestion);
                startTimer();
                updateNavPanel();
                debugLog(&quot;Quiz started successfully&quot;);
            } catch (e) {
                console.error(&quot;Error starting quiz:&quot;, e);
                debugLog(&quot;Failed to start quiz: &quot; + e.message);
                document.getElementById(&#x27;error-message&#x27;).innerHTML = &quot;Error starting quiz. Please check the console for details or contact support.&quot;;
                document.getElementById(&#x27;error-message&#x27;).classList.remove(&#x27;hidden&#x27;);
                document.getElementById(&#x27;quiz&#x27;).classList.add(&#x27;hidden&#x27;);
                document.getElementById(&#x27;instructions&#x27;).classList.remove(&#x27;hidden&#x27;);
            }
        }

        // Show question
        function showQuestion(index) {
            try {
                debugLog(`Showing question ${index + 1}`);
                currentQuestion = index;
                const q = questions[index];
                if (!q) {
                    throw new Error(`Question ${index} is undefined`);
                }
                document.getElementById(&#x27;question-number&#x27;).innerHTML = `Question &lt;span&gt;${index + 1}&lt;/span&gt; of ${questions.length}`;
                document.getElementById(&#x27;question-text&#x27;).innerHTML = q.text || &quot;No question text available&quot;;
                const imagesDiv = document.getElementById(&#x27;question-images&#x27;);
                imagesDiv.innerHTML = q.question_images &amp;&amp; q.question_images.length &gt; 0
                    ? q.question_images.map(url =&gt; `&lt;img src=&quot;${url}&quot; alt=&quot;Question Image&quot; class=&quot;max-w-full h-auto rounded-lg&quot;&gt;`).join(&#x27;&#x27;)
                    : &#x27;&#x27;;
                const optionsDiv = document.getElementById(&#x27;options&#x27;);
                optionsDiv.innerHTML = q.options &amp;&amp; q.options.length &gt; 0
                    ? q.options.map(opt =&gt; `
                        &lt;button class=&quot;option-btn w-full text-left p-3 border rounded-lg ${answers[index] === opt.label ? &#x27;selected&#x27; : &#x27;&#x27;}&quot; 
                                onclick=&quot;selectOption(${index}, &#x27;${opt.label}&#x27;)&quot; 
                                aria-label=&quot;Option ${opt.label}: ${opt.text}&quot;&gt;
                            ${opt.label}. ${opt.text}
                        &lt;/button&gt;
                    `).join(&#x27;&#x27;)
                    : &#x27;&lt;p class=&quot;text-red-500&quot;&gt;No options available&lt;/p&gt;&#x27;;
                document.getElementById(&#x27;previous-btn&#x27;).disabled = index === 0;
                document.getElementById(&#x27;next-btn&#x27;).disabled = index === questions.length - 1;
                document.getElementById(&#x27;mark-review&#x27;).classList.toggle(&#x27;marked&#x27;, markedForReview[index]);
                updateProgressBar();
                saveProgress();
                window.scrollTo({ top: 0, behavior: &#x27;smooth&#x27; });
                debugLog(`Question ${index + 1} displayed successfully`);
            } catch (e) {
                console.error(&quot;Error displaying question:&quot;, e);
                debugLog(&quot;Failed to display question: &quot; + e.message);
            }
        }

        // Select option
        function selectOption(index, label) {
            try {
                debugLog(`Selecting option ${label} for question ${index + 1}`);
                answers[index] = label;
                const optionsDiv = document.getElementById(&#x27;options&#x27;);
                const optionButtons = optionsDiv.querySelectorAll(&#x27;.option-btn&#x27;);
                optionButtons.forEach(btn =&gt; {
                    const btnLabel = btn.textContent.trim().split(&#x27;.&#x27;)[0];
                    btn.classList.toggle(&#x27;selected&#x27;, btnLabel === label);
                });
                updateNavPanel();
                saveProgress();
                debugLog(`Option ${label} selected for question ${index + 1}`);
            } catch (e) {
                console.error(&quot;Error selecting option:&quot;, e);
                debugLog(&quot;Failed to select option: &quot; + e.message);
            }
        }

        // Toggle mark for review
        function toggleMarkForReview() {
            try {
                debugLog(`Toggling mark for review on question ${currentQuestion + 1}`);
                markedForReview[currentQuestion] = !markedForReview[currentQuestion];
                document.getElementById(&#x27;mark-review&#x27;).classList.toggle(&#x27;marked&#x27;, markedForReview[currentQuestion]);
                updateNavPanel();
                saveProgress();
                debugLog(`Mark for review toggled for question ${currentQuestion + 1}`);
            } catch (e) {
                console.error(&quot;Error marking for review:&quot;, e);
                debugLog(&quot;Failed to mark for review: &quot; + e.message);
            }
        }

        // Navigate to previous question
        function showPreviousQuestion() {
            try {
                debugLog(`Navigating to previous question from ${currentQuestion + 1}`);
                if (currentQuestion &gt; 0) {
                    currentQuestion--;
                    showQuestion(currentQuestion);
                }
            } catch (e) {
                console.error(&quot;Error navigating to previous question:&quot;, e);
                debugLog(&quot;Failed to navigate to previous question: &quot; + e.message);
            }
        }

        // Navigate to next question
        function showNextQuestion() {
            try {
                debugLog(`Navigating to next question from ${currentQuestion + 1}`);
                if (currentQuestion &lt; questions.length - 1) {
                    currentQuestion++;
                    showQuestion(currentQuestion);
                }
            } catch (e) {
                console.error(&quot;Error navigating to next question:&quot;, e);
                debugLog(&quot;Failed to navigate to next question: &quot; + e.message);
            }
        }

        // Handle question navigation click
        function handleQuestionNavClick(index) {
            try {
                debugLog(`Navigating to question ${index + 1} via nav panel`);
                showQuestion(index);
                toggleNavPanel();
            } catch (e) {
                console.error(&quot;Error handling navigation click:&quot;, e);
                debugLog(&quot;Failed to navigate via nav panel: &quot; + e.message);
            }
        }

        // Start timer
        function startTimer() {
            try {
                debugLog(&quot;Starting timer&quot;);
                timerInterval = setInterval(() =&gt; {
                    if (timeRemaining &lt;= 0) {
                        debugLog(&quot;Timer expired, submitting test&quot;);
                        clearInterval(timerInterval);
                        submitTest();
                    } else {
                        timeRemaining--;
                        const minutes = Math.floor(timeRemaining / 60);
                        const seconds = timeRemaining % 60;
                        document.getElementById(&#x27;timer&#x27;).innerHTML = `Time Remaining: &lt;span&gt;${minutes.toString().padStart(2, &#x27;0&#x27;)}:${seconds.toString().padStart(2, &#x27;0&#x27;)}&lt;/span&gt;`;
                        saveProgress();
                    }
                }, 1000);
                debugLog(&quot;Timer started successfully&quot;);
            } catch (e) {
                console.error(&quot;Error starting timer:&quot;, e);
                debugLog(&quot;Failed to start timer: &quot; + e.message);
            }
        }

        // Update progress bar
        function updateProgressBar() {
            try {
                debugLog(&quot;Updating progress bar&quot;);
                const progress = ((currentQuestion + 1) / questions.length) * 100;
                document.getElementById(&#x27;progress-bar&#x27;).style.width = `${progress}%`;
                debugLog(&quot;Progress bar updated&quot;);
            } catch (e) {
                console.error(&quot;Error updating progress bar:&quot;, e);
                debugLog(&quot;Failed to update progress bar: &quot; + e.message);
            }
        }

        // Update quiz navigation panel
        // Update navigation panel (quiz or normal mode)
        function updateNavPanel(mode = 'quiz') {
            try {
                debugLog(&quot;Updating quiz/navigation panel, mode: &quot; + mode);
                const filter = document.getElementById(&#x27;nav-filter&#x27;).value;
                const navGrid = document.getElementById(&#x27;nav-grid&#x27;);
        
                // Use correct arrays for normal mode
                let statusArray = (mode === 'normal') ? normalModeAnswers : answers;
                let markedArray = (mode === 'normal') ? [] : markedForReview; // update if you have markedForReview for normal mode
        
                navGrid.innerHTML = questions.map((_, i) =&gt; {
                    if (filter === &#x27;answered&#x27; &amp;&amp; !statusArray[i]) return &#x27;&#x27;;
                    if (filter === &#x27;unanswered&#x27; &amp;&amp; statusArray[i]) return &#x27;&#x27;;
                    if (filter === &#x27;marked&#x27; &amp;&amp; !markedArray[i]) return &#x27;&#x27;;
                    return `
                        &lt;button class=&quot;question-nav-btn ${statusArray[i] ? &#x27;answered&#x27; : &#x27;unanswered&#x27;} ${markedArray[i] ? &#x27;marked-nav&#x27; : &#x27;&#x27;}&quot;
                                onclick=&quot;${mode === 'normal' ? `showNormalQuestion(${i})` : `handleQuestionNavClick(${i})`}&quot;
                                aria-label=&quot;Go to Question ${i + 1}&quot;&gt;
                            ${i + 1}
                        &lt;/button&gt;
                    `;
                }).join(&#x27;&#x27;);
                debugLog(&quot;Quiz/navigation panel updated&quot;);
            } catch (e) {
                console.error(&quot;Error updating quiz navigation panel:&quot;, e);
                debugLog(&quot;Failed to update quiz navigation panel: &quot; + e.message);
            }
        }
        
        // Update results navigation panel (quiz or normal mode)
        function updateResultsNavPanel(mode = 'quiz') {
            try {
                debugLog(&quot;Updating results navigation panel, mode: &quot; + mode);
                const filter = document.getElementById(&#x27;results-nav-filter&#x27;).value;
                const navGrid = document.getElementById(&#x27;results-nav-grid&#x27;);
        
                let statusArray = (mode === 'normal') ? normalModeAnswers : answers;
                let markedArray = (mode === 'normal') ? [] : markedForReview; // update if you have markedForReview for normal mode
        
                navGrid.innerHTML = questions.map((_, i) =&gt; {
                    if (filter === &#x27;answered&#x27; &amp;&amp; !statusArray[i]) return &#x27;&#x27;;
                    if (filter === &#x27;unanswered&#x27; &amp;&amp; statusArray[i]) return &#x27;&#x27;;
                    if (filter === &#x27;marked&#x27; &amp;&amp; !markedArray[i]) return &#x27;&#x27;;
                    return `
                        &lt;button class=&quot;result-nav-btn-grid ${statusArray[i] ? &#x27;answered&#x27; : &#x27;unanswered&#x27;} ${markedArray[i] ? &#x27;marked-nav&#x27; : &#x27;&#x27;}&quot;
                                onclick=&quot;${mode === 'normal' ? `showNormalResult(${i})` : `handleResultNavClick(${i})`}&quot;
                                aria-label=&quot;Go to Result for Question ${i + 1}&quot;&gt;
                            ${i + 1}
                        &lt;/button&gt;
                    `;
                }).join(&#x27;&#x27;);
                debugLog(&quot;Results navigation panel updated&quot;);
            } catch (e) {
                console.error(&quot;Error updating results navigation panel:&quot;, e);
                debugLog(&quot;Failed to update results navigation panel: &quot; + e.message);
            }
        }
        
        // Toggle quiz navigation panel (quiz or normal mode)
        function toggleNavPanel(mode) {
            try {
                const activeMode = mode || currentMode; // Use currentMode if mode not specified
                debugLog(&quot;Toggling quiz navigation panel, mode: &quot; + activeMode);
                const navPanel = document.getElementById(&#x27;nav-panel&#x27;);
                navPanel.classList.toggle(&#x27;hidden&#x27;);
                if (!navPanel.classList.contains(&#x27;hidden&#x27;)) {
                    updateNavPanel(activeMode);
                }
                debugLog(&quot;Quiz navigation panel toggled&quot;);
            } catch (e) {
                console.error(&quot;Error toggling quiz navigation panel:&quot;, e);
                debugLog(&quot;Failed to toggle quiz navigation panel: &quot; + e.message);
            }
        }
        
        // Toggle results navigation panel (quiz or normal mode)
        function toggleResultsNavPanel(mode) {
            try {
                const activeMode = mode || currentMode; // Use currentMode if mode not specified
                debugLog(&quot;Toggling results navigation panel, mode: &quot; + activeMode);
                const resultsNavPanel = document.getElementById(&#x27;results-nav-panel&#x27;);
                resultsNavPanel.classList.toggle(&#x27;hidden&#x27;);
                if (!resultsNavPanel.classList.contains(&#x27;hidden&#x27;)) {
                    updateResultsNavPanel(activeMode);
                }
                debugLog(&quot;Results navigation panel toggled&quot;);
            } catch (e) {
                console.error(&quot;Error toggling results navigation panel:&quot;, e);
                debugLog(&quot;Failed to toggle results navigation panel: &quot; + e.message);
            }
        }
        function handleResultNavClick(index) {"
    
    # New replacement code
    new_code = """function initQuiz() {function initQuiz() {
            try {
                debugLog(&quot;Initializing quiz&quot;);
                loadProgress();
                const startButton = document.getElementById(&#x27;start-test&#x27;);
                if (!startButton) {
                    throw new Error(&quot;Start test button not found&quot;);
                }
                startButton.addEventListener(&#x27;click&#x27;, startQuiz);
                debugLog(&quot;Start test button listener attached&quot;);
                document.getElementById(&#x27;previous-btn&#x27;).addEventListener(&#x27;click&#x27;, showPreviousQuestion);
                document.getElementById(&#x27;next-btn&#x27;).addEventListener(&#x27;click&#x27;, showNextQuestion);
                document.getElementById(&#x27;mark-review&#x27;).addEventListener(&#x27;click&#x27;, toggleMarkForReview);
                document.getElementById(&#x27;nav-toggle&#x27;).addEventListener(&#x27;click&#x27;, toggleNavPanel);
                document.getElementById(&#x27;submit-test&#x27;).addEventListener(&#x27;click&#x27;, showSubmitModal);
                document.getElementById(&#x27;continue-test&#x27;).addEventListener(&#x27;click&#x27;, closeExitModal);
                document.getElementById(&#x27;exit-test&#x27;).addEventListener(&#x27;click&#x27;, () =&gt; {
                    debugLog(&quot;Exiting test&quot;);
                    localStorage.removeItem(`quiz_${quizId}`);
                    window.location.reload();
                });
                document.getElementById(&#x27;cancel-submit&#x27;).addEventListener(&#x27;click&#x27;, closeSubmitModal);
                document.getElementById(&#x27;confirm-submit&#x27;).addEventListener(&#x27;click&#x27;, submitTest);
                document.getElementById(&#x27;take-again&#x27;).addEventListener(&#x27;click&#x27;, () =&gt; {
                    debugLog(&quot;Restarting test&quot;);
                    localStorage.removeItem(`quiz_${quizId}`);
                    window.location.reload();
                });
                document.getElementById(&#x27;close-nav&#x27;).addEventListener(&#x27;click&#x27;, toggleNavPanel);
                document.getElementById(&#x27;nav-filter&#x27;).addEventListener(&#x27;change&#x27;, updateNavPanel);
                document.getElementById(&#x27;prev-result&#x27;).addEventListener(&#x27;click&#x27;, showPreviousResult);
                document.getElementById(&#x27;next-result&#x27;).addEventListener(&#x27;click&#x27;, showNextResult);
                document.getElementById(&#x27;results-nav-toggle&#x27;).addEventListener(&#x27;click&#x27;, toggleResultsNavPanel);
                document.getElementById(&#x27;close-results-nav&#x27;).addEventListener(&#x27;click&#x27;, toggleResultsNavPanel);
                document.getElementById(&#x27;results-nav-filter&#x27;).addEventListener(&#x27;change&#x27;, updateResultsNavPanel);
                
                // Normal Mode event listeners
                document.getElementById(&#x27;start-normal-mode&#x27;).addEventListener(&#x27;click&#x27;, startNormalMode);
                document.getElementById(&#x27;normal-previous-btn&#x27;).addEventListener(&#x27;click&#x27;, showPreviousNormalQuestion);
                document.getElementById(&#x27;normal-next-btn&#x27;).addEventListener(&#x27;click&#x27;, showNextNormalQuestion);
                document.getElementById('normal-nav-toggle').addEventListener('click', function() {
                  toggleNavPanel('normal');
                });
                document.getElementById('normal-results-nav-toggle').addEventListener('click', function() {
                  toggleResultsNavPanel('normal');
                });                
                debugLog(&quot;Quiz initialized successfully&quot;);
            } catch (e) {
                console.error(&quot;Failed to initialize quiz:&quot;, e);
                debugLog(&quot;Failed to initialize quiz: &quot; + e.message);
                document.getElementById(&#x27;error-message&#x27;).innerHTML = &quot;Error initializing quiz. Please check the console for details or contact support.&quot;;
                document.getElementById(&#x27;normal-nav-toggle&#x27;).onclick = function() {
                  toggleNavPanel(&#x27;normal&#x27;);
                };
                document.getElementById(&#x27;normal-results-nav-toggle&#x27;).onclick = function() {
                  toggleResultsNavPanel(&#x27;normal&#x27;);
                };            
            }
        }

        // Start quiz
        function startQuiz() {
            try {
                currentMode = 'quiz'; // Set mode to quiz
                debugLog(&quot;Starting quiz&quot;);
                document.getElementById(&#x27;instructions&#x27;).classList.add(&#x27;hidden&#x27;);
                document.getElementById(&#x27;quiz&#x27;).classList.remove(&#x27;hidden&#x27;);
                showQuestion(currentQuestion);
                startTimer();
                updateNavPanel();
                debugLog(&quot;Quiz started successfully&quot;);
            } catch (e) {
                console.error(&quot;Error starting quiz:&quot;, e);
                debugLog(&quot;Failed to start quiz: &quot; + e.message);
                document.getElementById(&#x27;error-message&#x27;).innerHTML = &quot;Error starting quiz. Please check the console for details or contact support.&quot;;
                document.getElementById(&#x27;error-message&#x27;).classList.remove(&#x27;hidden&#x27;);
                document.getElementById(&#x27;quiz&#x27;).classList.add(&#x27;hidden&#x27;);
                document.getElementById(&#x27;instructions&#x27;).classList.remove(&#x27;hidden&#x27;);
            }
        }

        // Show question
        function showQuestion(index) {
            try {
                debugLog(`Showing question ${index + 1}`);
                currentQuestion = index;
                const q = questions[index];
                if (!q) {
                    throw new Error(`Question ${index} is undefined`);
                }
                document.getElementById(&#x27;question-number&#x27;).innerHTML = `Question &lt;span&gt;${index + 1}&lt;/span&gt; of ${questions.length}`;
                document.getElementById(&#x27;question-text&#x27;).innerHTML = q.text || &quot;No question text available&quot;;
                const imagesDiv = document.getElementById(&#x27;question-images&#x27;);
                imagesDiv.innerHTML = q.question_images &amp;&amp; q.question_images.length &gt; 0
                    ? q.question_images.map(url =&gt; `&lt;img src=&quot;${url}&quot; alt=&quot;Question Image&quot; class=&quot;max-w-full h-auto rounded-lg&quot;&gt;`).join(&#x27;&#x27;)
                    : &#x27;&#x27;;
                const optionsDiv = document.getElementById(&#x27;options&#x27;);
                optionsDiv.innerHTML = q.options &amp;&amp; q.options.length &gt; 0
                    ? q.options.map(opt =&gt; `
                        &lt;button class=&quot;option-btn w-full text-left p-3 border rounded-lg ${answers[index] === opt.label ? &#x27;selected&#x27; : &#x27;&#x27;}&quot; 
                                onclick=&quot;selectOption(${index}, &#x27;${opt.label}&#x27;)&quot; 
                                aria-label=&quot;Option ${opt.label}: ${opt.text}&quot;&gt;
                            ${opt.label}. ${opt.text}
                        &lt;/button&gt;
                    `).join(&#x27;&#x27;)
                    : &#x27;&lt;p class=&quot;text-red-500&quot;&gt;No options available&lt;/p&gt;&#x27;;
                document.getElementById(&#x27;previous-btn&#x27;).disabled = index === 0;
                document.getElementById(&#x27;next-btn&#x27;).disabled = index === questions.length - 1;
                document.getElementById(&#x27;mark-review&#x27;).classList.toggle(&#x27;marked&#x27;, markedForReview[index]);
                updateProgressBar();
                saveProgress();
                window.scrollTo({ top: 0, behavior: &#x27;smooth&#x27; });
                debugLog(`Question ${index + 1} displayed successfully`);
            } catch (e) {
                console.error(&quot;Error displaying question:&quot;, e);
                debugLog(&quot;Failed to display question: &quot; + e.message);
            }
        }

        // Select option
        function selectOption(index, label) {
            try {
                debugLog(`Selecting option ${label} for question ${index + 1}`);
                answers[index] = label;
                const optionsDiv = document.getElementById(&#x27;options&#x27;);
                const optionButtons = optionsDiv.querySelectorAll(&#x27;.option-btn&#x27;);
                optionButtons.forEach(btn =&gt; {
                    const btnLabel = btn.textContent.trim().split(&#x27;.&#x27;)[0];
                    btn.classList.toggle(&#x27;selected&#x27;, btnLabel === label);
                });
                updateNavPanel();
                saveProgress();
                debugLog(`Option ${label} selected for question ${index + 1}`);
            } catch (e) {
                console.error(&quot;Error selecting option:&quot;, e);
                debugLog(&quot;Failed to select option: &quot; + e.message);
            }
        }

        // Toggle mark for review
        function toggleMarkForReview() {
            try {
                debugLog(`Toggling mark for review on question ${currentQuestion + 1}`);
                markedForReview[currentQuestion] = !markedForReview[currentQuestion];
                document.getElementById(&#x27;mark-review&#x27;).classList.toggle(&#x27;marked&#x27;, markedForReview[currentQuestion]);
                updateNavPanel();
                saveProgress();
                debugLog(`Mark for review toggled for question ${currentQuestion + 1}`);
            } catch (e) {
                console.error(&quot;Error marking for review:&quot;, e);
                debugLog(&quot;Failed to mark for review: &quot; + e.message);
            }
        }

        // Navigate to previous question
        function showPreviousQuestion() {
            try {
                debugLog(`Navigating to previous question from ${currentQuestion + 1}`);
                if (currentQuestion &gt; 0) {
                    currentQuestion--;
                    showQuestion(currentQuestion);
                }
            } catch (e) {
                console.error(&quot;Error navigating to previous question:&quot;, e);
                debugLog(&quot;Failed to navigate to previous question: &quot; + e.message);
            }
        }

        // Navigate to next question
        function showNextQuestion() {
            try {
                debugLog(`Navigating to next question from ${currentQuestion + 1}`);
                if (currentQuestion &lt; questions.length - 1) {
                    currentQuestion++;
                    showQuestion(currentQuestion);
                }
            } catch (e) {
                console.error(&quot;Error navigating to next question:&quot;, e);
                debugLog(&quot;Failed to navigate to next question: &quot; + e.message);
            }
        }

        // Handle question navigation click
        function handleQuestionNavClick(index) {
            try {
                debugLog(`Navigating to question ${index + 1} via nav panel`);
                showQuestion(index);
                toggleNavPanel();
            } catch (e) {
                console.error(&quot;Error handling navigation click:&quot;, e);
                debugLog(&quot;Failed to navigate via nav panel: &quot; + e.message);
            }
        }

        // Start timer
        function startTimer() {
            try {
                debugLog(&quot;Starting timer&quot;);
                timerInterval = setInterval(() =&gt; {
                    if (timeRemaining &lt;= 0) {
                        debugLog(&quot;Timer expired, submitting test&quot;);
                        clearInterval(timerInterval);
                        submitTest();
                    } else {
                        timeRemaining--;
                        const minutes = Math.floor(timeRemaining / 60);
                        const seconds = timeRemaining % 60;
                        document.getElementById(&#x27;timer&#x27;).innerHTML = `Time Remaining: &lt;span&gt;${minutes.toString().padStart(2, &#x27;0&#x27;)}:${seconds.toString().padStart(2, &#x27;0&#x27;)}&lt;/span&gt;`;
                        saveProgress();
                    }
                }, 1000);
                debugLog(&quot;Timer started successfully&quot;);
            } catch (e) {
                console.error(&quot;Error starting timer:&quot;, e);
                debugLog(&quot;Failed to start timer: &quot; + e.message);
            }
        }

        // Update progress bar
        function updateProgressBar() {
            try {
                debugLog(&quot;Updating progress bar&quot;);
                const progress = ((currentQuestion + 1) / questions.length) * 100;
                document.getElementById(&#x27;progress-bar&#x27;).style.width = `${progress}%`;
                debugLog(&quot;Progress bar updated&quot;);
            } catch (e) {
                console.error(&quot;Error updating progress bar:&quot;, e);
                debugLog(&quot;Failed to update progress bar: &quot; + e.message);
            }
        }

        // Update quiz navigation panel
        // Update navigation panel (quiz or normal mode)
        function updateNavPanel(mode = 'quiz') {
            try {
                debugLog(&quot;Updating quiz/navigation panel, mode: &quot; + mode);
                const filter = document.getElementById(&#x27;nav-filter&#x27;).value;
                const navGrid = document.getElementById(&#x27;nav-grid&#x27;);
        
                // Use correct arrays for normal mode
                let statusArray = (mode === 'normal') ? normalModeAnswers : answers;
                let markedArray = (mode === 'normal') ? [] : markedForReview; // update if you have markedForReview for normal mode
        
                navGrid.innerHTML = questions.map((_, i) =&gt; {
                    if (filter === &#x27;answered&#x27; &amp;&amp; !statusArray[i]) return &#x27;&#x27;;
                    if (filter === &#x27;unanswered&#x27; &amp;&amp; statusArray[i]) return &#x27;&#x27;;
                    if (filter === &#x27;marked&#x27; &amp;&amp; !markedArray[i]) return &#x27;&#x27;;
                    return `
                        &lt;button class=&quot;question-nav-btn ${statusArray[i] ? &#x27;answered&#x27; : &#x27;unanswered&#x27;} ${markedArray[i] ? &#x27;marked-nav&#x27; : &#x27;&#x27;}&quot;
                                onclick=&quot;${mode === 'normal' ? `showNormalQuestion(${i})` : `handleQuestionNavClick(${i})`}&quot;
                                aria-label=&quot;Go to Question ${i + 1}&quot;&gt;
                            ${i + 1}
                        &lt;/button&gt;
                    `;
                }).join(&#x27;&#x27;);
                debugLog(&quot;Quiz/navigation panel updated&quot;);
            } catch (e) {
                console.error(&quot;Error updating quiz navigation panel:&quot;, e);
                debugLog(&quot;Failed to update quiz navigation panel: &quot; + e.message);
            }
        }
        
        // Update results navigation panel (quiz or normal mode)
        function updateResultsNavPanel(mode = 'quiz') {
            try {
                debugLog(&quot;Updating results navigation panel, mode: &quot; + mode);
                const filter = document.getElementById(&#x27;results-nav-filter&#x27;).value;
                const navGrid = document.getElementById(&#x27;results-nav-grid&#x27;);
        
                let statusArray = (mode === 'normal') ? normalModeAnswers : answers;
                let markedArray = (mode === 'normal') ? [] : markedForReview; // update if you have markedForReview for normal mode
        
                navGrid.innerHTML = questions.map((_, i) =&gt; {
                    if (filter === &#x27;answered&#x27; &amp;&amp; !statusArray[i]) return &#x27;&#x27;;
                    if (filter === &#x27;unanswered&#x27; &amp;&amp; statusArray[i]) return &#x27;&#x27;;
                    if (filter === &#x27;marked&#x27; &amp;&amp; !markedArray[i]) return &#x27;&#x27;;
                    return `
                        &lt;button class=&quot;result-nav-btn-grid ${statusArray[i] ? &#x27;answered&#x27; : &#x27;unanswered&#x27;} ${markedArray[i] ? &#x27;marked-nav&#x27; : &#x27;&#x27;}&quot;
                                onclick=&quot;${mode === 'normal' ? `showNormalResult(${i})` : `handleResultNavClick(${i})`}&quot;
                                aria-label=&quot;Go to Result for Question ${i + 1}&quot;&gt;
                            ${i + 1}
                        &lt;/button&gt;
                    `;
                }).join(&#x27;&#x27;);
                debugLog(&quot;Results navigation panel updated&quot;);
            } catch (e) {
                console.error(&quot;Error updating results navigation panel:&quot;, e);
                debugLog(&quot;Failed to update results navigation panel: &quot; + e.message);
            }
        }
        
        // Toggle quiz navigation panel (quiz or normal mode)
        function toggleNavPanel(mode) {
            try {
                const activeMode = mode || currentMode; // Use currentMode if mode not specified
                debugLog(&quot;Toggling quiz navigation panel, mode: &quot; + activeMode);
                const navPanel = document.getElementById(&#x27;nav-panel&#x27;);
                navPanel.classList.toggle(&#x27;hidden&#x27;);
                if (!navPanel.classList.contains(&#x27;hidden&#x27;)) {
                    updateNavPanel(activeMode);
                }
                debugLog(&quot;Quiz navigation panel toggled&quot;);
            } catch (e) {
                console.error(&quot;Error toggling quiz navigation panel:&quot;, e);
                debugLog(&quot;Failed to toggle quiz navigation panel: &quot; + e.message);
            }
        }
        
        // Toggle results navigation panel (quiz or normal mode)
        function toggleResultsNavPanel(mode) {
            try {
                const activeMode = mode || currentMode; // Use currentMode if mode not specified
                debugLog(&quot;Toggling results navigation panel, mode: &quot; + activeMode);
                const resultsNavPanel = document.getElementById(&#x27;results-nav-panel&#x27;);
                resultsNavPanel.classList.toggle(&#x27;hidden&#x27;);
                if (!resultsNavPanel.classList.contains(&#x27;hidden&#x27;)) {
                    updateResultsNavPanel(activeMode);
                }
                debugLog(&quot;Results navigation panel toggled&quot;);
            } catch (e) {
                console.error(&quot;Error toggling results navigation panel:&quot;, e);
                debugLog(&quot;Failed to toggle results navigation panel: &quot; + e.message);
            }
        }
        function handleResultNavClick(index) {'")
    replace_code_in_files()
