# Importações
from pytube import YouTube
from pytube.cli import on_progress
from pytube import Playlist
import moviepy.editor as mp
import PySimpleGUI as sg
import os
import string

# Definir função para baixar do YouTube
def download_audio():
    #Baixar áudio e converter arquivo em formato .mp4 para .mp3
    link = valores['url']
    yt = YouTube(link,on_progress_callback=on_progress)
    title = yt.title
    title = [letter for letter in title if letter not in string.punctuation]
    title = ''.join(title)

    print('Título = ',title)
    print('Baixando...')

    audio = yt.streams.get_audio_only()

    audio.download(filename=title+'.mp4')

    clip = mp.AudioFileClip(title+'.mp4')
    clip.write_audiofile(title+'.mp3')

    os.remove(title+'.mp4')

    print(yt.title + " has been successfully downloaded.")
            
def download_video():
    #Baixar vídeo
    link = valores['url']

    yt = YouTube(link,on_progress_callback=on_progress)
    title = yt.title
    title = [letter for letter in title if letter not in string.punctuation]
    title = ''.join(title)
    print('Título = ',title)
    print('Baixando...')
    ys = yt.streams.get_highest_resolution()
    ys.download(filename=title+'.mp4')
        
def download_playlist():
    #Baixar Playlist
    link = valores['url']

    pl = Playlist(link)

    for url in pl.video_urls:

        yt = YouTube(url,on_progress_callback=on_progress)
        title = yt.title
        title = [letter for letter in title if letter not in string.punctuation]
        title = ''.join(title)
        print("Titulo = ", title)
        v = yt.streams.get_audio_only()
        v.download(output_path='/home/magnum/Música/Downloads',filename=title+'.mp4')
        os.chdir('/home/magnum/Música/Downloads')
        clip = mp.AudioFileClip(title+'.mp4')
        clip.write_audiofile(title+'.mp3')
        os.remove(title+'.mp4')

    print("Downloads concluídos!")
    
# Interface PySimpleGUI
sg.theme('DarkRed1')

layout = [
    [sg.Text('Insira a URL:')],
    [sg.Input(size=(45,0),key='url',background_color='white')],
    [sg.Radio('Áudio',1,key='aud'),
     sg.Radio('Vídeo',1,key='vid'),
     sg.Radio('Playlist',1,key='pla')],
    [sg.Button('Converter!',button_color='white'),
    sg.Button('Finalizar!',button_color='white')],
    [sg.Output(size=(45,10),background_color='white')]
]

janela = sg.Window('Conversor YouTube para MP3',layout=layout)

try:
    while True:
        evento,valores = janela.Read()
        if evento == 'Converter!' and valores['aud'] == True:
            download_audio()
            
        if evento == 'Converter!' and valores['vid'] == True:
            download_video()
            
        if evento == 'Converter!' and valores['pla'] == True:
            download_playlist()
            
        if evento == 'Finalizar!':
            janela.close()
            break
            
        if evento == sg.WIN_CLOSED:
            break
except:
    print('Ocorreu um erro!')
    
while True:
    evento,valores = janela.Read()
    if evento == sg.WIN_CLOSED or evento == 'Finalizar!':
        break
janela.close()