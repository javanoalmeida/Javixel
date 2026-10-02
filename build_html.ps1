$utf8 = New-Object System.Text.UTF8Encoding $false

# Get base64 for logo
$logoBytes = [System.IO.File]::ReadAllBytes("javixel_logo.jpg")
$logoB64 = [System.Convert]::ToBase64String($logoBytes)

# Get base64 for title
$titleBytes = [System.IO.File]::ReadAllBytes("javixel_title.jpg")
$titleB64 = [System.Convert]::ToBase64String($titleBytes)

$html = @"
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Javixel</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #f1f5f9;
            --primary: #0078D7;
            --primary-hover: #005a9e;
            --text-main: #1e293b;
            --text-muted: #475569;
            --border-color: rgba(0, 0, 0, 0.1);
        }
        
        body {
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
            background: var(--bg-color);
            background-image: url('data:image/jpeg;base64,$logoB64');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .container {
            width: 90%;
            max-width: 600px;
            background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.93)), url('data:image/jpeg;base64,$logoB64');
            background-size: cover;
            background-position: center;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 2.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.2);
            text-align: center;
        }

        .title-img {
            max-width: 240px;
            margin-bottom: 1rem;
            mix-blend-mode: multiply;
        }

        p {
            color: var(--text-muted);
            margin-bottom: 2rem;
            line-height: 1.5;
            font-size: 0.95rem;
        }

        .drop-zone {
            border: 2px dashed var(--primary);
            border-radius: 16px;
            padding: 3rem 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            background: rgba(0, 120, 215, 0.05);
            margin-bottom: 1.5rem;
        }

        .drop-zone:hover, .drop-zone.dragover {
            background: rgba(0, 120, 215, 0.1);
            border-color: var(--primary-hover);
            transform: translateY(-2px);
        }

        .drop-zone p {
            margin: 0;
            color: var(--text-main);
            font-weight: 500;
        }

        .drop-zone span {
            font-size: 0.85rem;
            color: var(--text-muted);
        }

        input[type="file"] {
            display: none;
        }

        .settings {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(0, 0, 0, 0.04);
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
        }

        .settings label {
            font-size: 0.9rem;
            font-weight: 600;
        }

        .settings input[type="number"] {
            background: #ffffff;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 0.5rem;
            border-radius: 8px;
            width: 80px;
            text-align: center;
            font-weight: bold;
            font-family: inherit;
        }
        
        .settings input[type="number"]:focus {
            outline: none;
            border-color: var(--primary);
        }

        .btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 0.8rem 2rem;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .btn:hover:not(:disabled) {
            background: var(--primary-hover);
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 120, 215, 0.3);
        }

        .btn:disabled {
            background: #94a3b8;
            cursor: not-allowed;
            opacity: 0.8;
        }

        .progress-container {
            margin-top: 1.5rem;
            display: none;
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(0,0,0,0.1);
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 0.5rem;
        }

        .progress-fill {
            height: 100%;
            background: var(--primary);
            width: 0%;
            transition: width 0.3s ease;
        }

        .status-text {
            font-size: 0.85rem;
            color: var(--text-muted);
            font-weight: 500;
        }

        #logArea {
            margin-top: 1rem;
            background: rgba(0,0,0,0.05);
            border-radius: 8px;
            padding: 0.8rem;
            font-size: 0.8rem;
            color: #334155;
            max-height: 120px;
            overflow-y: auto;
            text-align: left;
            display: none;
            border: 1px solid rgba(0,0,0,0.05);
        }
        
        #logArea p {
            margin: 2px 0;
            color: inherit;
        }
    </style>
</head>
<body>

    <div class="container">
        <img src="data:image/jpeg;base64,`$titleB64" alt="Javixel" class="title-img">
        <p>Processamento 100% local no seu navegador. Nenhuma imagem é enviada para a internet.</p>

        <div class="drop-zone" id="dropZone">
            <p>Clique ou arraste suas imagens aqui</p>
            <span>Suporta JPG, PNG, WEBP</span>
            <input type="file" id="fileInput" multiple accept=".jpg,.jpeg,.png,.webp,.bmp">
        </div>

        <div class="settings">
            <label for="maxSize">Tamanho Máximo (px):</label>
            <input type="number" id="maxSize" value="3000" min="100" max="8000">
        </div>

        <button class="btn" id="processBtn" disabled>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
            Processar e Baixar (ZIP)
        </button>

        <div class="progress-container" id="progressContainer">
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="status-text" id="statusText">0% concluído</div>
        </div>
        
        <div id="logArea"></div>
        
        <p style="margin-top: 2rem; margin-bottom: 0; font-size: 0.75rem; font-style: italic;">Criado por: Javan Oliveira de Almeida</p>
    </div>

    <script>
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');
        const processBtn = document.getElementById('processBtn');
        const progressContainer = document.getElementById('progressContainer');
        const progressFill = document.getElementById('progressFill');
        const statusText = document.getElementById('statusText');
        const maxSizeInput = document.getElementById('maxSize');
        const logArea = document.getElementById('logArea');

        let selectedFiles = [];

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            handleFiles(dt.files);
        });

        dropZone.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

        function handleFiles(files) {
            selectedFiles = Array.from(files).filter(file => file.type.startsWith('image/'));
            
            if (selectedFiles.length > 0) {
                dropZone.querySelector('p').textContent = `${selectedFiles.length} imagem(ns) selecionada(s)`;
                processBtn.disabled = false;
            } else {
                dropZone.querySelector('p').textContent = 'Clique ou arraste suas imagens aqui';
                processBtn.disabled = true;
            }
        }

        function log(message) {
            logArea.style.display = 'block';
            const p = document.createElement('p');
            p.textContent = message;
            logArea.appendChild(p);
            logArea.scrollTop = logArea.scrollHeight;
        }

        function resizeImage(file, maxSize) {
            return new Promise((resolve, reject) => {
                const img = new Image();
                const url = URL.createObjectURL(file);
                
                img.onload = () => {
                    URL.revokeObjectURL(url);
                    let width = img.width;
                    let height = img.height;
                    
                    let needsResize = false;

                    if (width > maxSize || height > maxSize) {
                        needsResize = true;
                        if (width > height) {
                            height = Math.round((height * maxSize) / width);
                            width = maxSize;
                        } else {
                            width = Math.round((width * maxSize) / height);
                            height = maxSize;
                        }
                    }

                    if (!needsResize) {
                        resolve({ file: file, name: file.name, resized: false, width: img.width, height: img.height });
                        return;
                    }

                    const canvas = document.createElement('canvas');
                    canvas.width = width;
                    canvas.height = height;
                    const ctx = canvas.getContext('2d');
                    
                    ctx.imageSmoothingEnabled = true;
                    ctx.imageSmoothingQuality = 'high';
                    
                    ctx.drawImage(img, 0, 0, width, height);
                    
                    let mimeType = file.type;
                    let quality = 0.90;
                    
                    canvas.toBlob((blob) => {
                        resolve({ blob: blob, name: file.name, resized: true, width, height });
                    }, mimeType, quality);
                };
                
                img.onerror = () => reject(new Error('Erro ao carregar a imagem ' + file.name));
                img.src = url;
            });
        }

        processBtn.addEventListener('click', async () => {
            if (selectedFiles.length === 0) return;

            const maxSize = parseInt(maxSizeInput.value) || 3000;
            processBtn.disabled = true;
            progressContainer.style.display = 'block';
            logArea.innerHTML = '';
            log(`Iniciando processamento de ${selectedFiles.length} imagens...`);
            
            const zip = new JSZip();
            let processedCount = 0;

            try {
                for (let i = 0; i < selectedFiles.length; i++) {
                    const file = selectedFiles[i];
                    statusText.textContent = `Processando: ${file.name} (${i + 1}/${selectedFiles.length})`;
                    
                    const result = await resizeImage(file, maxSize);
                    
                    if (result.resized) {
                        zip.file(result.name, result.blob);
                        log(`Redimensionada: ${result.name} -> ${result.width}x${result.height}`);
                    } else {
                        zip.file(result.name, result.file);
                        log(`Copiada (já era menor): ${result.name}`);
                    }

                    processedCount++;
                    const percent = (processedCount / selectedFiles.length) * 100;
                    progressFill.style.width = `${percent}%`;
                }

                statusText.textContent = 'Gerando arquivo ZIP para download...';
                log('Compactando imagens em um arquivo .zip...');

                const zipBlob = await zip.generateAsync({ type: 'blob' });
                const downloadUrl = URL.createObjectURL(zipBlob);
                
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = 'imagens_redimensionadas.zip';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(downloadUrl);

                statusText.textContent = 'Download concluído!';
                log('Processo finalizado com sucesso!');
                
            } catch (error) {
                console.error(error);
                statusText.textContent = 'Ocorreu um erro no processamento.';
                log('ERRO: ' + error.message);
            } finally {
                processBtn.disabled = false;
                setTimeout(() => {
                    progressFill.style.width = '0%';
                    progressContainer.style.display = 'none';
                }, 4000);
            }
        });
    </script>
</body>
</html>
"@

[System.IO.File]::WriteAllText("Javixel.html", $html, $utf8)
