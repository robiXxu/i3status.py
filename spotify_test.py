import dbus


try:
    sessionBus = dbus.SessionBus()
    spotify_object = sessionBus.get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
    spotify_props = dbus.Interface(spotify_object,'org.freedesktop.DBus.Properties')

    spotify_meta = spotify_props.Get('org.mpris.MediaPlayer2.Player', 'Metadata')

    print(spotify_meta['xesam:artist'][0])
    print(spotify_meta['xesam:title'])

except Exception as e:
    # spotify is closed
    if isinstance(e, dbus.exceptions.DBusException):
        print('')
    else:
        print(e)
