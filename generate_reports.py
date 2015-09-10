from workflow.models import CSSCall
from datetime import datetime, timedelta
import random
from django.contrib.auth.models import User

names = [u'Ann Solis', u'Sharon Redarte', u'Rasheta', u'Shawna Webster', u'Diane DeGuzman', u'Karen Jackson', u'Jane Ferrier', u'Vikki Carlisle', u'Ted Davis', u'Tina Causnika', u'Lynn Hawkins', u'Vicki Carlisle', u'John Bats', u'Tom Ansley', u'Army', u'Eileen Hubert', u'Tony Sowell', u'Jane Ferrier', u'Resa Garibato', u'Angelo Garcia']
addresses = [u'525 Capitol', u'TTZ', u'118 Louisiana', u'Vallejo Times Herald', u'St Vincent Hill', u'Caldwell', u'680 Starfish', u'1031 Caldwell', u'1039 Caldwell', u'Santa Rosa', u'water billing', u'1346 Santa Clara', u'2241 Sacramento', u'1008 Del Mar Ave']
phones = [u'9165051208', u'6553322', u'5102676056', u'7077048872', u'', u'6558168', u'5541988', u'5577160', u'3733245', u'7073198737', u'5541988', u'5088401', u'7073420570', u'6452601', u'6486676', u'7076441863', u'7075544855', u'7072083389', u'7073104775']

for i in xrange(0, 10):

    CSSCall.objects.create(
        date=str(datetime.now() - timedelta(days=random.random() * 100)),
        name=random.choice(names),
        phone=random.choice(phones),
        address=random.choice(addresses)
    )
