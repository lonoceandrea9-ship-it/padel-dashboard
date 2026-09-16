<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Padel Performance Dashboard</title>
    <style>
        * { box-sizing: border-box; touch-action: manipulation; }
        :root {
            --bg-primary: #0f172a;
            --bg-card: #1e293b;
            --accent-blue: #38bdf8;
            --accent-purple: #a855f7;
            --accent-green: #22c55e;
            --accent-whatsapp: #25d366;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-main);
            margin: 0;
            -webkit-tap-highlight-color: transparent;
        }
        header h1 { color: var(--accent-blue); margin: 0 0 4px 0; font-size: 1.4rem; }
        header p { color: var(--text-muted); margin: 0; font-size: 0.8rem; }
        
        .main-container {
            max-width: 1000px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .card {
            background-color: var(--bg-card);
            border-radius: 14px;
            padding: 16px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.05);
            width: 100%;
        }
        .card h2 { margin-top: 0; text-align: center; font-size: 1.05rem; }
        
        .profile-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 12px; }
        .input-group { display: flex; flex-direction: column; gap: 4px; flex: 1 1 130px; }
        .input-group label { font-size: 0.8rem; color: var(--text-muted); }
        .input-group input[type="text"] {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 8px;
            padding: 10px;
            color: #fff;
            font-size: 0.95rem;
            width: 100%;
            outline: none;
        }
        
        .actions-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 10px;
        }
        
        .btn {
            border: none;
            padding: 12px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 0.85rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            transition: opacity 0.2s, transform 0.1s;
            text-decoration: none;
            color: #fff;
        }
        .btn:active { transform: scale(0.98); }
        .btn-whatsapp { background-color: #25d366; color: #fff; }
        .btn-save-img { background-color: var(--accent-purple); color: #fff; }
        .btn-share-link { background-color: var(--accent-blue); color: #0f172a; }

        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 16px;
        }
        .tech-title { color: var(--accent-blue); }
        .mental-title { color: var(--accent-purple); }
        
        .chart-container {
            position: relative;
            width: 100%;
            height: 260px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        canvas {
            width: 100% !important;
            height: 100% !important;
        }

        .controls-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 16px;
        }
        .control-group { display: flex; flex-direction: column; gap: 8px; }
        .control-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            background: rgba(255, 255, 255, 0.03);
            padding: 8px 12px;
            border-radius: 8px;
        }
        .control-item label { font-size: 0.85rem; flex: 1; }
        .control-item input[type="range"] {
            flex: 1.2;
            height: 24px;
            accent-color: var(--accent-blue);
        }
        .control-item.purple input[type="range"] { accent-color: var(--accent-purple); }
        .control-item .val-badge { font-weight: bold; min-width: 20px; text-align: right; }

        .modal-overlay {
            display: none;
            position: fixed;
            top:0; left:0; right:0; bottom:0;
            background: rgba(0,0,0,0.85);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 16px;
            overflow-y: auto;
        }
        .modal {
            background: var(--bg-card);
            border-radius: 14px;
            padding: 20px;
            width: 100%;
            max-width: 460px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .modal img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 12px 0;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .modal input[type="text"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.2);
            color: #fff;
            border-radius: 6px;
        }
        .modal-btn {
            background: var(--accent-blue);
            color: #0f172a;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 8px;
        }
        
        .toast {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--accent-green);
            color: #fff;
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            display: none;
            z-index: 2000;
        }
    </style>
</head>
<body>

    <header>
        <h1 id="playerTitle">Padel Performance Dashboard</h1>
        <p>Valutazione da 1 a 10 • Auto-salvato sul dispositivo</p>
    </header>

    <div class="main-container">
        <!-- PROFILO GIOCATORE & AZIONI -->
        <div class="card">
            <h2>Profilo Giocatore & Condivisione</h2>
            <div class="profile-grid">
                <div class="input-group">
                    <label for="firstName">Nome</label>
                    <input type="text" id="firstName" placeholder="Nome" oninput="onDataChange()">
                </div>
                <div class="input-group">
                    <label for="lastName">Cognome</label>
                    <input type="text" id="lastName" placeholder="Cognome" oninput="onDataChange()">
                </div>
            </div>
            
            <div class="actions-grid">
                <button class="btn btn-whatsapp" onclick="shareOnWhatsApp()">
                    💬 WhatsApp
                </button>
                <button class="btn btn-save-img" onclick="saveResultAsImage()">
                    💾 Salva Scheda (PNG)
                </button>
                <button class="btn btn-share-link" id="shareBtn" onclick="shareOrCopyLink()">
                    🔗 Copia Link
                </button>
            </div>
        </div>

        <!-- GRAFICI CANVAS NATIVI -->
        <div class="charts-grid">
            <div class="card">
                <h2 class="tech-title">Abilità Tecniche</h2>
                <div class="chart-container">
                    <canvas id="techCanvas"></canvas>
                </div>
            </div>
            <div class="card">
                <h2 class="mental-title">Atteggiamento & Tattica</h2>
                <div class="chart-container">
                    <canvas id="mentalCanvas"></canvas>
                </div>
            </div>
        </div>

        <!-- CONTROLLI -->
        <div class="card">
            <h2>Pannello Controllo Valori</h2>
            <div class="controls-grid">
                <div class="control-group">
                    <h3 class="tech-title" style="margin:0 0 4px 0; font-size:0.95rem;">Tecnica</h3>
                    <div class="control-item"><label>Volea</label><input type="range" id="volley" min="1" max="10" value="8" oninput="onDataChange()"><span id="volley-val" class="val-badge">8</span></div>
                    <div class="control-item"><label>Smash</label><input type="range" id="smash" min="1" max="10" value="7" oninput="onDataChange()"><span id="smash-val" class="val-badge">7</span></div>
                    <div class="control-item"><label>Bandeja</label><input type="range" id="bandeja" min="1" max="10" value="8" oninput="onDataChange()"><span id="bandeja-val" class="val-badge">8</span></div>
                    <div class="control-item"><label>Servizio</label><input type="range" id="serve" min="1" max="10" value="7" oninput="onDataChange()"><span id="serve-val" class="val-badge">7</span></div>
                    <div class="control-item"><label>Difesa da Fondo</label><input type="range" id="defense" min="1" max="10" value="9" oninput="onDataChange()"><span id="defense-val" class="val-badge">9</span></div>
                    <div class="control-item"><label>Chiquita</label><input type="range" id="chiquita" min="1" max="10" value="6" oninput="onDataChange()"><span id="chiquita-val" class="val-badge">6</span></div>
                </div>
                <div class="control-group">
                    <h3 class="mental-title" style="margin:0 0 4px 0; font-size:0.95rem;">Tattica & Mental</h3>
                    <div class="control-item purple"><label>Intesa di Coppia</label><input type="range" id="chemistry" min="1" max="10" value="9" oninput="onDataChange()"><span id="chemistry-val" class="val-badge">9</span></div>
                    <div class="control-item purple"><label>Gestione Errore</label><input type="range" id="errorManagement" min="1" max="10" value="7" oninput="onDataChange()"><span id="errorManagement-val" class="val-badge">7</span></div>
                    <div class="control-item purple"><label>Posizionamento</label><input type="range" id="positioning" min="1" max="10" value="8" oninput="onDataChange()"><span id="positioning-val" class="val-badge">8</span></div>
                    <div class="control-item purple"><label>Concentrazione</label><input type="range" id="focus" min="1" max="10" value="8" oninput="onDataChange()"><span id="focus-val" class="val-badge">8</span></div>
                    <div class="control-item purple"><label>Resistenza</label><input type="range" id="stamina" min="1" max="10" value="9" oninput="onDataChange()"><span id="stamina-val" class="val-badge">9</span></div>
                    <div class="control-item purple"><label>Intensità</label><input type="range" id="intensity" min="1" max="10" value="7" oninput="onDataChange()"><span id="intensity-val" class="val-badge">7</span></div>
                </div>
            </div>
        </div>
    </div>

    <!-- MODALE ANTEPRIMA IMMAGINE / LINK -->
    <div class="modal-overlay" id="mainModal">
        <div class="modal">
            <h3 id="modalTitle" style="margin-top:0">Scheda Generata</h3>
            <div id="modalContent"></div>
            <button class="modal-btn" onclick="closeModal()">Chiudi</button>
        </div>
    </div>

    <!-- TOAST NOTIFICATION -->
    <div class="toast" id="toastMsg">✓ Salvato!</div>

    <script>
        const techKeys = ['volley', 'smash', 'bandeja', 'serve', 'defense', 'chiquita'];
        const techLabels = ['Volea', 'Smash', 'Bandeja', 'Servizio', 'Difesa', 'Chiquita'];
        
        const mentalKeys = ['chemistry', 'errorManagement', 'positioning', 'focus', 'stamina', 'intensity'];
        const mentalLabels = ['Intesa', 'Errori', 'Posizione', 'Focus', 'Resistenza', 'Intensità'];

        // DISEGNATORE RADAR CANVAS NATIVO
        function drawRadarChart(canvasId, labels, dataValues, lineColor, fillColor) {
            const canvas = document.getElementById(canvasId);
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            
            const rect = canvas.getBoundingClientRect();
            const dpr = window.devicePixelRatio || 1;
            
            canvas.width = rect.width * dpr;
            canvas.height = rect.height * dpr;
            ctx.scale(dpr, dpr);

            const width = rect.width;
            const height = rect.height;
            const centerX = width / 2;
            const centerY = height / 2;
            const radius = Math.min(centerX, centerY) - 32;

            ctx.clearRect(0, 0, width, height);

            const numAxes = labels.length;
            const levels = 5;

            // Griglia ragnatela
            for (let l = 1; l <= levels; l++) {
                const r = (radius / levels) * l;
                ctx.beginPath();
                for (let i = 0; i < numAxes; i++) {
                    const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
                    const x = centerX + r * Math.cos(angle);
                    const y = centerY + r * Math.sin(angle);
                    if (i === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }
                ctx.closePath();
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
                ctx.lineWidth = 1;
                ctx.stroke();
            }

            // Assi ed Etichette
            ctx.font = 'bold 10px -apple-system, sans-serif';
            ctx.fillStyle = '#94a3b8';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            for (let i = 0; i < numAxes; i++) {
                const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
                const x = centerX + radius * Math.cos(angle);
                const y = centerY + radius * Math.sin(angle);

                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.lineTo(x, y);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
                ctx.stroke();

                const labelR = radius + 18;
                const lx = centerX + labelR * Math.cos(angle);
                const ly = centerY + labelR * Math.sin(angle);
                ctx.fillText(labels[i], lx, ly);
            }

            // Poligono Dati
            ctx.beginPath();
            for (let i = 0; i < numAxes; i++) {
                const val = Math.max(1, Math.min(10, dataValues[i]));
                const r = (radius / 10) * val;
                const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
                const x = centerX + r * Math.cos(angle);
                const y = centerY + r * Math.sin(angle);
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.closePath();
            ctx.fillStyle = fillColor;
            ctx.fill();
            ctx.strokeStyle = lineColor;
            ctx.lineWidth = 2.5;
            ctx.stroke();

            // Punti
            for (let i = 0; i < numAxes; i++) {
                const val = Math.max(1, Math.min(10, dataValues[i]));
                const r = (radius / 10) * val;
                const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
                const x = centerX + r * Math.cos(angle);
                const y = centerY + r * Math.sin(angle);
                ctx.beginPath();
                ctx.arc(x, y, 4, 0, Math.PI * 2);
                ctx.fillStyle = lineColor;
                ctx.fill();
            }
        }

        function renderAll() {
            const tVals = techKeys.map(id => parseInt(document.getElementById(id).value));
            const mVals = mentalKeys.map(id => parseInt(document.getElementById(id).value));

            techKeys.forEach((id, i) => document.getElementById(id + '-val').innerText = tVals[i]);
            mentalKeys.forEach((id, i) => document.getElementById(id + '-val').innerText = mVals[i]);

            drawRadarChart('techCanvas', techLabels, tVals, '#38bdf8', 'rgba(56, 189, 248, 0.3)');
            drawRadarChart('mentalCanvas', mentalLabels, mVals, '#a855f7', 'rgba(168, 85, 247, 0.3)');

            const fname = document.getElementById('firstName').value.trim();
            const lname = document.getElementById('lastName').value.trim();
            const fullName = `${fname} ${lname}`.trim();
            document.getElementById('playerTitle').innerText = fullName ? `${fullName} - Dashboard` : `Padel Performance Dashboard`;
        }

        function onDataChange() {
            renderAll();
            saveToLocalStorage();
        }

        function saveToLocalStorage() {
            const data = {
                fname: document.getElementById('firstName').value,
                lname: document.getElementById('lastName').value,
                tech: techKeys.map(id => document.getElementById(id).value),
                mental: mentalKeys.map(id => document.getElementById(id).value)
            };
            try { localStorage.setItem('padel_dashboard_data', JSON.stringify(data)); } catch(e){}
        }

        function generateShareUrl() {
            const fname = document.getElementById('firstName').value;
            const lname = document.getElementById('lastName').value;
            const tVals = techKeys.map(id => document.getElementById(id).value).join(',');
            const mVals = mentalKeys.map(id => document.getElementById(id).value).join(',');

            let baseUrl = window.location.href.split('?')[0];
            if (!baseUrl.startsWith('http')) {
                baseUrl = 'https://padel-dashboard.local/';
            }

            const url = new URL(baseUrl);
            if (fname) url.searchParams.set('fname', fname);
            if (lname) url.searchParams.set('lname', lname);
            url.searchParams.set('tech', tVals);
            url.searchParams.set('mental', mVals);
            return url.toString();
        }

        // 💬 CONDIVISIONE WHATSAPP
        function shareOnWhatsApp() {
            const fname = document.getElementById('firstName').value.trim();
            const lname = document.getElementById('lastName').value.trim();
            const name = `${fname} ${lname}`.trim() || 'Giocatore';
            
            const tVals = techKeys.map(id => parseInt(document.getElementById(id).value));
            const mVals = mentalKeys.map(id => parseInt(document.getElementById(id).value));
            
            const avgTech = (tVals.reduce((a,b)=>a+b,0) / tVals.length).toFixed(1);
            const avgMental = (mVals.reduce((a,b)=>a+b,0) / mVals.length).toFixed(1);
            
            const shareUrl = generateShareUrl();
            
            const text = `🎾 *Scheda Valutazione Padel*\n👤 *Giocatore:* ${name}\n\n⚡ *Media Tecnica:* ${avgTech}/10\n🧠 *Media Tattica/Mental:* ${avgMental}/10\n\nApri la scheda completa qui:\n${shareUrl}`;
            
            const waUrl = `https://wa.me/?text=${encodeURIComponent(text)}`;
            window.open(waUrl, '_blank');
        }

        // 💾 SALVA RISULTATO COME IMMAGINE PNG
        function saveResultAsImage() {
            const fname = document.getElementById('firstName').value.trim() || 'Giocatore';
            const lname = document.getElementById('lastName').value.trim() || '';
            const fullName = `${fname} ${lname}`.trim();

            const cCanvas = document.createElement('canvas');
            cCanvas.width = 800;
            cCanvas.height = 700;
            const ctx = cCanvas.getContext('2d');

            // Sfondo
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(0, 0, 800, 700);

            // Header
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(20, 20, 760, 80);
            ctx.strokeStyle = 'rgba(255,255,255,0.1)';
            ctx.strokeRect(20, 20, 760, 80);

            ctx.font = 'bold 24px -apple-system, sans-serif';
            ctx.fillStyle = '#38bdf8';
            ctx.textAlign = 'center';
            ctx.fillText(fullName ? `${fullName} - Scheda Padel` : 'Padel Performance Dashboard', 400, 55);

            ctx.font = '14px -apple-system, sans-serif';
            ctx.fillStyle = '#94a3b8';
            ctx.fillText('Valutazione Prestazionale Personalizzata', 400, 80);

            // Disegna Grafico Tecnico a sinistra
            const techCanvas = document.getElementById('techCanvas');
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(20, 110, 370, 360);
            ctx.strokeRect(20, 110, 370, 360);

            ctx.font = 'bold 16px -apple-system, sans-serif';
            ctx.fillStyle = '#38bdf8';
            ctx.fillText('Abilità Tecniche', 205, 140);
            ctx.drawImage(techCanvas, 30, 150, 350, 300);

            // Disegna Grafico Mental a destra
            const mentalCanvas = document.getElementById('mentalCanvas');
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(410, 110, 370, 360);
            ctx.strokeRect(410, 110, 370, 360);

            ctx.font = 'bold 16px -apple-system, sans-serif';
            ctx.fillStyle = '#a855f7';
            ctx.fillText('Atteggiamento & Tattica', 595, 140);
            ctx.drawImage(mentalCanvas, 420, 150, 350, 300);

            // Dettaglio Valori in Basso
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(20, 480, 760, 190);
            ctx.strokeRect(20, 480, 760, 190);

            ctx.font = 'bold 14px -apple-system, sans-serif';
            ctx.textAlign = 'left';
            
            // Colonna Tecnica
            ctx.fillStyle = '#38bdf8';
            ctx.fillText('TECNICA:', 40, 510);
            techKeys.forEach((id, idx) => {
                const val = document.getElementById(id).value;
                const label = techLabels[idx];
                ctx.fillStyle = '#f8fafc';
                ctx.font = '13px -apple-system, sans-serif';
                const col = idx < 3 ? 0 : 1;
                const row = idx % 3;
                ctx.fillText(`${label}: ${val}/10`, 40 + col * 170, 535 + row * 24);
            });

            // Colonna Mental
            ctx.fillStyle = '#a855f7';
            ctx.font = 'bold 14px -apple-system, sans-serif';
            ctx.fillText('TATTICA & MENTAL:', 430, 510);
            mentalKeys.forEach((id, idx) => {
                const val = document.getElementById(id).value;
                const label = mentalLabels[idx];
                ctx.fillStyle = '#f8fafc';
                ctx.font = '13px -apple-system, sans-serif';
                const col = idx < 3 ? 0 : 1;
                const row = idx % 3;
                ctx.fillText(`${label}: ${val}/10`, 430 + col * 170, 535 + row * 24);
            });

            const dataUrl = cCanvas.toDataURL('image/png');

            // Prova a scaricare direttamente
            const link = document.createElement('a');
            link.download = `Padel_Performance_${fname}_${lname}.png`.replace(/\s+/g, '_');
            link.href = dataUrl;
            
            // Mostra Modale con Immagine per salvataggio facile su mobile
            document.getElementById('modalTitle').innerText = '🖼️ Immagine Generata!';
            document.getElementById('modalContent').innerHTML = `
                <p style="font-size:0.85rem; color:var(--text-muted); margin-top:0;">Tieni premuto sull'immagine per salvarla nelle tue foto o scaricarla:</p>
                <img src="${dataUrl}" alt="Scheda Padel">
                <br>
                <a href="${dataUrl}" download="${link.download}" style="display:inline-block; padding:10px 16px; background:var(--accent-purple); color:#fff; text-decoration:none; font-weight:bold; border-radius:8px; margin-top:6px;">⬇️ Scarica Immagine</a>
            `;
            document.getElementById('mainModal').style.display = 'flex';
        }

        async function shareOrCopyLink() {
            const shareUrl = generateShareUrl();

            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(shareUrl).then(showToast);
            } else {
                document.getElementById('modalTitle').innerText = '📋 Copia il tuo link';
                document.getElementById('modalContent').innerHTML = `
                    <p style="font-size:0.85rem; color:var(--text-muted)">Seleziona e copia il link qui sotto:</p>
                    <input type="text" value="${shareUrl}" readonly onclick="this.select()">
                `;
                document.getElementById('mainModal').style.display = 'flex';
            }
        }

        function showToast() {
            const toast = document.getElementById('toastMsg');
            toast.style.display = 'block';
            setTimeout(() => { toast.style.display = 'none'; }, 2000);
        }

        function closeModal() {
            document.getElementById('mainModal').style.display = 'none';
        }

        function loadInitialData() {
            const params = new URLSearchParams(window.location.search);
            
            if (params.has('fname') || params.has('tech')) {
                if (params.has('fname')) document.getElementById('firstName').value = params.get('fname');
                if (params.has('lname')) document.getElementById('lastName').value = params.get('lname');
                
                if (params.has('tech')) {
                    const t = params.get('tech').split(',');
                    techKeys.forEach((id, i) => { if (t[i]) document.getElementById(id).value = t[i]; });
                }
                if (params.has('mental')) {
                    const m = params.get('mental').split(',');
                    mentalKeys.forEach((id, i) => { if (m[i]) document.getElementById(id).value = m[i]; });
                }
            } else {
                try {
                    const saved = localStorage.getItem('padel_dashboard_data');
                    if (saved) {
                        const parsed = JSON.parse(saved);
                        if (parsed.fname) document.getElementById('firstName').value = parsed.fname;
                        if (parsed.lname) document.getElementById('lastName').value = parsed.lname;
                        if (parsed.tech) techKeys.forEach((id, i) => { if (parsed.tech[i]) document.getElementById(id).value = parsed.tech[i]; });
                        if (parsed.mental) mentalKeys.forEach((id, i) => { if (parsed.mental[i]) document.getElementById(id).value = parsed.mental[i]; });
                    }
                } catch(e){}
            }

            renderAll();
        }

        window.addEventListener('resize', renderAll);
        window.addEventListener('load', loadInitialData);
    </script>
</body>
</html>
