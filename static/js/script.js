// كود الجافاسكريبت لموقع ProEstate
document.addEventListener('DOMContentLoaded', function() {
    
    // تهيئة جميع المكونات
    initSmoothScroll();
    initPropertyCards();
    initFilterForm();
    initContactForm();
    initImageGallery();
    initCounters();
    initBackToTop();
    
    console.log('✅ ProEstate website initialized successfully');
});

// التمرير السلس للروابط
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const target = document.querySelector(targetId);
            if (target) {
                const headerHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// تأثيرات بطاقات العقارات
function initPropertyCards() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // تطبيق التأثير على البطاقات
    const propertyCards = document.querySelectorAll('.property-card');
    propertyCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
    
    // إضافة تأثير hover للصور
    const propertyImages = document.querySelectorAll('.property-card img');
    propertyImages.forEach(img => {
        img.parentElement.classList.add('img-hover-zoom');
    });
}

// إدارة نموذج الفلتر
function initFilterForm() {
    const filterForm = document.querySelector('#propertyFilter');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            // إضافة تأثير التحميل
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>جاري البحث...';
            submitBtn.disabled = true;
            
            // استمرار الإرسال العادي للنموذج
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 1000);
        });
        
        // إعادة تعيين الفلتر
        const resetBtn = document.querySelector('#resetFilter');
        if (resetBtn) {
            resetBtn.addEventListener('click', function() {
                filterForm.reset();
                filterForm.submit();
            });
        }
    }
}

// التحقق من نموذج الاتصال
function initContactForm() {
    const contactForm = document.querySelector('#contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = this.querySelectorAll('input, textarea, select');
            
            // التحقق من الحقول المطلوبة
            inputs.forEach(input => {
                if (input.hasAttribute('required') && !input.value.trim()) {
                    isValid = false;
                    showFieldError(input, 'هذا الحقل مطلوب');
                } else {
                    clearFieldError(input);
                }
            });
            
            // التحقق من صحة البريد الإلكتروني
            const emailInput = this.querySelector('input[type="email"]');
            if (emailInput && emailInput.value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(emailInput.value)) {
                    isValid = false;
                    showFieldError(emailInput, 'يرجى إدخال بريد إلكتروني صحيح');
                }
            }
            
            // التحقق من رقم الهاتف
            const phoneInput = this.querySelector('input[name="phone"]');
            if (phoneInput && phoneInput.value) {
                const phoneRegex = /^[\+]?[0-9]{10,15}$/;
                if (!phoneRegex.test(phoneInput.value.replace(/[\s\-\(\)]/g, ''))) {
                    isValid = false;
                    showFieldError(phoneInput, 'يرجى إدخال رقم هاتف صحيح');
                }
            }
            
            if (!isValid) {
                e.preventDefault();
                showToast('يرجى تصحيح الأخطاء في النموذج', 'error');
            } else {
                // إضافة تأثير التحميل
                const submitBtn = this.querySelector('button[type="submit"]');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>جاري الإرسال...';
                submitBtn.disabled = true;
            }
        });
    }
}

// إدارة معرض الصور
function initImageGallery() {
    const mainImage = document.querySelector('#mainPropertyImage');
    const thumbnails = document.querySelectorAll('.property-thumbnail');
    
    if (mainImage && thumbnails.length > 0) {
        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', function() {
                const newSrc = this.getAttribute('data-full');
                const newAlt = this.getAttribute('data-alt');
                
                // تأثير التلاشي
                mainImage.style.opacity = '0';
                
                setTimeout(() => {
                    mainImage.src = newSrc;
                    mainImage.alt = newAlt;
                    mainImage.style.opacity = '1';
                    
                    // تحديث الصورة النشطة
                    thumbnails.forEach(t => t.classList.remove('active', 'border-primary'));
                    this.classList.add('active', 'border-primary');
                }, 200);
            });
        });
    }
}

// عدّاد الإحصائيات
function initCounters() {
    const counters = document.querySelectorAll('.counter');
    if (counters.length > 0) {
        const observerOptions = {
            threshold: 0.5
        };
        
        const counterObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = +counter.getAttribute('data-target');
                    const duration = 2000;
                    const step = target / (duration / 16);
                    let current = 0;
                    
                    const timer = setInterval(() => {
                        current += step;
                        if (current >= target) {
                            counter.textContent = formatNumber(target);
                            clearInterval(timer);
                        } else {
                            counter.textContent = formatNumber(Math.floor(current));
                        }
                    }, 16);
                    
                    counterObserver.unobserve(counter);
                }
            });
        }, observerOptions);
        
        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }
}

// زر العودة للأعلى
function initBackToTop() {
    const backToTop = document.createElement('button');
    backToTop.innerHTML = '<i class="fas fa-chevron-up"></i>';
    backToTop.className = 'btn btn-primary back-to-top';
    backToTop.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 1000;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: none;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    `;
    
    document.body.appendChild(backToTop);
    
    backToTop.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTop.style.display = 'flex';
        } else {
            backToTop.style.display = 'none';
        }
    });
}

// وظائف مساعدة
function showFieldError(input, message) {
    clearFieldError(input);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.textContent = message;
    
    input.classList.add('is-invalid');
    input.parentNode.appendChild(errorDiv);
}

function clearFieldError(input) {
    input.classList.remove('is-invalid');
    const existingError = input.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

function showToast(message, type = 'info') {
    // إنشاء عنصر Toast
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show`;
    toast.style.cssText = `
        position: fixed;
        top: 100px;
        left: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    `;
    
    toast.innerHTML = `
        <i class="fas fa-${getToastIcon(type)} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // إزالة Toast تلقائياً بعد 5 ثواني
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 5000);
}

function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function formatNumber(num) {
    return new Intl.NumberFormat('ar-SA').format(num);
}

// وظائف API
const ProEstateAPI = {
    // جلب العقارات
    getProperties: async function(filters = {}) {
        try {
            const queryParams = new URLSearchParams(filters).toString();
            const response = await fetch(`/api/properties?${queryParams}`);
            const data = await response.json();
            
            if (data.success) {
                return data.data;
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Error fetching properties:', error);
            showToast('حدث خطأ في جلب البيانات', 'error');
            return [];
        }
    },
    
    // جلب تفاصيل عقار
    getProperty: async function(propertyId) {
        try {
            const response = await fetch(`/api/property/${propertyId}`);
            const data = await response.json();
            
            if (data.success) {
                return data.data;
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Error fetching property:', error);
            showToast('حدث خطأ في جلب بيانات العقار', 'error');
            return null;
        }
    },
    
    // إرسال رسالة اتصال
    sendMessage: async function(formData) {
        try {
            const response = await fetch('/contact', {
                method: 'POST',
                body: formData
            });
            
            return response.ok;
        } catch (error) {
            console.error('Error sending message:', error);
            return false;
        }
    }
};

// جعل الوظائف متاحة globally
window.ProEstate = {
    API: ProEstateAPI,
    showToast: showToast,
    formatNumber: formatNumber
};

// تهيئة مكونات Bootstrap
if (typeof bootstrap !== 'undefined') {
    // تهيئة tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // تهيئة popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}