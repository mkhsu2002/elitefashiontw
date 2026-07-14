// Elite Fashion - Main JavaScript File

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    let mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navbarContainer = document.querySelector('.navbar .container');

    if (!mobileMenuToggle && navMenu && navbarContainer) {
        mobileMenuToggle = document.createElement('button');
        mobileMenuToggle.className = 'mobile-menu-toggle';
        mobileMenuToggle.type = 'button';
        mobileMenuToggle.setAttribute('aria-label', '開啟選單');
        mobileMenuToggle.setAttribute('aria-expanded', 'false');
        mobileMenuToggle.innerHTML = '<span></span><span></span><span></span>';
        navbarContainer.insertBefore(mobileMenuToggle, navMenu);
    }
    
    if (mobileMenuToggle && navMenu) {
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
    if (typeof window.gtag === 'function') {
        window.gtag('event', action, {
            event_category: category,
            event_label: label
        });
    }
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
            setStatus('已收到你的訊息，Elite Fashion 編輯團隊會盡快回覆。', 'success');
        } catch (error) {
            setStatus(error.message || '訊息暫時無法送出，請直接寄信到 northpathca@gmail.com。', 'error');
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = '發送訊息';
        }
    });
});

// Newsletter subscription forms
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.newsletter-form');
    const subscribeEndpoint = 'https://tw.elitefasion.com/api/subscribe';

    forms.forEach(function(form) {
        if (form.dataset.newsletterEnhanced === 'true') {
            return;
        }
        form.dataset.newsletterEnhanced = 'true';

        const emailInput = form.querySelector('input[type="email"]');
        const submitButton = form.querySelector('button[type="submit"]');
        if (!emailInput || !submitButton) {
            return;
        }

        let status = form.querySelector('.newsletter-status');
        if (!status) {
            status = document.createElement('p');
            status.className = 'newsletter-status';
            status.setAttribute('role', 'status');
            status.setAttribute('aria-live', 'polite');
            form.appendChild(status);
        }

        const setNewsletterStatus = function(message, type) {
            status.textContent = message;
            status.className = `newsletter-status is-visible is-${type}`;
        };

        form.addEventListener('submit', async function(event) {
            event.preventDefault();

            const email = String(emailInput.value || '').trim();
            if (!validateEmail(email)) {
                setNewsletterStatus('請填寫有效的電子郵件。', 'error');
                return;
            }

            const originalText = submitButton.textContent;
            submitButton.disabled = true;
            submitButton.textContent = '訂閱中...';
            setNewsletterStatus('正在加入訂閱名單。', 'success');

            try {
                const response = await fetch(form.getAttribute('data-endpoint') || subscribeEndpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email,
                        source: form.getAttribute('data-source') || window.location.pathname,
                        company: String(new FormData(form).get('company') || '').trim()
                    })
                });
                const result = await response.json().catch(function() {
                    return {};
                });

                if (!response.ok || !result.ok) {
                    throw new Error(result.error || '訂閱暫時無法完成，請稍後再試。');
                }

                form.reset();
                setNewsletterStatus('訂閱完成，下一封精選文章會寄到你的信箱。', 'success');
            } catch (error) {
                setNewsletterStatus(error.message || '訂閱暫時無法完成，請稍後再試。', 'error');
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = originalText;
            }
        });
    });
});

// Controlled in-article AdSense placements. Overlay formats must be disabled in AdSense.
document.addEventListener('DOMContentLoaded', function() {
    const config = {
        client: 'ca-pub-1555443662858445',
        slot: window.ELITE_ARTICLE_AD_SLOT ||
            document.documentElement.getAttribute('data-article-ad-slot') ||
            '5072221630',
        maxSlots: 2
    };

    if (!config.slot || document.querySelector('.elite-ad-unit')) {
        return;
    }

    const articleContainer = document.querySelector('.article-container');
    if (!articleContainer || articleContainer.hasAttribute('data-no-article-ads')) {
        return;
    }

    const contentRoot = document.querySelector('.product-article-main') ||
        document.querySelector('.article-body') ||
        articleContainer;

    const createAdUnit = function(index) {
        const wrapper = document.createElement('aside');
        wrapper.className = 'elite-ad-unit';
        wrapper.setAttribute('aria-label', '廣告');
        wrapper.dataset.adIndex = String(index);

        const label = document.createElement('span');
        label.className = 'elite-ad-label';
        label.textContent = '廣告';

        const ad = document.createElement('ins');
        ad.className = 'adsbygoogle';
        ad.style.display = 'block';
        ad.dataset.adClient = config.client;
        ad.dataset.adSlot = config.slot;
        ad.dataset.adFormat = 'auto';
        ad.dataset.fullWidthResponsive = 'true';

        wrapper.appendChild(label);
        wrapper.appendChild(ad);

        window.adsbygoogle = window.adsbygoogle || [];
        window.setTimeout(function() {
            try {
                window.adsbygoogle.push({});
            } catch (error) {
                wrapper.classList.add('elite-ad-unit-empty');
            }
        }, 0);

        return wrapper;
    };

    const insertAfter = function(node, adUnit) {
        if (!node || !node.parentNode) {
            return false;
        }
        node.parentNode.insertBefore(adUnit, node.nextSibling);
        return true;
    };

    const placeInSectionedArticle = function() {
        const sections = Array.from(contentRoot.querySelectorAll(':scope > .article-section'))
            .filter(function(section) {
                return !section.closest('.article-related, .article-faq, .article-cta, aside');
            });

        if (sections.length < 2) {
            return 0;
        }

        let inserted = 0;
        const firstTarget = sections[1];
        if (insertAfter(firstTarget, createAdUnit(1))) {
            inserted += 1;
        }

        if (sections.length >= 5 && inserted < config.maxSlots) {
            const secondTarget = sections[Math.min(4, sections.length - 2)];
            if (secondTarget !== firstTarget && insertAfter(secondTarget, createAdUnit(2))) {
                inserted += 1;
            }
        }

        return inserted;
    };

    const placeInClassicArticleBody = function() {
        const headings = Array.from(contentRoot.querySelectorAll(':scope > h2'));
        if (headings.length < 3) {
            return 0;
        }

        headings[2].parentNode.insertBefore(createAdUnit(1), headings[2]);
        let inserted = 1;

        if (headings.length >= 6 && inserted < config.maxSlots) {
            headings[5].parentNode.insertBefore(createAdUnit(2), headings[5]);
            inserted += 1;
        }

        return inserted;
    };

    const inserted = placeInSectionedArticle() || placeInClassicArticleBody();
    if (!inserted) {
        const paragraphs = Array.from(contentRoot.querySelectorAll(':scope > p'));
        if (paragraphs.length >= 4) {
            insertAfter(paragraphs[2], createAdUnit(1));
        }
    }
});
