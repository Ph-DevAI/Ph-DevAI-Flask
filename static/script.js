// Load parallax backgrounds and apply simple parallax on scroll
document.querySelectorAll('.parallax-section').forEach(section=>{
    const url = section.querySelector('.parallax-bg').getAttribute('data-bg');
    section.querySelector('.parallax-bg').style.backgroundImage = `url('${url}')`;
});

function parallaxScroll(){
    document.querySelectorAll('.parallax-section').forEach(section=>{
    const rect = section.getBoundingClientRect();
    const bg = section.querySelector('.parallax-bg');
    if(!bg) return;
    const offset = (rect.top * -0.15);
    bg.style.transform = `translateY(${offset}px) scale(1.05)`;
    });
}
window.addEventListener('scroll', parallaxScroll); parallaxScroll();

// // Navbar show on scroll
// const nav = document.getElementById('mainNav');
// function checkNav(){
//     if(window.scrollY>60) nav.classList.add('scrolled'); else nav.classList.remove('scrolled');
//     if(window.scrollY<40) nav.classList.add('transparent'); else nav.classList.remove('transparent');
// }
// window.addEventListener('scroll', checkNav); checkNav();

// Swiper for services
const swiper = new Swiper('.mySwiper',{slidesPerView:1,spaceBetween:20,loop:true,autoplay:{delay:4500}, breakpoints:{768:{slidesPerView:2},1200:{slidesPerView:3}},navigation:{nextEl:'.swiper-button-next',prevEl:'.swiper-button-prev'}});

// Swiper for testimonials
const tSwiper = new Swiper('.testimonialsSwiper',{slidesPerView:1,spaceBetween:20,loop:true,autoplay:{delay:4500},pagination:{el:'.swiper-pagination',clickable:true}});

// Smooth anchors
document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',function(e){const t=document.querySelector(this.getAttribute('href'));if(t){e.preventDefault();window.scrollTo({top:t.offsetTop-70,behavior:'smooth'})}}));

// // Contact form (demo)
// document.getElementById('contactForm').addEventListener('submit',function(e){e.preventDefault();alert('Merci — votre message a été envoyé. NOUS VOUS CONTACTERONS LE PLUS TOT !!!.');this.reset();});

// Contact form (using Formspree)
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = new FormData(form);
  const response = await fetch(form.action, {
    method: "POST",
    body: data,
    headers: { "Accept": "application/json" }
  });

  if (response.ok) {
    alert("✅ Message envoyé avec succès !");
    form.reset();
  } else {
    alert("❌ Une erreur s’est produite. Réessaie plus tard.");
  }
});



// i18n texts (FR/EN)
const texts = {
    fr:{nav_home:'Accueil',nav_services:'Services',nav_courses:'Formations',nav_domains:'Domains PH',nav_testimonials:'Témoignages',nav_contact:'Contact',tagline:'Studio Web & IA — Solutions intelligentes',hero_title:'Nous construisons des applications intelligentes pour un monde connecté',hero_sub:"Sites vitrines, applications web, chatbots et formations — boostés par l'intelligence artificielle.",cta_explore:'Nos services',cta_contact:'Contactez-nous',cta_get_started:'Commencer',services_title:'Nos Services',services_sub:'Du site vitrine simple à l\'application intelligente — solutions sur-mesure adaptées à vos besoins.',svc_site:'Sites Web',svc_site_desc:'Standard : vitrine — Premium : domaine & email professionnel inclus.',svc_app:'Applications Web',svc_app_desc:'Outils sur-mesure : tableau de bord, CRM léger, plateformes éducatives. Possibilité d\'intégrer l\'IA.',svc_chatbot:'Chatbots',svc_chatbot_desc:'Chatbots multilingues, intégration WhatsApp/Website, scénarios métiers.',svc_design:'Design Graphique',svc_design_desc:'Branding, logos, UI/UX.',svc_ai_marketing:'IA & Marketing Digital',svc_ai_marketing_desc:'Automatisation campagnes, génération de contenus.',courses_title:'Formations',courses_sub:'Des parcours intensifs et boostés par l\'IA — adaptés aux débutants et aux professionnels.',course_dev_title:'Développement Web',course_dev_desc:'Objectifs : HTML/CSS/JS, backend Flask, déploiement, bases de données et intégration IA.',course_chat_title:'Chatbots',course_chat_desc:'Objectifs : création de chatbots conversationnels, intégration WhatsApp & web.',course_ia_title:'IA & Automatisation',course_ia_desc:'Objectifs : automatiser processus et workflows.',testimonials_title:'Témoignages',contact_title:'Contact',contact_sub:'Parlez-nous de votre projet — nous répondrons rapidement.',contact_send:'Envoyer'},
    en:{nav_home:'Home',nav_services:'Services',nav_courses:'Courses',nav_domains:'PH Domains',nav_testimonials:'Testimonials',nav_contact:'Contact',tagline:'Web & AI Studio — Smart solutions',hero_title:'We build intelligent apps for a connected world',hero_sub:'Websites, web apps, chatbots and training — boosted by artificial intelligence.',cta_explore:'Our services',cta_contact:'Contact us',cta_get_started:'Get started',services_title:'Our Services',services_sub:'From simple showcase sites to intelligent apps — bespoke solutions tailored to your needs.',svc_site:'Websites',svc_site_desc:'Standard: showcase — Premium: domain & professional email included.',svc_app:'Web Applications',svc_app_desc:'Custom tools: dashboards, CRMs, e-learning platforms. AI integration possible.',svc_chatbot:'Chatbots',svc_chatbot_desc:'Multilingual chatbots, WhatsApp/Website integration, business scenarios.',svc_design:'Graphic Design',svc_design_desc:'Branding, logos, UI/UX.',svc_ai_marketing:'AI & Digital Marketing',svc_ai_marketing_desc:'Campaign automation, content generation.',courses_title:'Courses',courses_sub:'Intensive, AI-boosted pathways — for beginners and professionals.',course_dev_title:'Web Development',course_dev_desc:'Goals: HTML/CSS/JS, Flask backend, deployment, DBs and AI integration.',course_chat_title:'Chatbots',course_chat_desc:'Goals: build conversational chatbots, WhatsApp & web integration.',course_ia_title:'AI & Automation',course_ia_desc:'Goals: automate processes and workflows.',testimonials_title:'Testimonials',contact_title:'Contact',contact_sub:'Tell us about your project — we will reply quickly.',contact_send:'Send'}
};

let lang='fr';
function applyTexts(){document.querySelectorAll('[data-i18n]').forEach(el=>{const key=el.getAttribute('data-i18n');if(texts[lang]&&texts[lang][key])el.textContent=texts[lang][key]});document.getElementById('lang-fr').classList.toggle('active',lang==='fr');document.getElementById('lang-en').classList.toggle('active',lang==='en');}
applyTexts();document.getElementById('lang-fr').addEventListener('click',()=>{lang='fr';applyTexts()});document.getElementById('lang-en').addEventListener('click',()=>{lang='en';applyTexts()});

// Set year
document.getElementById('year').textContent=new Date().getFullYear();
// Gestion du compteur de visiteurs
function updateVisitorCount() {
    let count = localStorage.getItem('visitorCount');
    if (!count) {
        count = 0;
    }
    count = parseInt(count) + 1;
    localStorage.setItem('visitorCount', count);
    return count;
}

// Animation des compteurs au scroll
function animateCounter(element, target) {
    let current = 0;
    const increment = target / 100;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            if (element.id === 'visitor-count') {
                element.textContent = target + '+';
            } else if (element.hasAttribute('data-target')) {
                element.textContent = target + '%';
            } else {
                element.textContent = target;
            }
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 20);
}

// Vérification si un élément est dans la vue
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    // Mise à jour du compteur de visiteurs
    const visitorCount = updateVisitorCount();
    document.getElementById('visitor-count').textContent = visitorCount;
    
    // Animation des compteurs au scroll
    let countersAnimated = false;
    
    window.addEventListener('scroll', function() {
        const statsSection = document.getElementById('stats');
        
        if (statsSection && isInViewport(statsSection) && !countersAnimated) {
            countersAnimated = true;
            
            const statNumbers = document.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {
                let target;
                if (stat.id === 'visitor-count') {
                    target = visitorCount;
                } else {
                    target = parseInt(stat.getAttribute('data-target'));
                }
                animateCounter(stat, target);
            });
        }
    });
});
