/* COWORKMILL English site: lightbox, copy address, list filters (2026-10-10) */
(function(){
  // photo lightbox
  var data=document.getElementById('photos'),P=[];
  try{P=data?JSON.parse(data.textContent):[]}catch(e){}
  var lb=document.getElementById('lb'),cur=0;
  function show(i){if(!P.length)return;cur=(i+P.length)%P.length;var im=document.getElementById('lbimg');im.src=P[cur][0];im.alt=P[cur][1];document.getElementById('lbcap').textContent=(cur+1)+' / '+P.length+' · '+P[cur][1];}
  if(lb&&P.length){
    document.addEventListener('click',function(e){var f=e.target.closest('[data-i]');if(f&&!e.target.closest('dialog')){show(+f.getAttribute('data-i'));if(lb.showModal)lb.showModal();}});
    document.getElementById('lbprev').onclick=function(){show(cur-1)};document.getElementById('lbnext').onclick=function(){show(cur+1)};document.getElementById('lbclose').onclick=function(){lb.close()};
    lb.addEventListener('keydown',function(e){if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1)});
    lb.addEventListener('click',function(e){if(e.target===lb)lb.close()});
  }
  // copy the Japanese address
  document.querySelectorAll('.cp').forEach(function(b){b.addEventListener('click',function(){var t=b.getAttribute('data-t');
    var done=function(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy address'},2000)};
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(done,function(){sel()})}else sel();
    function sel(){var r=document.createRange();r.selectNodeContents(b.closest('.taxi').querySelector('.ja'));var s=getSelection();s.removeAllRanges();s.addRange(r)}
  })});
  // list filters
  var list=document.getElementById('list');if(!list)return;
  var cards=[].slice.call(list.children),q=document.getElementById('fq'),fp=document.getElementById('fp'),ft=document.getElementById('ft'),fc=document.getElementById('fc'),fn=document.getElementById('fn');
  var st={q:'',p:'',t:[]};
  try{var u=new URLSearchParams(location.search);st.q=(u.get('q')||'').toLowerCase();st.p=u.get('pref')||'';st.t=u.get('t')?u.get('t').split(','):[]}catch(e){}
  function apply(push){
    var n=0,words=st.q.trim().split(/\s+/).filter(Boolean);
    cards.forEach(function(c){var ok=(!st.p||c.getAttribute('data-p')===st.p)&&words.every(function(w){return c.getAttribute('data-q').indexOf(w)>=0})&&st.t.every(function(t){return ('|'+c.getAttribute('data-t')+'|').indexOf('|'+t+'|')>=0});c.hidden=!ok;if(ok)n++});
    fc.textContent=n+' space'+(n===1?'':'s');fn.hidden=n>0;q.value=st.q;
    [].forEach.call(fp.children,function(b){b.classList.toggle('on',b.getAttribute('data-p')===st.p)});
    [].forEach.call(ft.children,function(b){b.setAttribute('aria-pressed',st.t.indexOf(b.getAttribute('data-t'))>=0)});
    if(push){var p=new URLSearchParams();if(st.q)p.set('q',st.q);if(st.p)p.set('pref',st.p);if(st.t.length)p.set('t',st.t.join(','));history.replaceState(null,'',location.pathname+(p.toString()?'?'+p:''))}
  }
  document.getElementById('fs').addEventListener('submit',function(e){e.preventDefault();st.q=q.value.toLowerCase();apply(true)});
  q.addEventListener('input',function(){st.q=q.value.toLowerCase();apply(true)});
  fp.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;st.p=b.getAttribute('data-p');apply(true)});
  ft.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var t=b.getAttribute('data-t'),i=st.t.indexOf(t);if(i>=0)st.t.splice(i,1);else st.t.push(t);apply(true)});
  apply(false);
})();
