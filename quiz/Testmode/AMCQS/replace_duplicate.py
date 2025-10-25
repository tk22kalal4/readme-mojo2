import os
import glob

old_code = '''function initQuiz() {function initQuiz() {'''

new_code = '''function initQuiz() {'''

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
