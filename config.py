V_MODULES = {
    'clock': {
        'command': 'python clock.py',
        'interval': 60
    },
    'gmail': {
        'command': 'python gmail/check.py',
        'interval': 300
    },
    'mpd': {
        'command': 'python mpd/check.py',
        'interval': 60
    },
    'news': {
        'command': 'python rss/check.py',
        'interval': 600
    }
}
