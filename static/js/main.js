// Main JavaScript for BLH Company

// Mobile menu toggle
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenu) {
        mobileMenu.classList.toggle('hidden');
    }
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(event) {
    const mobileMenu = document.getElementById('mobile-menu');
    const menuButton = document.querySelector('[onclick="toggleMobileMenu()"]');
    
    if (mobileMenu && !mobileMenu.contains(event.target) && !menuButton.contains(event.target)) {
        mobileMenu.classList.add('hidden');
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

// Form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('border-red-500');
            isValid = false;
        } else {
            field.classList.remove('border-red-500');
        }
    });
    
    return isValid;
}

// Contact form submission
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!validateForm(this)) {
                alert('필수 항목을 모두 입력해주세요.');
                return;
            }
            
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            
            // Show loading state
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>전송 중...';
            submitButton.disabled = true;
            
            try {
                const formData = new FormData(this);
                const data = Object.fromEntries(formData);
                
        const response = await fetch('/api/inquiry', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
            body: JSON.stringify({
                ...data,
                is_public: data.is_public === 'true'
            })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    alert('문의가 성공적으로 전송되었습니다.');
                    this.reset();
                } else {
                    alert('문의 전송 중 오류가 발생했습니다: ' + result.error);
                }
            } catch (error) {
                alert('문의 전송 중 오류가 발생했습니다.');
                console.error('Error:', error);
            } finally {
                // Reset button state
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }
        });
    }
});

// Share functionality
function shareNotice() {
    if (navigator.share) {
        navigator.share({
            title: document.title,
            text: 'BLH Company 공지사항',
            url: window.location.href
        });
    } else {
        // Fallback for browsers that don't support Web Share API
        navigator.clipboard.writeText(window.location.href).then(function() {
            alert('링크가 클립보드에 복사되었습니다.');
        }).catch(function() {
            // Fallback for browsers that don't support clipboard API
            const textArea = document.createElement('textarea');
            textArea.value = window.location.href;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            alert('링크가 클립보드에 복사되었습니다.');
        });
    }
}

// Print functionality
function printPage() {
    window.print();
}

// Loading animation
function showLoading(element) {
    element.innerHTML = '<div class="loading"></div>';
}

function hideLoading(element, originalContent) {
    element.innerHTML = originalContent;
}

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('.card, .bg-white, .bg-gray-50');
    animatedElements.forEach(el => {
        observer.observe(el);
    });
});

// Back to top button
function createBackToTopButton() {
    const button = document.createElement('button');
    button.innerHTML = '<i class="fas fa-arrow-up"></i>';
    button.className = 'fixed bottom-8 right-8 bg-primary text-white w-12 h-12 rounded-full shadow-lg hover:bg-secondary transition-colors z-50 hidden';
    button.id = 'back-to-top';
    
    button.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    document.body.appendChild(button);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            button.classList.remove('hidden');
        } else {
            button.classList.add('hidden');
        }
    });
}

// Initialize back to top button
document.addEventListener('DOMContentLoaded', function() {
    createBackToTopButton();
});

// Utility functions
const utils = {
    // Format date
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },
    
    // Format number with commas
    formatNumber: function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Throttle function
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// Export for use in other scripts
window.BLHCompany = {
    toggleMobileMenu,
    validateForm,
    shareNotice,
    printPage,
    showLoading,
    hideLoading,
    utils
};
