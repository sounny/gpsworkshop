// GPS Workshop Lab Manual - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }

    // Close menu when clicking a link
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
        });
    });

    // Schedule tabs
    const scheduleTabs = document.querySelectorAll('.schedule-tab');
    const scheduleContents = document.querySelectorAll('.schedule-content');

    scheduleTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetId = this.dataset.tab;

            // Update tabs
            scheduleTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            // Update content
            scheduleContents.forEach(content => {
                if (content.id === targetId) {
                    content.classList.remove('hidden');
                } else {
                    content.classList.add('hidden');
                }
            });
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add active state to current page in navigation
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-menu a').forEach(link => {
        const linkPage = link.getAttribute('href');
        if (linkPage === currentPage) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Code copy functionality
    document.querySelectorAll('.code-block').forEach(block => {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.textContent = 'Copy';
        copyBtn.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            padding: 0.25rem 0.75rem;
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 4px;
            color: #fff;
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.3s ease;
        `;
        
        copyBtn.addEventListener('click', async () => {
            const code = block.querySelector('code')?.textContent || block.textContent;
            try {
                await navigator.clipboard.writeText(code);
                copyBtn.textContent = 'Copied!';
                setTimeout(() => copyBtn.textContent = 'Copy', 2000);
            } catch (err) {
                copyBtn.textContent = 'Failed';
            }
        });

        block.style.position = 'relative';
        block.appendChild(copyBtn);
    });
});
