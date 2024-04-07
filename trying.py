from PIL import Image
import pygame
import requests
import pygame.image
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import pygame.mixer
from weather import *
from datetime import timedelta, datetime
from buttons import *
import os

# Initialize Screen
WIDTH, HEIGHT = 400, 450
pygame.display.set_caption("TaskTabby")

# Colors
BABY_BLUE = (184, 215, 233)
LIST_BLUE = (135, 206, 250)
SLIGHTLY_DARKER_BLUE = (91, 120, 201)
WHITE = (255, 255, 255)

# Initialize To-Do 
dialog_box = pygame.Surface((240, 230))
dialog_box.fill(LIST_BLUE)

# Check Mark Image
check_mark = pygame.image.load('checkmark.png')
check_mark = pygame.transform.scale(check_mark, (20, 20))
checkmark = pygame.image.load(os.path.join('checkmark.png'))
background_4_timer = pygame.image.load("images/bg_4_timer.png")

# Make Check Boxes
y_coord_box = 30

# Make Rectangles for Text
box1 = box2 = box3 = box4 = box5 = pygame.image.load('text_box.png')
box1 = box2 = box3 = box4 = box5 = pygame.transform.scale(check_mark, (100, 20))
box1 = box2 = box3 = box4 = box5 = pygame.image.load(os.path.join('text_box.png'))

# Generate Check Boxes
def check_box(platform):
    y_coord = 28
    for i in range(5):
        pygame.draw.rect(platform, WHITE, pygame.Rect(20, y_coord, 20, 20), 3)
        y_coord += 40

# Generate Box for Title
def title_page():
    title = pygame.Surface((240, 30))
    title.fill(SLIGHTLY_DARKER_BLUE)
    return title

# Defining the buttons
button1 = pygame.Rect(32, 158, 20, 20)
button2 = pygame.Rect(32, 205, 20, 20)
button3 = pygame.Rect(32, 242, 20, 20)
button4 = pygame.Rect(32, 279, 20, 20)
button5 = pygame.Rect(32, 316, 20, 20)

#for pomodoro timer popup
def withinTimer(seconds):
    if seconds > (59 * 60):
        return seconds - 60
    elif seconds == 0 :
        return seconds + 60
    else:
        return seconds

def main():
    #weather set up
    weather_icons = {
    "Clear": {"day": "images/clear.png", "night": "images/clear night.png"},
    "Clouds": {"day": "images/scattered clouds.png", "night": "images/scattered clouds night.png"},
    "Drizzle": {"day": "images/rain shower.png", "night": "images/rain shower night.png"},
    "Rain": {"day": "images/rain.png", "night": "images/rain night.png"},
    "Thunderstorm": {"day": "images/thunderstorm.png", "night": "images/thunderstorm night.png"},
    "Snow": {"day": "images/snow.png", "night": "images/snow night.png"},
    "Atmosphere": {"day": "images/mist.png", "night": "images/mist night.png"}
    }
    bar = {
        "day": "images/day_bar.png",
        "night": "images/night_bar.png"
    }
    user_input = ""
    settings_icon = pygame.image.load('images/settings.png')
    exit_icon = pygame.image.load('images/exit.png')
    selected = pygame.image.load('images/selected button.png')
    selected_icon = pygame.transform.scale(selected, (15,15))
    empty = pygame.image.load('images/empty button.png')
    insert_city_bar = pygame.image.load('images/input city.png')
    spotify_bar = pygame.image.load('images/background_spotify.png')
    empty_icon = pygame.transform.scale(empty, (15,15))
    city = "Gainesville, Florida, USA"
    unit = "C"
    military_time = False
    military_time_toggle = Button(30, 21, empty_icon)
    settings = False


    #spotify api setup
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='a41b4ebf125a4727b0a6ed4d7c2ebba3',
                                               client_secret='b1253ba5b1a141dba8e93faf2abb8c98',
                                               redirect_uri="http://localhost/",
                                               scope="user-read-currently-playing, user-read-playback-state, user-modify-playback-state"))

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((400, 450))
    run_app = True
    white = (255, 255, 255)
    font = pygame.font.Font('VT323-Regular.ttf', 20) #sets the font for all the text

    #displaying play/pause button
    pauseButton = pygame.image.load('images/pause.png').convert_alpha()
    pauseButton = pygame.transform.scale(pauseButton, (30, 30))
    buttonRect = pauseButton.get_rect()
    buttonRect.center = (330, 410)
    playButton = pygame.image.load('images/play.png').convert_alpha()
    playButton = pygame.transform.scale(playButton, (30, 30))

    #try pausing Spotify immediately
    spotifyWorking = True

    try:
        sp.pause_playback(device_id=None)
        paused = True
    except:
        spotifyWorking = False

    if not spotifyWorking:
        try:
            sp.start_playback(device_id=None, context_uri=None, uris=None, offset=None, position_ms=None)
            sp.pause_playback(device_id=None)
            spotifyWorking = True
            paused = True
        except:
            spotifyWorking = False

    #set all of the initial values for displaying song information
    if spotifyWorking:
        pausedLineState = (sp.current_playback(market=None, additional_types=None))['progress_ms'] / (sp.current_playback(market="US", additional_types=None))['item']['duration_ms']
        pausedLineState = pausedLineState * 300
        songTitle = (sp.current_playback(market=None, additional_types=None))['item']['name']
        currSongTitle = songTitle
        artistText = font.render((sp.current_playback(market=None, additional_types=None))['item']['artists'][0]['name'], True, white, None)
        url = (sp.current_playback(market=None, additional_types=None))['item']['album']['images'][0]['url']
        img = Image.open(requests.get(url, stream=True).raw)
        smallImg = img.resize((40,40))
        mode = smallImg.mode
        size = smallImg.size
        data = smallImg.tobytes()
        py_image = pygame.image.fromstring(data, size, mode)
        albumRect = py_image.get_rect()
        albumRect.center = (60, 410)

    #displaying next button
    nextButton = pygame.image.load('images/arrow.png').convert_alpha()
    nextRect = nextButton.get_rect()
    nextRect.center = (360, 410)

    #displaying previous button
    prevButton = pygame.image.load('images/arrow.png').convert_alpha()
    prevButton = pygame.transform.rotate(prevButton, 180)
    prevRect = prevButton.get_rect()
    prevRect.center = (300, 410)

    #little icon on line
    lineIcon = pygame.image.load('images/icon.png').convert_alpha()
    lineIcon = pygame.transform.scale(lineIcon, (10, 10))
    
    #timer setup
    chimeSound = pygame.mixer.Sound("chime.mp3")
    TpauseButton = pygame.image.load('images/pause.png').convert_alpha()
    TpauseButton = pygame.transform.scale(TpauseButton, (30, 30))
    TbuttonRect = TpauseButton.get_rect()
    TbuttonRect.center = (300, 245)
    TplayButton = pygame.image.load('images/play.png').convert_alpha()
    TplayButton = pygame.transform.scale(TplayButton, (30, 30))
    CLOCK = pygame.time.Clock()
    #default values for pomodoro timers
    POMODORO_LENGTH = 1500 # 1500 secs / 25 mins
    SHORT_BREAK_LENGTH = 300 # 300 secs / 5 mins
    LONG_BREAK_LENGTH = 900 # 900 secs / 15 mins
    current_seconds = POMODORO_LENGTH
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    started = False
    Tfont = pygame.font.Font('VT323-Regular.ttf', 60)
    round = 1

    #timer labels
    pomoTimeText = font.render("Productive Time", True, white, None)
    pomoTimeTextRect = pomoTimeText.get_rect()
    sbTimeText = font.render("Short Break Time", True, white, None)
    sbTimeTextRect = sbTimeText.get_rect()
    lbTimeText = font.render("Long Break Time", True, white, None)
    lbTimeTextRect = pomoTimeText.get_rect()
    timerLabelRect=pomoTimeTextRect
    timerLabelRect.center = (325, 165)

    #timer setting button
    TsettingButton = pygame.image.load('images/timerIcon.png').convert_alpha()
    TsettingButton = pygame.transform.scale(TsettingButton, (30, 30))
    TsettingRect = TsettingButton.get_rect()
    TsettingRect.center = (350, 245)

    image_click = False
    user_input1, user_input2, user_input3, user_input4, user_input5 = "", "", "", "", ""
    button1_state, button2_state, button3_state, button4_state, button5_state, = False, False, False, False, False

    #while loop for displaying everything
    while run_app:
        CLOCK.tick(60)
        #coloring in screen
        screen.fill((184, 215, 233))

        screen.fill(BABY_BLUE)

        # Blit the various screens
        check_box(dialog_box)
        todo_title = title_page()
        screen.blit(dialog_box, (15, 130))
        screen.blit(todo_title, (15, 115))
        AddText(screen, 26, "To-Do List", WHITE, 90, 120)

        # Text Boxes
        screen.blit(box1, (60, 153))
        screen.blit(box2, (60, 193))
        screen.blit(box3, (60, 233))
        screen.blit(box4, (60, 273))
        screen.blit(box5, (60, 313))

        #managing events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_app = False
                sp.pause_playback(device_id=None)
                sys.exit() #added this


            if event.type == pygame.USEREVENT and started:
                    current_seconds -= 1
            #mouse clicked
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                #play button is clicked
                if buttonRect.collidepoint(pos) :
                    if not paused: #was playing
                        sp.pause_playback(device_id=None)
                        paused = True
                        pausedLineState = (sp.current_playback(market=None, additional_types=None))['progress_ms'] / (sp.current_playback(market="US", additional_types=None))['item']['duration_ms']
                        pausedLineState = pausedLineState * 300
                    else : #was paused
                        sp.start_playback(device_id=None, context_uri=None, uris=None, offset=None, position_ms=None)
                        paused = False
                if nextRect.collidepoint(pos) :
                    sp.next_track(device_id=None)
                    paused = False
                if prevRect.collidepoint(pos) :
                    sp.previous_track(device_id=None)
                    paused = False
                if TbuttonRect.collidepoint(pos) :
                    if started:
                        started = False
                    else:
                        started = True


                #

                #updating pomodoro settings
                if TsettingRect.collidepoint(pos) :
                    popup = pygame.display.set_mode((300, 300))
                    popupDisplay = True

                    #buttons setup
                    pUpButton = pygame.image.load('images/arrow.png').convert_alpha()
                    pUpButton = pygame.transform.scale(pUpButton, (30, 30))
                    pUpButton = pygame.transform.rotate(pUpButton, 90)
                    pUpRect = pUpButton.get_rect()
                    pUpRect.center = (75, 75)

                    pDownButton = pygame.image.load('images/arrow.png').convert_alpha()
                    pDownButton = pygame.transform.scale(pDownButton, (30, 30))
                    pDownButton = pygame.transform.rotate(pDownButton, 270)
                    pDownRect = pDownButton.get_rect()
                    pDownRect.center = (225, 75)

                    sbUpButton = pygame.image.load('images/arrow.png').convert_alpha()
                    sbUpButton = pygame.transform.scale(sbUpButton, (30, 30))
                    sbUpButton = pygame.transform.rotate(sbUpButton, 90)
                    sbUpRect = sbUpButton.get_rect()
                    sbUpRect.center = (75, 150)

                    sbDownButton = pygame.image.load('images/arrow.png').convert_alpha()
                    sbDownButton = pygame.transform.scale(sbDownButton, (30, 30))
                    sbDownButton = pygame.transform.rotate(sbDownButton, 270)
                    sbDownRect = sbDownButton.get_rect()
                    sbDownRect.center = (225, 150)

                    lbUpButton = pygame.image.load('images/arrow.png').convert_alpha()
                    lbUpButton = pygame.transform.scale(lbUpButton, (30, 30))
                    lbUpButton = pygame.transform.rotate(lbUpButton, 90)
                    lbUpRect = lbUpButton.get_rect()
                    lbUpRect.center = (75, 225)

                    lbDownButton = pygame.image.load('images/arrow.png').convert_alpha()
                    lbDownButton = pygame.transform.scale(lbDownButton, (30, 30))
                    lbDownButton = pygame.transform.rotate(lbDownButton, 270)
                    lbDownRect = lbDownButton.get_rect()
                    lbDownRect.center = (225, 225)
                    
                    #text label setup
                    pomoTimeTextRect.center = (150, 115)
                    sbTimeTextRect.center = (150, 190)
                    lbTimeTextRect.center = (150, 265)

                    while popupDisplay:
                        popup.fill((184, 215, 233))
                        for event in pygame.event.get():
                            pos = pygame.mouse.get_pos()
                            if event.type == pygame.QUIT:
                                popupDisplay = False

                            if event.type == pygame.MOUSEBUTTONUP :
                                if pUpRect.collidepoint(pos) :
                                    POMODORO_LENGTH = withinTimer(POMODORO_LENGTH + 60)
                                if pDownRect.collidepoint(pos) :
                                    POMODORO_LENGTH = withinTimer(POMODORO_LENGTH - 60)
                                if sbUpRect.collidepoint(pos) :
                                    SHORT_BREAK_LENGTH = withinTimer(SHORT_BREAK_LENGTH + 60)
                                if sbDownRect.collidepoint(pos) :
                                    SHORT_BREAK_LENGTH = withinTimer(SHORT_BREAK_LENGTH - 60)
                                if lbUpRect.collidepoint(pos) :
                                    LONG_BREAK_LENGTH = withinTimer(LONG_BREAK_LENGTH + 60)
                                if lbDownRect.collidepoint(pos) :
                                    LONG_BREAK_LENGTH = withinTimer(LONG_BREAK_LENGTH - 60)

                        #displaying buttons
                        popup.blit(pUpButton, pUpRect)
                        popup.blit(pDownButton, pDownRect)
                        popup.blit(sbUpButton, sbUpRect)
                        popup.blit(sbDownButton, sbDownRect)
                        popup.blit(lbUpButton, lbUpRect)
                        popup.blit(lbDownButton, lbDownRect)

                        #display text labels
                        screen.blit(pomoTimeText, pomoTimeTextRect)
                        screen.blit(sbTimeText, sbTimeTextRect)
                        screen.blit(lbTimeText, lbTimeTextRect)

                        #display times
                        if POMODORO_LENGTH >= 0:
                            display_minutes = int(POMODORO_LENGTH / 60) % 60
                        pomo_text = Tfont.render(f"{display_minutes:02}", True, "white")
                        pomo_text_rect = pomo_text.get_rect()
                        pomo_text_rect.center = (150, 75)
                        screen.blit(pomo_text, pomo_text_rect)
                        if SHORT_BREAK_LENGTH >= 0:
                            display_minutes = int(SHORT_BREAK_LENGTH / 60) % 60
                        sb_text = Tfont.render(f"{display_minutes:02}", True, "white")
                        sb_text_rect = pomo_text.get_rect()
                        sb_text_rect.center = (150, 150)
                        screen.blit(sb_text, sb_text_rect)
                        if LONG_BREAK_LENGTH >= 0:
                            display_minutes = int(LONG_BREAK_LENGTH / 60) % 60
                        lb_text = Tfont.render(f"{display_minutes:02}", True, "white")
                        lb_text_rect = lb_text.get_rect()
                        lb_text_rect.center = (150, 225)
                        screen.blit(lb_text, lb_text_rect)
                        
                        pygame.display.flip()

                    #display original screen again
                    screen = pygame.display.set_mode((400, 450))
                    current_seconds = POMODORO_LENGTH
                    screen.fill((184, 215, 233))
                    timerLabelRect=pomoTimeTextRect
                    timerLabelRect.center = (325, 165)
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_BACKSPACE): 
                    if(settings and bar_.get_rect().collidepoint(pygame.mouse.get_pos())): user_input = user_input[:-1] #deleting for city input
                elif (event.key >= pygame.K_a and event.key <= pygame.K_z) or pygame.K_COMMA:
                    if(settings and bar_.get_rect().collidepoint(pygame.mouse.get_pos())): #adding for city
                        user_input += event.unicode
            
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_BACKSPACE):
                    if(box1.get_rect(center=(110, 163)).collidepoint(pygame.mouse.get_pos())): user_input1 = user_input1[:-1]
                elif (event.key >= pygame.K_a and event.key <= pygame.K_z) or pygame.K_COMMA:
                    if(box1.get_rect(center=(110, 163)).collidepoint(pygame.mouse.get_pos())):
                        user_input1 += event.unicode


            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_BACKSPACE):
                    if(box2.get_rect(center=(125, 203)).collidepoint(pygame.mouse.get_pos())): user_input2 = user_input2[:-1]
                elif (event.key >= pygame.K_a and event.key <= pygame.K_z) or pygame.K_COMMA:
                    if(box2.get_rect(center=(125, 203)).collidepoint(pygame.mouse.get_pos())):
                        user_input2 += event.unicode

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_BACKSPACE):
                    if(box3.get_rect(center=(125, 243)).collidepoint(pygame.mouse.get_pos())): user_input3 = user_input3[:-1]
                elif (event.key >= pygame.K_a and event.key <= pygame.K_z) or pygame.K_COMMA:
                    if(box3.get_rect(center=(125, 243)).collidepoint(pygame.mouse.get_pos())):
                        user_input3 += event.unicode

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_BACKSPACE):
                    if(box4.get_rect(center=(125, 283)).collidepoint(pygame.mouse.get_pos())): user_input4 = user_input4[:-1]
                elif (event.key >= pygame.K_a and event.key <= pygame.K_z) or pygame.K_COMMA:
                    if(box4.get_rect(center=(125, 283)).collidepoint(pygame.mouse.get_pos())):
                        user_input4 += event.unicode

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_BACKSPACE):
                    if(box5.get_rect(center=(125, 323)).collidepoint(pygame.mouse.get_pos())): user_input5 = user_input5[:-1]
                elif (event.key >= pygame.K_a and event.key <= pygame.K_z) or pygame.K_COMMA:
                    if(box5.get_rect(center=(125, 323)).collidepoint(pygame.mouse.get_pos())):
                        user_input5 += event.unicode
            pos = pygame.mouse.get_pos()
            
        if button1.collidepoint(pos) or button2.collidepoint(pos) or button3.collidepoint(pos) or button4.collidepoint(pos) or button5.collidepoint(pos):
            if button1.collidepoint(pos):
                screen.blit(check_mark, (38, 155))
            if button2.collidepoint(pos):
                screen.blit(check_mark, (38, 195))
            if button3.collidepoint(pos):
                screen.blit(check_mark, (38, 235))
            if button4.collidepoint(pos):
                screen.blit(check_mark, (38, 275))
            if button5.collidepoint(pos):
                screen.blit(check_mark, (38, 315))

            # Disappearing and Reappearing for Checkmarks.
            # As well as selecting and deselecting.
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if button1.collidepoint(click) or button2.collidepoint(click) or button3.collidepoint(click) or button4.collidepoint(click) or button5.collidepoint(pos):
                    image_click = True
                    # Houses the Checkmark Functionality
            
            if image_click:
                image_click = False
                if button1.collidepoint(click):
                    screen.blit(check_mark, (38, 155))
                    button1_state = not button1_state
                if button2.collidepoint(click):
                    screen.blit(check_mark, (38, 195))
                    button2_state = not button2_state
                if button3.collidepoint(click):
                    screen.blit(check_mark, (38, 235))
                    button3_state = not button3_state
                if button4.collidepoint(click):
                    screen.blit(check_mark, (38, 275))
                    button4_state = not button4_state
                if button5.collidepoint(click):
                    screen.blit(check_mark, (38, 315))
                    button5_state = not button5_state

        if button1_state:
            screen.blit(check_mark, (38, 155))
        if button2_state:
            screen.blit(check_mark, (38, 195))
        if button3_state:
            screen.blit(check_mark, (38, 235))
        if button4_state:
            screen.blit(check_mark, (38, 275))
        if button5_state:
            screen.blit(check_mark, (38, 315))

        user_input1 = user_input1[:14]
        user_input2 = user_input2[:14]
        user_input3 = user_input3[:14]
        user_input4 = user_input4[:14]
        user_input5 = user_input5[:14]
        AddText(screen, 20, user_input1, (0,0,0), 70, 160)
        AddText(screen, 20, user_input5, (0,0,0), 70, 320)
        AddText(screen, 20, user_input3, (0,0,0), 70, 240)
        AddText(screen, 20, user_input4, (0,0,0), 70, 280)
        AddText(screen, 20, user_input2, (0,0,0), 70, 200)
        screen.blit(background_4_timer, (260,148))
        screen.blit(spotify_bar, (0,380))
        if spotifyWorking:
            #displaying lines
            pygame.draw.line(screen, (157, 163, 245), 
                    [50, 440], 
                    [350, 440], 5)
            if paused:
                pygame.draw.line(screen, (86, 94, 204), 
                        [50, 440], 
                        [pausedLineState + 50, 440], 5)
                screen.blit(lineIcon, (pausedLineState + 50, 435))
            if not paused:
                songProgress = (sp.current_playback(market=None, additional_types=None))['progress_ms'] / (sp.current_playback(market="US", additional_types=None))['item']['duration_ms']
                songProgress = songProgress * 300
                pygame.draw.line(screen, (86, 94, 204), 
                        [50, 440], 
                        [songProgress + 50, 440], 5)
        
                #displaying icon on line
                screen.blit(lineIcon, (songProgress + 50, 435))

                if songProgress < 15 :
                    songTitle = (sp.current_playback(market=None, additional_types=None))['item']['name']
                    if not currSongTitle == songTitle : # song changed
                        #displaying song title
                        currSongTitle = songTitle

                        #displaying artist name
                        artistText = font.render((sp.current_playback(market=None, additional_types=None))['item']['artists'][0]['name'], True, white, None)

                        #displaying album cover image
                        url = (sp.current_playback(market=None, additional_types=None))['item']['album']['images'][0]['url']
                        img = Image.open(requests.get(url, stream=True).raw)
                        smallImg = img.resize((40,40))
                        mode = smallImg.mode
                        size = smallImg.size
                        data = smallImg.tobytes()
                        py_image = pygame.image.fromstring(data, size, mode)
                        albumRect = py_image.get_rect()
                        albumRect.center = (60, 410)

            #display song info
            if len(songTitle) > 17 :
                songTitle = songTitle[:17] + "..."
            songText = font.render(songTitle, True, white, None)
            songTextRect = songText.get_rect()
            songTextRect.center = (200, 400)
            artistTextRect = artistText.get_rect()
            artistTextRect.center = (200, 420)
            screen.blit(songText, songTextRect)
            screen.blit(py_image, albumRect)
            screen.blit(artistText, artistTextRect)

            #displaying buttons
            if paused :
                screen.blit(playButton, buttonRect)
            elif not paused :
                screen.blit(pauseButton, buttonRect)
            screen.blit(prevButton, prevRect)
            screen.blit(nextButton, nextRect)

        #displaying timer
        if started :
                screen.blit(TpauseButton, TbuttonRect)
        elif not started :
                screen.blit(TplayButton, TbuttonRect)
        if current_seconds > 0:
            display_seconds = current_seconds % 60
            display_minutes = int(current_seconds / 60) % 60
        if current_seconds <= 0:
            pygame.mixer.Sound.play(chimeSound)
            if round % 6 == 0:
                current_seconds = LONG_BREAK_LENGTH
                round += 1
            elif round % 2 == 0:
                current_seconds = SHORT_BREAK_LENGTH
                round += 1
            elif round % 2 == 1:
                current_seconds = POMODORO_LENGTH
                round += 1
        timer_text = Tfont.render(f"{display_minutes:02}:{display_seconds:02}", True, "white")
        timer_text_rect = timer_text.get_rect()
        timer_text_rect.center = (325, 200)
        
        screen.blit(timer_text, timer_text_rect)
        screen.blit(TsettingButton, TsettingRect)
        if round % 6 == 0:
            screen.blit(lbTimeText, timerLabelRect)
        elif round % 2 == 0:
            screen.blit(sbTimeText, timerLabelRect)
        elif round % 2 == 1:
            screen.blit(pomoTimeText, timerLabelRect)
        
        if not spotifyWorking:
            Font = pygame.font.Font('VT323-Regular.ttf', 30)
            text = Font.render("- Spotify is not connected :( -", True, white)
            screen.blit(text, (15, 400))

        if(not settings):
    #do weather determinations
            weather_data = get_weather(city, unit)
            weather_condition = weather_data[1]
            weather_description = weather_data[2]
            temp = str(weather_data[0]) + unit

            #time determinations
            time_determinations = get_time(city)
            day_or_night = time_determinations[1]
            
            sunrise_time = time_determinations[0][0]
            sunset_time = time_determinations[0][1]
            local_time = time_determinations[0][2]
            local_time_for_non_military = time_determinations[0][2]

            if not military_time:
                if(local_time.hour > 12):
                    subtract_12 = timedelta(hours=-12)
                    local_time = local_time + subtract_12
                    sunset_time = sunset_time + subtract_12
                elif(local_time.hour == 0):
                    add_12 = timedelta(hours=12)
                    local_time = local_time + add_12
                    sunrise_time = sunrise_time + add_12

            weather_picture = (weather_icons.get(weather_condition, {}).get(day_or_night))
            weather = pygame.image.load(weather_picture).convert_alpha()
            bar_path = bar.get(day_or_night)
            bar_ = pygame.image.load(bar_path).convert_alpha()
            settings_bar = pygame.image.load(bar_path).convert_alpha()
        
            if(day_or_night == "day"):
                weather_color = (0,0,0)
            else:
                weather_color = (255,255,255)

            if(not military_time):
                if(00 <= local_time_for_non_military.hour < 12):
                    time_thing = "AM"
                else:
                    time_thing = "PM"
            

            if( day_or_night == "day"):
                sun = sunset_time.strftime("%H:%M")
                sun_pic = pygame.image.load('images/sunset.png').convert_alpha()
            else:
                sun = sunrise_time.strftime("%H:%M")
                sun_pic = pygame.image.load('images/sunrise.png').convert_alpha()

            #Images
            screen.blit(bar_,(25,10))
            screen.blit(weather, (30,20))
            screen.blit(sun_pic, (135, 85))
            
            # Text
            AddText(screen, 20, sun, weather_color, 145, 87)
            if(not military_time): AddText(screen, 18, time_thing, weather_color, 360, 50)
            AddText(screen, 25, local_time.strftime("%Y-%m-%d"),weather_color, 260, 78)
            AddText(screen, 30, local_time.strftime("%H:%M"), weather_color, 296, 50)
            AddText(screen, 45, temp, weather_color, 135, 25)
            AddText(screen, 18, weather_description, weather_color, 135, 60)
        
            setting_button = Button(353, 10, settings_icon)
            

            if setting_button.draw(screen):
                settings = True
        
        if settings:
            screen.blit(settings_bar, (25,10))
            exit_button = Button(353, 85, exit_icon)
            if exit_button.draw(screen):
                settings = False
                if(user_input!= ""):city = user_input
                else: city = city
          
            if(unit == "F"): coordinates_for_paw = (30, 42)
            elif(unit == "C"): coordinates_for_paw = (30, 60)
            elif(unit == "K"): coordinates_for_paw = (30, 78)

            far_button = Button(30, 42, empty_icon)
            celcius_button = Button(30, 60, empty_icon)
            kelvin_button = Button(30, 78, empty_icon)

            screen.blit(empty_icon, (30, 21))

            if far_button.draw(screen) and settings:
                unit = "F"
            elif celcius_button.draw(screen) and settings:
                unit = "C"
            elif kelvin_button.draw(screen) and settings:
                unit = "K"

            if military_time_toggle.draw(screen) and settings:
                if(military_time):
                    military_time = False
                else:
                    military_time = True
            
            screen.blit(empty_icon, (30, 42))
            AddText(screen, 18, "Fahrenheit", weather_color, 50, 42)
            screen.blit(empty_icon, (30, 60))
            AddText(screen, 18, "Celcius", weather_color, 50, 60)
            screen.blit(empty_icon, (30, 78))
            AddText(screen, 18, "Kelvin", weather_color, 50, 78)
            screen.blit(selected_icon, coordinates_for_paw)
            if(military_time): screen.blit(selected_icon, (30,21))
            AddText(screen, 18, "Military Time", weather_color, 50, 21)

            screen.blit(insert_city_bar, (140, 78))
            AddText(screen, 20, user_input,(0,0,0), 140, 78)
            AddText(screen, 20, "Change City :P", weather_color, 140, 55)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()