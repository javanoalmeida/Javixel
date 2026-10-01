import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageOps, ImageTk, ImageChops
import threading

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def trim_white_margin(im):
    # Remove as margens brancas da imagem
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Javixel")
        self.width = 540
        self.height = 480 # Aumentado de 450 para 480 para mostrar ainda mais margem na parte inferior
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)
        
        # Variáveis
        self.input_folder_str = tk.StringVar()
        self.output_folder_str = tk.StringVar()
        self.max_size_var = tk.StringVar(value="3000") # Padrão
        self.selected_files = []
        self.cancel_process = False
        
        # Canvas para colocar a imagem no fundo de tudo (Interface inteira)
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, highlightthickness=0, bg="white")
        self.canvas.pack(fill="both", expand=True)

        try:
            logo_path = resource_path("javixel_logo.jpg")
            img = Image.open(logo_path)
            self.root.iconphoto(False, ImageTk.PhotoImage(img))
            
            img = trim_white_margin(img)
            
            # Alinhando a imagem de fundo com as margens dos campos de texto
            # A largura dos campos vai aproximadamente do pixel 30 ao 480 (450px de largura)
            target_width = 450
            ratio = target_width / float(img.width)
            new_height = int(float(img.height) * float(ratio))
            
            img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
            
            white_bg = Image.new("RGB", img.size, (255, 255, 255))
            img = Image.blend(img.convert("RGB"), white_bg, 0.85)
            
            self.bg_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(self.width//2, self.height//2 + 20, image=self.bg_img, anchor="center")
        except Exception as e:
            print("Logo não encontrada:", e)

        # Adicionando os elementos visuais "flutuando"
        y_offset = 50
        
        # Título - Retornando para um tamanho menor
        try:
            title_path = resource_path("javixel_title.jpg")
            img_title = Image.open(title_path)
            img_title = trim_white_margin(img_title)
            
            # Largura reduzida para o tamanho anterior que você gostava
            t_width = 180 
            t_ratio = t_width / float(img_title.width)
            t_height = int(float(img_title.height) * float(t_ratio))
            img_title = img_title.resize((t_width, t_height), Image.Resampling.LANCZOS)
            
            white_bg = Image.new("RGB", img_title.size, (255, 255, 255))
            img_title = Image.blend(img_title.convert("RGB"), white_bg, 0.1)
            
            self.title_img = ImageTk.PhotoImage(img_title)
            self.canvas.create_image(self.width//2, y_offset, image=self.title_img, anchor="center")
            y_offset += (t_height // 2) + 20
        except Exception as e:
            print("Imagem do título não encontrada:", e)
            self.canvas.create_text(self.width//2, y_offset, text="J A V I X E L", font=("Segoe UI", 16, "bold"), fill="#0078D7")
            y_offset += 40
        
        # Seleção de Imagens
        self.canvas.create_text(30, y_offset, text="Imagens Selecionadas:", font=("Segoe UI", 10, "bold"), anchor="w", fill="#333")
        entry_in = tk.Entry(root, textvariable=self.input_folder_str, width=35, state='readonly')
        self.canvas.create_window(185, y_offset, window=entry_in, anchor="w")
        btn_in = tk.Button(root, text="Procurar", command=self.browse_input)
        self.canvas.create_window(415, y_offset, window=btn_in, anchor="w")
        
        y_offset += 45
        
        # Pasta de Destino
        self.canvas.create_text(30, y_offset, text="Pasta de Destino:", font=("Segoe UI", 10, "bold"), anchor="w", fill="#333")
        entry_out = tk.Entry(root, textvariable=self.output_folder_str, width=35, state='readonly')
        self.canvas.create_window(185, y_offset, window=entry_out, anchor="w")
        btn_out = tk.Button(root, text="Procurar", command=self.browse_output)
        self.canvas.create_window(415, y_offset, window=btn_out, anchor="w")
        
        y_offset += 45
        
        # Tamanho Máximo Customizável
        self.canvas.create_text(30, y_offset, text="Tamanho Máximo (px):", font=("Segoe UI", 10, "bold"), anchor="w", fill="#333")
        entry_size = tk.Entry(root, textvariable=self.max_size_var, width=15)
        self.canvas.create_window(185, y_offset, window=entry_size, anchor="w")
        
        y_offset += 55
        
        # Progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(root, variable=self.progress_var, maximum=100, length=460)
        self.canvas.create_window(self.width//2, y_offset, window=self.progress_bar, anchor="center")
        
        y_offset += 30
        
        # Status
        self.status_label = tk.Label(root, text="Aguardando seleção das imagens e pasta...", bg="white", fg="#333")
        self.canvas.create_window(self.width//2, y_offset, window=self.status_label, anchor="center")
        
        y_offset += 50
        
        # Botões (Iniciar e Cancelar)
        self.start_btn = tk.Button(
            root, 
            text="Iniciar", 
            command=self.start_process, 
            bg="#0078D7", 
            fg="white", 
            font=("Segoe UI", 10, "bold"),
            width=15
        )
        self.canvas.create_window(self.width//2 - 80, y_offset, window=self.start_btn, anchor="center")

        self.cancel_btn = tk.Button(
            root, 
            text="Cancelar", 
            command=self.cancel_action, 
            bg="#d9534f", 
            fg="white", 
            disabledforeground="#fce4e4", # Para o texto ficar clarinho em vez de preto quando desativado!
            font=("Segoe UI", 10, "bold"),
            width=15,
            state=tk.DISABLED
        )
        self.canvas.create_window(self.width//2 + 80, y_offset, window=self.cancel_btn, anchor="center")

        y_offset += 50

        # Créditos do Criador
        self.canvas.create_text(self.width//2, y_offset, text="Criado por: Javan Oliveira de Almeida", font=("Segoe UI", 8, "italic"), fill="#555")


    def browse_input(self):
        files = filedialog.askopenfilenames(
            title="Selecione as imagens",
            filetypes=[
                ("Arquivos de Imagem", "*.jpg *.jpeg *.png *.bmp *.webp"),
                ("Todos os Arquivos", "*.*")
            ]
        )
        if files:
            self.selected_files = list(files)
            if len(self.selected_files) == 1:
                self.input_folder_str.set("1 imagem selecionada")
            else:
                self.input_folder_str.set(f"{len(self.selected_files)} imagens selecionadas")

    def browse_output(self):
        folder = filedialog.askdirectory(title="Selecione a pasta de destino")
        if folder:
            self.output_folder_str.set(folder)

    def cancel_action(self):
        self.cancel_process = True
        self.status_label.config(text="Cancelando... Aguarde finalizar a imagem atual.")
        self.cancel_btn.config(state=tk.DISABLED)

    def start_process(self):
        output_dir = self.output_folder_str.get()
        
        if not self.selected_files or not output_dir:
            messagebox.showwarning("Atenção", "Você precisa selecionar as imagens e a pasta de destino antes de iniciar.")
            return
            
        try:
            max_size = int(self.max_size_var.get())
            if max_size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Atenção", "O tamanho máximo deve ser um número inteiro positivo.")
            return
            
        self.cancel_process = False
        self.start_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Verificando imagens, por favor aguarde...")
        self.progress_var.set(0)
        
        thread = threading.Thread(target=self.run_resize, args=(self.selected_files, output_dir, max_size))
        thread.daemon = True
        thread.start()
        
    def run_resize(self, input_files, output_folder, max_size):
        if not os.path.exists(output_folder):
            try:
                os.makedirs(output_folder)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível criar a pasta de destino:\n{e}")
                self.reset_ui()
                return

        total_files = len(input_files)
        progress_step = 100 / total_files
        
        processed_count = 0

        for i, input_path in enumerate(input_files):
            if self.cancel_process:
                self.status_label.config(text="Processo cancelado pelo usuário.")
                messagebox.showinfo("Cancelado", f"Processo interrompido!\n{processed_count} imagens foram redimensionadas antes do cancelamento.")
                self.reset_ui()
                return

            filename = os.path.basename(input_path)
            output_path = os.path.join(output_folder, filename)

            try:
                with Image.open(input_path) as img:
                    img = ImageOps.exif_transpose(img)
                    width, height = img.size
                    
                    if width > max_size or height > max_size:
                        if width > height:
                            new_width = max_size
                            new_height = int((max_size / width) * height)
                        else:
                            new_height = max_size
                            new_width = int((max_size / height) * width)
                        
                        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        resized_img.save(output_path, quality=90, optimize=True)
                        processed_count += 1
                        
            except Exception as e:
                print(f"Erro ao processar {filename}: {e}")
                
            self.progress_var.set((i + 1) * progress_step)
            self.status_label.config(text=f"Processando: {i+1} de {total_files}")
            self.root.update_idletasks()
            
        self.status_label.config(text=f"Concluído! {processed_count} imagens redimensionadas.")
        messagebox.showinfo("Sucesso", f"Processo finalizado!\n{processed_count} imagens redimensionadas\ne as menores foram ignoradas.")
        self.reset_ui()

    def reset_ui(self):
        self.start_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
