import os
import glob

old_code = '''img {
        max-width: 100%;
        max-height: 400px;
        width: auto;
        height: auto;
        display: block;
        margin: 10px auto;
        border-radius: 4px;
        object-fit: contain;
    }'''

new_code = '''img {
        max-width: 100%;
        max-height: 400px;
        width: auto;
        height: auto;
        display: block;
        margin: 10px auto;
        border-radius: 4px;
        object-fit: contain;
    }
    
    .button-group {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }
    
    .button-group button {
        flex: 1;
        min-width: 120px;
    }
    
    /* For question images specifically */
    .question_images img,
    .explanation_images img {
        max-height: 350px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    /* Mobile-specific adjustments */
    @media (max-width: 640px) {
        .question-nav-btn, .result-nav-btn-grid {
            width: 38px;
            height: 38px;
            font-size: 14px;
        }
        .nav-panel, .results-nav-panel {
            width: 100%;
            max-width: 100%;
            overscroll-behavior: contain;
        }
        .option-btn {
            padding: 12px;
            font-size: 14px;
        }
        .header-text {
            font-size: 1.5rem;
        }
        .subheader-text {
            font-size: 0.875rem;
        }
        .button-group, .result-nav {
            flex-direction: column;
            gap: 0.5rem;
        }
        .result-nav-btn {
            width: 100%;
            text-align: center;
        }
        img {
            max-height: 300px;
        }
        .question_images img,
        .explanation_images img {
            max-height: 250px;
        }
    }
    .video-placeholder {
        width: 400px;
        height: 300px;
        background-color: #e5e7eb;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        margin-top: 10px;
        border-radius: 8px;
        border: 1px solid #d1d5db;
    }
    .play-icon {
        font-size: 40px;
        color: #2c5282;
    }
    .video-loading {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border: 4px solid #e5e7eb;
        border-top: 4px solid #2c5282;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
    
    #normal-explanation {
        /* Ensure explanation section does not overflow */
        overflow-x: auto;
        max-width: 100%;
    }
    
    #normal-explanation table {
        display: block;
        overflow-x: auto;
        min-width: 100%;
        white-space: nowrap;
    }
    
    @keyframes spin {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    body, html {
        padding-bottom: 0 !important;
        margin-bottom: 0 !important;
    }
    #quiz, #results, #instructions {
        padding-bottom: 0 !important;
        margin-bottom: 0 !important;
    }'''

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
