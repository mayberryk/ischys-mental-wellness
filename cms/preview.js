const articleTopics = {"psychiatric-medication-management": "Medication Management", "adhd-treatment-utah": "ADHD", "anxiety-depression-treatment": "Anxiety & Depression", "womens-mental-health": "Women’s Mental Health", "addiction-recovery": "Addiction & Recovery", "trauma-ptsd": "Trauma & PTSD", "integrative-psychiatry": "Integrative Psychiatry"};
CMS.registerPreviewStyle('body{font:17px/1.7 system-ui;color:#21454a;background:#faf8f1;padding:32px;max-width:760px;margin:auto}h1,h2,h3{font-family:Georgia,serif;color:#084f55;line-height:1.2}img{max-width:100%;height:auto}small{color:#5b6260}',{raw:true});
CMS.registerPreviewTemplate('articles',function(props){
  const data=props.entry.get('data');
  return window.h('article',{},window.h('small',{},'ARTICLE PREVIEW · Saving a draft does not publish it'),window.h('p',{style:{color:'#084f55',fontWeight:600}},(data.get('services')||[]).map(key=>articleTopics[key]||key).join(' · ')),window.h('h1',{},data.get('title')||'Your article title'),window.h('p',{},data.get('description')),data.get('image')?window.h('img',{src:props.getAsset(data.get('image')).toString(),alt:data.get('image_alt')||''}):null,props.widgetFor('body'));
});
CMS.registerEventListener({name:'preSave',handler:({entry})=>{
  if(entry.get('collection')!=='articles')return;
  let data=entry.get('data');
  data=data.set('status',data.get('approved')===true?'published':'draft');
  if(!data.get('services')?.size)throw new Error('Choose at least one article topic.');
  if(!data.get('path'))data=data.set('path','/learning/'+data.get('key')+'/');
  if(data.get('image')&&!data.get('image_alt'))throw new Error('Please describe the cover image before saving.');
  return data;
}});
CMS.registerPreviewTemplate('plans',function(props){
  const plans=props.entry.getIn(['data','plans']);
  return window.h('section',{},window.h('h1',{},'Insurance preview'),window.h('p',{},'Active plans appear in the footer and on the insurance page. Pending and inactive plans stay hidden.'),window.h('div',{style:{display:'grid',gridTemplateColumns:'repeat(2,minmax(0,1fr))',gap:16}},plans?plans.filter(p=>p.get('status')==='active').map(p=>window.h('div',{key:p.get('id'),style:{background:'white',padding:20,borderRadius:12}},p.get('logo')?window.h('img',{src:props.getAsset(p.get('logo')).toString(),alt:'',style:{width:'100%',height:60,objectFit:'contain'}}):null,window.h('strong',{},p.get('name')),window.h('p',{},p.get('details')))).toArray():[]));
});
