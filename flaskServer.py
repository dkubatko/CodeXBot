from flask import Flask, render_template, send_file, request
from flask_socketio import SocketIO, join_room, leave_room
import flask.logging
import flask_settings as settings
import logging
import threading
from CodeXBot import TwitchBot as Bot

app = Flask(__name__, template_folder='frontend')
socketio = SocketIO(app)
logger = logging.getLogger('flask_app')

TESTING_CHANNEL = 'miva1337'

# Connect to testing channel
bot = Bot(settings.BOT_USERNAME, settings.BOT_CLIENT_ID,
          settings.BOT_TOKEN, TESTING_CHANNEL)

# if (settings.DEBUG):
#     app.config['DEBUG'] = True

# emit one message through socket to the specified room
def socket_emit(event, message, room):
    global socketio, bot
    try:
        socketio.emit(event, message, room=room)
    except Exception as e:
        logger.warning("Failed to send message to room "\
            "{0} due to {1}".format(room, e))
        bot.set_socket(None, None)




def log_setup(app, logger):
    log_f = logging.FileHandler(settings.FLASK_LOG_FILE)
    log_s = logging.StreamHandler()

    if (settings.DEBUG):
        logger.setLevel(logging.DEBUG)
        log_f.setLevel(logging.DEBUG)
        log_s.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # app.logger.removeHandler()
    # Set formatter for requests
    formatter = settings.RequestFormatter(settings.REQUEST_FORMAT)

    log_f.setFormatter(formatter)
    log_s.setFormatter(formatter)

    app.logger.addHandler(log_f)
    app.logger.addHandler(log_s)

    # Set formatter for info
    log_f_app = logging.FileHandler(settings.FLASK_LOG_FILE)
    log_s_app = logging.StreamHandler()

    formatter = logging.Formatter(settings.FLASK_APP_LOG_FORMAT)

    log_f_app.setFormatter(formatter)
    log_s_app.setFormatter(formatter)

    logger.addHandler(log_f_app)
    logger.addHandler(log_s_app)

    logger.info("Successfully set up logging")


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    app.logger.info("Connected user with username <{0}>".format(username))
    return render_template('login.html', username = username)


@socketio.on('update')
def handle_update_socket(json):
    username = json['username']
    app.logger.info('Received update request for {0}'.format(username))
    global bot
    bot.set_socket(socket_emit, request.sid)

if (__name__ == '__main__'):
    socketio.start_background_task(target=bot.start)
    log_setup(app, logger)
    socketio.run(app)
