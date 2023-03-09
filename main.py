import os

import pytube
import openai
import subprocess
from dotenv import load_dotenv
from os import environ
import sys


class Transcript:
    """
    Class to transcribe any YouTube video to text.

    Attributes:
        _environment (Environment): `Environment` object for getting the
            api key and various other environment variables.
        _video (pytube.YouTube): `pytube.Video` object containing the video
            to get the transcripts for.
        _audio (pytube.Stream): Audio stream of `video`.
    """

    def __init__(self,
                 output_filepath: str = "transcript.txt",
                 ):
        """
        Initializes required variables for the `Transcript` object.

        Args:
            output_filepath: Filepath of where the transcript will be
                saved.
        """
        self._environment = Environment()

        self._video = None

        # Init audio variables
        self._audio = None
        self._audio_filepath = ""
        self._audio_filename = ""

        # Init transcription variables
        self._transcript = None
        self._transcript_filepath = output_filepath

    def _set_youtube_video(self,
                           *args,
                           url: str = "",
                           **kwargs,
                           ):
        """
        Sets the `pytube.YouTube` object with a valid YouTube url.

        The user is prompted for a valid YouTube video url. Using the
        valid url, a new `pytube.YouTube` object is created and bound
         to `video`.

        Args:
            *args: Additional arguments to send to the `pytube.YouTube`
                object.
            url: Valid YouTube video url. Optional.
            **kwargs: Additional keyword arguments to send to the
                `pytube.YouTube` object.
        """
        print(url)
        if not url:
            url = input("Enter a youtube video url: ")

        self._video = pytube.YouTube(url, *args, **kwargs)

    def _set_audio(self) -> None:
        """Gets the audio and its filename and filepath from `video`."""
        self._audio = self._video.streams.get_audio_only()
        self._audio_filepath = self._audio.get_file_path()
        self._audio_filename = self._audio.default_filename

    def transcribe_video(self, *args, video_url: str = "", **kwargs) -> None:
        """
        Transcribes a YouTube video to text using OpenAIs Whisper

        Accepts a YouTube url in `video_url` if one does not already exist in
        the object. The video is passed to OpenAIs whisper and transcribed. The
        text is then saved to a file specified by `transcript_filepath`. Audio
        that was downloaded for transcription is deleted at the end.

        Args:
            args: Any additional arguments to be passed to a
                `pytube.YouTube` object.
            video_url: YouTube video to transcribe.
            kwargs: Any additional arguments to be passed to a
                `pytube.YouTube` object.
        """
        # Check that video exists or user provided a url
        if not self._video or video_url:
            self._set_youtube_video(*args, url=video_url, **kwargs)

        # Get audio file of current video
        self._set_audio()

        # Save audio before attempting to transcribe
        self._save_audio()

        audio_file = open(self._audio_filepath, 'rb')
        try:
            print("Attempting to transcribe audio...")
            # Get transcript
            self._transcript = openai.Audio.transcribe(
                "whisper-1",
                file=audio_file,
            ).get("text")
            print("Successfully transcribed audio.")
        except openai.error.AuthenticationError as error:
            print("===========ERROR==============")
            print(f"Error: {error.error}")
            print(f"Code: {error.code}")
            print(f"Message: {error.user_message}")
            print("==============================")
        else:
            self.save_transcript()
            self.print_transcript()
        finally:
            audio_file.close()
            self._delete_audio_linux()

    def save_transcript(self) -> None:
        """Saves `transcript` to a text file at `transcript_filepath`"""
        with open(self._transcript_filepath, "w", encoding='utf-8') \
                as file:
            # Write transcript to file
            print("Saving transcript...")
            print(self._transcript, file=file)
            print(f"Saved transcript to: {self._transcript_filepath}")

    def print_transcript(self) -> None:
        """Prints transcript text."""
        print("Transcript:")
        print(self._transcript)

    def _save_audio(self, *args, **kwargs):
        """Saves `audio` to a .mp3 file."""
        print("Downloading audio file...")
        self._audio.download(*args, **kwargs)
        print("Audio file downloaded.")

    def _delete_audio_linux(self) -> None:
        """Unix-compatible method to remove audio file."""
        print("Removing audio file...")
        subprocess.run(f'rm -f ./"{self._audio_filename}"', shell=True)
        print(f"Audio file removed at: {self._audio_filepath}")

    def _delete_audio_windows(self) -> None:
        """Windows-compatible method to remove audio file."""
        print("Removing audio file...")
        subprocess.run(f'del ./"{self._audio_filename}"', shell=True)
        print(f"Audio file removed at: {self._audio_filepath}")

    def set_api_key(self, api_key: str = "") -> None:
        self._environment.set_openai_api_key(api_key)

    def get_api_key(self) -> str:
        return self._environment.get_api_key()


class Environment:
    """
    Attributes:
        env_file_exists (bool): Whether a .env file exists.
        _API_KEY (str): API Key to be used with OpenAI.
        environment (os.environ): The operating system environment,
            including environment variables.
        args (list[str, ...]): Arguments passed to the script via
            terminal.
        args_length (int): How many arguments were passed to the script
            via terminal.
    """

    def __init__(self):
        # Load environment variables
        self.env_file_exists = load_dotenv()
        self._API_KEY = environ.get("OPENAI_API_KEY") or ""
        self.environment = os.environ
        self.args = sys.argv
        self.args_length = len(self.args)

    def get_api_key(self) -> str:
        """Returns `_API_KEY` attribute."""
        return self._API_KEY

    def _set_api_key(self, api_key: str) -> None:
        """Sets `_API_KEY` attribute."""
        self._API_KEY = api_key

    def set_openai_api_key(self, api_key: str = "") -> None:
        """Sets openai api key and prompts user if one doesn't exist."""
        if api_key:
            self._set_api_key(api_key)
            openai.api_key = self.get_api_key()
        elif self.env_file_exists:
            openai.api_key = self.get_api_key()
        else:
            self._set_api_key(input("Enter your api key: "))

        openai.api_key = self.get_api_key()


if __name__ == "__main__":
    e = Transcript()
    e.set_api_key()
    e.transcribe_video()
