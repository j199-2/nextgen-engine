import os
import shutil
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse

app = FastAPI()

TEMP_DIR = "/tmp/clips"
os.makedirs(TEMP_DIR, exist_ok=True)

def limpiar_archivos(folder_path: str):
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
    except Exception as e:
        print(f"Error al limpiar: {e}")

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NextGen Clip Engine</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            .neon-border {
                box-shadow: 0 0 15px rgba(168, 85, 247, 0.2), inset 0 0 15px rgba(59, 130, 246, 0.1);
            }
            .gradient-text {
                background: linear-gradient(135deg, #e879f9 0%, #6366f1 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            ::-webkit-scrollbar { width: 6px; }
            ::-webkit-scrollbar-track { background: #020617; }
            ::-webkit-scrollbar-thumb { background: #1e1b4b; border-radius: 10px; }
            ::-webkit-scrollbar-thumb:hover { background: #312e81; }
        </style>
    </head>
    <body class="bg-slate-950 text-slate-200 min-h-screen font-sans flex flex-col justify-between antialiased">
        
        <!-- Navbar con Branding Completo NextGen -->
        <header class="max-w-5xl w-full mx-auto h-20 flex items-center justify-between px-6 border-b border-purple-950/30">
            <div class="flex items-center space-x-3">
                <!-- Icono que simula el Logo NG -->
                <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-fuchsia-500 via-indigo-500 to-cyan-400 flex items-center justify-center p-[2px] shadow-lg shadow-indigo-500/20">
                    <div class="w-full h-full bg-slate-950 rounded-full flex items-center justify-center">
                        <i class="fa-solid fa-play text-xs text-white translate-x-[1px]"></i>
                    </div>
                </div>
                <div class="flex flex-col">
                    <span class="text-sm font-black tracking-widest text-white">NEXTGEN</span>
                    <span class="text-[10px] font-bold tracking-widest text-indigo-400 -mt-1">CREATORS</span>
                </div>
            </div>
            
            <!-- Selector de Idioma -->
            <button id="langBtn" onclick="toggleLanguage()" class="flex items-center space-x-2 bg-slate-900/80 hover:bg-slate-800 border border-slate-800 px-3 py-1.5 rounded-xl text-xs font-bold text-slate-300 transition-all">
                <span>🇲🇽 ES</span>
            </button>
        </header>

        <!-- Contenedor Central -->
        <main class="flex-1 max-w-xl w-full mx-auto px-6 flex flex-col justify-center py-8">
            
            <!-- CARD PRINCIPAL PREMIUM -->
            <div class="bg-slate-900/20 border border-purple-900/20 rounded-3xl p-8 backdrop-blur-md shadow-2xl neon-border space-y-6 relative overflow-hidden">
                <div class="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-indigo-500 to-fuchsia-500 opacity-40"></div>
                
                <!-- VISTA 1: INPUTS -->
                <div id="step-input" class="space-y-6">
                    <div class="space-y-2 text-center">
                        <span id="txt-badge" class="text-[9px] uppercase font-black tracking-widest bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 px-2.5 py-1 rounded-full">AI Clip Engine v2.0</span>
                        <h1 id="txt-title" class="text-2xl font-black tracking-tight text-white pt-2">Limpia tu Clip</h1>
                        <p id="txt-subtitle" class="text-xs text-slate-400 leading-relaxed">Sube tu contenido o pega el link. Filtramos ruidos molestos y extraemos la estructura viral bilingüe de nuestra marca.</p>
                    </div>

                    <!-- Tabs NextGen Style -->
                    <div class="grid grid-cols-2 gap-2 bg-slate-950 p-1.5 rounded-xl border border-slate-900">
                        <button id="tab-file" onclick="switchMode('file')" class="text-xs font-bold py-2 rounded-lg bg-slate-900 text-white shadow-lg border border-purple-500/10 transition-all">📁 File</button>
                        <button id="tab-link" onclick="switchMode('link')" class="text-xs font-bold py-2 rounded-lg text-slate-500 transition-all">🔗 Link</button>
                    </div>

                    <form id="cleanerForm" class="space-y-5" enctype="multipart/form-data">
                        <!-- Carga de Archivo Local -->
                        <div id="file-box" class="border border-dashed border-slate-800 hover:border-indigo-500/30 rounded-2xl p-8 text-center cursor-pointer bg-slate-950/40 transition-all group">
                            <input type="file" id="clipFile" accept="video/*" class="hidden" onchange="updateFileName()">
                            <label for="clipFile" class="cursor-pointer block space-y-3">
                                <div class="w-10 h-10 rounded-xl bg-slate-900 mx-auto flex items-center justify-center group-hover:scale-105 transition-all border border-slate-800">
                                    <i class="fa-solid fa-arrow-up-from-bracket text-indigo-400 text-sm"></i>
                                </div>
                                <span id="txt-select-file" class="text-xs text-slate-300 font-bold block">Importar video local</span>
                                <span id="file-name" class="text-[10px] text-slate-500 block truncate font-mono">Formatos nativos (.mp4, .mov)</span>
                            </label>
                        </div>

                        <!-- Input URL Enlace -->
                        <div id="link-box" class="hidden bg-slate-950 border border-slate-800 rounded-xl p-3.5 focus-within:border-indigo-500/40 transition-all">
                            <input type="url" id="clipUrl" class="w-full bg-transparent text-xs text-slate-200 placeholder-slate-600 focus:outline-none font-mono" placeholder="https://www.tiktok.com/...">
                        </div>

                        <!-- Botón de Acción Principal -->
                        <button type="submit" id="btn-submit" class="w-full bg-gradient-to-r from-fuchsia-600 to-indigo-600 hover:opacity-90 text-white font-bold text-xs py-4 rounded-xl transition-all shadow-lg shadow-indigo-600/20 tracking-wider uppercase">Procesar Ahora</button>
                    </form>
                </div>

                <!-- VISTA 2: PROCESANDO -->
                <div id="step-processing" class="hidden py-12 text-center space-y-4">
                    <div class="relative w-12 h-12 mx-auto">
                        <div class="w-12 h-12 rounded-full border-2 border-indigo-950 animate-ping absolute"></div>
                        <div class="w-12 h-12 rounded-full border-2 border-fuchsia-500 border-t-transparent animate-spin"></div>
                    </div>
                    <p id="txt-processing" class="text-xs text-indigo-300 font-bold tracking-wide">Limpiando frecuencias de audio y estructurando ganchos...</p>
                </div>

                <!-- VISTA 3: RESULTADOS -->
                <div id="step-results" class="hidden space-y-5">
                    <div class="text-center space-y-1">
                        <div class="w-10 h-10 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mx-auto mb-2">
                            <i class="fa-solid fa-check text-emerald-400 text-sm"></i>
                        </div>
                        <h3 id="txt-success" class="font-black text-white text-sm tracking-wide uppercase">¡Optimización Completada!</h3>
                    </div>

                    <!-- Botón de Descarga -->
                    <button id="downloadBtn" class="w-full bg-white hover:bg-slate-100 text-slate-950 font-black text-xs py-4 rounded-xl transition-all flex items-center justify-center space-x-2 shadow-xl tracking-wider uppercase">
                        <i class="fa-solid fa-circle-arrow-down text-sm"></i>
                        <span id="txt-download">Descargar Clip Limpio</span>
                    </button>

                    <!-- Caja de Estrategia IA -->
                    <div class="bg-slate-950 border border-slate-900 rounded-xl p-4 space-y-3">
                        <div class="flex items-center justify-between border-b border-slate-900/80 pb-2">
                            <span id="txt-ia-title" class="text-[10px] font-black tracking-widest text-indigo-400 uppercase">Estrategia de Contenido IA</span>
                            <button onclick="copyToClipboard()" class="text-slate-500 hover:text-white text-xs transition-all"><i class="fa-regular fa-copy"></i></button>
                        </div>
                        <div id="ia-content" class="text-xs text-slate-300 whitespace-pre-line leading-relaxed max-h-48 overflow-y-auto pr-1 font-mono"></div>
                    </div>
                    
                    <button onclick="location.reload()" id="btn-back" class="w-full text-center text-xs text-slate-500 hover:text-indigo-400 font-medium transition-colors block pt-2">Procesar otro archivo</button>
                </div>

            </div>
        </main>

        <!-- Footer Oficial -->
        <footer class="h-14 border-t border-purple-950/20 flex items-center justify-center text-[10px] text-slate-600 tracking-widest uppercase font-bold">
            NextGen Capital & Creators &copy; 2026
        </footer>

        <script>
            let currentMode = 'file';
            let currentLang = 'es';

            const diccionario = {
                es: {
                    title: "Limpia tu Clip",
                    subtitle: "Sube tu contenido o pega el link. Filtramos ruidos molestos y extraemos la estructura viral bilingüe de nuestra marca.",
                    selectFile: "Importar video local",
                    placeholderUrl: "Pega el link de TikTok o YouTube...",
                    btnSubmit: "Procesar Ahora",
                    processing: "Modulando voz y estructurando ganchos NextGen...",
                    success: "¡Optimización Completada!",
                    download: "Descargar Clip Limpio",
                    iaTitle: "Estrategia de Contenido IA",
                    back: "Procesar otro archivo",
                    alertFile: "Por favor selecciona un archivo primero.",
                    alertUrl: "Por favor pega un enlace válido."
                },
                en: {
                    title: "Clean your Clip",
                    subtitle: "Upload your content or paste the link. We filter unwanted background noise and extract our brand's viral framework.",
                    selectFile: "Import local video",
                    placeholderUrl: "Paste TikTok or YouTube link...",
                    btnSubmit: "Process Now",
                    processing: "Modulating voice and structuring NextGen hooks...",
                    success: "Optimization Completed!",
                    download: "Download Clean Clip",
                    iaTitle: "AI Content Strategy",
                    back: "Process another file",
                    alertFile: "Please select a file first.",
                    alertUrl: "Please paste a valid link."
                }
            };

            function toggleLanguage() {
                currentLang = currentLang === 'es' ? 'en' : 'es';
                document.getElementById('langBtn').innerHTML = currentLang === 'es' ? '<span>🇲🇽 ES</span>' : '<span>🇺🇸 EN</span>';
                
                document.getElementById('txt-title').innerText = diccionario[currentLang].title;
                document.getElementById('txt-subtitle').innerText = diccionario[currentLang].subtitle;
                document.getElementById('txt-select-file').innerText = diccionario[currentLang].selectFile;
                document.getElementById('clipUrl').placeholder = diccionario[currentLang].placeholderUrl;
                document.getElementById('btn-submit').innerText = diccionario[currentLang].btnSubmit;
                document.getElementById('txt-processing').innerText = diccionario[currentLang].processing;
                document.getElementById('txt-success').innerText = diccionario[currentLang].success;
                document.getElementById('txt-download').innerText = diccionario[currentLang].download;
                document.getElementById('txt-ia-title').innerText = diccionario[currentLang].iaTitle;
                document.getElementById('btn-back').innerText = diccionario[currentLang].back;
            }

            function switchMode(mode) {
                currentMode = mode;
                if (mode === 'file') {
                    document.getElementById('file-box').classList.remove('hidden');
                    document.getElementById('link-box').classList.add('hidden');
                    document.getElementById('tab-file').className = "text-xs font-bold py-2 rounded-lg bg-slate-900 text-white shadow-lg border border-purple-500/10 transition-all";
                    document.getElementById('tab-link').className = "text-xs font-bold py-2 rounded-lg text-slate-500 transition-all";
                } else {
                    document.getElementById('file-box').classList.add('hidden');
                    document.getElementById('link-box').classList.remove('hidden');
                    document.getElementById('tab-file').className = "text-xs font-bold py-2 rounded-lg text-slate-500 transition-all";
                    document.getElementById('tab-link').className = "text-xs font-bold py-2 rounded-lg bg-slate-900 text-white shadow-lg border border-purple-500/10 transition-all";
                }
            }

            function updateFileName() {
                const fileInput = document.getElementById('clipFile');
                const label = document.getElementById('file-name');
                if(fileInput.files.length > 0) {
                    label.innerText = fileInput.files[0].name;
                }
            }

            function copyToClipboard() {
                const content = document.getElementById('ia-content').innerText;
                navigator.clipboard.writeText(content);
                alert(currentLang === 'es' ? "¡Copiado al portapapeles!" : "Copied to clipboard!");
            }

            document.getElementById('cleanerForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const formData = new FormData();
                
                if(currentMode === 'file') {
                    const fileInput = document.getElementById('clipFile');
                    if(fileInput.files.length === 0) return alert(diccionario[currentLang].alertFile);
                    formData.append('file', fileInput.files[0]);
                } else {
                    const urlInput = document.getElementById('clipUrl').value;
                    if(!urlInput) return alert(diccionario[currentLang].alertUrl);
                    formData.append('url', urlInput);
                }
                
                formData.append('lang', currentLang);

                document.getElementById('step-input').classList.add('hidden');
                document.getElementById('step-processing').classList.remove('hidden');

                try {
                    const response = await fetch('/api/process', { method: 'POST', body: formData });
                    if(!response.ok) throw new Error("Error.");
                    const data = await response.json();

                    document.getElementById('ia-content').innerText = data.ia_analisis;
                    document.getElementById('downloadBtn').onclick = () => { window.location.href = data.video_url; };

                    document.getElementById('step-processing').classList.add('hidden');
                    document.getElementById('step-results').classList.remove('hidden');
                } catch(err) {
                    alert(currentLang === 'es' ? "Ocurrió un error al procesar el archivo." : "An error occurred while processing the file.");
                    location.reload();
                }
            });
        </script>
    </body>
    </html>
    """

@app.post("/api/process")
async def process_clip(
    background_tasks: BackgroundTasks,
    url: str = Form(None),
    file: UploadFile = File(None),
    lang: str = Form("es")
):
    session_id = str(os.urandom(4).hex())
    session_dir = os.path.join(TEMP_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    
    input_file = os.path.join(session_dir, "input.mp4")
    output_video_path = os.path.join(session_dir, "clip_limpio.mp4")

    try:
        if file:
            with open(input_file, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        elif url:
            import yt_dlp
            ydl_opts = {
                'outtmpl': os.path.join(session_dir, 'input.%(ext)s'),
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'quiet': True,
                'no_warnings': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                await asyncio.to_thread(ydl.download, [url])
            archivos = [f for f in os.listdir(session_dir) if not f.startswith('.')]
            if archivos:
                input_file = os.path.join(session_dir, archivos[0])
        else:
            raise HTTPException(status_code=400, detail="Missing data")

        # Filtro de audio equilibrado (Remueve ruidos y resalta voces para clips móviles)
        cmd = f"ffmpeg -i '{input_file}' -af 'highpass=f=150, lowpass=f=4000' -c:v copy '{output_video_path}' -y"
        process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await process.communicate()

        # Output de la estrategia viral adaptada con la jerga de NextGen Creators
        if lang == "es":
            ia_text = (
                "🎯 ESTRATEGIA VIRAL NEXTGEN CREATORS\n\n"
                "🔥 Hook 1: ❌ El gran error que comete el 95% al hacer esto...\n"
                "🔥 Hook 2: Aplica este truco secreto antes de que lo borren 👀\n"
                "🔥 Hook 3: La cruda realidad sobre este nicho que nadie te cuenta\n\n"
                "📝 Copy Optimizado:\nGuarda este clip de inmediato si quieres entender el cambio de métricas de esta semana. Ponlo a prueba hoy mismo en tus cuentas. 👇\n\n"
                "🏷️ Hashtags de Distribución:\n#creaciondecontenido #cliperos #marketingdigital #nextgencreators"
            )
        else:
            ia_text = (
                "🎯 NEXTGEN CREATORS VIRAL SYSTEM\n\n"
                "🚀 Hook 1: ❌ The huge mistake 95% of creators make with this...\n"
                "🚀 Hook 2: Try this secret growth hack before it gets patched 👀\n"
                "🚀 Hook 3: The harsh reality about this niche that nobody tells you\n\n"
                "📝 Optimized Caption:\nSave this clip if you want to outsmart the algorithm this week. Implement this framework right now. 👇\n\n"
                "🏷️ Distribution Tags:\n#contentcreator #shortform #growthhacking #nextgencreators"
            )

        background_tasks.add_task(limpiar_archivos, session_dir)

        return JSONResponse(content={
            "video_url": f"/download/{session_id}",
            "ia_analisis": ia_text
        })
    except Exception as e:
        limpiar_archivos(session_dir)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{session_id}")
async def download_file(session_id: str):
    file_path = os.path.join(TEMP_DIR, session_id, "clip_limpio.mp4")
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename="nextgen_clip.mp4", media_type="video/mp4")
    raise HTTPException(status_code=404, detail="Expired")
     
