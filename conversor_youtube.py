# Importações
from pytube import YouTube
from pytube.cli import on_progress
from pytube import Playlist
import moviepy.editor as mp
import PySimpleGUI as sg
import os
import string

# Definir funções para baixar do YouTube
def download_audio():
    #Baixar áudio e converter arquivo em formato .mp4 para .mp3
    link = valores['url']
    caminho = valores['folder']
    tra_caminho = f'{caminho}'
    
    yt = YouTube(link,on_progress_callback=on_progress)
    title = yt.title
    title = [letter for letter in title if letter not in string.punctuation]
    title = ''.join(title)

    print('Título = ',title)
    print('Baixando...')

    audio = yt.streams.get_audio_only()

    audio.download(output_path=tra_caminho,filename=title+'.mp4')
    os.chdir(tra_caminho)
    clip = mp.AudioFileClip(title+'.mp4')
    clip.write_audiofile(title+'.mp3')

    os.remove(title+'.mp4')

    janela['output'].Update('')
    print(yt.title + " has been successfully downloaded.")
            
def download_video():
    #Baixar vídeo
    link = valores['url']
    caminho = valores['folder']
    tra_caminho = f'{caminho}'

    yt = YouTube(link,on_progress_callback=on_progress)
    title = yt.title
    title = [letter for letter in title if letter not in string.punctuation]
    title = ''.join(title)
    print('Título = ',title)
    print('Baixando...')
    ys = yt.streams.get_highest_resolution()
    ys.download(output_path=tra_caminho,filename=title+'.mp4')

    janela['output'].Update('')
    print(yt.title + " has been successfully downloaded.")
        
def download_pl_audio():
    #Baixar Playlist de Áudios
    link = valores['url']
    caminho = valores['folder']
    tra_caminho = f'{caminho}'

    pl = Playlist(link)

    for url in pl.video_urls:

        yt = YouTube(url,on_progress_callback=on_progress)
        title = yt.title
        title = [letter for letter in title if letter not in string.punctuation]
        title = ''.join(title)
        print("Titulo = ", title)
        ys = yt.streams.get_audio_only()
        ys.download(output_path=tra_caminho,filename=title+'.mp4')
        os.chdir(tra_caminho)
        clip = mp.AudioFileClip(title+'.mp4')
        clip.write_audiofile(title+'.mp3')
        os.remove(title+'.mp4')
    
    janela['output'].Update('')
    print("Downloads concluídos!")

def download_pl_video():
    #Baixar Playlist de Vídeos
    link = valores['url']
    caminho = valores['folder']
    tra_caminho = f'{caminho}'

    pl = Playlist(link)

    for url in pl.video_urls:

        yt = YouTube(url,on_progress_callback=on_progress)
        title = yt.title
        title = [letter for letter in title if letter not in string.punctuation]
        title = ''.join(title)
        print("Titulo = ", title)
        ys = yt.streams.get_audio_only()
        ys.download(output_path=tra_caminho,filename=title+'.mp4')

    janela['output'].Update('')
    print("Downloads concluídos!")
    
# Interface PySimpleGUI
sg.theme('DarkRed1')

layout = [
    [sg.Text('Insira a URL:')],
    [sg.Input(size=(45,0),key='url',background_color='white')],
    [sg.Text('Pasta de Destino:')],
    [sg.Input(size=(45,0),key='path',background_color='white')],
    [sg.FolderBrowse('Procurar Pasta',target='path',key='folder')],
    [sg.Radio('Áudio',1,key='aud'),
     sg.Radio('Vídeo',1,key='vid')],
    [sg.Radio('Vídeo Único',2,key='viu'),
     sg.Radio('Playlist',2,key='pla')],
    [sg.Button('Converter!',button_color='white'),
    sg.Button('Finalizar!',button_color='white')],
    [sg.Output(size=(45,10),background_color='white',key='output')]
]

janela = sg.Window('YouDownload',layout=layout)

try:
    while True:
        evento,valores = janela.Read()
        if evento == 'Converter!' and valores['aud'] and valores['viu']:
            download_audio()
            
        if evento == 'Converter!' and valores['vid'] and valores['viu']:
            download_video()
            
        if evento == 'Converter!' and valores['aud'] and valores['pla']:
            download_pl_audio()
            
        if evento == 'Converter!' and valores['vid'] and valores['pla']:
            download_pl_video()
            
        if evento == 'Finalizar!':
            janela.close()
            break
            
        if evento == sg.WIN_CLOSED:
            break

        janela['url'].Update('')
        janela['path'].Update('')

except:
    print('Ocorreu um erro!')
    
while True:
    evento,valores = janela.Read()
    if evento == sg.WIN_CLOSED or evento == 'Finalizar!':
        break
janela.close()
