from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'demographics'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    years = range(1920, 2005)
    # See: https://www.census.gov/topics/education/educational-attainment/about.html for education list
    list_of_education = [
        'Kein Schulabschluss',
        'Allgemeine oder fachgebundene Hochschulreife',
        'Bachelorabschluss',
        'Masterabschluss',
        'Diplom',
        'Promotion'
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def likertScale(label, low, high, n, blank = False):
    if low != '':
        CHOICES = [(0, str(0) + " (" + low + ")")]
    else:
        CHOICES = [(0, str(0))]
    for x in range(1, n):
        CHOICES = CHOICES + [(x, str(x))]
    if high != '':
        CHOICES = CHOICES + [(n, str(n) + " (" + high + ")")]
    else:
        CHOICES = CHOICES + [(n, str(n))]
    return models.IntegerField(
        choices=CHOICES,
        label=label,
        widget=widgets.RadioSelectHorizontal,
        blank=blank,
    )

class Player(BasePlayer):
    yearOfBirth = models.IntegerField(choices=C.years, label="Mein Geburtsjahr ist:")
    male = models.IntegerField(widget=widgets.RadioSelectHorizontal, choices=[[0, 'weiblich'], [1, 'männlich'], [99, 'divers'],
                                                                                [98, 'keine Angabe'], ],
                               label="Ich bin")
    education = models.StringField(choices=C.list_of_education,
                                   label="Mein höchster Bildungsabschluss ist:")
    country = models.StringField(label="Ich lebe in:")

    iban = models.StringField(label="IBAN (für Vergütung):")
    name = models.StringField(label="Name des Kontoinhabers (für Vergütung):")

    study = models.StringField(label="Was studieren Sie?")
    politics =likertScale(
        'Auf einer Skala von 1 bis 10, bei der 1 für sehr links und 10 für sehr rechts steht, wo ordnen Sie sich politisch ein?',
        '', '', 10)

    simplicity_1 =likertScale(
        'Ich bevorzuge einfache Erklärungen (1 bis 10, 1 = trifft überhaupt nicht zu, 10 = trifft vollkommen zu).',
        '', '', 10)
    simplicity_2 = models.StringField(label="Ich bin davon überzeugt, dass die meisten Menschen einfache Erklärungen bevorzugen.",
        choices=['Ja', 'Nein'])
    dataverbal_1 =likertScale(
        'Ich bevorzuge Daten über verbale Erklärungen (1 bis 10, 1 = trifft überhaupt nicht zu, 10 = trifft vollkommen zu).',
        '', '', 10)
    dataverbal_2 = models.StringField(label="Ich bin davon überzeugt, dass die meisten Menschen Daten über verbale Erklärungen bevorzugen.",
        choices=['Ja', 'Nein'])



    TimeSurvey = likertScale(
        'Wie bereit sind Sie, auf etwas zu verzichten, das Ihnen heute nützt, um in Zukunft mehr davon zu erhalten? Bitte geben Sie Ihre Antwort auf einer Skala von 0 bis 10 an, wobei 0 bedeutet, dass Sie "überhaupt nicht gewillt" sind und eine 10 bedeutet, dass Sie "sehr gewillt" sind. ',
        '', '', 10)
    RiskSurvey = likertScale(
        'Wie gewillt sind Sie im Allgemeinen, Risikos einzugehen? Bitte verwenden Sie eine Skala von 0 bis 10, wobei 0 "völlig ungewillt" und 10 "sehr gewillt" bedeutet.',
        '', '', 10)
    AltruismSurvey = likertScale(
        'Wie bereit sind Sie, für gute Zwecke zu spenden, ohne eine Gegenleistung zu erwarten? Bitte geben Sie Ihre Antwort auf einer Skala von 0 bis 10 an, wobei 0 bedeutet, dass Sie "überhaupt nicht dazu bereit" sind, und 10 bedeutet, dass Sie "sehr dazu bereit" sind.',
        '', '', 10)


# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['yearOfBirth', 'male', 'education', 'country', 'study', 'politics', 'iban', 'name']

class Risk_Narratives(Page):
    form_model = 'player'
    form_fields = ['TimeSurvey', 'RiskSurvey', 'AltruismSurvey', 'simplicity_1', 'simplicity_2', 'dataverbal_1', 'dataverbal_2']



class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Demographics, Risk_Narratives, Results]
