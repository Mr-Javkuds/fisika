/**
 * =============================================
 * PYTHON LEARNING DOCUMENTATION - MAIN SCRIPT
 * =============================================
 * Handles all interactive functionality including:
 * - Dark mode toggle
 * - Code tabs
 * - Copy to clipboard
 * - Smooth scroll
 * - Accordion panels
 * - Scroll progress indicator
 * =============================================
 */

// =============================
// DARK MODE FUNCTIONALITY
// =============================
class DarkModeManager {
    constructor() {
        this.toggleBtn = document.getElementById('darkModeToggle');
        this.html = document.documentElement;
        this.init();
    }

    init() {
        // Load saved preference
        const savedTheme = localStorage.getItem('theme') || 'light';
        if (savedTheme === 'dark') {
            this.html.classList.add('dark');
        }

        // Add event listener
        if (this.toggleBtn) {
            this.toggleBtn.addEventListener('click', () => this.toggle());
        }
    }

    toggle() {
        this.html.classList.toggle('dark');
        const theme = this.html.classList.contains('dark') ? 'dark' : 'light';
        localStorage.setItem('theme', theme);
    }
}

// =============================
// CODE TABS FUNCTIONALITY
// =============================
class CodeTabsManager {
    constructor() {
        this.tabs = document.querySelectorAll('.code-tab');
        this.contents = document.querySelectorAll('.code-tab-content');
        this.init();
    }

    init() {
        this.tabs.forEach(tab => {
            tab.addEventListener('click', (e) => this.switchTab(e.currentTarget));
        });
    }

    switchTab(clickedTab) {
        const targetId = clickedTab.getAttribute('data-target');

        // Remove active state from all tabs
        this.tabs.forEach(tab => {
            tab.classList.remove('active', 'border-purple-500', 'text-purple-600', 
                'dark:text-purple-400', 'bg-purple-50', 'dark:bg-purple-900/30');
            tab.classList.add('text-gray-600', 'dark:text-gray-400');
        });

        // Add active state to clicked tab
        clickedTab.classList.add('active', 'border-purple-500', 'text-purple-600', 
            'dark:text-purple-400', 'bg-purple-50', 'dark:bg-purple-900/30');
        clickedTab.classList.remove('text-gray-600', 'dark:text-gray-400');

        // Hide all contents
        this.contents.forEach(content => {
            content.classList.add('hidden');
        });

        // Show target content
        const targetContent = document.getElementById(targetId);
        if (targetContent) {
            targetContent.classList.remove('hidden');
        }
    }
}

// =============================
// COPY CODE FUNCTIONALITY
// =============================
class CopyCodeManager {
    constructor() {
        this.init();
    }

    init() {
        // Attach to window for inline onclick handlers
        window.copyCode = (button) => this.copyToClipboard(button);
    }

    async copyToClipboard(button) {
        const codeBlock = button.parentElement.querySelector('code');
        if (!codeBlock) return;

        const code = codeBlock.textContent;

        try {
            await navigator.clipboard.writeText(code);
            this.showCopyFeedback(button);
        } catch (err) {
            console.error('Failed to copy:', err);
        }
    }

    showCopyFeedback(button) {
        const originalHTML = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check mr-1"></i>Copied!';
        
        setTimeout(() => {
            button.innerHTML = originalHTML;
        }, 2000);
    }
}

// =============================
// SMOOTH SCROLL FUNCTIONALITY
// =============================
class SmoothScrollManager {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = anchor.getAttribute('href');
                const target = document.querySelector(targetId);
                
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
}

// =============================
// SCROLL PROGRESS INDICATOR
// =============================
class ScrollProgressManager {
    constructor() {
        this.indicator = this.createIndicator();
        this.init();
    }

    createIndicator() {
        const div = document.createElement('div');
        div.className = 'scroll-indicator';
        div.style.width = '0%';
        document.body.appendChild(div);
        return div;
    }

    init() {
        window.addEventListener('scroll', () => this.updateProgress());
        this.updateProgress(); // Initial update
    }

    updateProgress() {
        const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        this.indicator.style.width = scrolled + '%';
    }
}

// =============================
// INTERSECTION OBSERVER (Fade In)
// =============================
class FadeInObserver {
    constructor() {
        this.options = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };
        this.init();
    }

    init() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, this.options);

        // Observe all sections
        document.querySelectorAll('section').forEach(section => {
            observer.observe(section);
        });
    }
}

// =============================
// ACCORDION FUNCTIONALITY
// =============================
class AccordionManager {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('.accordion-header').forEach(header => {
            header.addEventListener('click', () => this.toggle(header));
        });
    }

    toggle(header) {
        const content = header.nextElementSibling;
        const icon = header.querySelector('.accordion-icon');
        
        if (content && content.classList.contains('accordion-content')) {
            content.classList.toggle('active');
            
            if (icon) {
                icon.classList.toggle('fa-chevron-down');
                icon.classList.toggle('fa-chevron-up');
            }
        }
    }
}

// =============================
// CODE COMPARISON SLIDER
// =============================
class ComparisonSlider {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (this.container) {
            this.init();
        }
    }

    init() {
        const slider = this.container.querySelector('.comparison-slider');
        const beforeCode = this.container.querySelector('.before-code');
        
        if (slider && beforeCode) {
            slider.addEventListener('input', (e) => {
                const value = e.target.value;
                beforeCode.style.width = value + '%';
            });
        }
    }
}

// =============================
// SEARCH FUNCTIONALITY
// =============================
class SearchManager {
    constructor() {
        this.searchInput = document.getElementById('searchInput');
        if (this.searchInput) {
            this.init();
        }
    }

    init() {
        this.searchInput.addEventListener('input', (e) => this.search(e.target.value));
    }

    search(query) {
        const sections = document.querySelectorAll('section[id]');
        const lowerQuery = query.toLowerCase();

        sections.forEach(section => {
            const text = section.textContent.toLowerCase();
            const shouldShow = text.includes(lowerQuery);
            
            section.style.display = shouldShow ? '' : 'none';
        });
    }
}

// =============================
// TOOLTIP MANAGER
// =============================
class TooltipManager {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            element.addEventListener('mouseenter', (e) => this.show(e));
            element.addEventListener('mouseleave', () => this.hide());
        });
    }

    show(event) {
        const tooltipText = event.target.getAttribute('data-tooltip');
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip-popup';
        tooltip.textContent = tooltipText;
        tooltip.id = 'active-tooltip';
        
        document.body.appendChild(tooltip);
        
        const rect = event.target.getBoundingClientRect();
        tooltip.style.position = 'absolute';
        tooltip.style.left = rect.left + 'px';
        tooltip.style.top = (rect.bottom + 5) + 'px';
    }

    hide() {
        const tooltip = document.getElementById('active-tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    }
}

// =============================
// INITIALIZE ALL MANAGERS
// =============================
class App {
    constructor() {
        this.managers = [];
        this.init();
    }

    init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initManagers());
        } else {
            this.initManagers();
        }
    }

    initManagers() {
        try {
            this.managers.push(new DarkModeManager());
            this.managers.push(new CodeTabsManager());
            this.managers.push(new CopyCodeManager());
            this.managers.push(new SmoothScrollManager());
            this.managers.push(new ScrollProgressManager());
            this.managers.push(new FadeInObserver());
            this.managers.push(new AccordionManager());
            this.managers.push(new SearchManager());
            this.managers.push(new TooltipManager());
            
            console.log('✅ All managers initialized successfully');
        } catch (error) {
            console.error('❌ Error initializing managers:', error);
        }
    }
}

// Initialize the application
const app = new App();
