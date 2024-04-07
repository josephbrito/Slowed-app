from pytube import YouTube
import os

def LoadingDownload(stream, chunk, bytes):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Status: {round(pct_completed, 2)} %")

 
def DownloadVideo(url):
    yt = YouTube(url, on_progress_callback=LoadingDownload)

    try:
        video = yt.streams.filter(only_audio=True).first()
        destination = 'songs/'
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        return new_file
    except Exception as e:
        print("An error ocurred: ")
        print(e)
        return
