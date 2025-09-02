/**
 * Enhanced Chapter Loader with flexible filename matching
 * Reduces loading time and handles naming variations
 */
class ChapterLoader {
  constructor() {
    this.cache = new Map();
  }

  /**
   * Normalize filename for flexible matching
   */
  normalizeFilename(filename) {
    return filename
      .toLowerCase()
      .replace(/[_\-\s]+/g, '') // Remove underscores, dashes, spaces
      .replace(/[^a-z0-9]/g, '') // Keep only alphanumeric
      .replace(/\.json$/i, ''); // Remove .json extension
  }

  /**
   * Generate possible filename variations
   */
  generateFilenameVariations(originalFilename) {
    const variations = new Set();
    const baseName = originalFilename.replace(/\.json$/i, '');
    
    // Add original
    variations.add(originalFilename);
    
    // Add with different separators
    [baseName, baseName.toLowerCase(), baseName.toUpperCase()].forEach(name => {
      variations.add(name + '.json');
      variations.add(name.replace(/[\s_-]+/g, '_') + '.json');
      variations.add(name.replace(/[\s_-]+/g, '-') + '.json');
      variations.add(name.replace(/[\s_-]+/g, '') + '.json');
      variations.add(name.replace(/[\s_-]+/g, ' ') + '.json');
    });
    
    return Array.from(variations);
  }

  /**
   * Fast batch check for file existence
   */
  async batchCheckFiles(platform, subject, filenames) {
    const results = new Map();
    const promises = filenames.map(async (filename) => {
      try {
        const response = await fetch(`${platform}/${subject}/${filename}`, { method: 'HEAD' });
        return { filename, exists: response.ok };
      } catch {
        return { filename, exists: false };
      }
    });

    const checks = await Promise.all(promises);
    checks.forEach(({ filename, exists }) => {
      results.set(filename, exists);
    });

    return results;
  }

  /**
   * Find best matching file for a chapter
   */
  async findMatchingFile(platform, subject, expectedFilename, availableFiles = null) {
    const cacheKey = `${platform}/${subject}/${expectedFilename}`;
    
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    // Generate all possible variations
    const variations = this.generateFilenameVariations(expectedFilename);
    
    let matchedFile = null;

    // If we have a list of available files, do smart matching
    if (availableFiles && availableFiles.length > 0) {
      const normalizedExpected = this.normalizeFilename(expectedFilename);
      
      // Try exact match first
      matchedFile = variations.find(variation => 
        availableFiles.includes(variation)
      );
      
      // Try normalized matching
      if (!matchedFile) {
        matchedFile = availableFiles.find(file => 
          this.normalizeFilename(file) === normalizedExpected
        );
      }
    } else {
      // Batch check variations for existence
      const existenceMap = await this.batchCheckFiles(platform, subject, variations);
      matchedFile = variations.find(variation => existenceMap.get(variation));
    }

    this.cache.set(cacheKey, matchedFile);
    return matchedFile;
  }

  /**
   * Load chapters efficiently in manifest order
   */
  async loadChapters(platform, subject, manifestChapters) {
    const availableChapters = [];
    
    // Try to get directory listing for smarter matching
    let availableFiles = [];
    try {
      const dirResponse = await fetch(`${platform}/${subject}/`);
      if (dirResponse.ok) {
        const text = await dirResponse.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, 'text/html');
        const links = doc.querySelectorAll('a[href$=".json"]');
        availableFiles = Array.from(links).map(link => {
          const href = link.getAttribute('href');
          return href.includes('/') ? href.split('/').pop() : href;
        });
      }
    } catch (e) {
      console.log('Directory listing not available, using individual checks');
    }

    // Process chapters in manifest order with parallel loading
    const chapterPromises = manifestChapters.map(async (chapter, index) => {
      try {
        const matchedFile = await this.findMatchingFile(
          platform, 
          subject, 
          chapter.file, 
          availableFiles.length > 0 ? availableFiles : null
        );

        if (!matchedFile) {
          return null;
        }

        const response = await fetch(`${platform}/${subject}/${matchedFile}`);
        if (!response.ok) {
          return null;
        }

        const data = await response.json();
        if (!data.questions || data.questions.length === 0) {
          return null;
        }

        return {
          name: chapter.name,
          filename: matchedFile,
          questionCount: data.questions.length,
          originalIndex: index // Preserve manifest order
        };
      } catch (error) {
        console.warn(`Failed to load chapter ${chapter.file}:`, error);
        return null;
      }
    });

    const results = await Promise.all(chapterPromises);
    
    // Filter out failed loads and sort by original manifest order
    return results
      .filter(chapter => chapter !== null)
      .sort((a, b) => a.originalIndex - b.originalIndex);
  }

  /**
   * Clear cache
   */
  clearCache() {
    this.cache.clear();
  }
}

// Export for global use
window.ChapterLoader = ChapterLoader;