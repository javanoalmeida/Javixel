import os
from PIL import Image

def resize_images(input_folder, output_folder, max_size=3000):
    """
    Redimensiona as imagens na pasta de entrada para que o maior lado tenha no máximo max_size.
    A proporção da imagem original é mantida.
    """
    # Cria a pasta de saída se ela não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extensões de imagens suportadas
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    for filename in os.listdir(input_folder):
        ext = os.path.splitext(filename)[1].lower()
        if ext in valid_extensions:
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                with Image.open(input_path) as img:
                    width, height = img.size
                    
                    # Se um dos lados for maior que 3000px, redimensionamos
                    if width > max_size or height > max_size:
                        if width > height:
                            new_width = max_size
                            new_height = int((max_size / width) * height)
                        else:
                            new_height = max_size
                            new_width = int((max_size / height) * width)
                        
                        # Usa LANCZOS para alta qualidade no redimensionamento
                        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        # Salva mantendo boa qualidade (apenas para JPEG/WEBP, png ignora quality)
                        resized_img.save(output_path, quality=90, optimize=True)
                        print(f"Redimensionada: {filename} -> {new_width}x{new_height}")
                    else:
                        # Se já for menor que 3000px, apenas salva na nova pasta
                        img.save(output_path)
                        print(f"Copiada (já era menor): {filename} -> {width}x{height}")
            except Exception as e:
                print(f"Erro ao processar {filename}: {e}")

if __name__ == "__main__":
    # Defina aqui os caminhos para as suas pastas
    # Use caminhos absolutos se preferir, ex: r"C:\Caminho\Para\Imagens"
    INPUT_FOLDER = "./imagens_originais"
    OUTPUT_FOLDER = "./imagens_redimensionadas"
    
    print(f"Iniciando o redimensionamento das imagens na pasta: {INPUT_FOLDER}")
    resize_images(INPUT_FOLDER, OUTPUT_FOLDER, max_size=3000)
    print("Processo finalizado!")
