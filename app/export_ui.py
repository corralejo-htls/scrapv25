"""
export_ui.py — BookingScraper Pro v6.0.0 Build 93
==================================================

Panel HTML de exportación de datos a la API externa.

Servido en:  GET /export/ui  (HTMLResponse)

Cambios Build 93 (STRUCT-EXPORT-004):
  - Los checkboxes de idiomas se cargan dinámicamente desde
    GET /export/languages (fuente de verdad: ENABLED_LANGUAGES).
  - EXT_API_DEFAULT_LANGUAGES ya no está hardcodeado en el panel;
    el servidor lo aplica como restricción si está configurado.
  - El panel muestra todos los idiomas scrapeados marcados por defecto;
    el usuario puede desmarcar los que no quiera exportar en esa sesión.
  - is_complete se evalúa contra ENABLED_LANGUAGES, no lista fija.

Platform: Windows 11 / Python 3.14 / FastAPI / PostgreSQL 14+
"""

from __future__ import annotations

_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:14px;background:#f5f6f8;color:#1a1d23;padding:20px}
h1{font-size:18px;font-weight:600;color:#1a1d23;margin-bottom:4px}
.sub{font-size:12px;color:#6b7280;margin-bottom:16px}
.status-bar{display:flex;align-items:center;gap:10px;padding:10px 14px;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;margin-bottom:12px}
.dot{width:8px;height:8px;border-radius:50%;background:#16a34a;flex-shrink:0}
.dot-warn{background:#f59e0b}.dot-err{background:#ef4444}
.status-label{font-size:13px;font-weight:500}
.status-detail{margin-left:auto;font-size:11px;font-family:monospace;color:#6b7280}
.lang-bar{display:flex;align-items:center;gap:12px;padding:10px 14px;background:#fff;border:1px solid #e5e7eb;border-radius:8px;margin-bottom:16px;flex-wrap:wrap}
.lang-bar-label{font-size:12px;font-weight:600;color:#374151;white-space:nowrap}
.lang-checks{display:flex;gap:8px;flex-wrap:wrap;flex:1}
.lang-check{display:flex;align-items:center;gap:5px;cursor:pointer;padding:4px 10px;border:1px solid #e5e7eb;border-radius:20px;font-size:12px;font-family:monospace;font-weight:600;transition:all .15s;user-select:none}
.lang-check.active{background:#eff6ff;border-color:#3b82f6;color:#1d4ed8}
.lang-check.inactive{background:#f9fafb;color:#9ca3af;text-decoration:line-through}
.lang-check input{width:0;height:0;opacity:0;position:absolute}
.lang-source{font-size:10px;color:#9ca3af;white-space:nowrap}
.lang-restricted{font-size:11px;color:#f59e0b;padding:3px 8px;background:#fffbeb;border-radius:12px}
.tabs{display:flex;border-bottom:1px solid #e5e7eb;margin-bottom:16px}
.tab{padding:9px 18px;font-size:13px;border:none;background:none;border-bottom:2px solid transparent;cursor:pointer;color:#6b7280;font-family:inherit}
.tab.active{color:#1a1d23;border-bottom-color:#1a1d23;font-weight:600}
.tab:hover:not(.active){color:#1a1d23}
.tab-content{display:none}.tab-content.active{display:block}
.label{font-size:12px;font-weight:600;color:#374151;margin-bottom:6px;text-transform:uppercase;letter-spacing:.4px}
.hint{font-size:11px;color:#9ca3af;margin-bottom:8px}
.mode-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px}
.mode-card{padding:10px 12px;border:1px solid #e5e7eb;border-radius:8px;cursor:pointer;background:#fff}
.mode-card:hover{border-color:#93c5fd}
.mode-card.sel{border:2px solid #3b82f6;background:#eff6ff}
.mode-title{font-size:13px;font-weight:600;color:#1a1d23;margin-bottom:2px}
.mode-sub{font-size:11px;color:#6b7280}
.mode-card.sel .mode-sub{color:#1d4ed8}
textarea{width:100%;font-family:monospace;font-size:13px;padding:9px 10px;border:1px solid #d1d5db;border-radius:6px;background:#fff;color:#1a1d23;resize:vertical}
textarea:focus{outline:none;border-color:#3b82f6;box-shadow:0 0 0 3px rgba(59,130,246,.12)}
.sep-row{display:flex;align-items:center;gap:6px;margin-top:6px;font-size:11px;color:#6b7280;flex-wrap:wrap}
.sep-chip{font-family:monospace;background:#f3f4f6;border:1px solid #e5e7eb;border-radius:4px;padding:1px 6px;font-size:11px;color:#374151}
.upload-zone{border:2px dashed #d1d5db;border-radius:8px;padding:20px;text-align:center;cursor:pointer;background:#fafafa}
.upload-zone:hover{border-color:#3b82f6}
.upload-zone.loaded{border-color:#16a34a;background:#f0fdf4}
.upload-text{font-size:13px;color:#6b7280}
.csv-preview{font-family:monospace;font-size:11px;color:#374151;margin-top:8px;padding:6px 10px;background:#f3f4f6;border-radius:6px;word-break:break-all}
.hotel-list{display:flex;flex-direction:column;gap:5px;margin-top:10px}
.hotel-row{display:flex;align-items:center;gap:8px;padding:8px 10px;border:1px solid #e5e7eb;border-radius:7px;background:#fff}
.hotel-row.excl{opacity:.55;background:#fff7ed}
.hotel-row.notfound{opacity:.45;background:#fef2f2}
.h-ref{font-family:monospace;font-size:12px;font-weight:700;color:#2563eb;min-width:54px}
.h-name{font-size:13px;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lang-pills{display:flex;gap:3px;flex-shrink:0}
.lp{font-size:10px;padding:1px 5px;border-radius:10px;font-family:monospace;font-weight:600}
.lp-ok{background:#d1fae5;color:#065f46}.lp-miss{background:#fee2e2;color:#991b1b}
.badge{font-size:11px;font-weight:600;padding:2px 8px;border-radius:12px;white-space:nowrap;flex-shrink:0}
.b-ok{background:#d1fae5;color:#065f46}.b-warn{background:#fef3c7;color:#92400e}.b-err{background:#fee2e2;color:#991b1b}
.warn-box{display:flex;gap:8px;align-items:flex-start;padding:10px 12px;background:#fffbeb;border:1px solid #fcd34d;border-radius:7px;font-size:12px;color:#92400e;margin-top:8px}
.info-box{display:flex;gap:8px;align-items:flex-start;padding:10px 12px;background:#eff6ff;border:1px solid #bfdbfe;border-radius:7px;font-size:12px;color:#1e40af;margin-bottom:10px}
.fields-grid{display:grid;grid-template-columns:1fr 1fr;gap:5px}
.field-row{display:flex;align-items:center;gap:8px;padding:8px 10px;border:1px solid #e5e7eb;border-radius:7px;background:#fff}
.field-row.locked{background:#f9fafb;opacity:.6}.field-row.inactive{opacity:.4}
.field-name{font-size:12px;font-family:monospace;flex:1;color:#1a1d23}
.cov-bar{width:44px;height:5px;background:#e5e7eb;border-radius:3px;overflow:hidden;flex-shrink:0}
.cov-fill{height:100%;border-radius:3px}
.cov-pct{font-size:10px;min-width:28px;text-align:right;font-family:monospace;font-weight:600}
.fields-toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.fields-legend{font-size:11px;color:#9ca3af;margin-top:8px}
.tog{position:relative;width:32px;height:18px;flex-shrink:0}
.tog input{opacity:0;width:0;height:0;position:absolute}
.tog-slider{position:absolute;inset:0;border-radius:18px;cursor:pointer;background:#d1d5db}
.tog-slider:before{content:"";position:absolute;height:14px;width:14px;left:2px;bottom:2px;border-radius:50%;background:#fff;transition:.15s;box-shadow:0 1px 2px rgba(0,0,0,.2)}
input:checked+.tog-slider{background:#16a34a}
input:checked+.tog-slider:before{transform:translateX(14px)}
input:disabled+.tog-slider{cursor:not-allowed;opacity:.5}
.prev-hotel{border:1px solid #e5e7eb;border-radius:8px;overflow:hidden;margin-bottom:8px}
.prev-head{display:flex;align-items:center;gap:8px;padding:9px 12px;background:#f9fafb;border-bottom:1px solid #e5e7eb}
.prev-fields-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:3px;padding:8px 12px}
.pf{font-size:11px;font-family:monospace;display:flex;align-items:center;gap:3px;padding:2px 0}
.pf-ok{color:#16a34a}.pf-off{color:#d1d5db;text-decoration:line-through}.pf-warn{color:#f59e0b}
.sum-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:14px}
.sum-card{padding:12px;background:#fff;border:1px solid #e5e7eb;border-radius:8px;text-align:center}
.sum-num{font-size:24px;font-weight:700;color:#1a1d23}
.sum-lbl{font-size:11px;color:#6b7280;margin-top:2px}
.result-row{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:7px;font-size:12px;margin-bottom:4px}
.r-ok{background:#d1fae5;color:#065f46}.r-skip{background:#fef3c7;color:#92400e}.r-err{background:#fee2e2;color:#991b1b}
.r-ref{font-family:monospace;font-weight:700;min-width:54px}
.btn-p{padding:9px 20px;background:#1a1d23;color:#fff;border:none;border-radius:7px;cursor:pointer;font-size:13px;font-weight:600;font-family:inherit}
.btn-p:hover{opacity:.82}.btn-p:disabled{opacity:.35;cursor:not-allowed}
.btn-s{padding:8px 16px;background:#fff;border:1px solid #d1d5db;border-radius:7px;cursor:pointer;font-size:13px;color:#1a1d23;font-family:inherit}
.btn-s:hover{background:#f3f4f6}
.btn-row{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}
.spinner{display:inline-block;width:14px;height:14px;border:2px solid #d1d5db;border-top-color:#1a1d23;border-radius:50%;animation:spin .6s linear infinite;vertical-align:middle;margin-right:4px}
@keyframes spin{to{transform:rotate(360deg)}}
.divider{height:1px;background:#e5e7eb;margin:14px 0}
.json-box{font-family:monospace;font-size:11px;background:#1a1d23;color:#a8ff78;padding:12px;border-radius:7px;overflow-x:auto;white-space:pre;max-height:260px;overflow-y:auto}
.empty{padding:32px 0;text-align:center;color:#9ca3af;font-size:13px}
.action-bar{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;margin-bottom:12px}
.langs-info{font-size:12px;color:#6b7280;margin-bottom:10px;padding:8px 12px;background:#f9fafb;border-radius:7px;border:1px solid #e5e7eb}
"""

_HTML_BODY = """
<h1>Export Panel &mdash; BookingScraper Pro</h1>
<p class="sub">Visualizaci&oacute;n y exportaci&oacute;n de datos a la API externa &middot; v6.0.0 Build 93</p>

<div id="status-bar" class="status-bar">
  <span class="dot" id="api-dot"></span>
  <span class="status-label" id="api-label">Verificando API&hellip;</span>
  <span class="status-detail" id="api-detail"></span>
</div>

<div class="lang-bar" id="lang-bar">
  <span class="lang-bar-label">Idiomas a exportar:</span>
  <div class="lang-checks" id="lang-checks">
    <span style="font-size:12px;color:#9ca3af">Cargando idiomas&hellip;</span>
  </div>
  <span class="lang-source" id="lang-source"></span>
  <span id="lang-restricted" style="display:none" class="lang-restricted">&#9888; restringido por EXT_API_DEFAULT_LANGUAGES</span>
</div>

<div class="tabs">
  <button class="tab active" data-tab="sel">1 &mdash; Selecci&oacute;n</button>
  <button class="tab" data-tab="campos">2 &mdash; Campos</button>
  <button class="tab" data-tab="prev">3 &mdash; Visualizaci&oacute;n</button>
  <button class="tab" data-tab="exp">4 &mdash; Exportar</button>
</div>

<div id="tab-sel" class="tab-content active">
  <div class="label">Modo de entrada</div>
  <div class="mode-grid">
    <div class="mode-card sel" data-mode="manual" onclick="setMode('manual')">
      <div class="mode-title">Lista de external_ref</div>
      <div class="mode-sub">1 o varios identificadores</div>
    </div>
    <div class="mode-card" data-mode="all" onclick="setMode('all')">
      <div class="mode-title">Todos los completados</div>
      <div class="mode-sub">idiomas 100% completados</div>
    </div>
    <div class="mode-card" data-mode="csv" onclick="setMode('csv')">
      <div class="mode-title">Cargar CSV</div>
      <div class="mode-sub">Columna &uacute;nica: external_ref</div>
    </div>
  </div>

  <div id="mode-manual">
    <div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:4px">
      <span class="label" style="margin-bottom:0">external_ref &mdash; uno o varios</span>
    </div>
    <div class="sep-row" style="margin-bottom:6px">
      <span style="color:#9ca3af">Separadores v&aacute;lidos:</span>
      <span class="sep-chip">,</span>
      <span class="sep-chip">;</span>
      <span class="sep-chip">nueva l&iacute;nea</span>
      <span class="sep-chip">tabulador</span>
    </div>
    <textarea id="manual-input" rows="4"
      placeholder="77643, 78615, 78575&#10;&mdash; &oacute; uno por l&iacute;nea &mdash;&#10;77643&#10;78615"
      oninput="onManualChange()"></textarea>
    <div class="hint" style="margin-top:4px">
      Introducir el external_ref del sistema externo. El panel resuelve autom&aacute;ticamente el url_id interno y verifica idiomas.
    </div>
  </div>

  <div id="mode-all" style="display:none">
    <div class="info-box">
      <span>&#8505;</span>
      <span id="all-info-text">Se incluir&aacute;n todos los hoteles con los idiomas scrapeados completados. Los hoteles con idiomas pendientes quedan excluidos.</span>
    </div>
    <button class="btn-s" onclick="loadAllCompleted()">Cargar hoteles completados</button>
  </div>

  <div id="mode-csv" style="display:none">
    <div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:6px">
      <span class="label" style="margin-bottom:0">Archivo CSV</span>
      <span class="hint" style="margin-bottom:0">columna &uacute;nica: external_ref (con o sin cabecera)</span>
    </div>
    <div class="upload-zone" id="upload-zone" onclick="document.getElementById('csv-input').click()">
      <div class="upload-text" id="upload-text">
        <b>Clic para seleccionar archivo .csv</b><br>
        <span style="font-size:11px;font-family:monospace">formato: una columna, un external_ref por fila</span>
      </div>
      <div id="csv-preview" class="csv-preview" style="display:none"></div>
    </div>
    <input type="file" id="csv-input" accept=".csv,.txt" style="display:none" onchange="loadCSV(event)">
  </div>

  <div id="resolved-section" style="display:none">
    <div class="divider"></div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
      <span class="label" style="margin-bottom:0" id="resolved-title">Resoluci&oacute;n</span>
      <button class="btn-s" style="font-size:11px;padding:4px 10px" onclick="goTab('prev')">Ver datos &rarr;</button>
    </div>
    <div class="hotel-list" id="hotel-list"></div>
    <div id="warn-incomplete" class="warn-box" style="display:none">
      <span>&#9888;</span><span id="warn-incomplete-text"></span>
    </div>
  </div>
</div>

<div id="tab-campos" class="tab-content">
  <div class="fields-toolbar">
    <span class="label" style="margin-bottom:0" id="fields-count-label">Campos activos: 0 / 0</span>
    <div style="display:flex;gap:6px">
      <button class="btn-s" style="font-size:11px;padding:4px 10px" onclick="setAllFields(true)">Activar todos</button>
      <button class="btn-s" style="font-size:11px;padding:4px 10px" onclick="setAllFields(false)">Desactivar todos</button>
    </div>
  </div>
  <div class="fields-grid" id="fields-grid"></div>
  <div class="divider"></div>
  <div class="fields-legend">
    &#128274; = desactivado permanentemente &nbsp;&middot;&nbsp; barra = cobertura real en base de datos
  </div>
</div>

<div id="tab-prev" class="tab-content">
  <div id="prev-empty" class="empty">Selecciona hoteles en la pesta&ntilde;a Selecci&oacute;n para visualizar los datos.</div>
  <div id="prev-panel" style="display:none">
    <div class="action-bar">
      <div>
        <div style="font-size:13px;font-weight:600;margin-bottom:2px" id="prev-summary-title">&mdash;</div>
        <div style="font-size:11px;color:#6b7280" id="prev-langs-summary">&mdash;</div>
      </div>
      <button class="btn-p" onclick="runPreview()" id="btn-preview">Generar visualizaci&oacute;n</button>
    </div>
    <div id="prev-results"></div>
    <div id="prev-to-exp" style="display:none;margin-top:10px;text-align:right">
      <button class="btn-p" onclick="goTab('exp')">Pasar a exportar &rarr;</button>
    </div>
  </div>
</div>

<div id="tab-exp" class="tab-content">
  <div class="sum-grid">
    <div class="sum-card"><div class="sum-num" id="sum-valid">0</div><div class="sum-lbl">A enviar</div></div>
    <div class="sum-card"><div class="sum-num" id="sum-excl" style="color:#f59e0b">0</div><div class="sum-lbl">Excluidos</div></div>
    <div class="sum-card"><div class="sum-num" id="sum-nf" style="color:#ef4444">0</div><div class="sum-lbl">No encontrados</div></div>
    <div class="sum-card"><div class="sum-num" id="sum-fields">0</div><div class="sum-lbl">Campos activos</div></div>
  </div>
  <div class="langs-info" id="exp-langs-info"></div>
  <div id="exp-empty" class="warn-box" style="display:none">
    <span>&#9888;</span><span>Sin hoteles v&aacute;lidos seleccionados &mdash; ir a Selecci&oacute;n.</span>
  </div>
  <div id="exp-panel" style="display:none">
    <div class="btn-row" id="exp-btn-row">
      <button class="btn-p" onclick="runExport()" id="btn-export">Enviar a API externa</button>
      <button class="btn-s" onclick="goTab('prev')">Revisar visualizaci&oacute;n</button>
    </div>
    <div id="exp-results"></div>
    <div class="btn-row" id="exp-after" style="display:none">
      <button class="btn-s" onclick="resetExport()">Nueva exportaci&oacute;n</button>
    </div>
  </div>
</div>
"""

_JS = r"""
const FIELD_DEFS=[
  {key:"name",cov:100,on:true,can:true},{key:"rating",cov:92,on:true,can:true},
  {key:"address",cov:100,on:true,can:true},{key:"geoPosition",cov:100,on:true,can:true},
  {key:"services",cov:100,on:true,can:true},{key:"conditions",cov:92,on:true,can:true},
  {key:"toConsider",cov:85,on:true,can:true},{key:"images",cov:100,on:true,can:true},
  {key:"scoreReview",cov:100,on:true,can:true},{key:"scoreReviewBasedOn",cov:92,on:true,can:true},
  {key:"accommodationType",cov:100,on:true,can:true},{key:"longDescription",cov:100,on:true,can:true},
  {key:"categoryScoreReview",cov:100,on:true,can:true},{key:"nearbyPlaces",cov:100,on:true,can:true},
  {key:"seoDescription",cov:100,on:true,can:true},{key:"keywords",cov:100,on:true,can:true},
  {key:"guestValues",cov:92,on:true,can:true},{key:"extraInfo",cov:85,on:true,can:true},
  {key:"roomsQuantity",cov:69,on:true,can:true},{key:"rooms",cov:69,on:true,can:true},
  {key:"reviews",cov:15,on:false,can:true},
  {key:"priceRange",cov:0,on:false,can:false,reason:"Siempre null"},
  {key:"rooms.images",cov:0,on:false,can:false,reason:"GAP-ROOM-IMAGES pendiente"},
];

let st={
  mode:"manual", resolvedHotels:[], csvFile:null,
  fields:FIELD_DEFS.map(f=>({...f})),
  scrapedLangs:[], selectedLangs:[], langSource:"", langRestricted:false,
};

function covColor(c){return c===0?"#ef4444":c<70?"#f59e0b":c<85?"#fb923c":"#16a34a";}

document.addEventListener("DOMContentLoaded",async()=>{
  renderFields();
  await Promise.all([checkAPIStatus(),loadLanguages()]);
  updateExportTab();
});

async function checkAPIStatus(){
  try{
    const d=await fetchJSON("/export/config");
    const dot=document.getElementById("api-dot");
    const bar=document.getElementById("status-bar");
    if(d.ready){
      dot.className="dot";
      document.getElementById("api-label").textContent="API configurada y activa";
      bar.style.background="#f0fdf4";bar.style.borderColor="#bbf7d0";
      document.getElementById("api-detail").textContent="PATCH /update/{hotel_id}.json";
    }else{
      dot.className="dot dot-warn";
      document.getElementById("api-label").textContent="API no configurada — editar .env";
      bar.style.background="#fffbeb";bar.style.borderColor="#fcd34d";
      document.getElementById("api-detail").textContent="EXT_API_BASE_URL o EXT_API_KEY vacios";
    }
  }catch(e){
    document.getElementById("api-dot").className="dot dot-err";
    document.getElementById("api-label").textContent="Servidor no disponible";
  }
}

async function loadLanguages(){
  try{
    const d=await fetchJSON("/export/languages");
    st.scrapedLangs =d.scraped_languages||[];
    st.selectedLangs=[...(d.export_languages||d.scraped_languages||[])];
    st.langSource   =d.source||"ENABLED_LANGUAGES";
    st.langRestricted=d.restricted||false;
  }catch(e){
    st.scrapedLangs=["en","es","de","fr","it","pt"];
    st.selectedLangs=["en","es","de","fr","it","pt"];
  }
  renderLangBar();
  const ai=document.getElementById("all-info-text");
  if(ai&&st.scrapedLangs.length)
    ai.textContent="Se incluiran todos los hoteles con los "+st.scrapedLangs.length+" idiomas completados ("+st.scrapedLangs.join(", ")+"). Los hoteles con idiomas pendientes quedan excluidos.";
}

function renderLangBar(){
  const c=document.getElementById("lang-checks");
  c.innerHTML=st.scrapedLangs.map(lang=>{
    const checked=st.selectedLangs.includes(lang);
    const isEn=lang==="en";
    return `<label class="lang-check ${checked?"active":"inactive"}" id="lc-${lang}"><input type="checkbox" ${checked?"checked":""} ${isEn?"disabled":""} onchange="toggleLang('${lang}',this.checked)">${lang.toUpperCase()}</label>`;
  }).join("");
  document.getElementById("lang-source").textContent="fuente: "+st.langSource;
  document.getElementById("lang-restricted").style.display=st.langRestricted?"inline-flex":"none";
}

function toggleLang(lang,checked){
  if(lang==="en")return;
  if(checked){if(!st.selectedLangs.includes(lang))st.selectedLangs.push(lang);}
  else{st.selectedLangs=st.selectedLangs.filter(l=>l!==lang);}
  st.selectedLangs=["en",...st.selectedLangs.filter(l=>l!=="en")];
  st.scrapedLangs.forEach(l=>{
    const el=document.getElementById("lc-"+l);
    if(el)el.className="lang-check "+(st.selectedLangs.includes(l)?"active":"inactive");
  });
  resetPreview();updateExportTab();
}

function getSelectedLangsStr(){return st.selectedLangs.join(",");}

document.querySelectorAll(".tab").forEach(t=>t.addEventListener("click",()=>goTab(t.dataset.tab)));
function goTab(id){
  document.querySelectorAll(".tab").forEach(t=>t.classList.toggle("active",t.dataset.tab===id));
  document.querySelectorAll(".tab-content").forEach(c=>c.classList.toggle("active",c.id==="tab-"+id));
  if(id==="exp")updateExportTab();
  if(id==="prev")updatePrevTab();
}

function setMode(m){
  st.mode=m;st.resolvedHotels=[];
  document.querySelectorAll(".mode-card").forEach(c=>c.classList.toggle("sel",c.dataset.mode===m));
  document.getElementById("mode-manual").style.display=m==="manual"?"block":"none";
  document.getElementById("mode-all").style.display=m==="all"?"block":"none";
  document.getElementById("mode-csv").style.display=m==="csv"?"block":"none";
  document.getElementById("resolved-section").style.display="none";
  resetPreview();
}

let manualTimer=null;
function onManualChange(){clearTimeout(manualTimer);manualTimer=setTimeout(resolveManual,480);}

async function resolveManual(){
  const refs=parseRefs(document.getElementById("manual-input").value);
  if(!refs.length){document.getElementById("resolved-section").style.display="none";return;}
  await resolveRefs(refs);
}

function parseRefs(txt){return txt.split(/[,;\n\t]+/).map(s=>s.trim()).filter(Boolean);}

async function loadAllCompleted(){
  try{const d=await fetchJSON("/export/resolve?mode=all");st.resolvedHotels=d.hotels||[];renderResolved();}
  catch(e){alert("Error: "+e.message);}
}

function loadCSV(event){
  const file=event.target.files[0];if(!file)return;
  st.csvFile=file;
  const reader=new FileReader();
  reader.onload=async ev=>{
    const lines=ev.target.result.split(/\r?\n/).map(l=>l.trim()).filter(Boolean)
      .filter(l=>!/^external_ref$/i.test(l));
    const refs=lines.flatMap(l=>parseRefs(l));
    document.getElementById("upload-zone").classList.add("loaded");
    document.getElementById("upload-text").innerHTML="<b>"+esc(file.name)+"</b> — "+refs.length+" registros";
    const prev=document.getElementById("csv-preview");prev.style.display="block";
    prev.textContent=refs.slice(0,10).join(" - ")+(refs.length>10?" +"+(refs.length-10)+" mas":"");
    await resolveRefs(refs);
  };reader.readAsText(file);
}

async function resolveRefs(refs){
  try{const d=await fetchJSON("/export/resolve?refs="+encodeURIComponent(refs.join(",")));st.resolvedHotels=d.hotels||[];renderResolved();resetPreview();}
  catch(e){alert("Error al resolver: "+e.message);}
}

function renderResolved(){
  const h=st.resolvedHotels;
  const sec=document.getElementById("resolved-section");
  if(!h.length){sec.style.display="none";return;}
  sec.style.display="block";
  const valid=h.filter(x=>x.found&&x.is_complete);
  const excl=h.filter(x=>x.found&&!x.is_complete);
  const nf=h.filter(x=>!x.found);
  document.getElementById("resolved-title").textContent=valid.length+" ok - "+excl.length+" excluidos - "+nf.length+" no encontrados";
  document.getElementById("hotel-list").innerHTML=h.map(hotel=>{
    const cls=!hotel.found?"notfound":!hotel.is_complete?"excl":"";
    const langs=st.scrapedLangs.map(l=>`<span class="lp ${(hotel.languages_done||[]).includes(l)?"lp-ok":"lp-miss"}">${l}</span>`).join("");
    const badge=!hotel.found?`<span class="badge b-err">no encontrado</span>`:!hotel.is_complete?`<span class="badge b-warn">excluido</span>`:`<span class="badge b-ok">listo</span>`;
    return `<div class="hotel-row ${cls}"><span class="h-ref">${esc(hotel.external_ref)}</span><span class="h-name">${esc(hotel.hotel_name||"")}</span>${hotel.found?`<div class="lang-pills">${langs}</div>`:""} ${badge}</div>`;
  }).join("");
  const warn=document.getElementById("warn-incomplete");
  if(excl.length){warn.style.display="flex";document.getElementById("warn-incomplete-text").textContent=excl.length+" hotel(es) con idiomas incompletos - excluidos del envio";}
  else warn.style.display="none";
  updateExportTab();
}

function renderFields(){
  document.getElementById("fields-grid").innerHTML=st.fields.map(f=>{
    const inactive=!f.on&&f.can;
    return `<div class="field-row${!f.can?" locked":""}${inactive?" inactive":""}"><label class="tog"><input type="checkbox" ${!f.can?"disabled":""} ${f.on?"checked":""} onchange="toggleField('${f.key}',this.checked)"><span class="tog-slider"></span></label><span class="field-name">${esc(f.key)}</span><div class="cov-bar"><div class="cov-fill" style="width:${f.cov}%;background:${covColor(f.cov)}"></div></div><span class="cov-pct" style="color:${covColor(f.cov)}">${f.cov}%</span>${!f.can?`<span style="font-size:13px;cursor:help" title="${esc(f.reason||"")}">&#128274;</span>`:""}</div>`;
  }).join("");
  updateFieldsCount();
}

function toggleField(key,val){st.fields=st.fields.map(f=>f.key===key&&f.can?{...f,on:val}:f);renderFields();resetPreview();}
function setAllFields(val){st.fields=st.fields.map(f=>f.can?{...f,on:val}:f);renderFields();resetPreview();}
function updateFieldsCount(){
  const a=st.fields.filter(f=>f.on).length;
  document.getElementById("fields-count-label").textContent="Campos activos: "+a+" / "+st.fields.length;
  document.getElementById("sum-fields").textContent=a;
}

function updatePrevTab(){
  const valid=getValidHotels();
  document.getElementById("prev-empty").style.display=valid.length?"none":"";
  document.getElementById("prev-panel").style.display=valid.length?"":"none";
  if(!valid.length)return;
  document.getElementById("prev-summary-title").textContent=valid.length+" hotel(es) - "+st.fields.filter(f=>f.on).length+" campos activos";
  document.getElementById("prev-langs-summary").textContent="Idiomas: "+st.selectedLangs.join(", ")+" - dry-run sin envio";
}

async function runPreview(){
  const valid=getValidHotels();if(!valid.length)return;
  const btn=document.getElementById("btn-preview");
  btn.disabled=true;btn.innerHTML='<span class="spinner"></span>Generando...';
  try{
    const d=await postJSON("/export/preview/refs",{
      external_refs:valid.map(h=>h.external_ref),
      languages:getSelectedLangsStr(),
      fields:st.fields.filter(f=>f.on).map(f=>f.key).join(","),
      dry_run:true,
    });
    renderPreviewResults(d);
    document.getElementById("prev-to-exp").style.display="block";
  }catch(e){document.getElementById("prev-results").innerHTML=`<div class="warn-box"><span>x</span><span>Error: ${esc(e.message)}</span></div>`;}
  btn.disabled=false;btn.textContent="Generar visualizacion";
}

function renderPreviewResults(data){
  const el=document.getElementById("prev-results");
  const items=data.results||[];
  if(!items.length){el.innerHTML='<div class="empty">Sin resultados</div>';return;}
  el.innerHTML=items.map(item=>{
    const head=`<div class="prev-head"><span class="h-ref">${esc(item.external_ref)}</span><span style="font-size:13px;font-weight:600;flex:1">${esc(item.hotel_name||"")}</span>${item.error?`<span class="badge b-err">error</span>`:`<span class="badge b-ok">payload ok</span>`}</div>`;
    if(item.error)return`<div class="prev-hotel">${head}<div style="padding:8px 12px;font-size:12px;color:#991b1b">${esc(item.error)}</div></div>`;
    const fieldsHtml=st.fields.map(f=>`<div class="pf ${!f.on?"pf-off":f.cov===0?"pf-warn":"pf-ok"}">${!f.on?"- ":f.cov===0?"! ":"+ "}${esc(f.key)}</div>`).join("");
    const locales=item.payload&&item.payload.args&&item.payload.args.locales?item.payload.args.locales.join(", "):"";
    const json=item.payload?JSON.stringify(item.payload,null,2).split("\n").slice(0,18).join("\n")+"\n  ...":"";
    return`<div class="prev-hotel">${head}<div style="padding:4px 12px 2px;font-size:11px;color:#6b7280">idiomas en payload: <b>${esc(locales)}</b></div><div class="prev-fields-grid">${fieldsHtml}</div>${json?`<details style="padding:4px 12px 8px"><summary style="font-size:11px;cursor:pointer;color:#6b7280">Ver JSON</summary><div class="json-box">${esc(json)}</div></details>`:""}</div>`;
  }).join("");
}

function resetPreview(){document.getElementById("prev-results").innerHTML="";document.getElementById("prev-to-exp").style.display="none";}

function updateExportTab(){
  const valid=getValidHotels();const excl=getExcluded();const nf=getNotFound();
  document.getElementById("sum-valid").textContent=valid.length;
  document.getElementById("sum-excl").textContent=excl.length;
  document.getElementById("sum-nf").textContent=nf.length;
  document.getElementById("sum-fields").textContent=st.fields.filter(f=>f.on).length;
  document.getElementById("exp-langs-info").textContent=st.selectedLangs.length?"Idiomas en el payload: "+st.selectedLangs.join(", "):"Selecciona al menos un idioma";
  const empty=document.getElementById("exp-empty");const panel=document.getElementById("exp-panel");
  if(!valid.length){empty.style.display="flex";panel.style.display="none";}
  else{empty.style.display="none";panel.style.display="block";}
}

async function runExport(){
  const valid=getValidHotels();if(!valid.length)return;
  const btn=document.getElementById("btn-export");
  btn.disabled=true;btn.innerHTML='<span class="spinner"></span>Enviando...';
  document.getElementById("exp-results").innerHTML="";
  try{
    let d;
    if(st.mode==="csv"&&st.csvFile){
      const fd=new FormData();
      fd.append("file",st.csvFile);fd.append("languages",getSelectedLangsStr());
      fd.append("fields",st.fields.filter(f=>f.on).map(f=>f.key).join(","));fd.append("dry_run","false");
      const r=await fetch("/export/send/csv",{method:"POST",body:fd});d=await r.json();
    }else{
      d=await postJSON("/export/send/refs",{external_refs:valid.map(h=>h.external_ref),languages:getSelectedLangsStr(),fields:st.fields.filter(f=>f.on).map(f=>f.key).join(","),dry_run:false});
    }
    renderExportResults(d);
  }catch(e){document.getElementById("exp-results").innerHTML=`<div class="warn-box"><span>x</span><span>Error: ${esc(e.message)}</span></div>`;}
  btn.disabled=false;btn.textContent="Enviar a API externa";
  document.getElementById("exp-after").style.display="flex";
}

function renderExportResults(data){
  const el=document.getElementById("exp-results");const rows=data.results||[];
  if(!rows.length){el.innerHTML='<div class="empty">Sin resultados</div>';return;}
  const ok=rows.filter(r=>r.status==="ok").length;
  const skip=rows.filter(r=>r.status==="skip").length;
  const err=rows.filter(r=>r.status==="error").length;
  el.innerHTML=`<div style="font-size:12px;font-weight:600;color:#6b7280;margin-bottom:6px">Resultado: ${ok} enviados - ${skip} saltados - ${err} errores</div>`
    +rows.map(row=>{
      const cls=row.status==="ok"?"r-ok":row.status==="skip"?"r-skip":"r-err";
      const txt=row.status==="ok"?`HTTP ${row.response_status}`:row.status==="skip"?`! ${row.reason||""}`: `x ${row.error||row.reason||"error"}`;
      return`<div class="result-row ${cls}"><span class="r-ref">${esc(row.external_ref)}</span><span style="flex:1">${esc(row.hotel_name||"")}</span><span>${esc(txt)}</span></div>`;
    }).join("");
}

function resetExport(){document.getElementById("exp-results").innerHTML="";document.getElementById("exp-after").style.display="none";updateExportTab();}

function getValidHotels(){return st.resolvedHotels.filter(h=>h.found&&h.is_complete);}
function getExcluded(){return st.resolvedHotels.filter(h=>h.found&&!h.is_complete);}
function getNotFound(){return st.resolvedHotels.filter(h=>!h.found);}

function esc(s){return String(s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}
async function fetchJSON(url){const r=await fetch(url);if(!r.ok)throw new Error("HTTP "+r.status);return r.json();}
async function postJSON(url,body){const r=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});if(!r.ok)throw new Error("HTTP "+r.status);return r.json();}
"""

def build_export_ui_html() -> str:
    """Devuelve el HTML completo del panel de exportación Build 93."""
    return (
        "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n"
        "<meta charset=\"UTF-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>Export Panel \u2014 BookingScraper Pro</title>\n"
        "<style>\n" + _CSS + "\n</style>\n"
        "</head>\n<body>\n"
        + _HTML_BODY
        + "\n<script>\n" + _JS + "\n</script>\n"
        "</body>\n</html>"
    )
