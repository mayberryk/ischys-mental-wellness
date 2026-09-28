// Loaded only on generic pages in an explicitly reviewed production build.
// No condition/article URLs, form fields, search queries, or source attribution are sent.
(() => {
  const id = document.querySelector('script[data-measurement-id]')?.dataset.measurementId;
  if (!/^G-[A-Z0-9]+$/.test(id || '')) return;
  let enabled = false;
  const root = location.origin + '/';
  function enable() {
    if (enabled) return;
    enabled = true;
    window.dataLayer = window.dataLayer || [];
    const gtag = function () { window.dataLayer.push(arguments); };
    gtag('consent', 'default', {ad_storage:'denied', analytics_storage:'granted', ad_user_data:'denied', ad_personalization:'denied'});
    gtag('set', {page_location:root,page_title:'Ischys Integrative Mental Wellness',page_referrer:''});
    gtag('js', new Date());
    gtag('config', id, {send_page_view:false,allow_google_signals:false,allow_ad_personalization_signals:false,page_location:root,page_title:'Ischys Integrative Mental Wellness',page_referrer:''});
    const script = document.createElement('script');
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
    script.async = true; script.referrerPolicy = 'no-referrer'; document.head.append(script);
    window.addEventListener('ischys:conversion', event => {
      if (!['schedule_click','consultation_click','phone_click','portal_click','referral_click'].includes(event.detail?.event)) return;
      gtag('event',event.detail.event,{page_location:root,page_title:'Ischys Integrative Mental Wellness',page_referrer:'',send_to:id});
    });
  }
  let consent = null;
  try { consent = localStorage.getItem('ischys-analytics-consent'); } catch (_) {}
  if (consent === 'accepted') { enable(); return; }
  if (consent === 'declined') return;
  const banner = document.createElement('section');banner.className='consent';banner.setAttribute('aria-label','Optional analytics');
  banner.innerHTML='<strong>Optional website measurement</strong><p>Allow basic counts of scheduling and contact actions? We do not send health topics, worksheet answers, or search terms.</p><div class="actions"><button class="button" data-choice="accepted">Allow</button><button class="button secondary" data-choice="declined">No thanks</button></div>';
  banner.addEventListener('click',event=>{const choice=event.target.closest('[data-choice]')?.dataset.choice;if(!choice)return;try{localStorage.setItem('ischys-analytics-consent',choice);}catch(_){}if(choice==='accepted')enable();banner.remove();});
  document.body.append(banner);
})();
