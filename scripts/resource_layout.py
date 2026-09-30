"""Web layouts for the supplied print toolkit; source wording remains in content/."""
from html import escape
import re

# Section starts, list ranges, and worksheet prompts refer to the original block order.
LAYOUTS = {
 'welcome': {'sections':[0,6,17,25,34], 'lists':[(9,13),(27,30)], 'topics':[(22,23)], 'prompts':[]},
 'starting-point': {'sections':[0,4,43,49,51,54,70,73], 'lists':[(58,68),(77,81)], 'topics':[], 'prompts':[46,50,53,69,71]},
 'wellness-plan': {'sections':[0,7,26,43,54,65,78,100,113,122,128,133,142], 'lists':[(15,24),(30,42),(46,50),(57,61),(68,74),(105,111),(118,121),(136,139)], 'topics':[(2,3)], 'prompts':[10,13,52,63,76,103,114,115,124,125,126,127,130,131,132,140,141]},
 'hard-day': {'sections':[0,7,23,46,60,72,85,94,109,115,124,133,141], 'lists':[(10,20),(49,58),(63,66),(74,80),(89,92),(99,106),(144,149)], 'topics':[], 'prompts':[117,118,119,120,121,122,123,135,136,137,138,139]},
 'resources': {'sections':[0,7,12,20,38,45,49,53,64,73,78], 'lists':[(81,89)], 'topics':[(10,10),(15,16),(42,43)], 'prompts':[66,67,68,69,70,71,72]},
}

def render_resource(key, blocks, link_lookup):
 config = LAYOUTS[key]
 sections = config['sections']
 list_ranges = dict(config['lists'])
 topics = dict(config['topics'])
 prompts = set(config['prompts'])
 result, toc = [], []

 def render_range(start, end):
  output, prose = [], []
  def flush():
   if prose:
    output.append('<p>'+' '.join(escape(t) for t in prose)+'</p>');prose.clear()
  i = start
  while i < end:
   text = blocks[i]['text']
   if (key=='wellness-plan' and i==83) or (key=='hard-day' and i==30):
    flush()
    output.append('<div class="resource-comparisons">'+''.join('<div class="resource-comparison"><p><span>'+escape(blocks[n]['text'])+'</span> '+escape(blocks[n+1]['text'])+'</p><p><strong>'+escape(blocks[n+2]['text'])+'</strong> '+escape(blocks[n+3]['text'])+'</p></div>' for n in range(i,i+16,4))+'</div>')
    i+=16;continue
   if key=='welcome' and i==35:
    flush();output.append('<blockquote class="resource-question">'+escape(text)+'</blockquote>');i+=1;continue
   if i==len(blocks)-1 and text.startswith(('This toolkit','This wellness plan','This page is an educational','This resource page')):
    flush();output.append('<p class="resource-note">'+escape(text)+'</p>');i+=1;continue
   if key == 'starting-point' and i == 6:
    flush()
    rows=[]
    for first,last in [(7,7),(10,10),(13,13),(16,16),(19,19),(22,22),(25,25),(28,29),(32,33),(36,37)]:
     label=' '.join(blocks[n]['text'] for n in range(first,last+1))
     label=re.sub(r'\s+0 1 2 3 4 5 6 7 8 9$', '',label)
     title,question=label.split(' — ',1)
     rows.append('<div class="rating-row"><div><strong>'+escape(title)+'</strong><p>'+escape(question)+'</p></div><div class="rating-scale" aria-label="Rating from zero to ten">'+''.join('<span>'+str(n)+'</span>' for n in range(11))+'</div></div>')
    rows.append('<div class="rating-row"><strong>'+escape(blocks[40]['text'])+'</strong><div class="rating-scale" aria-label="Rating from zero to ten">'+''.join('<span>'+str(n)+'</span>' for n in range(11))+'</div></div>')
    output.append('<div class="rating-sheet">'+''.join(rows)+'</div>');i=43;continue
   if i in topics:
    flush();last=topics[i]
    labels=' '.join(blocks[n]['text'] for n in range(i,last+1)).split('•')
    output.append('<ul class="resource-topics">'+''.join('<li>'+escape(t.strip())+'</li>' for t in labels if t.strip())+'</ul>');i=last+1;continue
   if i in list_ranges:
    flush();last=list_ranges[i]
    output.append('<ul class="resource-list">'+''.join('<li>'+escape(blocks[n]['text'])+'</li>' for n in range(i,last+1))+'</ul>');i=last+1;continue
   if text.startswith('QR CODE:'):
    flush();dest,label=link_lookup[text[8:].strip()]
    output.append('<p><a class="text-link" href="'+escape(dest,quote=True)+'">'+escape(label)+' →</a></p>')
   elif '→' in text and blocks[i]['type']=='h2':
    flush()
    labels = ['Notice','Understand','Experiment','Track','Discuss'] if 'Experiment' in text else (['Stop','Breathe','Choose one thing'] if 'STOP' in text else ['Notice','Understand','Choose the next step','Reach out'])
    output.append('<ol class="resource-steps">'+''.join('<li>'+escape(t)+'</li>' for t in labels)+'</ol>')
   elif i in prompts:
    flush();output.append('<div class="worksheet-prompt"><p>'+escape(text)+'</p><div class="writing-space" aria-hidden="true"></div></div>')
   elif blocks[i]['type']=='h2':
    flush();output.append('<h3>'+escape(text)+'</h3>')
   elif '_' in text:
    flush();output.append('<p class="worksheet-line">'+escape(text)+'</p>')
   else:
    if prose and sum(len(t) for t in prose)+len(text)>280:flush()
    prose.append(text)
    # Rejoin short print lines into paragraphs without creating a wall of text.
    if sum(len(t) for t in prose)>260 or text.endswith(':'):flush()
   i+=1
  flush()
  return ''.join(output)

 for n,start in enumerate(sections):
  end=sections[n+1] if n+1<len(sections) else len(blocks)
  title=blocks[start]['text'];ident='section-'+str(start)
  if key=='resources' and start==7:title='Your Patient Portal'
  toc.append((ident,title))
  content=render_range(start+1,end)
  if key=='resources' and start==7:content=content.replace('<h3>Your Patient Portal</h3>','')
  urgent=(key=='hard-day' and start==124) or (key=='resources' and start==53)
  if key=='welcome' or urgent:
   result.append('<section class="resource-panel'+(' resource-urgent' if urgent else '')+'" id="'+ident+'"><h2>'+escape(title)+'</h2>'+content+'</section>')
  else:
   result.append('<details class="resource-panel resource-fold" id="'+ident+'"'+(' open' if n==0 else '')+'><summary><h2>'+escape(title)+'</h2><span class="resource-toggle" aria-hidden="true"></span></summary><div class="resource-section-body">'+content+'</div></details>')
 return ''.join(result),toc
