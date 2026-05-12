// Elite Fashion - Main JavaScript File

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            const isExpanded = navMenu.classList.contains('active');
            mobileMenuToggle.setAttribute('aria-expanded', isExpanded);
            
            // Toggle menu icon animation
            this.classList.toggle('active');
        });
        
        // Close mobile menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-menu a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                mobileMenuToggle.classList.remove('active');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
            });
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInsideMenu = navMenu.contains(event.target);
            const isClickOnToggle = mobileMenuToggle.contains(event.target);
            
            if (!isClickInsideMenu && !isClickOnToggle && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                mobileMenuToggle.classList.remove('active');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }
});

// Smooth Scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', function() {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        navbar.classList.remove('scroll-up');
        return;
    }
    
    if (currentScroll > lastScroll && !navbar.classList.contains('scroll-down')) {
        // Scrolling down
        navbar.classList.remove('scroll-up');
        navbar.classList.add('scroll-down');
    } else if (currentScroll < lastScroll && navbar.classList.contains('scroll-down')) {
        // Scrolling up
        navbar.classList.remove('scroll-down');
        navbar.classList.add('scroll-up');
    }
    
    lastScroll = currentScroll;
});

// Lazy loading images enhancement
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const image = entry.target;
                image.classList.add('loaded');
                observer.unobserve(image);
            }
        });
    });
    
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(function(img) {
        imageObserver.observe(img);
    });
}

// Add fade-in animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe article cards and topic cards
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.article-card, .topic-card');
    cards.forEach(function(card) {
        observer.observe(card);
    });
});

// Performance optimization: Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Handle window resize
const handleResize = debounce(function() {
    // Close mobile menu on resize to desktop
    if (window.innerWidth > 968) {
        const navMenu = document.querySelector('.nav-menu');
        const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
        
        if (navMenu && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            mobileMenuToggle.classList.remove('active');
            mobileMenuToggle.setAttribute('aria-expanded', 'false');
        }
    }
}, 250);

window.addEventListener('resize', handleResize);

// Analytics tracking (placeholder)
function trackEvent(category, action, label) {
    // Implement your analytics tracking here
    // Example: gtag('event', action, {'event_category': category, 'event_label': label});
    console.log('Event tracked:', category, action, label);
}

// Track article clicks
document.querySelectorAll('.article-link, .topic-link').forEach(function(link) {
    link.addEventListener('click', function(e) {
        const title = this.querySelector('.article-title, .topic-title');
        if (title) {
            trackEvent('Content', 'Click', title.textContent);
        }
    });
});

// Form validation (if needed in future)
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Contact form submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#contactForm');
    const status = document.querySelector('#contactFormStatus');

    if (!form || !status) {
        return;
    }

    const submitButton = form.querySelector('button[type="submit"]');
    const configuredEndpoint = form.getAttribute('data-endpoint');
    const contactEndpoint = configuredEndpoint || 'https://tw.elitefasion.com/api/contact';
    const setStatus = function(message, type) {
        status.textContent = message;
        status.className = `form-status is-visible is-${type}`;
    };

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const name = String(formData.get('name') || '').trim();
        const email = String(formData.get('email') || '').trim();
        const purpose = String(formData.get('purpose') || '').trim();
        const message = String(formData.get('message') || '').trim();

        if (name.length < 2) {
            setStatus('請留下姓名，至少讓我們知道該怎麼稱呼你。', 'error');
            return;
        }

        if (!validateEmail(email)) {
            setStatus('請填寫有效的電子郵件，我們才知道要回覆到哪裡。', 'error');
            return;
        }

        if (!purpose) {
            setStatus('請先選擇聯繫目的，這樣我們比較知道該由誰出面回信。', 'error');
            return;
        }

        if (message.length < 10) {
            setStatus('訊息內容可以再多一點點，至少讓我們知道這次聯繫的重點。', 'error');
            return;
        }

        const payload = {
            name,
            email,
            organization: String(formData.get('organization') || '').trim(),
            purpose,
            subject: String(formData.get('subject') || '').trim(),
            website: String(formData.get('website') || '').trim(),
            message,
            company: String(formData.get('company') || '').trim()
        };

        submitButton.disabled = true;
        submitButton.textContent = '發送中...';
        setStatus('訊息正在送出，請稍候。', 'success');

        try {
            const response = await fetch(contactEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            const result = await response.json().catch(function() {
                return {};
            });

            if (!response.ok || !result.ok) {
                throw new Error(result.error || '訊息暫時無法送出，請稍後再試。');
            }

            form.reset();
            setStatus('已收到你的訊息，NorthPath.CA 會盡快回覆。', 'success');
        } catch (error) {
            setStatus(error.message || '訊息暫時無法送出，請直接寄信到 northpathca@gmail.com。', 'error');
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = '發送訊息';
        }
    });
});

// Console message
console.log('%c Elite Fashion ', 'background: #000; color: #fff; font-size: 20px; padding: 10px;');
console.log('%c 引領時尚潮流，探索精英生活 ', 'font-size: 12px; color: #666;');
