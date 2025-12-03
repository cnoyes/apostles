#!/usr/bin/env python3
# Single-file local web app with mock data + Plotly charts
# Run: python3 app.py  (then open the printed LAN URL)

import os, socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Apostles • Age & Probability</title>
  <meta name="theme-color" content="#0F766E" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    :root{
      --bg:#0b1020; --card:#12182b; --muted:#9aa4b2; --text:#e6eaf0;
      --accent:#0F766E; --accent-2:#0C4A6E; --highlight:#E11D48;
    }
    *{box-sizing:border-box}
    body{margin:0;background:linear-gradient(180deg,#0b1020,#0e1427);color:var(--text);font:16px/1.45 "Inter",system-ui,-apple-system,Segoe UI,Roboto,Arial}
    .wrap{max-width:1100px;margin:0 auto;padding:20px}
    header{display:flex;align-items:center;gap:12px;margin:6px 0 18px}
    header h1{font-size:20px;margin:0}
    header p{margin:2px 0 0;color:var(--muted);font-size:14px}
    .grid{display:grid;grid-template-columns:1fr;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:1fr 1fr}}
    .card{background:var(--card);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:12px 12px 6px;box-shadow:0 6px 24px rgba(0,0,0,.25)}
    .card h3{margin:4px 6px 10px;font-size:16px}
    .details{margin-top:14px}
    .details h3{margin:0 0 8px}
    .kv{display:grid;grid-template-columns:140px 1fr;gap:6px 10px;font-size:14px;color:#cad2de}
    .kv b{color:#eaf0f7}
    a{color:#86e1d2}
    footer{margin:18px 0 8px;color:var(--muted);font-size:13px;text-align:center}
    .plot{width:100%;height:420px}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M4 6h16M4 12h16M4 18h16" stroke="#86e1d2" stroke-width="2" stroke-linecap="round"/></svg>
      <div>
        <h1>Apostles • Age & Probability</h1>
        <p>Click a bar to highlight across both charts. Double-click background to clear. Ordered by ordination (seniority).</p>
      </div>
    </header>

    <div class="grid">
      <div class="card">
        <h3>Current Age</h3>
        <div id="age" class="plot"></div>
      </div>
      <div class="card">
        <h3>Succession Probability</h3>
        <div id="prob" class="plot"></div>
      </div>
    </div>

    <div class="card details">
      <h3>Details</h3>
      <div id="details">
        <p style="color:#b8c2d3;margin:6px 0 0">Click a bar to see details here (age at ordination, years in quorum, and Wikipedia link).</p>
      </div>
    </div>

    <footer>Mock data • Names ignore middle initial “X” • © You</footer>
  </div>

<script>
// ---------- MOCK DATA (same columns as your RDS) ----------
const DATA = [
  {"First":"Dallin","Middle":"H","Last":"Oaks","Birth Date":"1932-08-12","Ordained Apostle":"1984-04-07","Age":93.1,"Age Label":93,"Prob":null,"Prob Label":""},
  {"First":"Jeffrey","Middle":"R","Last":"Holland","Birth Date":"1940-12-03","Ordained Apostle":"1994-06-23","Age":84.8,"Age Label":84,"Prob":0.666,"Prob Label":"67%"},
  {"First":"Henry","Middle":"B","Last":"Eyring","Birth Date":"1933-05-31","Ordained Apostle":"1995-04-01","Age":92.3,"Age Label":92,"Prob":0.250,"Prob Label":"25%"},
  {"First":"Dieter","Middle":"F","Last":"Uchtdorf","Birth Date":"1940-11-06","Ordained Apostle":"2004-10-02","Age":84.9,"Age Label":84,"Prob":0.361,"Prob Label":"36%"},
  {"First":"David","Middle":"A","Last":"Bednar","Birth Date":"1952-06-15","Ordained Apostle":"2004-10-02","Age":73.3,"Age Label":73,"Prob":0.586,"Prob Label":"59%"},
  {"First":"Quentin","Middle":"L","Last":"Cook","Birth Date":"1940-09-08","Ordained Apostle":"2007-10-06","Age":85.1,"Age Label":85,"Prob":0.129,"Prob Label":"13%"},
  {"First":"D","Middle":"Todd","Last":"Christofferson","Birth Date":"1945-01-24","Ordained Apostle":"2008-04-10","Age":80.7,"Age Label":80,"Prob":0.188,"Prob Label":"19%"},
  {"First":"Neil","Middle":"L","Last":"Andersen","Birth Date":"1951-08-09","Ordained Apostle":"2009-04-04","Age":74.2,"Age Label":74,"Prob":0.315,"Prob Label":"31%"},
  {"First":"Ronald","Middle":"A","Last":"Rasband","Birth Date":"1951-02-06","Ordained Apostle":"2015-10-03","Age":74.7,"Age Label":74,"Prob":0.234,"Prob Label":"23%"},
  {"First":"Gary","Middle":"E","Last":"Stevenson","Birth Date":"1955-08-06","Ordained Apostle":"2015-10-03","Age":70.2,"Age Label":70,"Prob":0.312,"Prob Label":"31%"},
  {"First":"Dale","Middle":"G","Last":"Renlund","Birth Date":"1952-11-13","Ordained Apostle":"2015-10-03","Age":72.9,"Age Label":72,"Prob":0.181,"Prob Label":"18%"},
  {"First":"Gerrit","Middle":"W","Last":"Gong","Birth Date":"1953-12-23","Ordained Apostle":"2018-03-31","Age":71.8,"Age Label":71,"Prob":0.178,"Prob Label":"18%"},
  {"First":"Ulisses","Middle":"X","Last":"Soares","Birth Date":"1958-10-02","Ordained Apostle":"2018-03-31","Age":67.0,"Age Label":67,"Prob":0.274,"Prob Label":"27%"},
  {"First":"Patrick","Middle":"X","Last":"Kearon","Birth Date":"1961-07-18","Ordained Apostle":"2023-12-08","Age":64.2,"Age Label":64,"Prob":0.308,"Prob Label":"31%"}
];

// ---------- Helpers ----------
const fmtName = (d) => {
  const mid = (!d.Middle || d.Middle === "" || d.Middle === "X") ? "" : ` ${d.Middle}.`;
  return `${d.First}${mid} ${d.Last}`;
};
const parseDate = (s) => new Date(s);
const fmtDate = (d) => d ? d.toLocaleDateString(undefined,{year:'numeric',month:'short',day:'numeric'}) : "";
const yearsBetween = (a,b) => Math.floor((b - a)/365.25/24/3600/1000);

// ---------- Transform + sort by ordination (seniority) ----------
const today = new Date();
const df = DATA
  .map(d => ({
    ...d,
    name: fmtName(d),
    birth: parseDate(d["Birth Date"]),
    ordained: parseDate(d["Ordained Apostle"])
  }))
  .sort((a,b) => a.ordained - b.ordained)
  .map((d,i) => ({
    ...d,
    seniority: i+1,
    age_at_ordination: yearsBetween(d.birth, d.ordained),
    years_in_quorum: yearsBetween(d.ordained, today),
    prob_val: d.Prob == null ? null : +d.Prob,
    prob_label: d["Prob Label"] || "",
    age_label: d["Age Label"]
  }));

const names = df.map(d => d.name);
const ages  = df.map(d => d.Age);
const prob  = df.map(d => d.prob_val ?? 0);

// Pack hover fields in customdata
const cd = df.map(d => [
  fmtDate(d.birth),
  fmtDate(d.ordained),
  d.age_at_ordination,
  d.years_in_quorum,
  d.seniority,
  (d.Prob==null) ? "—" : `${Math.round(d.Prob*1000)/10}%`
]);

// ---------- Selection state shared across charts ----------
const selected = new Set();
const selectedIndices = () => names.map((n,i)=>selected.has(n)?i:null).filter(i=>i!==null);

function applySelection(){
  const idx = [selectedIndices()];
  Plotly.restyle('age',  {selectedpoints: idx});
  Plotly.restyle('prob', {selectedpoints: idx});
  renderDetails();
}
function toggleSelection(name){
  selected.has(name) ? selected.delete(name) : selected.add(name);
  applySelection();
}
function clearSelection(){ selected.clear(); applySelection(); }

// ---------- AGE chart ----------
const ageTrace = {
  type:'bar', orientation:'h',
  y:names, x:ages,
  marker:{ color:'#0F766E' },
  text: df.map(d => d.age_label), textposition:'outside', cliponaxis:false,
  hovertemplate:
    '<b>%{y}</b><br>'+
    'Age: %{x:.1f}<br>'+
    'Born: %{customdata[0]}<br>'+
    'Ordained: %{customdata[1]}<br>'+
    'Age at ordination: %{customdata[2]}<br>'+
    'Years in Quorum: %{customdata[3]}<br>'+
    'Seniority: %{customdata[4]}<extra></extra>',
  customdata: cd,
  selected:{ marker:{opacity:1} },
  unselected:{ marker:{opacity:0.25} }
};
const ageLayout = {
  margin:{l:180,r:24,t:6,b:24},
  xaxis:{title:'Age (years)', rangemode:'tozero'},
  yaxis:{categoryorder:'array', categoryarray:names},
  paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)',
  font:{color:'#e6eaf0'},
  dragmode:false
};

// ---------- PROB chart ----------
const probTrace = {
  type:'bar', orientation:'h',
  y:names, x:prob,
  marker:{ color:'#0C4A6E' },
  text: df.map(d => d.prob_label), textposition:'outside', cliponaxis:false,
  hovertemplate:
    '<b>%{y}</b><br>'+
    'Probability: %{x:.1%}<br>'+
    'Ordained: %{customdata[1]}<br>'+
    'Age at ordination: %{customdata[2]}<br>'+
    'Years in Quorum: %{customdata[3]}<br>'+
    'Seniority: %{customdata[4]}<extra></extra>',
  customdata: cd,
  selected:{ marker:{opacity:1} },
  unselected:{ marker:{opacity:0.25} }
};
const probLayout = {
  margin:{l:180,r:24,t:6,b:24},
  xaxis:{title:'Probability', range:[0,1], tickformat:'.0%'},
  yaxis:{categoryorder:'array', categoryarray:names},
  paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)',
  font:{color:'#e6eaf0'},
  dragmode:false
};

const cfg = {responsive:true, displayModeBar:false};

(async function(){
  await Plotly.newPlot('age',  [ageTrace],  ageLayout,  cfg);
  await Plotly.newPlot('prob', [probTrace], probLayout, cfg);

  document.getElementById('age')
    .on('plotly_click', ev => { if(ev.points?.length){ toggleSelection(ev.points[0].y); }})
    .on('plotly_doubleclick', clearSelection);

  document.getElementById('prob')
    .on('plotly_click', ev => { if(ev.points?.length){ toggleSelection(ev.points[0].y); }})
    .on('plotly_doubleclick', clearSelection);

  renderDetails();
})();

// ---------- Details panel ----------
function renderDetails(){
  const el = document.getElementById('details');
  if (selected.size === 0) {
    el.innerHTML = '<p style="color:#b8c2d3;margin:6px 0 0">Click a bar to see details here.</p>';
    return;
  }
  const last = [...selected].slice(-1)[0];
  const row = df.find(d => d.name === last);
  const wiki = `https://en.wikipedia.org/wiki/${encodeURIComponent(row.First+' '+row.Last)}`;
  el.innerHTML = `
    <div class="kv">
      <b>Name</b><div>${row.name}</div>
      <b>Age</b><div>${row.Age.toFixed(1)}</div>
      <b>Born</b><div>${fmtDate(row.birth)}</div>
      <b>Ordained</b><div>${fmtDate(row.ordained)}</div>
      <b>Age at ordination</b><div>${row.age_at_ordination}</div>
      <b>Years in quorum</b><div>${row.years_in_quorum}</div>
      <b>Seniority</b><div>${row.seniority}</div>
      <b>Probability</b><div>${row.Prob==null ? '—' : (Math.round(row.Prob*1000)/10)+'%'}</div>
      <b>Wikipedia</b><div><a href="${wiki}" target="_blank" rel="noopener">Open article</a></div>
    </div>`;
}
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.end_headers()
            self.wfile.write(HTML.encode("utf-8"))
        else:
            self.send_error(404, "Not found")

    # Silence default logging
    def log_message(self, fmt, *args):
        pass

def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    host = "0.0.0.0"
    httpd = ThreadingHTTPServer((host, port), Handler)
    ip = get_lan_ip()
    print(f"\nServing locally:\n  • http://localhost:{port}")
    print(f"On your phone (same Wi-Fi):\n  • http://{ip}:{port}\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down…")
        httpd.server_close()

