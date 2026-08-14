import random
import json
import os

class Song:
    def __init__(self, title, artist, duration, is_downloaded=False):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.is_downloaded = is_downloaded

    def to_dict(self):
        return {
            "title": self.title,
            "artist": self.artist,
            "duration": self.duration,
            "is_downloaded": self.is_downloaded
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["artist"], data["duration"], data.get("is_downloaded", False))

    def __str__(self):
        download_badge = " 📥 [Downloaded]" if self.is_downloaded else ""
        return f"{self.title} - {self.artist} ({self.duration} mins){download_badge}"


class SpotifyUnlimitedPro:
    STORAGE_FILE = "downloaded_library.json"

    def __init__(self):
        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.is_repeat = False
        self.load_storage()

    def save_storage(self):
        """Saves all downloaded songs to a local JSON file."""
        downloaded_songs = [s.to_dict() for s in self.playlist if s.is_downloaded]
        with open(self.STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(downloaded_songs, f, indent=4)

    def load_storage(self):
        """Loads previously downloaded songs from local JSON storage."""
        if os.path.exists(self.STORAGE_FILE):
            try:
                with open(self.STORAGE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        self.playlist.append(Song.from_dict(item))
            except Exception:
                pass

    def add_song(self, title, artist, duration):
        # Check if song already exists in library
        for s in self.playlist:
            if s.title.lower() == title.lower() and s.artist.lower() == artist.lower():
                return
        song = Song(title, artist, duration)
        self.playlist.append(song)

    def show_playlist(self, filter_downloaded_only=False):
        songs_to_show = [s for s in self.playlist if s.is_downloaded] if filter_downloaded_only else self.playlist
        
        if not songs_to_show:
            print("\n⚠️ No songs found in this section!")
            return

        header = "--- Offline Downloaded Storage ---" if filter_downloaded_only else "--- Online / All Songs ---"
        print(f"\n{header}")
        for idx, song in enumerate(songs_to_show, 1):
            pointer = "👉 " if (self.is_playing and self.playlist[self.current_index] == song) else "   "
            print(f"{pointer}{idx}. {song}")
        print("------------------------------------------\n")

    def play(self):
        if not self.playlist:
            print("No songs available to play!")
            return
        self.is_playing = True
        current_song = self.playlist[self.current_index]
        source_type = "Offline Storage (Local)" if current_song.is_downloaded else "Cloud Stream"
        print(f"\n▶️ Now Playing: {current_song.title} - {current_song.artist} [{source_type}]")

    def pause(self):
        if self.is_playing:
            self.is_playing = False
            print("⏸ Music paused.")
        else:
            print("No music is currently playing.")

    def next_song(self):
        if not self.playlist:
            print("The playlist is empty!")
            return
        
        if self.is_repeat:
            print("🔂 Repeat Mode is ON. Replaying track...")
        else:
            self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def previous_song(self):
        if not self.playlist:
            print("The playlist is empty!")
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def play_specific_song(self, song_number):
        if 1 <= song_number <= len(self.playlist):
            self.current_index = song_number - 1
            self.play()
        else:
            print("❌ Invalid track number!")

    def download_song(self, song_number):
        """Downloads a specific track to permanent local storage."""
        if 1 <= song_number <= len(self.playlist):
            target_song = self.playlist[song_number - 1]
            if target_song.is_downloaded:
                print(f"ℹ️ '{target_song.title}' is already downloaded in offline storage!")
            else:
                target_song.is_downloaded = True
                self.save_storage()
                print(f"✅ '{target_song.title}' downloaded successfully to offline storage!")
        else:
            print("❌ Invalid track number!")

    def download_all_songs(self):
        """Downloads every track in the playlist with no restrictions."""
        if not self.playlist:
            print("No songs available to download!")
            return
        
        for song in self.playlist:
            song.is_downloaded = True
        self.save_storage()
        print(f"✅ All {len(self.playlist)} tracks downloaded to offline storage successfully!")

    def shuffle_playlist(self):
        if len(self.playlist) < 2:
            print("Not enough songs to shuffle!")
            return
        random.shuffle(self.playlist)
        self.current_index = 0
        print("🔀 Playlist shuffled!")
        self.play()

    def toggle_repeat(self):
        self.is_repeat = not self.is_repeat
        status = "ENABLED 🔂" if self.is_repeat else "DISABLED ➡️"
        print(f"Repeat Mode: {status}")


# --- Application Runner ---
if __name__ == "__main__":
    app = SpotifyUnlimitedPro()

    # Pre-loading catalog songs
    default_tracks = [
        ("Malare", "Vijay Yesudas", "5:15"),
        ("Darshana", "Hesham Abdul Wahab", "4:30"),
        ("Jimikki Kammal", "Shaan Rahman", "3:40"),
        ("Aalaporan Thamizhan", "A.R. Rahman", "5:45"),
        ("Enjoy Enjaami", "Dhee ft. Arivu", "4:10"),
        ("Pavizha Mazha", "K.S. Harisankar", "4:15")
    ]

    for title, artist, duration in default_tracks:
        app.add_song(title, artist, duration)

    while True:
        repeat_status = "ON 🔂" if app.is_repeat else "OFF"
        print("\n=== Spotify Unlimited Pro (Offline Storage & Downloads) ===")
        print(f"Repeat: {repeat_status} | Total Songs: {len(app.playlist)}")
        print("1. View All Songs")
        print("2. View Offline / Downloaded Songs Only")
        print("3. Play")
        print("4. Pause")
        print("5. Next Track")
        print("6. Previous Track")
        print("7. Play Specific Track (By Number)")
        print("8. 📥 Download a Song to Local Storage")
        print("9. ⚡ Download ALL Songs (Unlimited)")
        print("10. Shuffle Playlist")
        print("11. Toggle Repeat Mode")
        print("12. Add New Custom Track")
        print("13. Exit")

        choice = input("Enter your choice (1-13): ").strip()

        if choice == '1':
            app.show_playlist(filter_downloaded_only=False)
        elif choice == '2':
            app.show_playlist(filter_downloaded_only=True)
        elif choice == '3':
            app.play()
        elif choice == '4':
            app.pause()
        elif choice == '5':
            app.next_song()
        elif choice == '6':
            app.previous_song()
        elif choice == '7':
            try:
                num = int(input("Enter the song number: "))
                app.play_specific_song(num)
            except ValueError:
                print("❌ Enter a valid number!")
        elif choice == '8':
            try:
                num = int(input("Enter song number to download: "))
                app.download_song(num)
            except ValueError:
                print("❌ Enter a valid number!")
        elif choice == '9':
            app.download_all_songs()
        elif choice == '10':
            app.shuffle_playlist()
        elif choice == '11':
            app.toggle_repeat()
        elif choice == '12':
            title = input("Song title: ").strip()
            artist = input("Artist: ").strip()
            duration = input("Duration (e.g. 3:50): ").strip()
            if title and artist and duration:
                app.add_song(title, artist, duration)
                print(f"'{title}' added to queue!")
            else:
                print("❌ Details cannot be blank!")
        elif choice == '13':
            print("Exiting application... All downloads are saved offline!")
            break
        else:
            print("❌ Invalid option! Choose between 1 and 13.")
