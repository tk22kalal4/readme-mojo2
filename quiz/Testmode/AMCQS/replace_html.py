import os
import glob

old_code = '''&lt;li class=&quot;flex items-center gap-3&quot;&gt;
    &lt;i class=&quot;fa-solid fa-circle-check text-green-500&quot;&gt;&lt;/i&gt;
    Mobile-optimized interface for learning on-the-go
  &lt;/li&gt;
&lt;/ul&gt;
&lt;div class=&quot;mt-6 flex space-x-4 button-group md:flex-row flex-col&quot;&gt;
  &lt;button class=&quot;bg-[#2c5281] text-white px-6 py-2 rounded-lg hover:bg-[#2c5281] transition&quot; id=&quot;start-test&quot;&gt;Start Test&lt;/button&gt;
&lt;/div&gt;
&lt;div class=&quot;error-message hidden&quot; id=&quot;error-message&quot;&gt;&lt;/div&gt;
&lt;/div&gt;
&lt;/section&gt;'''

new_code = '''&lt;li class=&quot;flex items-center gap-3&quot;&gt;
    &lt;i class=&quot;fa-solid fa-circle-check text-green-500&quot;&gt;&lt;/i&gt;
    Mobile-optimized interface for learning on-the-go
  &lt;/li&gt;
&lt;/ul&gt;
&lt;div class=&quot;mt-6 flex space-x-4 button-group md:flex-row flex-col&quot;&gt;
  &lt;button class=&quot;bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-[#2c5281] transition&quot; id=&quot;start-normal-mode&quot;&gt;Normal Mode&lt;/button&gt;     
  &lt;button class=&quot;bg-[#2c5281] text-white px-6 py-2 rounded-lg hover:bg-[#2c5281] transition&quot; id=&quot;start-test&quot;&gt;Test Mode&lt;/button&gt;
 &lt;!-- Add this button in the instructions section --&gt;
&lt;/div&gt;
&lt;div class=&quot;error-message hidden&quot; id=&quot;error-message&quot;&gt;&lt;/div&gt;
&lt;/div&gt;
&lt;/section&gt;
&lt;!-- Normal Mode Section --&gt;
&lt;section class=&quot;container mx-auto px-4 md:px-6 pt-4 md:pt-6 pb-1 hidden section-transition&quot; id=&quot;normal-mode&quot;&gt;
  &lt;div class=&quot;bg-white rounded-lg shadow-md p-4 md:p-6&quot;&gt;
    &lt;h2 class=&quot;text-lg font-semibold mb-4&quot; id=&quot;normal-question-number&quot;&gt;Question &lt;span&gt;1&lt;/span&gt; of 4&lt;/h2&gt;
    &lt;!-- Question Content --&gt;
    &lt;div class=&quot;mb-6&quot; id=&quot;normal-question-content&quot;&gt;
      &lt;p class=&quot;text-gray-800 mb-4&quot; id=&quot;normal-question-text&quot;&gt;&lt;/p&gt;
      &lt;div class=&quot;flex flex-wrap gap-4 mb-4&quot; id=&quot;normal-question-images&quot;&gt;&lt;/div&gt;
      &lt;div class=&quot;space-y-3&quot; id=&quot;normal-options&quot;&gt;&lt;/div&gt;
    &lt;/div&gt;
    &lt;!-- Explanation Section (initially hidden) --&gt;
    &lt;div class=&quot;hidden mt-6 p-4 bg-gray-100 rounded-lg&quot; id=&quot;normal-explanation&quot;&gt;
      &lt;h3 class=&quot;font-semibold mb-2&quot;&gt;Explanation:&lt;/h3&gt;
      &lt;div id=&quot;normal-explanation-content&quot;&gt;&lt;/div&gt;
      &lt;div class=&quot;flex flex-wrap gap-4 mt-4&quot; id=&quot;normal-explanation-images&quot;&gt;&lt;/div&gt;
    &lt;/div&gt;
    &lt;!-- Navigation Buttons --&gt;
    &lt;div class=&quot;flex justify-between items-center mt-6&quot;&gt;
      &lt;button class=&quot;bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-[#2c5281] transition&quot; id=&quot;normal-previous-btn&quot; disabled&gt;Previous&lt;/button&gt;      
      &lt;button class=&quot;bg-transparent text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 transition flex items-center gap-1&quot; id=&quot;normal-nav-toggle&quot;&gt;
        Question 🧭
      &lt;/button&gt;
      &lt;button class=&quot;bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-[#2c5281] transition&quot; id=&quot;normal-next-btn&quot;&gt;Next Question&lt;/button&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/section&gt;

&lt;!-- Normal Mode Results Section --&gt;
&lt;section class=&quot;container mx-auto px-4 md:px-6 pt-4 md:pt-6 pb-1 hidden section-transition&quot; id=&quot;normal-mode-results&quot;&gt;
  &lt;div class=&quot;bg-white rounded-lg shadow-md p-4 md:p-6&quot;&gt;
    &lt;h2 class=&quot;text-xl font-semibold mb-4&quot;&gt;Normal Mode Results&lt;/h2&gt;
    &lt;p class=&quot;text-lg mb-2&quot;&gt;&lt;strong&gt;Correct:&lt;/strong&gt; &lt;span id=&quot;normal-correct-count&quot;&gt;0&lt;/span&gt;&lt;/p&gt;
    &lt;p class=&quot;text-lg mb-2&quot;&gt;&lt;strong&gt;Wrong:&lt;/strong&gt; &lt;span id=&quot;normal-wrong-count&quot;&gt;0&lt;/span&gt;&lt;/p&gt;
    &lt;p class=&quot;text-lg mb-4&quot;&gt;&lt;strong&gt;Total Questions:&lt;/strong&gt; &lt;span id=&quot;normal-total-count&quot;&gt;0&lt;/span&gt;&lt;/p&gt;
    &lt;div class=&quot;flex space-x-4 button-group md:flex-row flex-col mt-6&quot;&gt;
      &lt;button class=&quot;bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition&quot; onclick=&quot;restartNormalMode()&quot;&gt;Try Again&lt;/button&gt;
      &lt;button class=&quot;bg-transparent text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 transition flex items-center gap-1&quot; id=&quot;normal-results-nav-toggle&quot;&gt;
        Results 🧭
      &lt;/button&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/section&gt;'''

# Process all HTML files
for filepath in glob.glob('*.html'):
    try:
        # Try UTF-8 first
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        try:
            # Try latin-1 if UTF-8 fails
            with open(filepath, 'r', encoding='latin-1') as file:
                content = file.read()
        except:
            print(f'Skipped (encoding error): {filepath}')
            continue
    
    # Replace the code
    if old_code in content:
        content = content.replace(old_code, new_code)
        
        # Write back with UTF-8 encoding
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f'Updated: {filepath}')
        except:
            print(f'Failed to write: {filepath}')
    else:
        print(f'Pattern not found in: {filepath}')

print('\nAll files processed!')
