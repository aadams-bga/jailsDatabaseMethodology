import pdfplumber
import pandas as pd
import os

year = '2025'

# @title
checkresponses = {'gen1': '', 'gen2': '', 'gen3': '', 'admin1': '', 'admin1a': '',
                  'admin1b': '', 'admin2': '', 'admin3': '', 'admin4': '', 'admin5': '',
                  'admin6': '', 'admin7': '', 'admin8': '', 'admin9': '', 'admin10': '',
                  'personnel1': '', 'personnel2': '', 'personnel3': '', 'personnel4': '',
                  'personnel5': '', 'personnel6': '', 'personnel7': '', 'personnel8': '',
                  'personnel9': '', 'records1': '', 'records2': '', 'records3': '',
                  'adminproc1': '', 'adminproc2': '', 'adminproc3': '', 'adminproc4': '',
                  'adminproc5': '', 'adminproc6': '', 'adminproc7': '', 'adminproc7a': '',
                  'adminproc7b': '', 'adminproc7c': '', 'adminproc8': '', 'adminproc8a': '',
                  'adminproc8b': '', 'adminproc9': '', 'adminproc10': '', 'adminproc10a': '',
                  'adminproc11': '', 'adminproc11a': '', 'adminproc11b': '',
                  'adminproc12': '', 'adminproc12a': '', 'adminproc13': '', 'adminproc14': '',
                  'adminproc14a': '', 'adminproc14b': '', 'adminproc14c': '',
                  'adminproc14d': '', 'adminproc15': '', 'adminproc16': '', 'adminproc17': '',
                  'adminproc18': '', 'adminproc19': '', 'adminproc20': '', 'adminproc21': '',
                  'adminproc21a': '', 'adminproc22': '', 'adminproc22a1': '', 'adminproc22a2': '',
                  'adminproc22a3': '', 'adminproc23': '', 'adminproc24': '', 'adminproc25': '',
                  'adminproc26': '', 'adminproc27': '', 'adminproc28': '', 'adminproc29': '',
                  'adminproc30': '', 'adminproc31': '', 'adminproc32': '', 'adminproc32a': '',
                  'adminproc32b': '', 'adminproc32c': '', 'adminproc32d': '', 'adminproc32d': '',
                  'adminproc33': '', 'adminproc34': '', 'adminproc35': '', 'orientation1': '',
                  'orientation2': '', 'orientation3': '', 'releaseproc1': '', 'releaseproc2': '',
                  'releaseproc3': '', 'releaseproc4': '', 'releaseproc5': '', 'releaseproc6': '',
                  'releaseproc7': '', 'releaseproc8': '', 'releaseproc9_dismentill': '',
                  'releaseproc10_dismentill': '', 'releaseproc11_dismentill': '', 'classsep1': '',
                  'classsep2a': '', 'classsep2b': '', 'classsep2c': '', 'classsep2d': '',
                  'classsep2e': '', 'classsep2f': '', 'classsep2g': '', 'classsep3': '',
                  'housing1': '', 'housing2': '', 'housing3': '', 'housing4a': '', 'housing4b': '',
                  'housing4c': '', 'housing4d': '', 'housing4e': '', 'housing4f': '', 'housing5': '',
                  'housing6a': '', 'housing6b': '', 'housing6c': '', 'housing6d': '',
                  'housing6e': '', 'housing6f': '', 'housing6g': '', 'housing7': '', 'housing8': '',
                  'housing8a': '', 'housing8b': '', 'housing8c': '', 'housing9': '', 'housing10': '',
                  'housing11': '', 'med1': '', 'med2': '', 'med3': '', 'med4': '', 'med5': '',
                  'med6a': '', 'med6b': '', 'med6c': '', 'med6d': '', 'med6e': '', 'med6f': '',
                  'med6g': '', 'med6h': '', 'med6i': '', 'med7a': '', 'med7b': '', 'med7c': '',
                  'med7d': '', 'med7e': '', 'med7f': '', 'med7g': '', 'med7h': '', 'med7i': '',
                  'med8': '', 'med10': '', 'med11': '', 'med12': '', 'med12a': '', 'med12b': '',
                  'med12c': '', 'med13': '', 'med13a': '', 'med13b': '', 'med14': '', 'med15': '',
                  'med16': '', 'med17': '', 'med18': '', 'med19': '', 'med20': '', 'med21': '',
                  'med21a': '', 'med21b': '', 'med21c': '', 'med21d': '', 'med21e': '', 'med21f': '',
                  'med21g': '', 'cloth1': '', 'cloth2': '', 'cloth3': '', 'cloth4': '', 'cloth5': '',
                  'cloth6': '', 'cloth7': '', 'cloth8': '', 'food1': '', 'food2': '', 'food3': '',
                  'food4': '', 'food5': '', 'food6': '', 'food7': '', 'food8': '', 'food9': '',
                  'food9a': '', 'food9b': '', 'food10': '', 'food10a': '', 'food10b': '',
                  'food11': '', 'food12': '', 'food13': '', 'food14': '', 'food15': '',
                  'food16': '', 'food17': '', 'food18': '', 'food19': '', 'food20': '',
                  'food21': '', 'food22a': '', 'food22b': '', 'food23': '', 'food24': '',
                  'food25': '', 'san1': '', 'san2': '', 'san3': '', 'san4': '', 'san5': '',
                  'san6': '', 'san7': '', 'san8': '', 'san9': '', 'san10': '', 'san11': '',
                  'san12': '', 'san13': '', 'san14': '', 'san15': '', 'san16': '',
                  'san17': '', 'san18': '', 'san19': '', 'san20': '', 'san21': '',
                  'san22': '', 'san23': '', 'san24': '', 'san25': '', 'san26': '',
                  'san27': '', 'san28': '', 'supervision1': '', 'supervision2': '',
                  'supervision3': '', 'supervision4': '', 'supervision5': '', 'supervision6': '',
                  'supervision7': '', 'supervision8': '', 'sec1': '', 'sec2': '',
                  'sec3': '', 'sec4': '', 'sec5': '', 'sec6': '', 'sec7': '', 'sec8': '',
                  'sec9': '', 'sec10': '', 'sec11': '', 'sec12': '', 'sec13': '',
                  'sec14': '', 'sec15': '', 'sec16': '', 'sec17': '', 'sec18': '',
                  'sec19': '', 'sec20': '', 'sec21': '', 'sec21a': '', 'sec21b': '',
                  'sec21c': '', 'sec22': '', 'sec22a': '', 'sec22b': '', 'sec23': '',
                  'sec23a': '', 'sec23b': '', 'sec23c': '', 'sec24': '', 'safety1': '',
                  'safety2': '', 'safety3': '', 'safety4': '', 'safety5': '', 'safety6': '',
                  'safety7': '', 'safety8': '', 'safety9': '', 'safety10': '', 'safety11': '',
                  'safety12': '', 'discipline1a': '', 'discipline1b': '', 'discipline1c': '',
                  'discipline1d': '', 'discipline1e': '', 'discipline1f': '', 'discipline2': '',
                  'discipline3': '', 'discipline4': '', 'discipline5': '', 'discipline6': '',
                  'discipline6a': '', 'discipline6b': '', 'discipline7': '', 'discipline8': '',
                  'discipline8a': '', 'discipline8b': '', 'discipline9': '', 'discipline10a': '',
                  'discipline10b': '', 'discipline11': '', 'discipline12': '',
                  'discipline13': '', 'discipline14a': '', 'discipline14b': '',
                  'discipline14c': '', 'discipline15': '', 'discipline16': '',
                  'discipline17': '', 'discipline18': '', 'discipline19': '', 'discipline20': '',
                  'emp1': '', 'emp2': '', 'emp3': '', 'emp4': '', 'mail1': '', 'mail2': '',
                  'mail3': '', 'mail4': '', 'mail5': '', 'mail5a': '', 'mail5b': '',
                  'mail6': '', 'mail6a': '', 'mail7': '', 'mail8': '', 'mail9': '',
                  'mail10': '', 'mail11': '', 'mail12': '', 'mail13': '', 'mail14': '',
                  'mail15': '', 'mail16': '', 'mail17': '', 'mail18': '', 'mail19': '',
                  'mail20': '', 'mail21': '', 'mail22a': '', 'mail22b': '', 'mail22c': '',
                  'mail22d': '', 'mail22e': '', 'tele1': '', 'tele2': '', 'tele2a': '',
                  'tele2b': '', 'tele3': '', 'tele4': '', 'visit1': '', 'visit2': '',
                  'visit3': '', 'visit4': '', 'visit5': '', 'visit6': '', 'visit7': '',
                  'visit8': '', 'visit9': '', 'visit10': '', 'visit11': '', 'visit12': '',
                  'socserv1': '', 'socserv2': '', 'ed1': '', 'ed2': '', 'ed3': '',
                  'lib1': '', 'lib1a': '', 'lib1b': '', 'lib2': '', 'lib3': '',
                  'rel1': '', 'rel2': '', 'commissary1': '', 'commissary2': '',
                  'commissary3': '', 'commissary4': '', 'commissary5': '', 'commissary6': '',
                  'commissary7': '', 'commissary8': '', 'recleis1': '', 'recleis2': '',
                  'recleis3': '', 'recleis4': '', 'recleis5': '', 'juvedet1': '',
                  'juvedet2': '', 'juvedet3': '', 'juvedet4': '', 'juvedet4a': '',
                  'juvedet4b': '', 'juvedet5': '', 'juvedet6': '', 'juvedet7': '',
                  'juvedet8': '', 'juvedet9': '', 'juvedet10a': '', 'juvedet10b': '',
                  'juvedet11': '', 'juvedet11a': '', 'juvedet11b': '', 'juvedet11c': '',
                  'juvedet11d': '', 'juvedet11e': '', 'juvedet11f': '', 'juvedet11g': '',
                  'juvedet12': '', 'juvedet13': '', 'juvedet14': '', 'juvedet15': '',
                  'tempdet1': '', 'tempdet2': '', 'tempdet2a': '', 'tempdet2b': '',
                  'tempdet2c': '', 'tempdet3': '', 'tempdet4': '', 'tempdet5': '',
                  'tempdet5a': '', 'tempdet5b': '', 'tempdet6': '', 'tempdet7': '',
                  'tempdet7a': '', 'tempdet7b': '', 'tempdet8': '', 'tempdet9': '',
                  'tempdet9a': '', 'tempdet9b': '', 'tempdet9c': '', 'tempdet9d': '',
                  'tempdet10': '', 'tempdet10a': '', 'tempdet10b': '', 'youth1': '',
                  'youth2': '', 'youth3': '', 'youth3a': '', 'youth3b': '', 'youth4': '',
                  'youth5': '', 'youth6': '', 'youth6a': '', 'youth6b': '', 'youth6c': '',
                  'youth7': '', 'youth8': '', 'youth8a': '', 'youth8b': '', 'youth8c': '',
                  'youth9': '', 'filename': ''}

checkbbox = {'gen1': (420,70,612,95), 'gen2': (420,105,612,125), 'gen3': (420,150,612,170),
             'admin1': (420,200,612,230), 'admin1a': (420,230,612,250), 'admin1b': (420,250,612,270),
             'admin2': (420,275,612,300), 'admin3': (420,320,612,350), 'admin4': (420,350,612,370),
             'admin5': (420,390,612,410), 'admin6': (420,410,612,430), 'admin7': (420,440,612,450),
             'admin8': (420,480,612,510), 'admin9': (420,530,612,550), 'admin10': (420,580,612,600),
             'personnel1': (420,630,612,650), 'personnel2': (420,660,612,680),
             'personnel3': (420,690,612,710), 'personnel4': (420,70,612,90), 'personnel5': (420,100,612,130),
             'personnel6': (420,150,612,170), 'personnel7': (420,190,612,210), 'personnel8': (420,220,612,250),
             'personnel9': (420,250,612,280), 'records1': (420,300,612,320), 'records2': (420,330,612,350),
             'records3': (420,360,612,375), 'adminproc1': (420,410,612,430), 'adminproc2': (420,430,612,450),
             'adminproc3': (420,450,612,480), 'adminproc4': (420,480,612,510), 'adminproc5': (420,520,612,540),
             'adminproc6': (420,560,612,590), 'adminproc7': (420,590,612,610), 'adminproc7a': (420,610,612,630),
             'adminproc7b': (420,630,612,650), 'adminproc7c': (420,650,612,670),
             'adminproc8': (420,690,612,710), 'adminproc8a': (420,60,612,80), 'adminproc8b': (420,90,612,110),
             'adminproc9': (420,140,612,160), 'adminproc10': (420,170,612,200),
             'adminproc10a': (420,200,612,220), 'adminproc11': (420,220,612,250),
             'adminproc11a': (420,270,612,290), 'adminproc11b': (420,300,612,320),
             'adminproc12': (420,330,612,360), 'adminproc12a': (420,370,612,390),
             'adminproc13': (420,400,612,420), 'adminproc14': (420,430,612,450),
             'adminproc14a': (420,480,612,500), 'adminproc14b': (420,530,612,550),
             'adminproc14c': (420,560,612,580), 'adminproc14d': (420,590,612,610),
             'adminproc15': (420,650,612,670), 'adminproc16': (420,690,612,720),
             'adminproc17': (420,80,612,100), 'adminproc18': (420,110,612,130),
             'adminproc19': (420,170,612,190), 'adminproc20': (420,230,612,250),
             'adminproc21': (420,260,612,290), 'adminproc21a': (420,290,612,310),
             'adminproc22': (420,310,612,330), 'adminproc22a1': (420,370,612,390),
             'adminproc22a2': (420,390,612,410), 'adminproc22a3': (420,410,612,430),
             'adminproc23': (420,440,612,460), 'adminproc24': (420,470,612,490),
             'adminproc25': (420,500,612,520), 'adminproc26': (420,530,612,550),
             'adminproc27': (420,560,612,580), 'adminproc28': (420,590,612,610),
             'adminproc29': (420,610,612,630), 'adminproc30': (420,630,612,650),
             'adminproc31': (420,650,612,670), 'adminproc32': (420,690,612,710),
             'adminproc32a': (420,60,612,70), 'adminproc32b': (420,80,612,100),
             'adminproc32c': (420,100,612,120), 'adminproc32d': (420,120,612,140),
             'adminproc33': (420,150,612,170), 'adminproc34': (420,170,612,190),
             'adminproc35': (420,200,612,220), 'orientation1': (420,240,612,260),
             'orientation2': (420,260,612,280), 'orientation3': (420,280,612,300),
             'releaseproc1': (420,340,612,360), 'releaseproc2': (420,360,612,380),
             'releaseproc3': (420,400,612,420), 'releaseproc4': (420,420,612,440),
             'releaseproc5': (420,450,612,470), 'releaseproc6': (420,480,612,500),
             'releaseproc7': (420,510,612,530), 'releaseproc8': (420,550,612,570),
             'releaseproc9_dismentill': (420,610,612,630), 'releaseproc10_dismentill': (420,640,612,660),
             'releaseproc11_dismentill': (420,690,612,710), 'classsep1': (420,80,612,110),
             'classsep2a': (420,140,612,160), 'classsep2b': (420,160,612,180), 'classsep2c': (420,200,612,220),
             'classsep2d': (420,220,612,240), 'classsep2e': (420,260,612,280), 'classsep2f': (420,310,612,330),
             'classsep2g': (420,350,612,370), 'classsep3': (420,380,612,400), 'housing1': (420,460,612,480),
             'housing2': (420,490,612,510), 'housing3': (420,530,612,550), 'housing4a': (420,590,612,610),
             'housing4b': (420,620,612,640), 'housing4c': (420,640,612,660), 'housing4d': (420,660,612,680),
             'housing4e': (420,690,612,710), 'housing4f': (420,60,612,80), 'housing5': (420,90,612,110),
             'housing6a': (420,150,612,170), 'housing6b': (420,170,612,190), 'housing6c': (420,200,612,220),
             'housing6d': (420,220,612,240), 'housing6e': (420,240,612,260), 'housing6f': (420,260,612,280),
             'housing6g': (420,290,612,310), 'housing7': (420,320,612,340), 'housing8': (420,360,612,380),
             'housing8a': (420,400,612,420), 'housing8b': (420,470,612,490), 'housing8c': (420,510,612,530),
             'housing9': (420,530,612,550), 'housing10': (420,550,612,580), 'housing11': (420,590,612,610),
             'med1': (420,650,612,670), 'med2': (420,680,612,700), 'med3': (420,80,612,100),
             'med4': (420,110,612,140), 'med5': (420,160,612,180), 'med6a': (420,200,612,220),
             'med6b': (420,240,612,260), 'med6c': (420,260,612,280), 'med6d': (420,280,612,300),
             'med6e': (420,310,612,330), 'med6f': (420,330,612,350), 'med6g': (420,360,612,380),
             'med6h': (420,380,612,400), 'med6i': (420,400,612,420), 'med7a': (420,450,612,470),
             'med7b': (420,470,612,490), 'med7c': (420,510,612,530), 'med7d': (420,530,612,550),
             'med7e': (420,550,612,570), 'med7f': (420,570,612,590), 'med7g': (420,590,612,610),
             'med7h': (420,620,612,640), 'med7i': (420,620,612,660), 'med8': (420,680,612,700),
             'med10': (420,130,612,150), 'med11': (420,180,612,200), 'med12': (420,210,612,230),
             'med12a': (420,240,612,260), 'med12b': (420,280,612,300), 'med12c': (420,310,612,330),
             'med13': (420,330,612,350), 'med13a': (420,360,612,380), 'med13b': (420,390,612,410),
             'med14': (420,410,612,430), 'med15': (420,440,612,460), 'med16': (420,480,612,510),
             'med17': (420,540,612,560), 'med18': (420,570,612,600), 'med19': (420,630,612,650),
             'med20': (420,650,612,670), 'med21': (420,680,612,700), 'med21a': (420,700,612,720),
             'med21b': (420,60,612,80), 'med21c': (420,80,612,100), 'med21d': (420,100,612,120),
             'med21e': (420,120,612,140), 'med21f': (420,150,612,170), 'med21g': (420,170,612,190),
             'cloth1': (420,240,612,260), 'cloth2': (420,270,612,290), 'cloth3': (420,310,612,330),
             'cloth4': (420,30,612,350), 'cloth5': (420,350,612,370), 'cloth6': (420,390,612,410),
             'cloth7': (420,410,612,430), 'cloth8': (420,430,612,450), 'food1': (420,680,612,700),
             'food2': (420,700,612,720), 'food3': (420,60,612,70), 'food4': (420,80,612,100),
             'food5': (420,10,612,120), 'food6': (420,120,612,140), 'food7': (420,180,612,200),
             'food8': (420,230,612,250), 'food9': (420,260,612,290), 'food9a': (420,290,612,310),
             'food9b': (420,310,612,330), 'food10': (420,330,612,350), 'food10a': (420,350,612,370),
             'food10b': (420,380,612,400), 'food11': (420,380,612,420), 'food12': (420,420,612,440),
             'food13': (420,480,612,500), 'food14': (420,520,612,540), 'food15': (420,550,612,570),
             'food16': (420,590,612,610), 'food17': (420,620,612,640), 'food18': (420,640,612,660),
             'food19': (420,680,612,700), 'food20': (420,710,612,730), 'food21': (420,60,612,90),
             'food22a': (420,110,612,130), 'food22b': (420,130,612,150), 'food23': (420,160,612,180),
             'food24': (420,180,612,200), 'food25': (420,200,612,220), 'san1': (420,260,612,290),
             'san2': (420,300,612,320), 'san3': (420,320,612,340), 'san4': (420,360,612,380),
             'san5': (420,390,612,410), 'san6': (420,410,612,430), 'san7': (420,430,612,450),
             'san8': (420,470,612,490), 'san9': (420,490,612,510), 'san10': (420,510,612,530),
             'san11': (420,540,612,560), 'san12': (420,560,612,580), 'san13': (420,600,612,620),
             'san14': (420,630,612,650), 'san15': (420,670,612,690), 'san16': (420,690,612,710),
             'san17': (420,60,612,90), 'san18': (420,90,612,110), 'san19': (420,110,612,130),
             'san20': (420,150,612,170), 'san21': (420,180,612,210), 'san22': (420,220,612,240),
             'san23': (420,240,612,260), 'san24': (420,260,612,280), 'san25': (420,280,612,300),
             'san26': (420,310,612,330), 'san27': (420,340,612,360), 'san28': (420,360,612,380),
             'supervision1': (420,410,612,430), 'supervision2': (420,430,612,450),
             'supervision3': (420,470,612,490), 'supervision4': (420,510,612,530),
             'supervision5': (420,540,612,560), 'supervision6': (420,570,612,590),
             'supervision7': (420,590,612,610), 'supervision8': (420,630,612,650),
             'sec1': (420,720,612,740), 'sec2': (420,70,612,90), 'sec3': (420,90,612,110),
             'sec4': (420,120,612,140), 'sec5': (420,150,612,170), 'sec6': (420,150,612,190),
             'sec7': (420,190,612,210), 'sec8': (420,220,612,240), 'sec9': (420,240,612,260),
             'sec10': (420,260,612,280), 'sec11': (420,300,612,320), 'sec12': (420,340,612,360),
             'sec13': (420,360,612,380), 'sec14': (420,400,612,420), 'sec15': (420,480,612,500),
             'sec16': (420,480,612,520), 'sec17': (420,520,612,540), 'sec18': (420,540,612,560),
             'sec19': (420,570,612,590), 'sec20': (420,590,612,610), 'sec21': (420,610,612,630),
             'sec21a': (420,640,612,660), 'sec21b': (420,680,612,700), 'sec21c': (420,720,612,740),
             'sec22': (420,60,612,80), 'sec22a': (420,90,612,110), 'sec22b': (420,130,612,150),
             'sec23': (420,160,612,180), 'sec23a': (420,180,612,200), 'sec23b': (420,200,612,220),
             'sec23c': (420,250,612,270), 'sec24': (420,250,612,290), 'safety1': (420,380,612,400),
             'safety2': (420,420,612,440), 'safety3': (420,440,612,460), 'safety4': (420,480,612,500),
             'safety5': (420,510,612,530), 'safety6': (420,530,612,550), 'safety7': (420,550,612,570),
             'safety8': (420,590,612,610), 'safety9': (420,610,612,630), 'safety10': (420,630,612,650),
             'safety11': (420,670,612,690), 'safety12': (420,690,612,710), 'discipline1a': (420,100,612,120),
             'discipline1b': (420,120,612,140), 'discipline1c': (420,160,612,180),
             'discipline1d': (420,180,612,200), 'discipline1e': (420,200,612,220),
             'discipline1f': (420,240,612,260), 'discipline2': (420,260,612,280),
             'discipline3': (420,300,612,320), 'discipline4': (420,330,612,350),
             'discipline5': (420,350,612,370), 'discipline6': (420,390,612,410),
             'discipline6a': (420,430,612,450), 'discipline6b': (420,450,612,470),
             'discipline7': (420,480,612,500), 'discipline8': (420,520,612,540),
             'discipline8a': (420,540,612,560), 'discipline8b': (420,560,612,580),
             'discipline9': (420,600,612,620), 'discipline10a': (420,660,612,680),
             'discipline10b': (420,690,612,710), 'discipline11': (420,710,612,730),
             'discipline12': (420,80,612,100), 'discipline13': (420,100,612,120),
             'discipline14a': (420,150,612,170), 'discipline14b': (420,180,612,190),
             'discipline14c': (420,220,612,240), 'discipline15': (420,260,612,280),
             'discipline16': (420,310,612,330), 'discipline17': (420,330,612,350),
             'discipline18': (420,370,612,390), 'discipline19': (420,400,612,420),
             'discipline20': (420,440,612,460), 'emp1': (420,500,612,520), 'emp2': (420,540,612,560),
             'emp3': (420,570,612,590), 'emp4': (420,600,612,620), 'mail1': (420,650,612,670),
             'mail2': (420,670,612,690), 'mail3': (420,90,612,110), 'mail4': (420,130,612,150),
             'mail5': (420,160,612,180), 'mail5a': (420,180,612,200), 'mail5b': (420,200,612,220),
             'mail6': (420,230,612,250), 'mail6a': (420,260,612,280), 'mail7': (420,300,612,320),
             'mail8': (420,330,612,350), 'mail9': (420,380,612,400), 'mail10': (420,410,612,430),
             'mail11': (420,450,612,470), 'mail12': (420,470,612,490), 'mail13': (420,490,612,510),
             'mail14': (420,510,612,530), 'mail15': (420,540,612,560), 'mail16': (420,560,612,580),
             'mail17': (420,580,612,600), 'mail18': (420,610,612,630), 'mail19': (420,630,612,650),
             'mail20': (420,670,612,690), 'mail21': (420,700,612,720), 'mail22a': (420,90,612,110),
             'mail22b': (420,150,612,170), 'mail22c': (420,190,612,210), 'mail22d': (420,260,612,280),
             'mail22e': (420,290,612,310), 'tele1': (420,350,612,370), 'tele2': (420,370,612,390),
             'tele2a': (420,410,612,430), 'tele2b': (420,440,612,460), 'tele3': (420,460,612,480),
             'tele4': (420,500,612,520), 'visit1': (420,540,612,560), 'visit2': (420,560,612,590),
             'visit3': (420,590,612,610), 'visit4': (420,610,612,630), 'visit5': (420,640,612,660),
             'visit6': (420,660,612,680), 'visit7': (420,700,612,720), 'visit8': (420,720,612,740),
             'visit9': (420,70,612,90), 'visit10': (420,90,612,110), 'visit11': (420,110,612,130),
             'visit12': (420,130,612,150), 'socserv1': (420,180,612,200), 'socserv2': (420,210,612,230),
             'ed1': (420,250,612,270), 'ed2': (420,290,612,310), 'ed3': (420,320,612,340),
             'lib1': (420,360,612,380), 'lib1a': (420,390,612,410), 'lib1b': (420,410,612,430),
             'lib2': (420,430,612,450), 'lib3': (420,470,612,490), 'rel1': (420,530,612,550),
             'rel2': (420,550,612,570), 'commissary1': (420,600,612,620), 'commissary2': (420,620,612,640),
             'commissary3': (420,640,612,660), 'commissary4': (420,660,612,680),
             'commissary5': (420,710,612,730), 'commissary6': (420,70,612,90), 'commissary7': (420,110,612,130),
             'commissary8': (420,150,612,170), 'recleis1': (420,190,612,210), 'recleis2': (420,210,612,230),
             'recleis3': (420,230,612,250), 'recleis4': (420,270,612,290), 'recleis5': (420,290,612,310),
             'juvedet1': (420,340,612,360), 'juvedet2': (420,360,612,380), 'juvedet3': (420,380,612,400),
             'juvedet4': (420,410,612,430), 'juvedet4a': (420,440,612,460), 'juvedet4b': (420,460,612,480),
             'juvedet5': (420,500,612,520), 'juvedet6': (420,540,612,560), 'juvedet7': (420,580,612,600),
             'juvedet8': (420,600,612,620), 'juvedet9': (420,640,612,660), 'juvedet10a': (420,700,612,720),
             'juvedet10b': (420,70,612,90), 'juvedet11': (420,90,612,110), 'juvedet11a': (420,120,612,140),
             'juvedet11b': (420,160,612,180), 'juvedet11c': (420,200,612,220), 'juvedet11d': (420,220,612,240),
             'juvedet11e': (420,240,612,260), 'juvedet11f': (420,260,612,280), 'juvedet11g': (420,280,612,300),
             'juvedet12': (420,310,612,330), 'juvedet13': (420,340,612,360), 'juvedet14': (420,380,612,400),
             'juvedet15': (420,410,612,430), 'tempdet1': (420,470,612,490), 'tempdet2': (420,490,612,510),
             'tempdet2a': (420,510,612,530), 'tempdet2b': (420,550,612,570), 'tempdet2c': (420,570,612,590),
             'tempdet3': (420,590,612,610), 'tempdet4': (420,620,612,640), 'tempdet5': (420,640,612,660),
             'tempdet5a': (420,660,612,680), 'tempdet5b': (420,690,612,710), 'tempdet6': (420,70,612,90),
             'tempdet7': (420,90,612,110), 'tempdet7a': (420,110,612,130), 'tempdet7b': (420,150,612,170),
             'tempdet8': (420,170,612,190), 'tempdet9': (420,190,612,210), 'tempdet9a': (420,230,612,250),
             'tempdet9b': (420,250,612,270), 'tempdet9c': (420,290,612,310), 'tempdet9d': (420,320,612,340),
             'tempdet10': (420,340,612,360), 'tempdet10a': (420,360,612,380), 'tempdet10b': (420,390,612,410),
             'youth1': (420,450,612,470), 'youth2': (420,470,612,490), 'youth3': (420,510,612,590),
             'youth3a': (420,510,612,530), 'youth3b': (420,550,612,570), 'youth4': (420,570,612,590),
             'youth5': (420,590,612,610), 'youth6': (420,620,612,640), 'youth6a': (420,640,612,660),
             'youth6b': (420,680,612,700), 'youth6c': (420,700,612,720), 'youth7': (420,70,612,90),
             'youth8': (420,100,612,120), 'youth8a': (420,120,612,140), 'youth8b': (420,150,612,170),
             'youth8c': (420,170,612,190), 'youth9': (420,210,612,230)}

checkquestions = list(checkresponses.keys())

lastQuestions = ['personnel3', 'adminproc8', 'adminproc16', 'adminproc32', 'releaseproc11_dismentill',
                 'housing4e', 'med2', 'med8', 'med21a', 'food2', 'food20', 'san16',
                 'sec1', 'sec21c', 'safety12', 'discipline11', 'mail2', 'mail21',
                 'visit8', 'commissary5', 'juvedet10a', 'tempdet5b', 'youth6c']


vertresponses = {'med9staff':'','med9contract':'','med9hospital':'','foodtype_contract':'',
                 'foodtype_frozen':'','foodtype_onsite':''}

vertquestions = list(vertresponses.keys())

vertbbox = {'med9staff':(0,75,612,90),'med9contract':(0,90,612,102),'med9hospital':(0,103,612,118),
            'foodtype_contract':(0,500,612,515),'foodtype_frozen':(0,515,612,530),
            'foodtype_onsite':(0,550,612,570)}


#pdf.pages[1]
facilityName = (115,90,370,110)

consDate = (130,500,310,520)
renoDate = (410,500,612,520)

#capacityTot = (220,520,280,540)
#capacityMale = (310,520,340,540)
#capacityFem = (380,520,612,540)
capacity = (150,520,612,540)
#capacityJuvMale = (320,540,350,560)
#capacityJufFem = (420,540,612,560)
capacityJuv = (250,540,612,560)

#popTot = (220,560,280,580)
#popMale = (310,560,340,580)
#popFem = (380,560,612,580)
pop = (150,560,612,580)
#popJuvMale = (320,590,350,610)
#popJufFem = (420,590,612,610)
popJuv = (250,590,612,610)

#cellSing = (230,610,280,630)
#cellDoub = (320,610,340,630)
#cellOth = (370,610,612,630)
cells = (190,610,612,630)

#detRoomSing = (225,630,270,650)
#detRoomDoub = (315,630,340,650)
#detRoomOth = (365,610,612,650)
detRooms = (190,630,612,650)

#empFTMale = (225,650,280,670)
#empFTFem = (320,650,612,670)
#empPTMale = (230,670,280,690)
#empPTFem = (320,670,612,690)
#otherDutyMale = (230,690,280,710)
#otherDutyFem = (320,690,612,710)
empFT = (190,650,612,670)
empPT = (190,670,612,690)
otherDuty = (190,690,612,710)

#pdf.pages[7]
housingfloors=(0,420,612,450) # THIS IS THE TEXT

#pdf.pages[14]
supervision_lightsout=(0,670,612,690) #this is text

#pdf.pages[15]
sec14freq=(120,420,612,440) #weird - text

#pdf.pages[16]
#sec24tested=(145,300,310,320) #weird - text
#sec24type=(340,300,612,320) #weird - text
sec24text=(0,300,612,320)

#pdf.pages[10]
med9staff=(0,75,612,90) #weird one, skipped for now
med9contract=(0,90,612,102) #weird one, skipped for now
med9hospital=(0,103,612,118) #weird one, skipped for now

#pdf.pages[11]
foodtype_contract=(0,500,612,515) #weird - vert and seperately text
foodtype_frozen=(0,515,612,530)
foodtype_onsite=(0,550,612,570)



def checkboxTrack(pCurrent, tup):
  # check YES
  if len(pCurrent.crop((tup[0], tup[1], 450, tup[3])).lines) > 0:
      return "YES"
  #check N/A
  elif len(pCurrent.crop((450, tup[1], 490, tup[3])).lines) > 0:
      return "N/A"
  #check NO
  elif len(pCurrent.crop((490, tup[1], 612, tup[3])).lines) > 0:
      return "NO"
  else:
      return "ERR"

def textTaker(pdf_object,p):
  #textDict = {'facilityName':'','consDate':'','renoDate':'','capacityTot':'','capacityMale':'','capacityFem':'',
  #            'capacityJuvMale':'','capacityJufFem':'','popTot':'','popMale':'','popFem':'','popJuvMale':'',
  #            'popJufFem':'','cellSing':'','cellDoub':'','cellOth':'','detRoomSing':'','detRoomDoub':'',
  #            'detRoomOth':'','empFTMale':'','empFTFem':'','empPTMale':'','empPTFem':'','otherDutyMale':'',
  #            'otherDutyFem':'','housingfloors':'','supervision_lightsout':'','sec24text':''}
  textDict = {'facilityName':'','consDate':'','renoDate':'','capacityTot':'','capacity':'','capacityJuv':'',
              'pop':'','popJuv':'','cells':'','detRooms':'','empFT':'','empPT':'','otherDuty':'',
              'housingfloors':'','supervision_lightsout':'','sec24text':''}

  #pdf_object.pages[1]
  textDict['facilityName'] = pdf_object.pages[p].crop(facilityName).extract_text()
  textDict['consDate'] = pdf_object.pages[p].crop(consDate).extract_text()
  textDict['renoDate'] = pdf_object.pages[p].crop(renoDate).extract_text()
  #textDict['capacityTot'] = pdf_object.pages[p].crop(capacityTot).extract_text()
  #textDict['capacityMale'] = pdf_object.pages[p].crop(capacityMale).extract_text()
  #textDict['capacityFem'] = pdf_object.pages[p].crop(capacityFem).extract_text()
  #textDict['capacityJuvMale'] = pdf_object.pages[p].crop(capacityJuvMale).extract_text()
  #textDict['capacityJufFem'] = pdf_object.pages[p].crop(capacityJufFem).extract_text()
  textDict['capacity'] = pdf_object.pages[p].crop(capacity).extract_text()
  textDict['capacityJuv'] = pdf_object.pages[p].crop(capacityJuv).extract_text()
  #textDict['popTot'] = pdf_object.pages[p].crop(popTot).extract_text()
  #textDict['popMale'] = pdf_object.pages[p].crop(popMale).extract_text()
  #textDict['popFem'] = pdf_object.pages[p].crop(popFem).extract_text()
  #textDict['popJuvMale'] = pdf_object.pages[p].crop(popJuvMale).extract_text()
  #textDict['popJufFem'] = pdf_object.pages[p].crop(popJufFem).extract_text()
  textDict['pop'] = pdf_object.pages[p].crop(pop).extract_text()
  textDict['popJuv'] = pdf_object.pages[p].crop(popJuv).extract_text()

  #textDict['cellSing'] = pdf_object.pages[p].crop(cellSing).extract_text()
  #textDict['cellDoub'] = pdf_object.pages[p].crop(cellDoub).extract_text()
  #textDict['cellOth'] = pdf_object.pages[p].crop(cellOth).extract_text()
  textDict['cells'] = pdf_object.pages[p].crop(cells).extract_text()

  #textDict['detRoomSing'] = pdf_object.pages[p].crop(detRoomSing).extract_text()
  #textDict['detRoomDoub'] = pdf_object.pages[p].crop(detRoomDoub).extract_text()
  #textDict['detRoomOth'] = pdf_object.pages[p].crop(detRoomOth).extract_text()
  textDict['detRooms'] = pdf_object.pages[p].crop(detRooms).extract_text()

  #textDict['empFTMale'] = pdf_object.pages[p].crop(empFTMale).extract_text()
  #textDict['empFTFem'] = pdf_object.pages[p].crop(empFTFem).extract_text()
  textDict['empFT'] = pdf_object.pages[p].crop(empFT).extract_text()

  #textDict['empPTMale'] = pdf_object.pages[p].crop(empPTMale).extract_text()
  #textDict['empPTFem'] = pdf_object.pages[p].crop(empPTFem).extract_text()
  textDict['empPT'] = pdf_object.pages[p].crop(empPT).extract_text()

  #textDict['otherDutyMale'] = pdf_object.pages[p].crop(otherDutyMale).extract_text()
  #textDict['otherDutyFem'] = pdf_object.pages[p].crop(otherDutyFem).extract_text()
  textDict['otherDuty'] = pdf_object.pages[p].crop(otherDuty).extract_text()

  #pdf_object.pages[7]
  textDict['housingfloors'] = pdf_object.pages[p+6].crop(housingfloors).extract_text()
  #pdf_object.pages[14]
  textDict['supervision_lightsout'] = pdf_object.pages[p+13].crop(supervision_lightsout).extract_text()
  #pdf_object.pages[15]
  textDict['sec14freq'] = pdf_object.pages[p+14].crop(sec14freq).extract_text()
  #pdf_object.pages[16]
  textDict['sec24text'] = pdf_object.pages[p+15].crop(sec24text).extract_text()

  return textDict

def vertCheck(pCurrent, tup):
  # check YES
  if len(pCurrent.crop(tup).lines) > 0:
      return "YES"
  else:
      return "NO"

def scraper(pdf_filepath, filename, initial_checkresponses_template):
  # Create a fresh dictionary for the responses of the current PDF
  # This uses the globally defined 'combined_checkbox_template' as a template of keys with empty string values.
  current_pdf_responses = initial_checkresponses_template.copy()
  current_pdf_responses['filename'] = filename # Add filename to the dictionary
  print(filename)

  mainpdf = pdfplumber.open(pdf_filepath)

  page = 0
  checklist_flag = False
  pCurrent = mainpdf.pages[page]

  # Find the starting page for the main checklist items
  while checklist_flag == False:
    words = pCurrent.crop((0,50,400,70)).extract_text()
    if words == "Has the jail been approved to hold detainees who are under 18":
      checklist_flag = True
    else:
      page += 1
      pCurrent = mainpdf.pages[page]

  current_pdf_responses['year'] = year # Add the year to the dictionary

  # Extract text data using the updated textTaker function
  text_data = textTaker(mainpdf,page-1)

  # Process checkbbox items
  for key in checkbbox:
    current_pdf_responses[key] = checkboxTrack(pCurrent, checkbbox[key])
    if key in lastQuestions:
      page += 1
      pCurrent = mainpdf.pages[page]

  # Process vertbbox items on page 10
  pCurrent = mainpdf.pages[10]
  for key in ['med9staff', 'med9contract', 'med9hospital']:
    if key in vertbbox: # Ensure the key exists in vertbbox
      current_pdf_responses[key] = vertCheck(pCurrent, vertbbox[key])

  # Process vertbbox items on page 11
  pCurrent = mainpdf.pages[11]
  for key in ['foodtype_contract', 'foodtype_frozen', 'foodtype_onsite']:
    if key in vertbbox: # Ensure the key exists in vertbbox
      current_pdf_responses[key] = vertCheck(pCurrent, vertbbox[key])

  mainpdf.close() # Close the PDF after processing

  # Merge the text_data and the checkbox/vertical responses
  return {**text_data, **current_pdf_responses}

folderpath = f"/Users/aadams/dev/py/jailinspections/files/{year}"

mainframe = pd.DataFrame()

for filename in os.listdir(folderpath):
  if filename.endswith(".pdf"):
    full_path = os.path.join(folderpath, filename)
    combined_checkbox_template = {**checkresponses, **vertresponses}
    scraped_data_combined = scraper(pdf_filepath=full_path, filename=filename, initial_checkresponses_template=combined_checkbox_template)
    mainframe = pd.concat([mainframe, pd.DataFrame([scraped_data_combined])], ignore_index=True)

mainframe.to_csv(f"{year}output.csv", sep=',', encoding='utf-8', index=False, header=True)
