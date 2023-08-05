class Song:
    """Represents song properties"""

    def __init__(
        self,
        name: str,
        artist: str,
        url: str,
        duration: int = 0,
        is_high_quality: bool = False,
    ):
        self.name = name
        self.artist = artist
        self.url = url
        self.duration = duration
        self.is_high_quality = is_high_quality

    def __str__(self) -> str:
        return f"{self.name} - {self.artist}"
