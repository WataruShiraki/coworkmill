/* COWORKMILL filter + pagination patch (2026-05-16) */
(function(){
  var SUPABASE_URL="https://jakwntemjkwqwaqujffh.supabase.co";
  var SUPABASE_KEY="sb_publishable_bQ84WCmRiFUbpPemMcO9xQ_Dj9Mh1mQ";
  var PAGE_SIZE=50,currentPage=1,bySlug=null;
  var PREF_MAP={tokyo:"東京都",osaka:"大阪府",kyoto:"京都府",fukuoka:"福岡県",yokohama:"神奈川県",sapporo:"北海道"};
  var FAC_ALIAS={"power":["power","outlet"]},VIBE_ALIAS={"urban":["urban","highrise"]};
  function normWork(w){return String(w).toLowerCase().replace(/\s+/g,"").replace("call","");}
  function loadCache(){if(bySlug)return Promise.resolve();return fetch(SUPABASE_URL+"/rest/v1/spaces?status=eq.live&select=slug,name,area,address,prefecture,facilities,workstyle_tags,atmosphere_tags,vibe&limit=1000",{headers:{apikey:SUPABASE_KEY,Authorization:"Bearer "+SUPABASE_KEY}}).then(function(r){return r.json();}).then(function(data){bySlug={};data.forEach(function(s){bySlug[s.slug]=s;});});}
  function applyFilter(){
    var activeCities=[].slice.call(document.querySelectorAll(".sf-opt.on")).filter(function(el){return /toggleCity/.test(el.getAttribute("onclick")||"");}).map(function(el){var m=(el.getAttribute("onclick")||"").match(/'([^']+)'/);return m?m[1]:"";}).filter(Boolean);
    var activeWards=[].slice.call(document.querySelectorAll(".sf-ward.on")).map(function(e){return e.textContent.trim();}).filter(Boolean);
    var activeFacs=[].slice.call(document.querySelectorAll(".sf-opt.on[data-fac]")).map(function(e){return e.dataset.fac;});
    var activeVibes=[].slice.call(document.querySelectorAll(".sf-opt.on[data-vibe]")).map(function(e){return e.dataset.vibe;});
    var activeChips=[].slice.call(document.querySelectorAll(".chip.on")).map(function(c){return c.dataset.work;}).filter(Boolean);
    var sInput=document.querySelector(".sp-search-input");
    var q=(sInput?sInput.value:"").toLowerCase().trim().replace(/駅$/,"");
    var cards=[].slice.call(document.querySelectorAll(".lcard")),visibleCards=[];
    cards.forEach(function(card){
      var slug=(card.getAttribute("href")||"").split("/").pop();
      var d=(bySlug&&bySlug[slug])||{};
      var addr=d.address||"",area=d.area||"",pref=d.prefecture||"";
      var facs=Array.isArray(d.facilities)?d.facilities:[];
      var vibesArr=[];
      if(d.vibe)String(d.vibe).split(",").forEach(function(v){v=v.trim();if(v)vibesArr.push(v);});
      if(Array.isArray(d.atmosphere_tags))d.atmosphere_tags.forEach(function(v){vibesArr.push(v);});
      var works=(Array.isArray(d.workstyle_tags)?d.workstyle_tags:[]).map(normWork);
      var nameEl=card.querySelector(".lcard-name"),cityEl=card.querySelector(".lcard-city");
      var name=nameEl?nameEl.textContent:"",city=cityEl?cityEl.textContent:"";
      var matchText=!q||name.toLowerCase().indexOf(q)>-1||city.toLowerCase().indexOf(q)>-1||area.toLowerCase().indexOf(q)>-1||addr.toLowerCase().indexOf(q)>-1;
      var matchCity=!activeCities.length||activeCities.some(function(c){var pn=PREF_MAP[c];if(pn)return addr.indexOf(pn)>-1||pref===pn;if(c==="yokohama")return addr.indexOf("横浜")>-1;if(c==="sapporo")return addr.indexOf("札幌")>-1;return addr.indexOf(c)>-1;});
      var matchWard=!activeWards.length||activeWards.some(function(w){return addr.indexOf(w)>-1;});
      var matchFac=!activeFacs.length||activeFacs.every(function(f){return (FAC_ALIAS[f]||[f]).some(function(a){return facs.indexOf(a)>-1;});});
      var matchVibe=!activeVibes.length||activeVibes.some(function(v){return (VIBE_ALIAS[v]||[v]).some(function(a){return vibesArr.indexOf(a)>-1;});});
      var allChip=activeChips.indexOf("all")>-1;
      var matchWork=!activeChips.length||allChip||activeChips.some(function(w){return works.indexOf(w)>-1;});
      if(matchText&&matchCity&&matchWard&&matchFac&&matchVibe&&matchWork)visibleCards.push(card);
    });
    var total=visibleCards.length,totalPages=Math.max(1,Math.ceil(total/PAGE_SIZE));
    if(currentPage>totalPages)currentPage=totalPages;if(currentPage<1)currentPage=1;
    cards.forEach(function(c){c.style.display="none";});
    visibleCards.slice((currentPage-1)*PAGE_SIZE,currentPage*PAGE_SIZE).forEach(function(c){c.style.display="";});
    var cntEl=document.querySelector(".results-count"),cntNumEl=document.getElementById("results-count-num");
    if(cntEl)cntEl.textContent=total+" スペース";
    if(cntNumEl)cntNumEl.textContent=total;
    renderPagination(total,totalPages);
    showEmptyState(total===0);
  }
  function renderPagination(total,totalPages){
    var el=document.getElementById("cwm-pagination");
    var grid=document.querySelector(".spaces-grid")||document.querySelector("#spaces-grid")||document.querySelector(".grid");
    if(!grid)return;
    if(!el){el=document.createElement("div");el.id="cwm-pagination";el.className="pagination";grid.parentNode.insertBefore(el,grid.nextSibling);}
    if(total<=PAGE_SIZE){el.style.display="none";return;}
    el.style.display="flex";el.innerHTML="";
    var makeBtn=function(label,page,isActive,isDisabled){var b=document.createElement("button");b.className="pg-btn"+(isActive?" on":"");b.textContent=label;if(isDisabled)b.disabled=true;else b.onclick=function(e){e.preventDefault();currentPage=page;applyFilter();window.scrollTo({top:grid.offsetTop-100,behavior:"smooth"});};return b;};
    el.appendChild(makeBtn("‹",currentPage-1,false,currentPage<=1));
    var pages=[];
    if(totalPages<=7){for(var i=1;i<=totalPages;i++)pages.push(i);}else{pages.push(1);if(currentPage>4)pages.push("...");for(var j=Math.max(2,currentPage-1);j<=Math.min(totalPages-1,currentPage+1);j++)pages.push(j);if(currentPage<totalPages-3)pages.push("...");pages.push(totalPages);}
    pages.forEach(function(p){if(p==="..."){var s=document.createElement("span");s.style.cssText="padding:0 8px;color:#999;font-size:12px";s.textContent="...";el.appendChild(s);}else{el.appendChild(makeBtn(String(p),p,p===currentPage,false));}});
    el.appendChild(makeBtn("›",currentPage+1,false,currentPage>=totalPages));
  }
  function showEmptyState(show){
    var el=document.getElementById("cwm-empty-state");
    var grid=document.querySelector(".spaces-grid")||document.querySelector("#spaces-grid");
    if(!grid)return;
    if(show){if(!el){el=document.createElement("div");el.id="cwm-empty-state";el.style.cssText="text-align:center;padding:80px 20px;color:#999;font-size:14px;line-height:1.8;max-width:600px;margin:60px auto";el.innerHTML="<div style=\"font-size:48px;margin-bottom:16px;opacity:.3\">🔍</div><div style=\"font-size:18px;color:#bbb;margin-bottom:12px;font-weight:600\">条件に合う施設が見つかりませんでした</div><div>絞り込み条件を変更してお試しください</div>";grid.parentNode.insertBefore(el,grid.nextSibling);}el.style.display="block";}else if(el){el.style.display="none";}
  }
  function init(){
    loadCache().then(function(){
      var tries=0;
      function check(){
        if(typeof window.filterSidebar==="function"&&document.querySelectorAll(".lcard").length>0){
          window.filterSidebar=function(){currentPage=1;applyFilter();};
          applyFilter();
        }else if(tries<60){tries++;setTimeout(check,150);}
      }
      check();
    });
  }
  if(document.readyState==="complete")init();else window.addEventListener("load",init);
})();
