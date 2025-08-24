export class SearchPage {
  constructor() {
    this.currentView = 'search';
    this.platforms = ['marrow', 'dams', 'prepladder'];
    this.subjects = ['anatomy', 'physiology'];
  }

  async getAllTeachers() {
    const teachers = [];
    
    // Import all platform subject lists
    const marrowList = await import('../platforms/marrow/MarrowSubjectList.js');
    const damsList = await import('../platforms/dams/DamsSubjectList.js');
    const prepladderList = await import('../platforms/prepladder/PrepladderSubjectList.js');
    
    const marrowTeachers = new marrowList.MarrowSubjectList().subjects;
    const damsTeachers = new damsList.DamsSubjectList().subjects;
    const prepladderTeachers = new prepladderList.PrepladderSubjectList().subjects;
    
    // Format teacher data from each platform
    marrowTeachers.forEach(subject => {
      if (subject.teacher) {
        teachers.push({
          name: subject.teacher,
          subject: subject.name,
          platform: 'Marrow'
        });
      }
    });

    damsTeachers.forEach(subject => {
      if (subject.teacher) {
        teachers.push({
          name: subject.teacher,
          subject: subject.name,
          platform: 'DAMS'
        });
      }
    });

    prepladderTeachers.forEach(subject => {
      if (subject.teacher) {
        teachers.push({
          name: subject.teacher,
          subject: subject.name,
          platform: 'Prepladder'
        });
      }
    });

    return teachers;
  }

  async getAllLectures() {
    const lectures = [];
    const baseUrl = window.location.hostname === 'tk22kalal2.github.io' 
      ? '/web-app3/platforms'
      : './platforms';
    
    // Define platform structure with their subfolders
    const platformStructure = {
      'dams': ['damsb2beng', 'damsb2bhinglish', 'damsultlive'],
      'cerebellum': [''], // Direct JSON files in cerebellum folder
      'prepladder5': [''], // Direct JSON files in prepladder5 folder
      'prepladder6': [''],
      'prepladder6x': [''],
      'marrow': [''],
      'e-gurukul': [''],
      'physics-wala': ['']
    };
    
    for (const [platform, subfolders] of Object.entries(platformStructure)) {
      for (const subfolder of subfolders) {
        try {
          // Construct the correct path
          const folderPath = subfolder ? `${platform}/${subfolder}` : platform;
          
          // Get all JSON files in this folder
          const jsonFiles = await this.getJsonFiles(baseUrl, folderPath);
          
          for (const jsonFile of jsonFiles) {
            try {
              const response = await fetch(`${baseUrl}/${folderPath}/${jsonFile}`);
              if (response.ok) {
                const data = await response.json();
                if (data.lectures && Array.isArray(data.lectures)) {
                  data.lectures.forEach(lecture => {
                    lectures.push({
                      ...lecture,
                      subject: data.subjectName || jsonFile.replace('.json', ''),
                      platform: platform.charAt(0).toUpperCase() + platform.slice(1),
                      subfolder: subfolder || platform
                    });
                  });
                }
              }
            } catch (error) {
              console.log(`Could not load ${folderPath}/${jsonFile}:`, error);
            }
          }
        } catch (error) {
          console.log(`Error scanning ${platform}:`, error);
        }
      }
    }
    
    return lectures;
  }

  async getJsonFiles(baseUrl, folderPath) {
    // Since we can't list directory contents directly, we'll use known patterns
    const commonJsonFiles = [
      'anatomy.json', 'physiology.json', 'biochemistry.json', 'pathology.json',
      'pharmacology.json', 'microbiology.json', 'fmt.json', 'psm.json',
      'medicine.json', 'surgery.json', 'obgy.json', 'pediatrics.json',
      'ophthalmology.json', 'ent.json', 'orthopedics.json', 'anesthesia.json',
      'radiology.json', 'dermatology.json', 'psychiatry.json', 'clinicals.json',
      // Prepladder5 specific files
      'p5anatomy.json', 'p5physiology.json', 'p5biochemistry.json', 'p5pathology.json',
      'p5pharmacology.json', 'p5microbiology.json', 'p5fmt.json', 'p5psm.json',
      'p5clinicals.json', 'p5surgery.json', 'p5obgy.json', 'p5pediatrics.json',
      'p5ophthalmology.json', 'p5ent.json', 'p5orthopedics.json', 'p5anesthesia.json',
      'p5radiology.json', 'p5dermatology.json', 'p5pschiatry.json', 'p5rapidrevision.json',
      // Cerebellum files
      'cbanatomy.json', 'cbanesthesia.json', 'cbpediatrics.json', 'cbpharmacology.json', 'cbradiology.json',
      // DAMS specific files (based on actual structure seen)
      'anatomy dr sandeep.json', 'biochemsitry dr sonam.json', 'ent dr deepak arrora.json',
      'fmt dr mohit.json', 'medicine dr archin.json', 'medicine dr arvind.json', 'medicine dr bharat.json',
      'medicine dr rahul.json', 'medicine dr shrinath.json', 'micro dr suria.json', 'obgy dr deepti.json',
      'ophth dr sourab.json', 'ophthalm dr manish.json', 'optho dr tushar.json', 'patho dr gourav.json',
      'patho dr sanjeev.json', 'patho dr shagun.json', 'pedia dr sidharth.json', 'pediatric dr manoj.json',
      'pharma dr j thiru.json', 'pharmacology dr dinesh.json', 'physiology dr kamal.json',
      'psm dr kashish.json', 'psm dr sidharth.json', 'psych.json', 'radio.json', 'surgery deepak.json',
      'surgery dr dhruv.json', 'surgery dr gaurav.json', 'surgery dr kenny.json', 'surgery dr rajeev.json',
      'surgery dr sujoy.json', 'derma.json',
      // DAMS ultlive files
      'dulanatomy.json', 'dulfmt.json',
      // DAMS hinglish files  
      'dhradiology.json'
    ];
    
    const existingFiles = [];
    
    for (const file of commonJsonFiles) {
      try {
        const response = await fetch(`${baseUrl}/${folderPath}/${file}`);
        if (response.ok) {
          existingFiles.push(file);
        }
      } catch (error) {
        // File doesn't exist, continue
      }
    }
    
    return existingFiles;
  }

  render() {
    const container = document.createElement('div');
    container.className = 'search-page';

    const searchContainer = document.createElement('div');
    searchContainer.className = 'search-container';

    const searchBar = document.createElement('div');
    searchBar.className = 'enhanced-search-bar';

    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = 'Search...';
    searchInput.className = 'search-input';

    const searchTypeSelect = document.createElement('select');
    searchTypeSelect.className = 'search-type-select';
    searchTypeSelect.innerHTML = `
      <option value="teacher">Search by Teacher</option>
      <option value="lecture">Search by Lecture</option>
    `;

    const resultsContainer = document.createElement('div');
    resultsContainer.className = 'search-results';

    searchInput.addEventListener('input', async (e) => {
      const searchType = searchTypeSelect.value;
      const query = e.target.value.toLowerCase();
      
      if (query.length < 2) {
        resultsContainer.innerHTML = '<p class="search-prompt">Enter at least 2 characters to search</p>';
        return;
      }

      if (searchType === 'teacher') {
        const teachers = await this.getAllTeachers();
        const results = teachers.filter(teacher => 
          teacher.name.toLowerCase().includes(query) ||
          teacher.subject.toLowerCase().includes(query)
        );
        this.displayTeacherResults(results, resultsContainer);
      } else {
        const lectures = await this.getAllLectures();
        const results = lectures.filter(lecture =>
          lecture.title.toLowerCase().includes(query) ||
          lecture.subject.toLowerCase().includes(query)
        );
        this.displayLectureResults(results, resultsContainer);
      }
    });

    searchTypeSelect.addEventListener('change', () => {
      searchInput.value = '';
      resultsContainer.innerHTML = '';
    });

    searchBar.appendChild(searchInput);
    searchBar.appendChild(searchTypeSelect);
    searchContainer.appendChild(searchBar);
    container.appendChild(searchContainer);
    container.appendChild(resultsContainer);

    return container;
  }

  displayTeacherResults(results, container) {
    if (results.length === 0) {
      container.innerHTML = '<p class="no-results">No teachers found</p>';
      return;
    }

    container.innerHTML = results.map(teacher => `
      <div class="search-result-card" onclick="document.dispatchEvent(new CustomEvent('platformSelect', { detail: '${teacher.platform.toLowerCase()}' }))">
        <div class="result-header">
          <i class="fas fa-user-md"></i>
          <h3>${teacher.name}</h3>
        </div>
        <div class="result-details">
          <span><i class="fas fa-book-medical"></i> ${teacher.subject}</span>
          <span><i class="fas fa-building"></i> ${teacher.platform}</span>
        </div>
      </div>
    `).join('');
  }
  displayLectureResults(results, container) {
    if (results.length === 0) {
      container.innerHTML = '<p class="no-results">No lectures found</p>';
      return;
    }

    container.innerHTML = results.map(lecture => `
      <div class="search-result-card" onclick="document.dispatchEvent(new CustomEvent('subjectSelect', { detail: { platform: '${lecture.platform.toLowerCase()}', subject: '${lecture.subject}' } }))">
        <div class="result-header">
          <i class="fas fa-play-circle"></i>
          <h3>${lecture.title}</h3>
        </div>
        <div class="result-details">
          <span><i class="fas fa-book-medical"></i> ${lecture.subject}</span>
          <span><i class="fas fa-building"></i> ${lecture.platform}</span>
        </div>
      </div>
    `).join('');
  }
}
