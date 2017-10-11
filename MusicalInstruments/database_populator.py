""" This module populates an empty database with a default set of values """
import database_functions as db
import time

# Adding dummy data for categories
category_name = [
    'String instruments',
    'Percussion instruments',
    'Electronic instruments',
    'Woodwind instruments',
    'Brass instruments'
]
category_description = [
    "String instruments, stringed instruments, or chordophones are musical instruments that produce sound from vibrating strings when the performer plays or sounds the strings in some manner. Musicians play some string instruments by plucking the strings with their fingers or a plectrum, and others by hitting the strings with a light wooden hammer or by rubbing the strings with a bow. In some keyboard instruments, such as the harpsichord or piano, the musician presses a key that plucks the string or strikes it with a hammer. With bowed instruments, the player rubs the strings with a horsehair bow, causing them to vibrate. With a hurdy-gurdy, the musician operates a mechanical wheel that rubs the strings. Examples: guitar, violin, sitar, cello, viola, veena, banjo, mandolin, ukulele, and bouzouki.",
    "A percussion instrument is a musical instrument that is sounded by being struck or scraped by a beater (including attached or enclosed beaters or rattles); struck, scraped or rubbed by hand; or struck against another similar instrument. The percussion family is believed to include the oldest musical instruments, following the human voice. Examples: mridangam, tabla, ghatam, kanjira, timpani, snare drum, bass drum, cymbals, triangle, tambourine.",
    "An electronic musical instrument is a musical instrument that produces sound using electronic circuitry and/or digital devices. Such an instrument sounds by outputting an electrical, electronic or digital audio signal that ultimately is plugged into a power amplifier which drives a loudspeaker, creating the sound heard by the performer and/or listener. Examples: Synthesizers, Theremin, Drum Machine, Turntable.",
    "Woodwind instruments are a family of musical instruments within the more general category of wind instruments. There are two main types of woodwind instruments: flutes and reed instruments (otherwise called reed pipes). What differentiates these instruments from other wind instruments is the way in which they produce their sound. Examples are recorders, flutes, oboes, clarinets, saxophones, and bassoons.",
    "A Brass instrument is a musical instrument that produces sound by sympathetic vibration of air in a tubular resonator in sympathy with the vibration of the player's lips. Brass instruments are also called labrosones, literally meaning 'lip-vibrated instruments'. Examples are horns, trumpets, trombones, euphoniums, and tubas.",
]
category_image = [
    "https://ccrma.stanford.edu/~cc/pianoStrings.png",
    "http://necmusic.edu/sites/default/files/styles/large_landscape/public/2017-02/Inline16x9_Percussion-ReichBongos__0184.jpg",
    "http://factmag-images.s3.amazonaws.com/wp-content/uploads/2015/08/native-instruments-maschine.jpg",
    "http://www.pellegrinomusic.com/assets/images/Oboe.jpg",
    "http://images.wisegeek.com/man-in-red-holding-trumpet.jpg"
]

category_user = [1, 1, 1, 1, 1]

# Adding dummy data for category items
category_item_category_id = [
    1, 1, 1, 1, 1, 1,
    2, 2, 2, 2, 2, 2,
    3, 3,
    4, 4, 4, 4,
    5, 5, 5,
]
category_item_title = [
    "Guitar", "Violin", 'Veena', "Sitar", "Mandolin", "Banjo",
    "Mridangam", "Drums", "Tabla", "Ghatam", "Kanjira", "Xylophone",
    "Theremin", "Synthesizer",
    "Flute", "Saxophone", "Clarinet", "Oboe",
    "Horn", "Trumpet", "Tuba",
]
category_item_description = [
    "The guitar is a musical instrument classified as a fretted string instrument with anywhere from four to 18 strings, usually having six. The sound is projected either acoustically, using a hollow wooden or plastic and wood box (for an acoustic guitar), or through electrical amplifier and a speaker (for an electric guitar). It is typically played by strumming or plucking the strings with the fingers, thumb or fingernails of the right hand or with a pick while fretting (or pressing against the frets) the strings with the fingers of the left hand. The guitar is a type of chordophone, traditionally constructed from wood and strung with either gut, nylon or steel strings and distinguished from other chordophones by its construction and tuning. The modern guitar was preceded by the gittern, the vihuela, the four-course Renaissance guitar, and the five-course baroque guitar, all of which contributed to the development of the modern six-string instrument.",
    "The violin is a wooden string instrument in the violin family. It is the smallest and highest-pitched instrument in the family in regular use. Smaller violin-type instruments are known, including the violino piccolo and the kit violin, but these are virtually unused in the 2010s. The violin typically has four strings tuned in perfect fifths, and is most commonly played by drawing a bow across its strings, though it can also be played by plucking the strings with the fingers (pizzicato). Violins are important instruments in a wide variety of musical genres. They are most prominent in the Western classical tradition and in many varieties of folk music. They are also frequently used in genres of folk including country music and bluegrass music and in jazz. Electric violins are used in some forms of rock music; further, the violin has come to be played in many non-Western music cultures, including Indian music and Iranian music. The violin is sometimes informally called a fiddle, particularly in Irish traditional music and bluegrass, but this nickname is also used regardless of the type of music played on it.",
    "The veena is a multistringed chordophone of the Indian subcontinent. It is an ancient musical instrument that evolved into many variations, such as lutes, zithers and arched harps. The many regional designs have different names such as the Rudra veena, the Saraswati veena, the Mohan veena and others. The North Indian design, that has been used in classical Hindustani music, is a stick zither. About 3.5 to 4 feet (1 to 1.2 meters) long to fit the measurements of the musician, it has a hollow body and two large resonating gourds under each end. It has four main strings which are melody type, and three auxiliary drone strings. To play, the musician plucks the melody strings downward with a plectrum worn on the first and second fingers, while the drone strings are strummed with the little finger of the playing hand. The musician stops the resonating strings, when so desired, with the fingers of the free hand. The veena has been generally replaced with the sitar in north Indian performances. The South Indian veena design, used in classical Carnatic music, is a lute. It is a long-necked, pear-shaped lute, but instead of the lower gourd of the north Indian design it has a pear shaped wooden piece. It too, however, has 24 frets, four melody strings, three drone strings, and played quite similar. It remains an important and popular string instrument in classical Carnatic music.",
    "The sitar is a plucked stringed instrument used mainly in Hindustani music and Indian classical music. The instrument is believed to have been derived from the veena, an ancient Indian instrument, which was modified by a Mughal court musician to conform with the tastes of his Mughal patrons and named after a Persian instrument called the setar (meaning three strings). The sitar flourished in the 16th and 17th centuries and arrived at its present form in 18th-century India. It derives its distinctive timbre and resonance from sympathetic strings, bridge design, a long hollow neck and a gourd-shaped resonance chamber. In appearance, the sitar is similar to the tanpura, except that it has frets.",
    "A mandolin is a stringed musical instrument in the lute family and is usually plucked with a plectrum or 'pick'. It commonly has four courses of doubled metal strings tuned in unison (8 strings), although five (10 strings) and six (12 strings) course versions also exist. The courses are normally tuned in a succession of perfect fifths. It is the soprano member of a family that includes the mandola, octave mandolin, mandocello and mandobass.",
    "The banjo is a four-, five- or six-stringed instrument with a thin membrane stretched over a frame or cavity as a resonator, called the head. The membrane, or head, is typically made of plastic, although animal skin is still occasionally but rarely used, and the frame is typically circular.",

    "The Mridangam is a percussion instrument from India of ancient origin. It is the primary rhythmic accompaniment in a Carnatic music ensemble, and in Dhrupad, where it is known as Pakhawaj. During a percussion ensemble, the mridangam is often accompanied by the ghatam, kanjira, and morsing.",
    "A drum kit - also called a drum set, trap set, or simply drums - is a collection of drums and other percussion instruments, typically cymbals, which are set up on stands to be played by a single player, with drumsticks held in both hands, and the feet operating pedals that control the hi-hat cymbal and the beater for the bass drum. A drum kit consists of a mix of drums (categorized classically as membranophones, Hornbostel-Sachs high-level classification 2) and idiophones - most significantly cymbals, but can also include the woodblock and cowbell (classified as Hornbostel-Sachs high-level classification 1). A standard modern kit contains: a snare drum, a bass drum, one or more toms, a hi-hat and one or more cymbals.",
    "The Tabla is a South Asian membranophone percussion instrument (similar to bongos), consisting of a pair of drums, used in traditional, classical, popular and folk music. It has been a particularly important instrument in Hindustani classical music since the 18th century, and remains in use in India, Pakistan, Nepal, Bangladesh, and Sri Lanka. The tabla consists of two single headed, barrel shaped small drums of slightly different size and shapes.",
    "The Ghatam is a percussion instrument used in the Carnatic music of South India. A variant played in Punjab and known as gharha as is a part of Punjabi folk traditions. The ghatam is one of the most ancient percussion instruments of South India. It is a clay pot with narrow mouth. From the mouth, it slants outwards to form a ridge. Made mainly of clay backed with brass or copper filings with a small amount of iron filings, the pitch of the ghatam varies according to its size. The pitch can be slightly altered by the application of plasticine clay or water.",
    "The kanjira, khanjira, khanjiri or ganjira, a South Indian frame drum, is an instrument of the tambourine family. As a folk and bhajan instrument, it has been used for many centuries. It was modified to a frame drum with a single pair of jingles by Manpoondia Pillai in the 1880s, who is credited with bringing the instrument to the classical stage. It is used primarily in concerts of Carnatic music (South Indian classical music) as a supporting instrument for the mridangam.",
    "The xylophone is a musical instrument in the percussion family that consists of wooden bars struck by mallets. Each bar is an idiophone tuned to a pitch of a musical scale, whether pentatonic or heptatonic in the case of many African and Asian instruments, diatonic in many western children's instruments, or chromatic for orchestral use. The term xylophone may be used generally, to include all such instruments such as the marimba, balafon and even the semantron.",

    "The theremin is an electronic musical instrument controlled without physical contact by the thereminist (performer). It is named after the Westernized name of its Soviet inventor, Leon Theremin, who patented the device in 1928. The instrument's controlling section usually consists of two metal antennas that sense the relative position of the thereminist's hands and control oscillators for frequency with one hand, and amplitude (volume) with the other. The electric signals from the theremin are amplified and sent to a loudspeaker.",
    "A synthesizer (often abbreviated as synth, also spelled synthesiser) is an electronic musical instrument that generates electric signals that are converted to sound through instrument amplifiers and loudspeakers or headphones. Synthesizers may either imitate instruments like piano, Hammond organ, flute, vocals; natural sounds like ocean waves, etc.; or generate new electronic timbres. They are often played with a musical keyboard, but they can be controlled via a variety of other input devices, including music sequencers, instrument controllers, fingerboards, guitar synthesizers, wind controllers, and electronic drums. Synthesizers without built-in controllers are often called sound modules, and are controlled via USB, MIDI or CV/gate using a controller device, often a MIDI keyboard or other controller.",

    "The flute is a family of musical instruments in the woodwind group. Unlike woodwind instruments with reeds, a flute is an aerophone or reedless wind instrument that produces its sound from the flow of air across an opening. According to the instrument classification of Hornbostel-Sachs, flutes are categorized as edge-blown aerophones. A musician who plays the flute can be referred to as a flute player, flautist, flutist or, less commonly, fluter or flutenist. Flutes, including the famous Bansuri, have been an integral part of Indian classical music since 1500 BC.",
    "The saxophone (also referred to as the sax) is a family of woodwind instruments. Saxophones are usually made of brass and played with a single-reed mouthpiece similar to that of the clarinet. Like the clarinet, saxophones have holes in the instrument which the player closes using a system of key mechanisms. When the player presses a key, a pad either covers a hole or lifts off a hole, lowering or raising the pitch, respectively.",
    "The clarinet is a musical-instrument family belonging to the group known as the woodwind instruments. It has a single-reed mouthpiece, a straight cylindrical tube with an almost cylindrical bore, and a flared bell. A person who plays a clarinet is called a clarinetist (sometimes spelled clarinettist).",
    "Oboes are a family of double reed woodwind instruments. The most common oboe plays in the treble or soprano range. Oboes are usually made of wood, but there are also oboes made of synthetic materials. A soprano oboe measures roughly 65 cm (25 1/2 in) long, with metal keys, a conical bore and a flared bell. Sound is produced by blowing into the reed and vibrating a column of air. The distinctive tone is versatile and has been described as 'bright'. When oboe is used alone, it is generally taken to mean the treble instrument rather than other instruments of the family, such as the cor anglais (English horn) or oboe d'amore.",

    "A horn is any of a family of musical instruments made of a tube, usually made of metal and often curved in various ways, with one narrow end into which the musician blows, and a wide end from which sound emerges. In horns, unlike some other brass instruments such as the trumpet, the bore gradually increases in width through most of its length-that is to say, it is conical rather than cylindrical.",
    "A trumpet is a blown musical instrument commonly used in classical and jazz ensembles. The trumpet group contains the instruments with the highest register in the brass family. Trumpet-like instruments have historically been used as signaling devices in battle or hunting, with examples dating back to at least 1500 BC; they began to be used as musical instruments only in the late 14th or early 15th century. Trumpets, which are blow horns are used in art music styles, for instance in orchestras, concert bands, and jazz ensembles, as well as in popular music. They are played by blowing air through nearly-closed lips (called the player's embouchure), producing a 'buzzing' sound that starts a standing wave vibration in the air column inside the instrument. Since the late 15th century they have primarily been constructed of brass tubing, usually bent twice into a rounded rectangular shape.",
    "The tuba is the largest and lowest-pitched musical instrument in the brass family. Like all brass instruments, sound is produced by moving air past the lips, causing them to vibrate or 'buzz' into a large cupped mouthpiece. It first appeared in the mid 19th-century, making it one of the newer instruments in the modern orchestra and concert band. The tuba largely replaced the ophicleide.",
]
category_item_image = [
    "https://dk1xgl0d43mu1.cloudfront.net/user_files/esp/product_images/000/020/352/xlarge.png?1453394879",
    "https://s.financesonline.com/uploads/viola.jpg",
    "http://mfas3.s3.amazonaws.com/objects/SC166757.jpg",
    "https://sriveenavani.com/courses/images/sitar.png",
    "http://www.fmicassets.com/Damroot/Zoom/10007/2718030521_gtr_frt_001_rr.png",
    "https://www.nps.gov/blri/learn/historyculture/images/1af28fc7fe044cd9ac5b7510477c0006_1.png",

    "http://4.bp.blogspot.com/-a2eykmgrXUg/Uz7y3bX3A7I/AAAAAAAABJE/LVB5iQI1R6Y/s1600/pakhawaj_fivestar1_gross.jpg",
    "https://i.pinimg.com/originals/54/e7/4c/54e74cabff3ef633517d251126950e77.jpg",
    "http://jamunamusic.com/wp-content/uploads/2012/11/tabla.jpg",
    "https://i.pinimg.com/originals/1e/bb/ef/1ebbef161ae35d6d5c1f98d09c7e3c8c.jpg",
    "http://culturalinfusion.org.au/wp-content/uploads/2016/10/Kanjira-1.jpg",
    "https://capitolmusic.files.wordpress.com/2013/07/xylophone.jpg",

    "https://wonderopolis.org/wp-content/uploads//2014/10/dreamstime_xl_8529471-Custom.jpg",
    "https://www.korg.de/fileadmin/_korg/_produkte/synthesizer/kr_ms20mini/01_MS-20-mini_front_with-Patch.jpg",

    "https://img.banggood.com/thumb/water/2014/chenqiuna/08/SKU180582/SKU180582m2.jpg",
    "http://www.bestsaxophonewebsiteever.com/wp-content/uploads/Yamaha-YTS-82Z-II-700.jpg",
    "http://www.klarinetensaxofoonstage.be/wp-content/uploads/klarinet.jpg",
    "http://www.instrumentoutfitters.com/assets/images/355.jpg",

    "https://upload.wikimedia.org/wikipedia/commons/6/63/French_horn_front.png",
    "http://www.trumpethub.com/wp-content/uploads/2014/09/Yamaha-YTR-2335.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Yamaha_Bass_tuba_YFB-822.tif/lossy-page1-369px-Yamaha_Bass_tuba_YFB-822.tif.jpg",
]

category_item_user = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

print "Adding %d categories:" % len(category_name)
for i in range(len(category_name)):
    category_obj = {'name': category_name[i], 'description': category_description[i], 'image': category_image[i], 'user_id': category_user[i]}
    db.new_category(category_obj)
print "All categories added."

print "Adding %d category items:" % len(category_item_title)
for i in range(len(category_item_title)):
    category_item_obj = {'title': category_item_title[i], 'description': category_item_description[i], 'image': category_item_image[i], 'user_id': category_item_user[i]}
    db.new_category_item(category_item_category_id[i], category_item_obj)
    time.sleep(1)
print "All category items added."
print "Done with DB population"
