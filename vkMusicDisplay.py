import requests
import time
import bot_settings as settings
import logging

class VKMusicDisplay:
    def __init__(self, code, redirect_uri):
        # Preset
        self._log_setup()

        self._redirect_uri = redirect_uri
        self.connected = self._connect(code)

        # Initialize socketio
        self._emit = None
        self._sid = None

        self.current = None
        #test
        self.get_audio()

    def _log_setup(self):
        self.logger = logging.getLogger('vkmusic')
        log_f = logging.FileHandler(settings.VK_LOG_FILE)
        log_s = logging.StreamHandler()

        if (settings.DEBUG):
            self.logger.setLevel(logging.DEBUG)
            log_f.setLevel(logging.DEBUG)
            log_s.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(settings.LOG_FORMATTER)
        log_f.setFormatter(formatter)
        log_s.setFormatter(formatter)

        self.logger.addHandler(log_f)
        self.logger.addHandler(log_s)

    def _connect(self, code):
        params = {
            'client_id': settings.VK_CLIENT_ID,
            'client_secret': settings.VK_CLIENT_SECRET,
            'redirect_uri': self._redirect_uri,
            'code': code
        }
        data = requests.get(settings.VK_ACCESS_TOKEN_LINK, params=params)

        if data.status_code != 200:
            self.logger.error("Failed to connect to VK API")
            return False
        
        resp = data.json()
        
        token = resp.get('access_token')

        if not token:
            self.logger.error("No access token provided")
            return False

        self.token = token
        return True

    # Set communication to frontend
    def set_socket(self, emit_func, sid):
        self.logger.debug("Socket set up for VK audio")
        self._emit = emit_func
        self._sid = sid

    def start(self):
        while self.connected:
            success, audio = self.get_audio()

            if success and self.current != audio:
                self.logger.info('Audio update to {0}'.format(audio))
                # Set current track
                self.current = audio

                # Emit event
                if self._sid:
                    self._emit('audio', {'audio': audio}, room=self._sid)
                
                # Update file
                f = open(settings.VK_MUSIC_OUT_FILE, 'w')
                f.write(audio + ' '*settings.VK_MUSIC_SPACE_AMOUNT) # separate two scrolls
                f.close()

            # Wait delay
            time.sleep(settings.VK_STATUS_POLL_DELAY)
    
    # Disable poling
    def stop(self):
        self.logger.info("Stopping current VKMD instance")
        self.connected = False

    # Build audio string from audio object
    def _build_audio_string(self, audio):
        return audio['artist'] + ' - ' + audio['title'] 

    def get_audio(self):
        params = {
            'access_token': self.token,
            'fields': "status",
            'v': settings.VK_API_VERSION,
        }
        data = requests.get(settings.VK_API_LINK + 'users.get', params=params)
        
        try:
            response = data.json()['response'][0]
        except:
            self.logger("Error retireving user info")
            return False, None
        
        if 'status_audio' not in response.keys():
            return True, settings.VK_NO_AUDIO

        audio = response.get('status_audio')
        return True, self._build_audio_string(audio)