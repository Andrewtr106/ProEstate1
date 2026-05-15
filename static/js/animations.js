// ====== GSAP Scroll + UI helpers ======
(function () {
  // Progress bar (in case base.html script is removed/overridden)
  window.addEventListener('scroll', function () {
    const progress = document.getElementById('scrollProgress');
    if (!progress) return;
    const scrollPct = (window.scrollY / Math.max(1, (document.body.scrollHeight - window.innerHeight))) * 100;
    progress.style.width = scrollPct + '%';
  });

  // Navbar scroll effect
  window.addEventListener('scroll', function () {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  });

  // Smooth page loader removal (if present)
  window.addEventListener('load', function () {
    const loader = document.getElementById('pageLoader');
    if (!loader) return;
    if (typeof gsap !== 'undefined') {
      gsap.to(loader, {
        opacity: 0,
        duration: 0.6,
        delay: 0.3,
        onComplete: function () {
          loader.style.display = 'none';
        }
      });
    } else {
      loader.style.display = 'none';
    }
  });

  // ====== Hero Typed.js (home page) ======
  const typedEl = document.getElementById('typed-text');
  if (typedEl && typeof Typed !== 'undefined') {
    new Typed('#typed-text', {
      strings: [
        'Find Your Dream Home 🏡',
        'ابحث عن منزل أحلامك 🏡',
        'Invest in Your Future 🏢',
        'استثمر في مستقبلك 🏢',
        'Luxury Properties Await ✨',
        'العقارات الفاخرة في انتظارك ✨'
      ],
      typeSpeed: 60,
      backSpeed: 30,
      backDelay: 2000,
      loop: true,
      smartBackspace: true
    });
  }

  // ====== AOS init ======
  if (typeof AOS !== 'undefined') {
    AOS.init({ duration: 800, once: true, offset: 100 });
  }

  // ====== GSAP ScrollTrigger entrance animations ======
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);

    // Section headings
    document.querySelectorAll('.section-heading').forEach(function (el) {
      gsap.from(el, {
        scrollTrigger: { trigger: el, start: 'top 80%' },
        y: 30,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out'
      });
    });

    // Property cards staggered entrance (cards must have .property-card)
    document.querySelectorAll('.property-card').forEach(function (card, i) {
      gsap.from(card, {
        scrollTrigger: { trigger: card, start: 'top 85%' },
        opacity: 0,
        y: 80,
        scale: 0.95,
        duration: 0.7,
        delay: (i % 3) * 0.15,
        ease: 'power3.out'
      });
    });

    // Navbar scrolled state and hero parallax (basic)
    const hero = document.getElementById('hero');
    if (hero) {
      gsap.fromTo(hero, {
        y: 0,
        scale: 1
      }, {
        y: -10,
        scale: 1.02,
        scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true }
      });
    }

    // Stats counter (CountUp.js) using viewport enter
    if (typeof CountUp !== 'undefined') {
      const statsObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const value = el.getAttribute('data-count');
          if (!value) return;
          const count = new CountUp.CountUp(el, value, {
            duration: 2.5,
            useEasing: true,
            useGrouping: true
          });
          count.start();
          statsObserver.unobserve(el);
        });
      }, { threshold: 0.2 });

      document.querySelectorAll('.stat-number').forEach(function (el) {
        statsObserver.observe(el);
      });
    }
  }

  // ====== Vanilla Tilt ======
  if (typeof VanillaTilt !== 'undefined') {
    if (document.querySelectorAll('.property-card').length > 0) {
      VanillaTilt.init(document.querySelectorAll('.property-card'), {
        max: 12,
        speed: 400,
        glare: true,
        'max-glare': 0.2,
        scale: 1.03
      });
    }
  }

  // ====== Three.js hero particles/building (home page only) ======
  const heroCanvas = document.getElementById('hero-canvas');
  if (heroCanvas && typeof THREE !== 'undefined') {
    try {
      const canvasEl = heroCanvas; // canvas element already in DOM

      const renderer = new THREE.WebGLRenderer({
        canvas: canvasEl,
        alpha: true,
        antialias: true
      });

      const scene = new THREE.Scene();

      const camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / Math.max(1, window.innerHeight),
        0.1,
        1000
      );
      camera.position.z = 8;

      function resize() {
        const w = window.innerWidth;
        const h = window.innerHeight;
        renderer.setSize(w, h);
        camera.aspect = w / Math.max(1, h);
        camera.updateProjectionMatrix();
      }
      resize();
      window.addEventListener('resize', resize);

      // Particles
      const particleCount = 200;
      const geometry = new THREE.BufferGeometry();
      const positions = new Float32Array(particleCount * 3);

      for (let i = 0; i < particleCount * 3; i++) {
        positions[i] = (Math.random() - 0.5) * 30;
      }
      geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

      const material = new THREE.PointsMaterial({
        color: 0xFFD700,
        size: 0.08,
        transparent: true,
        opacity: 0.85
      });

      const particles = new THREE.Points(geometry, material);
      scene.add(particles);

      // Simple "house" geometry
      const houseGroup = new THREE.Group();

      const bodyGeo = new THREE.BoxGeometry(2, 1.5, 1.5);
      const bodyMat = new THREE.MeshPhongMaterial({ color: 0x2196F3, transparent: true, opacity: 0.85 });
      const body = new THREE.Mesh(bodyGeo, bodyMat);

      const roofGeo = new THREE.ConeGeometry(1.5, 1, 4);
      const roofMat = new THREE.MeshPhongMaterial({ color: 0xFF6B35 });
      const roof = new THREE.Mesh(roofGeo, roofMat);
      roof.position.y = 1.25;
      roof.rotation.y = Math.PI / 4;

      houseGroup.add(body, roof);
      scene.add(houseGroup);

      // Lights
      scene.add(new THREE.AmbientLight(0xffffff, 0.5));
      const dirLight = new THREE.DirectionalLight(0xffffff, 1);
      dirLight.position.set(5, 5, 5);
      scene.add(dirLight);

      let last = performance.now();

      function animate() {
        requestAnimationFrame(animate);

        const now = performance.now();
        const dt = (now - last) / 1000;
        last = now;

        particles.rotation.y += dt * 0.8;
        houseGroup.rotation.y += dt * 0.6;
        houseGroup.position.y = Math.sin(Date.now() * 0.001) * 0.3;

        renderer.render(scene, camera);
      }

      animate();
    } catch (e) {
      // Do not break page if Three.js fails
      console.warn('Three.js hero init failed:', e);
    }
  }
})();
