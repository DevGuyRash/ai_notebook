import pytube
from typing import Callable, Any, Dict, Optional


class YtVideo(pytube.YouTube):
    """
    Extends the `pytube.YouTube` class.

    Attributes:
        audio (pytube.Stream): Audio stream object.
        audio_filepath (str): Filepath for audio file.
        audio_filename (str): Filename for audio file.
    """

    def __init__(
            self,
            url: str,
            on_progress_callback: Optional[
                Callable[[Any, bytes, int], None]] = None,
            on_complete_callback: Optional[
                Callable[[Any, Optional[str]], None]] = None,
            proxies: Dict[str, str] = None,
            use_oauth: bool = False,
            allow_oauth_cache: bool = True
    ):
        """
        Construct a `YtVideo` object.

        Args:
            url: A valid YouTube watch URL.
            on_progress_callback: (Optional) User defined callback
                function for stream download progress events.
            on_complete_callback: (Optional) User defined callback
                function for stream download complete events.
            proxies: (Optional) A dict mapping protocol to proxy
                address which will be used by pytube.
            use_oauth: (Optional) Prompt the user to authenticate
                to YouTube. If allow_oauth_cache is set to True, the
                user should only be prompted once.
            allow_oauth_cache: (Optional) Cache OAuth tokens locally
                on the machine. Defaults to True. These tokens are
                only generated if use_oauth is set to True as well.
        """
        super().__init__(
            url=url,
            on_progress_callback=on_progress_callback,
            on_complete_callback=on_complete_callback,
            proxies=proxies,
            use_oauth=use_oauth,
            allow_oauth_cache=allow_oauth_cache,
        )
        self.audio = self.streams.get_audio_only()
        self.audio_filepath = self.audio.get_file_path()
        self.audio_filename = self.audio.default_filename

    def save_audio_file(self) -> None:
        """Saves `audio` to a .mp3 file at `audio_filepath`"""
        print("Downloading audio file...")
        self.audio.download()
        print("Audio file downloaded.")






