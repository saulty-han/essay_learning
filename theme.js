/* theme.js — unified dark/light theme toggle for all deep-analysis pages */
(function(){
  const KEY='theme',DARK='dark',LIGHT='light';
  const btn=document.createElement('button');
  btn.id='theme-toggle';
  btn.style.cssText='position:fixed;top:16px;right:16px;z-index:9999;width:42px;height:42px;border-radius:50%;border:2px solid rgba(255,255,255,.25);background:rgba(30,30,50,.7);color:#fff;font-size:20px;cursor:pointer;backdrop-filter:blur(6px);transition:all .3s';
  document.documentElement.appendChild(btn);
  function apply(t){
    document.documentElement.setAttribute('data-theme',t);
    btn.textContent=t===LIGHT?'🌙':'☀️';
    localStorage.setItem(KEY,t);
    fixSvgColors(t);
  }
  btn.onclick=()=>apply(localStorage.getItem(KEY)===LIGHT?DARK:LIGHT);
  apply(localStorage.getItem(KEY)||DARK);

  /* ===== SVG colour mapping ===== */
  const darkFillMap={
    '#1a2340':'#eef0ff','#252a3a':'#f0f1f5','#1e2130':'#f5f6fa','#181b25':'#f8f9fc',
    '#141720':'#eef0f5','#10182a':'#edf0fa','#122030':'#eef3f8','#101a20':'#eef2f5',
    '#182030':'#eef3fa','#101a28':'#edf2f8','#0e1820':'#ecf0f5','#1a2b30':'#eef8f0',
    '#253530':'#e8f5ea','#1e3020':'#e5f5e8','#142820':'#e8f5ec','#10201a':'#e8f5eb',
    '#2a1a3a':'#f3eeff','#2b1a30':'#f5eef3','#302030':'#f5eef5','#1a1520':'#f3eef5',
    '#201820':'#f5eef3','#1a1020':'#f3ecf5','#221828':'#f5eef8','#0a0a0f':'#f8f9fc',
    '#111118':'#f0f1f5','#18181f':'#f5f6fa','#222230':'#e8e8ee','#2a2a38':'#e0e0e8',
    '#0d1520':'#ecf2f8','#0f1a28':'#edf2f8','#1a1a2e':'#eef0ff','#1c2235':'#eef0f8',
    '#1e2840':'#eef1fa','#202840':'#eef1fa','#222840':'#eef1fa'
  };
  const darkStrokeMap={
    '#2a2d3a':'#ccc','#333':'#bbb','#444':'#aaa','#555':'#999','#222230':'#ddd',
    '#2a2a38':'#e0e0e8','#3a3d4a':'#bbb','#1a1a2e':'#ccc'
  };
  const lightTextMap={
    '#fff':'#333','#ffffff':'#333','#FFF':'#333','#ccc':'#666','#ddd':'#666',
    '#aaa':'#555','#888':'#555','#999':'#555','#bbb':'#555','#666':'#888',
    '#555':'#666',
    'rgba(255,255,255,.7)':'rgba(0,0,0,.55)','rgba(255,255,255,.6)':'rgba(0,0,0,.45)',
    'rgba(255,255,255,.8)':'rgba(0,0,0,.6)','rgba(255,255,255,.5)':'rgba(0,0,0,.4)'
  };

  function fixSvgColors(theme){
    document.querySelectorAll('svg').forEach(svg=>{
      svg.querySelectorAll('[fill]').forEach(el=>{
        const v=el.getAttribute('fill');
        if(!v||v==='none')return;
        if(theme===LIGHT){
          const low=v.toLowerCase();
          if(darkFillMap[low])el.setAttribute('fill',darkFillMap[low]);
          else if(lightTextMap[low])el.setAttribute('fill',lightTextMap[low]);
        }else{
          const orig=el.getAttribute('data-original-fill');
          if(orig)el.setAttribute('fill',orig);
        }
      });
      svg.querySelectorAll('[stroke]').forEach(el=>{
        const v=el.getAttribute('stroke');
        if(!v||v==='none')return;
        if(theme===LIGHT){
          const low=v.toLowerCase();
          if(darkStrokeMap[low])el.setAttribute('stroke',darkStrokeMap[low]);
        }else{
          const orig=el.getAttribute('data-original-stroke');
          if(orig)el.setAttribute('stroke',orig);
        }
      });
    });
  }

  /* ===== Light-theme CSS overrides ===== */
  const lightCSS=`
    html[data-theme="light"] body{background:#f5f6fa;color:#222;}
    html[data-theme="light"] .container{background:#fff;}
    html[data-theme="light"] .hero-title{color:#1a1a2e;}
    html[data-theme="light"] .hero-sub{color:#444;}
    html[data-theme="light"] .venue{color:#666;}
    html[data-theme="light"] .venue a{color:#666;}
    html[data-theme="light"] .section-title{color:#1a1a2e;}
    html[data-theme="light"] .section-desc{color:#333;}
    html[data-theme="light"] .module-card{background:#f8f9fc;border-color:#dde;}
    html[data-theme="light"] .module-card h3{color:#1a1a2e;}
    html[data-theme="light"] .module-card p{color:#444;}
    html[data-theme="light"] .data-table{background:#fff;border-color:#dde;}
    html[data-theme="light"] .data-table th{background:#eef0f5;color:#333;}
    html[data-theme="light"] .data-table td{color:#333;border-color:#dde;}
    html[data-theme="light"] .formula-box{background:#f8f9fc;color:#333;border-color:#dde;}
    html[data-theme="light"] .code-block{background:#f0f1f5;color:#333;}
    html[data-theme="light"] .code-block pre{color:#333;}
    html[data-theme="light"] .qa-card{background:#f8f9fc;border-color:#dde;}
    html[data-theme="light"] .qa-q{color:#1a1a2e;}
    html[data-theme="light"] .qa-a{color:#444;}
    html[data-theme="light"] .tag{background:#eef0f5;color:#333;border-color:#dde;}
    html[data-theme="light"] .divider{border-color:#dde;}
    html[data-theme="light"] .toc a{color:#444;}
    html[data-theme="light"] .toc a:hover{color:#0cebeb;}
    html[data-theme="light"] .back-btn{background:#f0f1f5;color:#333;border-color:#dde;}
    html[data-theme="light"] .back-btn:hover{background:#eef0f5;}
    html[data-theme="light"] .fc{color:#666;}
    html[data-theme="light"] .paper-figure{background:#f8f9fc;border-color:#dde;}
    html[data-theme="light"] .arch-card{background:#f8f9fc;border-color:#dde;}
    html[data-theme="light"] .arch-card h4{color:#1a1a2e;}
    html[data-theme="light"] .arch-card p{color:#444;}
    html[data-theme="light"] .step-flow{background:#f8f9fc;border-color:#dde;}
    html[data-theme="light"] .step-flow h4{color:#1a1a2e;}
    html[data-theme="light"] .step-flow p{color:#444;}
    html[data-theme="light"] .highlight-box{background:#eef8f0;border-color:#b5e8c0;color:#333;}
    html[data-theme="light"] .warn-box{background:#fef7e8;border-color:#f0d060;color:#333;}
    html[data-theme="light"] .info-box{background:#eef0ff;border-color:#aab;color:#333;}
    html[data-theme="light"] .kv-row{border-color:#dde;}
    html[data-theme="light"] .kv-key{color:#555;}
    html[data-theme="light"] .kv-val{color:#222;}
    html[data-theme="light"] .footer{color:#888;}
    html[data-theme="light"] svg text{fill-opacity:1;}
    html[data-theme="light"] svg .arrow-path{stroke:#aaa;}
    html[data-theme="light"] .prompt-box{background:#f0f1f5;border-color:#dde;color:#333;}
    html[data-theme="light"] .prompt-label{background:#dde;color:#333;}
    html[data-theme="light"] .comp-card{background:#f8f9fc;border-color:#dde;}
    html[data-theme="light"] .comp-card h4{color:#1a1a2e;}
    html[data-theme="light"] .comp-card p{color:#444;}
    html[data-theme="light"] .insight-box{background:#eef8f0;border-color:#b5e8c0;}
    html[data-theme="light"] .insight-box h4{color:#1a6a3a;}
    html[data-theme="light"] .insight-box p{color:#333;}
    html[data-theme="light"] .limit-box{background:#fef7e8;border-color:#f0d060;}
    html[data-theme="light"] .limit-box h4{color:#8a6d00;}
    html[data-theme="light"] .limit-box p{color:#333;}
  `;
  const style=document.createElement('style');
  style.textContent=lightCSS;
  document.head.appendChild(style);
})();
