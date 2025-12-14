/**
 * SECTION LOADER - Dynamic Section Loading
 * Loads HTML sections on demand for modular architecture
 */

// Section configuration
const SECTIONS = [
  'data_types',
  'functions',
  'loops',
  'oop',
  'physics',
  'structure',
  'clean_code',
  'best_practices'
];

// Loading indicator
function showLoading() {
  const container = document.getElementById('sections-container');
  container.innerHTML = `
    <div class="flex justify-center items-center py-20">
      <div class="text-center">
        <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4"></div>
        <p class="text-lg text-gray-600 dark:text-gray-400">Loading sections...</p>
      </div>
    </div>
  `;
}

// Load single section
async function loadSection(sectionName) {
  try {
    const response = await fetch(`sections/${sectionName}.html`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const html = await response.text();
    return html;
  } catch (error) {
    console.error(`Failed to load section ${sectionName}:`, error);
    return `
      <section id="${sectionName}" class="py-20 px-6 bg-red-50 dark:bg-red-900/20">
        <div class="container mx-auto max-w-6xl text-center">
          <h2 class="text-2xl font-bold text-red-600 dark:text-red-400 mb-4">
            ⚠️ Failed to load section: ${sectionName}
          </h2>
          <p class="text-gray-700 dark:text-gray-300">
            Please check console for details.
          </p>
        </div>
      </section>
    `;
  }
}

// Load all sections
async function loadAllSections() {
  showLoading();
  const container = document.getElementById('sections-container');

  let allContent = '';

  // Load sections sequentially to maintain order
  for (const section of SECTIONS) {
    const html = await loadSection(section);
    allContent += html;
  }

  // Inject all content at once
  container.innerHTML = allContent;

  // Initialize features after sections loaded
  initializeAfterLoad();
}

// Initialize features after sections are loaded
function initializeAfterLoad() {
  // Re-initialize Prism syntax highlighting
  if (window.Prism) {
    Prism.highlightAll();
  }

  // Log success
  console.log('✅ All sections loaded successfully!');
  console.log(`📊 Loaded ${SECTIONS.length} sections`);
}

// Auto-load when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadAllSections);
} else {
  loadAllSections();
}
