import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
from moviepy.editor import *

def select_directory():
    save_dir = filedialog.askdirectory()
    entry_dir.delete(0, tk.END)
    entry_dir.insert(tk.END, save_dir)

def download_video():
    url = entry_url.get()
    save_dir = entry_dir.get()

    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        video.download(save_dir)

        # Converter o vídeo em MP3
        video_file = video.default_filename
        mp3_file = video_file.split('.')[0] + '.mp3'
        video_path = os.path.join(save_dir, video_file)
        mp3_path = os.path.join(save_dir, mp3_file)
        video_clip = AudioFileClip(video_path)
        video_clip.write_audiofile(mp3_path)
        video_clip.close()
        os.remove(video_path)

        # Exibir aviso de conclusão
        label_status.config(text="Arquivo MP3 salvo com sucesso!")

    except Exception as e:
        label_status.config(text="Erro ao baixar o vídeo: " + str(e))

# Configuração da interface gráfica
window = tk.Tk()
window.title("Baixar Áudio do YouTube @teozica")
window.geometry("400x200")

label_url = tk.Label(window, text="URL do vídeo:")
label_url.pack()
entry_url = tk.Entry(window, width=40)
entry_url.pack()

label_dir = tk.Label(window, text="Diretório de salvamento:")
label_dir.pack()
entry_dir = tk.Entry(window, width=40)
entry_dir.pack()

button_browse = tk.Button(window, text="Selecionar diretório", command=select_directory)
button_browse.pack()

button_download = tk.Button(window, text="Baixar", command=download_video)
button_download.pack()

label_status = tk.Label(window, text="")
label_status.pack()

window.mainloop()