from transformers import Transcript

if __name__ == "__main__":
    transcript = Transcript()
    transcript.set_api_key()
    transcript.transcribe_yt_video("https://www.youtube.com/watch?v=-LIIf7E-qFI")
    transcript.print_transcript()
