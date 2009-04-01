# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Archiveitems(models.Model):
    intid = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=60, blank=True)
    title = models.CharField(max_length=384, blank=True)
    subtitle = models.CharField(max_length=384, blank=True)
    description = models.TextField(blank=True)
    startdate = models.CharField(max_length=90, blank=True)
    starttime = models.CharField(max_length=90, blank=True)
    size = models.IntegerField()
    filename = models.TextField()
    hascutlist = models.IntegerField()
    cutlist = models.TextField(blank=True)
    class Meta:
        db_table = u'archiveitems'

class Callsignnetworkmap(models.Model):
    id = models.IntegerField(primary_key=True)
    callsign = models.CharField(unique=True, max_length=60)
    network = models.CharField(max_length=60)
    class Meta:
        db_table = u'callsignnetworkmap'

class Capturecard(models.Model):
    cardid = models.IntegerField(primary_key=True)
    videodevice = models.CharField(max_length=384, blank=True)
    audiodevice = models.CharField(max_length=384, blank=True)
    vbidevice = models.CharField(max_length=384, blank=True)
    cardtype = models.CharField(max_length=96, blank=True)
    defaultinput = models.CharField(max_length=96, blank=True)
    audioratelimit = models.IntegerField(null=True, blank=True)
    hostname = models.CharField(max_length=765, blank=True)
    dvb_swfilter = models.IntegerField(null=True, blank=True)
    dvb_sat_type = models.IntegerField()
    dvb_wait_for_seqstart = models.IntegerField()
    skipbtaudio = models.IntegerField(null=True, blank=True)
    dvb_on_demand = models.IntegerField()
    dvb_diseqc_type = models.IntegerField(null=True, blank=True)
    firewire_port = models.IntegerField()
    firewire_node = models.IntegerField()
    firewire_speed = models.IntegerField()
    firewire_model = models.CharField(max_length=96, blank=True)
    firewire_connection = models.IntegerField()
    dbox2_port = models.IntegerField()
    dbox2_httpport = models.IntegerField()
    dbox2_host = models.CharField(max_length=96, blank=True)
    signal_timeout = models.IntegerField()
    channel_timeout = models.IntegerField()
    dvb_tuning_delay = models.IntegerField()
    contrast = models.IntegerField()
    brightness = models.IntegerField()
    colour = models.IntegerField()
    hue = models.IntegerField()
    diseqcid = models.IntegerField(null=True, blank=True)
    dvb_eitscan = models.IntegerField()
    class Meta:
        db_table = u'capturecard'

class Cardinput(models.Model):
    cardinputid = models.IntegerField(primary_key=True)
    cardid = models.IntegerField()
    sourceid = models.IntegerField()
    inputname = models.CharField(max_length=96)
    externalcommand = models.CharField(max_length=384, blank=True)
    preference = models.IntegerField()
    shareable = models.CharField(max_length=3, blank=True)
    tunechan = models.CharField(max_length=30, blank=True)
    startchan = models.CharField(max_length=30, blank=True)
    freetoaironly = models.IntegerField(null=True, blank=True)
    diseqc_port = models.IntegerField(null=True, blank=True)
    diseqc_pos = models.FloatField(null=True, blank=True)
    lnb_lof_switch = models.IntegerField(null=True, blank=True)
    lnb_lof_hi = models.IntegerField(null=True, blank=True)
    lnb_lof_lo = models.IntegerField(null=True, blank=True)
    displayname = models.CharField(max_length=192)
    radioservices = models.IntegerField(null=True, blank=True)
    dishnet_eit = models.IntegerField()
    recpriority = models.IntegerField()
    quicktune = models.IntegerField()
    class Meta:
        db_table = u'cardinput'

class Channel(models.Model):
    chanid = models.IntegerField()
    channum = models.CharField(max_length=30)
    freqid = models.CharField(max_length=30, blank=True)
    sourceid = models.IntegerField(null=True, blank=True)
    callsign = models.CharField(max_length=60)
    name = models.CharField(max_length=192)
    icon = models.CharField(max_length=765)
    finetune = models.IntegerField(null=True, blank=True)
    videofilters = models.CharField(max_length=765)
    xmltvid = models.CharField(max_length=192)
    recpriority = models.IntegerField()
    contrast = models.IntegerField(null=True, blank=True)
    brightness = models.IntegerField(null=True, blank=True)
    colour = models.IntegerField(null=True, blank=True)
    hue = models.IntegerField(null=True, blank=True)
    tvformat = models.CharField(max_length=30)
    commfree = models.IntegerField()
    visible = models.IntegerField()
    outputfilters = models.CharField(max_length=765)
    useonairguide = models.IntegerField(null=True, blank=True)
    mplexid = models.IntegerField(null=True, blank=True)
    serviceid = models.IntegerField(null=True, blank=True)
    atscsrcid = models.IntegerField(null=True, blank=True)
    tmoffset = models.IntegerField()
    atsc_major_chan = models.IntegerField()
    atsc_minor_chan = models.IntegerField()
    last_record = models.DateTimeField()
    default_authority = models.CharField(max_length=96)
    commmethod = models.IntegerField()
    class Meta:
        db_table = u'channel'

class Codecparams(models.Model):
    profile = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=384, primary_key=True)
    value = models.CharField(max_length=384, blank=True)
    class Meta:
        db_table = u'codecparams'

class Credits(models.Model):
    person = models.IntegerField()
    chanid = models.IntegerField(unique=True)
    starttime = models.DateTimeField(unique=True)
    role = models.CharField(max_length=303)
    class Meta:
        db_table = u'credits'

class Customexample(models.Model):
    rulename = models.CharField(max_length=192, primary_key=True)
    fromclause = models.TextField()
    whereclause = models.TextField()
    search = models.IntegerField()
    class Meta:
        db_table = u'customexample'

class DiseqcConfig(models.Model):
    cardinputid = models.IntegerField()
    diseqcid = models.IntegerField()
    value = models.CharField(max_length=48)
    class Meta:
        db_table = u'diseqc_config'

class DiseqcTree(models.Model):
    diseqcid = models.IntegerField(primary_key=True)
    parentid = models.IntegerField(null=True, blank=True)
    ordinal = models.IntegerField()
    type = models.CharField(max_length=48)
    subtype = models.CharField(max_length=48)
    description = models.CharField(max_length=96)
    switch_ports = models.IntegerField()
    rotor_hi_speed = models.FloatField()
    rotor_lo_speed = models.FloatField()
    rotor_positions = models.CharField(max_length=765)
    lnb_lof_switch = models.IntegerField()
    lnb_lof_hi = models.IntegerField()
    lnb_lof_lo = models.IntegerField()
    cmd_repeat = models.IntegerField()
    lnb_pol_inv = models.IntegerField()
    class Meta:
        db_table = u'diseqc_tree'

class Displayprofilegroups(models.Model):
    name = models.CharField(max_length=384, primary_key=True)
    hostname = models.CharField(max_length=765, primary_key=True)
    profilegroupid = models.IntegerField(unique=True)
    class Meta:
        db_table = u'displayprofilegroups'

class Displayprofiles(models.Model):
    profilegroupid = models.IntegerField()
    profileid = models.IntegerField()
    value = models.CharField(max_length=384)
    data = models.CharField(max_length=765)
    class Meta:
        db_table = u'displayprofiles'

class DtvMultiplex(models.Model):
    mplexid = models.IntegerField(primary_key=True)
    sourceid = models.IntegerField(null=True, blank=True)
    transportid = models.IntegerField(null=True, blank=True)
    networkid = models.IntegerField(null=True, blank=True)
    frequency = models.IntegerField(null=True, blank=True)
    inversion = models.CharField(max_length=3, blank=True)
    symbolrate = models.IntegerField(null=True, blank=True)
    fec = models.CharField(max_length=30, blank=True)
    polarity = models.CharField(max_length=3, blank=True)
    modulation = models.CharField(max_length=30, blank=True)
    bandwidth = models.CharField(max_length=3, blank=True)
    lp_code_rate = models.CharField(max_length=30, blank=True)
    transmission_mode = models.CharField(max_length=3, blank=True)
    guard_interval = models.CharField(max_length=30, blank=True)
    visible = models.IntegerField()
    constellation = models.CharField(max_length=30, blank=True)
    hierarchy = models.CharField(max_length=30, blank=True)
    hp_code_rate = models.CharField(max_length=30, blank=True)
    sistandard = models.CharField(max_length=30, blank=True)
    serviceversion = models.IntegerField(null=True, blank=True)
    updatetimestamp = models.DateTimeField()
    class Meta:
        db_table = u'dtv_multiplex'

class DtvPrivatetypes(models.Model):
    sitype = models.CharField(max_length=12)
    networkid = models.IntegerField()
    private_type = models.CharField(max_length=60)
    private_value = models.CharField(max_length=300)
    class Meta:
        db_table = u'dtv_privatetypes'

class Dvdbookmark(models.Model):
    serialid = models.CharField(max_length=48, primary_key=True)
    name = models.CharField(max_length=96, blank=True)
    title = models.IntegerField()
    audionum = models.IntegerField()
    subtitlenum = models.IntegerField()
    framenum = models.IntegerField()
    timestamp = models.DateTimeField()
    class Meta:
        db_table = u'dvdbookmark'

class Dvdinput(models.Model):
    intid = models.IntegerField(primary_key=True)
    hsize = models.IntegerField(null=True, blank=True)
    vsize = models.IntegerField(null=True, blank=True)
    ar_num = models.IntegerField(null=True, blank=True)
    ar_denom = models.IntegerField(null=True, blank=True)
    fr_code = models.IntegerField(null=True, blank=True)
    letterbox = models.IntegerField(null=True, blank=True)
    v_format = models.CharField(max_length=48, blank=True)
    class Meta:
        db_table = u'dvdinput'

class Dvdtranscode(models.Model):
    intid = models.IntegerField(primary_key=True)
    input = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=384)
    sync_mode = models.IntegerField(null=True, blank=True)
    use_yv12 = models.IntegerField(null=True, blank=True)
    cliptop = models.IntegerField(null=True, blank=True)
    clipbottom = models.IntegerField(null=True, blank=True)
    clipleft = models.IntegerField(null=True, blank=True)
    clipright = models.IntegerField(null=True, blank=True)
    f_resize_h = models.IntegerField(null=True, blank=True)
    f_resize_w = models.IntegerField(null=True, blank=True)
    hq_resize_h = models.IntegerField(null=True, blank=True)
    hq_resize_w = models.IntegerField(null=True, blank=True)
    grow_h = models.IntegerField(null=True, blank=True)
    grow_w = models.IntegerField(null=True, blank=True)
    clip2top = models.IntegerField(null=True, blank=True)
    clip2bottom = models.IntegerField(null=True, blank=True)
    clip2left = models.IntegerField(null=True, blank=True)
    clip2right = models.IntegerField(null=True, blank=True)
    codec = models.CharField(max_length=384)
    codec_param = models.CharField(max_length=384, blank=True)
    bitrate = models.IntegerField(null=True, blank=True)
    a_sample_r = models.IntegerField(null=True, blank=True)
    a_bitrate = models.IntegerField(null=True, blank=True)
    two_pass = models.IntegerField(null=True, blank=True)
    tc_param = models.CharField(max_length=384, blank=True)
    class Meta:
        db_table = u'dvdtranscode'

class EitCache(models.Model):
    chanid = models.IntegerField(primary_key=True)
    eventid = models.IntegerField(primary_key=True)
    tableid = models.IntegerField()
    version = models.IntegerField()
    endtime = models.IntegerField()
    status = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'eit_cache'

class Favorites(models.Model):
    favid = models.IntegerField(primary_key=True)
    userid = models.IntegerField()
    chanid = models.IntegerField()
    class Meta:
        db_table = u'favorites'

class Filemarkup(models.Model):
    filename = models.TextField()
    mark = models.IntegerField()
    offset = models.IntegerField(null=True, blank=True)
    type = models.IntegerField()
    class Meta:
        db_table = u'filemarkup'

class Gallerymetadata(models.Model):
    image = models.CharField(max_length=765, primary_key=True)
    angle = models.IntegerField()
    class Meta:
        db_table = u'gallerymetadata'

class Gamemetadata(models.Model):
    system = models.CharField(max_length=384)
    romname = models.CharField(max_length=384)
    gamename = models.CharField(max_length=384)
    genre = models.CharField(max_length=384)
    year = models.CharField(max_length=30)
    favorite = models.IntegerField(null=True, blank=True)
    rompath = models.CharField(max_length=765)
    gametype = models.CharField(max_length=192)
    diskcount = models.IntegerField()
    country = models.CharField(max_length=384)
    crc_value = models.CharField(max_length=192)
    display = models.IntegerField()
    version = models.CharField(max_length=192)
    publisher = models.CharField(max_length=384)
    class Meta:
        db_table = u'gamemetadata'

class Gameplayers(models.Model):
    gameplayerid = models.IntegerField(primary_key=True)
    playername = models.CharField(unique=True, max_length=192)
    workingpath = models.CharField(max_length=765)
    rompath = models.CharField(max_length=765)
    screenshots = models.CharField(max_length=765)
    commandline = models.TextField()
    gametype = models.CharField(max_length=192)
    extensions = models.CharField(max_length=384)
    spandisks = models.IntegerField()
    class Meta:
        db_table = u'gameplayers'

class Housekeeping(models.Model):
    tag = models.CharField(max_length=192, primary_key=True)
    lastrun = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'housekeeping'

class Inputgroup(models.Model):
    cardinputid = models.IntegerField()
    inputgroupid = models.IntegerField()
    inputgroupname = models.CharField(max_length=96)
    class Meta:
        db_table = u'inputgroup'

class Inuseprograms(models.Model):
    chanid = models.IntegerField()
    starttime = models.DateTimeField()
    recusage = models.CharField(max_length=384)
    lastupdatetime = models.DateTimeField()
    hostname = models.CharField(max_length=765)
    rechost = models.CharField(max_length=192)
    recdir = models.CharField(max_length=765)
    class Meta:
        db_table = u'inuseprograms'

class Jobqueue(models.Model):
    id = models.IntegerField(primary_key=True)
    chanid = models.IntegerField(unique=True)
    starttime = models.DateTimeField(unique=True)
    inserttime = models.DateTimeField(unique=True)
    type = models.IntegerField(unique=True)
    cmds = models.IntegerField()
    flags = models.IntegerField()
    status = models.IntegerField()
    statustime = models.DateTimeField()
    hostname = models.CharField(max_length=765)
    args = models.TextField()
    comment = models.CharField(max_length=384)
    schedruntime = models.DateTimeField()
    class Meta:
        db_table = u'jobqueue'

class Jumppoints(models.Model):
    destination = models.CharField(max_length=384, primary_key=True)
    description = models.CharField(max_length=765, blank=True)
    keylist = models.CharField(max_length=384, blank=True)
    hostname = models.CharField(max_length=765, primary_key=True)
    class Meta:
        db_table = u'jumppoints'

class Keybindings(models.Model):
    context = models.CharField(max_length=96, primary_key=True)
    action = models.CharField(max_length=96, primary_key=True)
    description = models.CharField(max_length=765, blank=True)
    keylist = models.CharField(max_length=384, blank=True)
    hostname = models.CharField(max_length=765, primary_key=True)
    class Meta:
        db_table = u'keybindings'

class Keyword(models.Model):
    phrase = models.CharField(unique=True, max_length=384)
    searchtype = models.IntegerField(unique=True)
    class Meta:
        db_table = u'keyword'

class Mamemetadata(models.Model):
    romname = models.CharField(max_length=384)
    manu = models.CharField(max_length=384)
    cloneof = models.CharField(max_length=384)
    romof = models.CharField(max_length=384)
    driver = models.CharField(max_length=384)
    cpu1 = models.CharField(max_length=384)
    cpu2 = models.CharField(max_length=384)
    cpu3 = models.CharField(max_length=384)
    cpu4 = models.CharField(max_length=384)
    sound1 = models.CharField(max_length=384)
    sound2 = models.CharField(max_length=384)
    sound3 = models.CharField(max_length=384)
    sound4 = models.CharField(max_length=384)
    players = models.IntegerField()
    buttons = models.IntegerField()
    image_searched = models.IntegerField()
    rom_path = models.CharField(max_length=765)
    class Meta:
        db_table = u'mamemetadata'

class Mamesettings(models.Model):
    romname = models.CharField(max_length=384)
    usedefault = models.IntegerField()
    fullscreen = models.IntegerField()
    scanlines = models.IntegerField()
    extra_artwork = models.IntegerField()
    autoframeskip = models.IntegerField()
    autocolordepth = models.IntegerField()
    rotleft = models.IntegerField()
    rotright = models.IntegerField()
    flipx = models.IntegerField()
    flipy = models.IntegerField()
    scale = models.IntegerField()
    antialias = models.IntegerField()
    translucency = models.IntegerField()
    beam = models.FloatField()
    flicker = models.FloatField()
    vectorres = models.IntegerField()
    analogjoy = models.IntegerField()
    mouse = models.IntegerField()
    winkeys = models.IntegerField()
    grabmouse = models.IntegerField()
    joytype = models.IntegerField()
    sound = models.IntegerField()
    samples = models.IntegerField()
    fakesound = models.IntegerField()
    volume = models.IntegerField()
    cheat = models.IntegerField()
    extraoption = models.CharField(max_length=384)
    class Meta:
        db_table = u'mamesettings'

class MoviesMovies(models.Model):
    id = models.IntegerField(primary_key=True)
    moviename = models.CharField(max_length=765, blank=True)
    rating = models.CharField(max_length=30, blank=True)
    runningtime = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'movies_movies'

class MoviesShowtimes(models.Model):
    id = models.IntegerField(primary_key=True)
    theaterid = models.IntegerField()
    movieid = models.IntegerField()
    showtimes = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'movies_showtimes'

class MoviesTheaters(models.Model):
    id = models.IntegerField(primary_key=True)
    theatername = models.CharField(max_length=300, blank=True)
    theateraddress = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = u'movies_theaters'

class MusicAlbumart(models.Model):
    albumart_id = models.IntegerField(primary_key=True)
    filename = models.CharField(max_length=765)
    directory_id = models.IntegerField()
    imagetype = models.IntegerField()
    song_id = models.IntegerField()
    embedded = models.IntegerField()
    class Meta:
        db_table = u'music_albumart'

class MusicAlbums(models.Model):
    album_id = models.IntegerField(primary_key=True)
    artist_id = models.IntegerField()
    album_name = models.CharField(max_length=765)
    year = models.IntegerField()
    compilation = models.IntegerField()
    class Meta:
        db_table = u'music_albums'

class MusicArtists(models.Model):
    artist_id = models.IntegerField(primary_key=True)
    artist_name = models.CharField(max_length=765)
    class Meta:
        db_table = u'music_artists'

class MusicDirectories(models.Model):
    directory_id = models.IntegerField(primary_key=True)
    path = models.TextField()
    parent_id = models.IntegerField()
    class Meta:
        db_table = u'music_directories'

class MusicGenres(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=765)
    class Meta:
        db_table = u'music_genres'

class MusicPlaylists(models.Model):
    playlist_id = models.IntegerField(primary_key=True)
    playlist_name = models.CharField(max_length=765)
    playlist_songs = models.TextField()
    last_accessed = models.DateTimeField()
    length = models.IntegerField()
    songcount = models.IntegerField()
    hostname = models.CharField(max_length=765)
    class Meta:
        db_table = u'music_playlists'

class MusicSmartplaylistCategories(models.Model):
    categoryid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=384)
    class Meta:
        db_table = u'music_smartplaylist_categories'

class MusicSmartplaylistItems(models.Model):
    smartplaylistitemid = models.IntegerField(primary_key=True)
    smartplaylistid = models.IntegerField()
    field = models.CharField(max_length=150)
    operator = models.CharField(max_length=60)
    value1 = models.CharField(max_length=765)
    value2 = models.CharField(max_length=765)
    class Meta:
        db_table = u'music_smartplaylist_items'

class MusicSmartplaylists(models.Model):
    smartplaylistid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=384)
    categoryid = models.IntegerField()
    matchtype = models.CharField(max_length=21)
    orderby = models.CharField(max_length=384)
    limitto = models.IntegerField()
    class Meta:
        db_table = u'music_smartplaylists'

class MusicSongs(models.Model):
    song_id = models.IntegerField(primary_key=True)
    filename = models.TextField()
    name = models.CharField(max_length=765)
    track = models.IntegerField()
    artist_id = models.IntegerField()
    album_id = models.IntegerField()
    genre_id = models.IntegerField()
    year = models.IntegerField()
    length = models.IntegerField()
    numplays = models.IntegerField()
    rating = models.IntegerField()
    lastplay = models.DateTimeField(null=True, blank=True)
    date_entered = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    format = models.CharField(max_length=12)
    mythdigest = models.CharField(max_length=765, blank=True)
    size = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=765, blank=True)
    comment = models.CharField(max_length=765, blank=True)
    disc_count = models.IntegerField(null=True, blank=True)
    disc_number = models.IntegerField(null=True, blank=True)
    track_count = models.IntegerField(null=True, blank=True)
    start_time = models.IntegerField(null=True, blank=True)
    stop_time = models.IntegerField(null=True, blank=True)
    eq_preset = models.CharField(max_length=765, blank=True)
    relative_volume = models.IntegerField(null=True, blank=True)
    sample_rate = models.IntegerField(null=True, blank=True)
    bitrate = models.IntegerField(null=True, blank=True)
    bpm = models.IntegerField(null=True, blank=True)
    directory_id = models.IntegerField()
    class Meta:
        db_table = u'music_songs'

class MusicStats(models.Model):
    num_artists = models.IntegerField()
    num_albums = models.IntegerField()
    num_songs = models.IntegerField()
    num_genres = models.IntegerField()
    total_time = models.CharField(max_length=36)
    total_size = models.CharField(max_length=30)
    class Meta:
        db_table = u'music_stats'

class Musicmetadata(models.Model):
    intid = models.IntegerField(primary_key=True)
    artist = models.CharField(max_length=384)
    compilation_artist = models.CharField(max_length=384)
    album = models.CharField(max_length=384)
    title = models.CharField(max_length=384)
    genre = models.CharField(max_length=384)
    year = models.IntegerField()
    tracknum = models.IntegerField()
    length = models.IntegerField()
    filename = models.TextField()
    rating = models.IntegerField()
    lastplay = models.DateTimeField()
    playcount = models.IntegerField()
    mythdigest = models.CharField(max_length=765, blank=True)
    size = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    format = models.CharField(max_length=12, blank=True)
    description = models.CharField(max_length=765, blank=True)
    comment = models.CharField(max_length=765, blank=True)
    compilation = models.IntegerField(null=True, blank=True)
    composer = models.CharField(max_length=765, blank=True)
    disc_count = models.IntegerField(null=True, blank=True)
    disc_number = models.IntegerField(null=True, blank=True)
    track_count = models.IntegerField(null=True, blank=True)
    start_time = models.IntegerField(null=True, blank=True)
    stop_time = models.IntegerField(null=True, blank=True)
    eq_preset = models.CharField(max_length=765, blank=True)
    relative_volume = models.IntegerField(null=True, blank=True)
    sample_rate = models.IntegerField(null=True, blank=True)
    bpm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'musicmetadata'

class Musicplaylist(models.Model):
    playlistid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=384)
    hostname = models.CharField(max_length=765, blank=True)
    songlist = models.TextField()
    class Meta:
        db_table = u'musicplaylist'

class Mythlog(models.Model):
    logid = models.IntegerField(primary_key=True)
    module = models.CharField(max_length=96)
    priority = models.IntegerField()
    acknowledged = models.IntegerField(null=True, blank=True)
    logdate = models.DateTimeField(null=True, blank=True)
    host = models.CharField(max_length=384, blank=True)
    message = models.CharField(max_length=765)
    details = models.TextField(blank=True)
    class Meta:
        db_table = u'mythlog'

class MythwebSessions(models.Model):
    id = models.CharField(max_length=384, primary_key=True)
    modified = models.DateTimeField()
    data = models.TextField()
    class Meta:
        db_table = u'mythweb_sessions'

class Neskeyword(models.Model):
    keyword = models.CharField(max_length=24, blank=True)
    value = models.CharField(max_length=240, blank=True)
    class Meta:
        db_table = u'neskeyword'

class Nestitle(models.Model):
    id = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=480, blank=True)
    designer = models.IntegerField(null=True, blank=True)
    publisher = models.IntegerField(null=True, blank=True)
    releasedate = models.TextField(blank=True) # This field type is a guess.
    screenshot = models.IntegerField(null=True, blank=True)
    keywords = models.CharField(max_length=120, blank=True)
    class Meta:
        db_table = u'nestitle'

class Netflix(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    category = models.CharField(max_length=765)
    url = models.CharField(max_length=765)
    ico = models.CharField(max_length=765, blank=True)
    updated = models.IntegerField(null=True, blank=True)
    is_queue = models.IntegerField(null=True, blank=True)
    queue = models.CharField(max_length=96, primary_key=True)
    class Meta:
        db_table = u'netflix'

class Networkiconmap(models.Model):
    id = models.IntegerField(primary_key=True)
    network = models.CharField(unique=True, max_length=60)
    url = models.CharField(max_length=765)
    class Meta:
        db_table = u'networkiconmap'

class Newssites(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    category = models.CharField(max_length=765)
    url = models.CharField(max_length=765)
    ico = models.CharField(max_length=765, blank=True)
    updated = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'newssites'

class Oldfind(models.Model):
    recordid = models.IntegerField(primary_key=True)
    findid = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'oldfind'

class Oldprogram(models.Model):
    oldtitle = models.CharField(max_length=384, primary_key=True)
    airdate = models.DateTimeField()
    class Meta:
        db_table = u'oldprogram'

class Oldrecorded(models.Model):
    chanid = models.IntegerField()
    starttime = models.DateTimeField(primary_key=True)
    endtime = models.DateTimeField()
    title = models.CharField(max_length=384)
    subtitle = models.CharField(max_length=384)
    description = models.TextField()
    category = models.CharField(max_length=192)
    seriesid = models.CharField(max_length=120)
    programid = models.CharField(max_length=120)
    findid = models.IntegerField()
    recordid = models.IntegerField()
    station = models.CharField(max_length=60, primary_key=True)
    rectype = models.IntegerField()
    duplicate = models.IntegerField()
    recstatus = models.IntegerField()
    reactivate = models.IntegerField()
    generic = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'oldrecorded'

class People(models.Model):
    person = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=384)
    class Meta:
        db_table = u'people'

class Phonecallhistory(models.Model):
    recid = models.IntegerField(primary_key=True)
    displayname = models.TextField()
    url = models.TextField()
    timestamp = models.TextField()
    duration = models.IntegerField()
    directionin = models.IntegerField()
    directoryref = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'phonecallhistory'

class Phonedirectory(models.Model):
    intid = models.IntegerField(primary_key=True)
    nickname = models.TextField()
    firstname = models.TextField(blank=True)
    surname = models.TextField(blank=True)
    url = models.TextField()
    directory = models.TextField()
    photofile = models.TextField(blank=True)
    speeddial = models.IntegerField()
    onhomelan = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'phonedirectory'

class Pidcache(models.Model):
    chanid = models.IntegerField()
    pid = models.IntegerField()
    tableid = models.IntegerField()
    class Meta:
        db_table = u'pidcache'

class Playgroup(models.Model):
    name = models.CharField(max_length=96, primary_key=True)
    titlematch = models.CharField(max_length=765)
    skipahead = models.IntegerField()
    skipback = models.IntegerField()
    timestretch = models.IntegerField()
    jump = models.IntegerField()
    class Meta:
        db_table = u'playgroup'

class Powerpriority(models.Model):
    priorityname = models.CharField(max_length=192, primary_key=True)
    recpriority = models.IntegerField()
    selectclause = models.TextField()
    class Meta:
        db_table = u'powerpriority'

class Profilegroups(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=384, blank=True)
    cardtype = models.CharField(max_length=96)
    is_default = models.IntegerField(null=True, blank=True)
    hostname = models.CharField(unique=True, max_length=765, blank=True)
    class Meta:
        db_table = u'profilegroups'

class Program(models.Model):
    chanid = models.IntegerField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    title = models.CharField(max_length=384)
    subtitle = models.CharField(max_length=384)
    description = models.TextField()
    category = models.CharField(max_length=192)
    category_type = models.CharField(max_length=192)
    airdate = models.TextField() # This field type is a guess.
    stars = models.FloatField()
    previouslyshown = models.IntegerField()
    title_pronounce = models.CharField(max_length=384)
    stereo = models.IntegerField()
    subtitled = models.IntegerField()
    hdtv = models.IntegerField()
    closecaptioned = models.IntegerField()
    partnumber = models.IntegerField()
    parttotal = models.IntegerField()
    seriesid = models.CharField(max_length=120)
    originalairdate = models.DateField(null=True, blank=True)
    showtype = models.CharField(max_length=90)
    colorcode = models.CharField(max_length=60)
    syndicatedepisodenumber = models.CharField(max_length=60)
    programid = models.CharField(max_length=120)
    manualid = models.IntegerField()
    generic = models.IntegerField(null=True, blank=True)
    listingsource = models.IntegerField()
    first = models.IntegerField()
    last = models.IntegerField()
    audioprop = models.CharField(max_length=144)
    subtitletypes = models.CharField(max_length=93)
    videoprop = models.CharField(max_length=57)
    class Meta:
        db_table = u'program'

class Programgenres(models.Model):
    chanid = models.IntegerField(primary_key=True)
    starttime = models.DateTimeField(primary_key=True)
    relevance = models.CharField(max_length=3, primary_key=True)
    genre = models.CharField(max_length=90, blank=True)
    class Meta:
        db_table = u'programgenres'

class Programrating(models.Model):
    chanid = models.IntegerField(unique=True)
    starttime = models.DateTimeField()
    system = models.CharField(max_length=24)
    rating = models.CharField(unique=True, max_length=48, blank=True)
    class Meta:
        db_table = u'programrating'

class Recgrouppassword(models.Model):
    recgroup = models.CharField(unique=True, max_length=96)
    password = models.CharField(max_length=30)
    class Meta:
        db_table = u'recgrouppassword'

class Record(models.Model):
    recordid = models.IntegerField(primary_key=True)
    type = models.IntegerField()
    chanid = models.IntegerField(null=True, blank=True)
    starttime = models.TextField() # This field type is a guess.
    startdate = models.DateField()
    endtime = models.TextField() # This field type is a guess.
    enddate = models.DateField()
    title = models.CharField(max_length=384)
    subtitle = models.CharField(max_length=384)
    description = models.TextField()
    category = models.CharField(max_length=192)
    profile = models.CharField(max_length=384)
    recpriority = models.IntegerField()
    autoexpire = models.IntegerField()
    maxepisodes = models.IntegerField()
    maxnewest = models.IntegerField()
    startoffset = models.IntegerField()
    endoffset = models.IntegerField()
    recgroup = models.CharField(max_length=96)
    dupmethod = models.IntegerField()
    dupin = models.IntegerField()
    station = models.CharField(max_length=60)
    seriesid = models.CharField(max_length=120)
    programid = models.CharField(max_length=120)
    search = models.IntegerField()
    autotranscode = models.IntegerField()
    autocommflag = models.IntegerField()
    autouserjob1 = models.IntegerField()
    autouserjob2 = models.IntegerField()
    autouserjob3 = models.IntegerField()
    autouserjob4 = models.IntegerField()
    findday = models.IntegerField()
    findtime = models.TextField() # This field type is a guess.
    findid = models.IntegerField()
    inactive = models.IntegerField()
    parentid = models.IntegerField()
    transcoder = models.IntegerField()
    tsdefault = models.FloatField()
    playgroup = models.CharField(max_length=96)
    prefinput = models.IntegerField()
    next_record = models.DateTimeField()
    last_record = models.DateTimeField()
    last_delete = models.DateTimeField()
    storagegroup = models.CharField(max_length=96)
    avg_delay = models.IntegerField()
    class Meta:
        db_table = u'record'

class RecordTmp(models.Model):
    recordid = models.IntegerField()
    type = models.IntegerField()
    chanid = models.IntegerField(null=True, blank=True)
    starttime = models.TextField() # This field type is a guess.
    startdate = models.DateField()
    endtime = models.TextField() # This field type is a guess.
    enddate = models.DateField()
    title = models.CharField(max_length=384)
    subtitle = models.CharField(max_length=384)
    description = models.TextField()
    category = models.CharField(max_length=192)
    profile = models.CharField(max_length=384)
    recpriority = models.IntegerField()
    autoexpire = models.IntegerField()
    maxepisodes = models.IntegerField()
    maxnewest = models.IntegerField()
    startoffset = models.IntegerField()
    endoffset = models.IntegerField()
    recgroup = models.CharField(max_length=96)
    dupmethod = models.IntegerField()
    dupin = models.IntegerField()
    station = models.CharField(max_length=60)
    seriesid = models.CharField(max_length=120)
    programid = models.CharField(max_length=120)
    search = models.IntegerField()
    autotranscode = models.IntegerField()
    autocommflag = models.IntegerField()
    autouserjob1 = models.IntegerField()
    autouserjob2 = models.IntegerField()
    autouserjob3 = models.IntegerField()
    autouserjob4 = models.IntegerField()
    findday = models.IntegerField()
    findtime = models.TextField() # This field type is a guess.
    findid = models.IntegerField()
    inactive = models.IntegerField()
    parentid = models.IntegerField()
    transcoder = models.IntegerField()
    tsdefault = models.FloatField()
    playgroup = models.CharField(max_length=96)
    prefinput = models.IntegerField()
    next_record = models.DateTimeField()
    last_record = models.DateTimeField()
    last_delete = models.DateTimeField()
    storagegroup = models.CharField(max_length=96)
    avg_delay = models.IntegerField()
    class Meta:
        db_table = u'record_tmp'

class Recorded(models.Model):
    chanid = models.IntegerField(primary_key=True)
    starttime = models.DateTimeField(primary_key=True)
    endtime = models.DateTimeField()
    title = models.CharField(max_length=384)
    subtitle = models.CharField(max_length=384)
    description = models.TextField()
    category = models.CharField(max_length=192)
    hostname = models.CharField(max_length=765)
    bookmark = models.IntegerField()
    editing = models.IntegerField()
    cutlist = models.IntegerField()
    autoexpire = models.IntegerField()
    commflagged = models.IntegerField()
    recgroup = models.CharField(max_length=96)
    recordid = models.IntegerField(null=True, blank=True)
    seriesid = models.CharField(max_length=120)
    programid = models.CharField(max_length=120)
    lastmodified = models.DateTimeField()
    filesize = models.IntegerField()
    stars = models.FloatField()
    previouslyshown = models.IntegerField(null=True, blank=True)
    originalairdate = models.DateField(null=True, blank=True)
    preserve = models.IntegerField()
    findid = models.IntegerField()
    deletepending = models.IntegerField()
    transcoder = models.IntegerField()
    timestretch = models.FloatField()
    recpriority = models.IntegerField()
    basename = models.CharField(max_length=765)
    progstart = models.DateTimeField()
    progend = models.DateTimeField()
    playgroup = models.CharField(max_length=96)
    profile = models.CharField(max_length=96)
    duplicate = models.IntegerField()
    transcoded = models.IntegerField()
    watched = models.IntegerField()
    storagegroup = models.CharField(max_length=96)
    class Meta:
        db_table = u'recorded'

class Recordedcredits(models.Model):
    person = models.IntegerField()
    chanid = models.IntegerField(unique=True)
    starttime = models.DateTimeField(unique=True)
    role = models.CharField(max_length=303)
    class Meta:
        db_table = u'recordedcredits'

class Recordedfile(models.Model):
    chanid = models.IntegerField(primary_key=True)
    starttime = models.DateTimeField(primary_key=True)
    basename = models.CharField(max_length=384)
    filesize = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    fps = models.FloatField()
    aspect = models.FloatField()
    audio_sample_rate = models.IntegerField()
    audio_bits_per_sample = models.IntegerField()
    audio_channels = models.IntegerField()
    audio_type = models.CharField(max_length=765)
    video_type = models.CharField(max_length=765)
    comment = models.CharField(max_length=765)
    class Meta:
        db_table = u'recordedfile'

class Recordedmarkup(models.Model):
    chanid = models.IntegerField(primary_key=True)
    starttime = models.DateTimeField(primary_key=True)
    mark = models.IntegerField(primary_key=True)
    offset = models.CharField(max_length=96, blank=True)
    type = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'recordedmarkup'

class Recordedprogram(models.Model):
    chanid = models.IntegerField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    title = models.CharField(max_length=384)
    subtitle = models.CharField(max_length=384)
    description = models.TextField()
    category = models.CharField(max_length=192)
    category_type = models.CharField(max_length=192)
    airdate = models.TextField() # This field type is a guess.
    stars = models.FloatField()
    previouslyshown = models.IntegerField()
    title_pronounce = models.CharField(max_length=384)
    stereo = models.IntegerField()
    subtitled = models.IntegerField()
    hdtv = models.IntegerField()
    closecaptioned = models.IntegerField()
    partnumber = models.IntegerField()
    parttotal = models.IntegerField()
    seriesid = models.CharField(max_length=120)
    originalairdate = models.DateField(null=True, blank=True)
    showtype = models.CharField(max_length=90)
    colorcode = models.CharField(max_length=60)
    syndicatedepisodenumber = models.CharField(max_length=60)
    programid = models.CharField(max_length=120)
    manualid = models.IntegerField(primary_key=True)
    generic = models.IntegerField(null=True, blank=True)
    listingsource = models.IntegerField()
    first = models.IntegerField()
    last = models.IntegerField()
    audioprop = models.CharField(max_length=144)
    subtitletypes = models.CharField(max_length=93)
    videoprop = models.CharField(max_length=57)
    class Meta:
        db_table = u'recordedprogram'

class Recordedrating(models.Model):
    chanid = models.IntegerField(unique=True)
    starttime = models.DateTimeField()
    system = models.CharField(max_length=24)
    rating = models.CharField(unique=True, max_length=48, blank=True)
    class Meta:
        db_table = u'recordedrating'

class Recordedseek(models.Model):
    chanid = models.IntegerField(primary_key=True)
    starttime = models.DateTimeField(primary_key=True)
    mark = models.IntegerField(primary_key=True)
    offset = models.IntegerField()
    type = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'recordedseek'

class Recordingprofiles(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=384, blank=True)
    videocodec = models.CharField(max_length=384, blank=True)
    audiocodec = models.CharField(max_length=384, blank=True)
    profilegroup = models.IntegerField()
    class Meta:
        db_table = u'recordingprofiles'

class Recordmatch(models.Model):
    recordid = models.IntegerField(null=True, blank=True)
    chanid = models.IntegerField(null=True, blank=True)
    starttime = models.DateTimeField(null=True, blank=True)
    manualid = models.IntegerField(null=True, blank=True)
    oldrecduplicate = models.IntegerField(null=True, blank=True)
    recduplicate = models.IntegerField(null=True, blank=True)
    findduplicate = models.IntegerField(null=True, blank=True)
    oldrecstatus = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'recordmatch'

class Romdb(models.Model):
    crc = models.CharField(max_length=192)
    name = models.CharField(max_length=384)
    description = models.CharField(max_length=384)
    category = models.CharField(max_length=384)
    year = models.CharField(max_length=30)
    manufacturer = models.CharField(max_length=384)
    country = models.CharField(max_length=384)
    publisher = models.CharField(max_length=384)
    platform = models.CharField(max_length=192)
    filesize = models.IntegerField(null=True, blank=True)
    flags = models.CharField(max_length=192)
    version = models.CharField(max_length=192)
    binfile = models.CharField(max_length=192)
    class Meta:
        db_table = u'romdb'

class Schemalock(models.Model):
    schemalock = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'schemalock'

class Settings(models.Model):
    value = models.CharField(max_length=384)
    data = models.TextField(blank=True)
    hostname = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'settings'

class Snessettings(models.Model):
    romname = models.CharField(max_length=384)
    usedefault = models.IntegerField()
    transparency = models.IntegerField()
    sixteen = models.IntegerField()
    hires = models.IntegerField()
    interpolate = models.IntegerField()
    nomodeswitch = models.IntegerField()
    fullscreen = models.IntegerField()
    stretch = models.IntegerField()
    nosound = models.IntegerField()
    soundskip = models.IntegerField()
    stereo = models.IntegerField()
    soundquality = models.IntegerField()
    envx = models.IntegerField()
    threadsound = models.IntegerField()
    syncsound = models.IntegerField()
    interpolatedsound = models.IntegerField()
    buffersize = models.IntegerField()
    nosamplecaching = models.IntegerField()
    altsampledecode = models.IntegerField()
    noecho = models.IntegerField()
    nomastervolume = models.IntegerField()
    nojoy = models.IntegerField()
    interleaved = models.IntegerField()
    altinterleaved = models.IntegerField()
    hirom = models.IntegerField()
    lowrom = models.IntegerField()
    header = models.IntegerField()
    noheader = models.IntegerField()
    pal = models.IntegerField()
    ntsc = models.IntegerField()
    layering = models.IntegerField()
    nohdma = models.IntegerField()
    nospeedhacks = models.IntegerField()
    nowindows = models.IntegerField()
    extraoption = models.CharField(max_length=384)
    class Meta:
        db_table = u'snessettings'

class Storagegroup(models.Model):
    id = models.IntegerField(primary_key=True)
    groupname = models.CharField(unique=True, max_length=96)
    hostname = models.CharField(max_length=192)
    dirname = models.CharField(unique=True, max_length=765)
    class Meta:
        db_table = u'storagegroup'

class Streams(models.Model):
    folder = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    url = models.CharField(max_length=765)
    description = models.CharField(max_length=765, blank=True)
    handler = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'streams'

class Tvchain(models.Model):
    chanid = models.IntegerField(primary_key=True)
    starttime = models.DateTimeField(primary_key=True)
    chainid = models.CharField(max_length=384)
    chainpos = models.IntegerField()
    discontinuity = models.IntegerField()
    watching = models.IntegerField()
    hostprefix = models.CharField(max_length=384)
    cardtype = models.CharField(max_length=96)
    input = models.CharField(max_length=96)
    channame = models.CharField(max_length=96)
    endtime = models.DateTimeField()
    class Meta:
        db_table = u'tvchain'

class Upnpmedia(models.Model):
    intid = models.IntegerField(primary_key=True)
    class_field = models.CharField(max_length=192, db_column='class') # Field renamed because it was a Python reserved word.
    itemtype = models.CharField(max_length=384)
    parentid = models.IntegerField()
    itemproperties = models.CharField(max_length=765)
    filepath = models.CharField(max_length=1536)
    title = models.CharField(max_length=765)
    filename = models.CharField(max_length=1536)
    coverart = models.CharField(max_length=1536)
    class Meta:
        db_table = u'upnpmedia'

class Videocast(models.Model):
    intid = models.IntegerField(primary_key=True)
    cast = models.CharField(max_length=384)
    class Meta:
        db_table = u'videocast'

class Videocategory(models.Model):
    intid = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=384)
    class Meta:
        db_table = u'videocategory'

class Videocountry(models.Model):
    intid = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=384)
    class Meta:
        db_table = u'videocountry'

class Videogenre(models.Model):
    intid = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=384)
    class Meta:
        db_table = u'videogenre'

class Videometadata(models.Model):
    intid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=384)
    director = models.CharField(max_length=384)
    plot = models.TextField(blank=True)
    rating = models.CharField(max_length=384)
    inetref = models.CharField(max_length=765)
    year = models.IntegerField()
    userrating = models.FloatField()
    length = models.IntegerField()
    showlevel = models.IntegerField()
    filename = models.TextField()
    coverfile = models.TextField()
    childid = models.IntegerField()
    browse = models.IntegerField()
    playcommand = models.CharField(max_length=765, blank=True)
    category = models.IntegerField()
    class Meta:
        db_table = u'videometadata'

class Videometadatacast(models.Model):
    idvideo = models.IntegerField()
    idcast = models.IntegerField()
    class Meta:
        db_table = u'videometadatacast'

class Videometadatacountry(models.Model):
    idvideo = models.IntegerField()
    idcountry = models.IntegerField()
    class Meta:
        db_table = u'videometadatacountry'

class Videometadatagenre(models.Model):
    idvideo = models.IntegerField()
    idgenre = models.IntegerField()
    class Meta:
        db_table = u'videometadatagenre'

class Videosource(models.Model):
    sourceid = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=384)
    xmltvgrabber = models.CharField(max_length=384, blank=True)
    userid = models.CharField(max_length=384)
    freqtable = models.CharField(max_length=48)
    lineupid = models.CharField(max_length=192, blank=True)
    password = models.CharField(max_length=192, blank=True)
    useeit = models.IntegerField()
    class Meta:
        db_table = u'videosource'

class Videotypes(models.Model):
    intid = models.IntegerField(primary_key=True)
    extension = models.CharField(max_length=384)
    playcommand = models.CharField(max_length=765)
    f_ignore = models.IntegerField(null=True, blank=True)
    use_default = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'videotypes'

class Weatherdatalayout(models.Model):
    location = models.CharField(max_length=192, primary_key=True)
    dataitem = models.CharField(max_length=192, primary_key=True)
    weatherscreens_screen = models.ForeignKey(Weatherscreens)
    weathersourcesettings_sourceid = models.ForeignKey(Weathersourcesettings, db_column='weathersourcesettings_sourceid')
    class Meta:
        db_table = u'weatherdatalayout'

class Weatherscreens(models.Model):
    screen_id = models.IntegerField(primary_key=True)
    draworder = models.IntegerField()
    container = models.CharField(max_length=192)
    hostname = models.CharField(max_length=765, blank=True)
    units = models.IntegerField()
    class Meta:
        db_table = u'weatherscreens'

class Weathersourcesettings(models.Model):
    sourceid = models.IntegerField(primary_key=True)
    source_name = models.CharField(max_length=192)
    update_timeout = models.IntegerField()
    retrieve_timeout = models.IntegerField()
    hostname = models.CharField(max_length=765, blank=True)
    path = models.CharField(max_length=765, blank=True)
    author = models.CharField(max_length=384, blank=True)
    version = models.CharField(max_length=96, blank=True)
    email = models.CharField(max_length=765, blank=True)
    types = models.TextField(blank=True)
    class Meta:
        db_table = u'weathersourcesettings'

class Websites(models.Model):
    grp = models.CharField(max_length=765)
    dsc = models.CharField(max_length=765, blank=True)
    url = models.CharField(max_length=765, primary_key=True)
    updated = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'websites'

