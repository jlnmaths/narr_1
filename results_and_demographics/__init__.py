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

    nie = models.StringField(label="Haben Sie in der Vergangenheit investiert?", choices=['Ich habe noch nie investiert! (Rest freilassen)', 'Ich habe in der Vergangenheit investiert (siehe unten)'])
    sa = models.IntegerField(min=0, max=100, label="Welchen Anteil Ihres bisher investierten Geldes haben Sie in Staatsanleihen investiert? Geben Sie dies bitte in Prozent an.", initial = 0, blank=True)
    ua = models.IntegerField(min=0, max=100, label="Welchen Anteil Ihres bisher investierten Geldes haben Sie in Unternehmensanleihen investiert? Geben Sie dies bitte in Prozent an.", initial = 0, blank=True)
    bc = models.IntegerField(min=0, max=100, label="Welchen Anteil Ihres bisher investierten Geldes haben Sie in Blue Chip Aktien (große Unternehmen, z.B. Microsoft, Apple, Volkswagen) investiert? Geben Sie dies bitte in Prozent an.", initial = 0, blank=True)
    immo = models.IntegerField(min=0, max=100, label="Welchen Anteil Ihres bisher investierten Geldes haben Sie in Immobilien (nicht für Eigengebrauch) investiert? Geben Sie dies bitte in Prozent an.", initial = 0, blank=True)
    invf = models.IntegerField(min=0, max=100, label="Welchen Anteil Ihres bisher investierten Geldes haben Sie in Investmentfonds investiert? Geben Sie dies bitte in Prozent an.", initial = 0, blank=True)
    etf =  models.IntegerField(min=0, max=100, label="Welchen Anteil Ihres bisher investierten Geldes haben Sie in ETFs investiert? Geben Sie dies bitte in Prozent an.", initial = 0, blank=True)
    rohst = models.IntegerField(min=0, max=100, label="Welchen Anteil Ihres bisher investierten Geldes haben Sie in Rohstoffe investiert? Geben Sie dies bitte in Prozent an.", initial = 0, blank=True)
    krypto = models.IntegerField(min=0, max=100, label="Welchen Anteil Ihres bisher investierten Geldes haben Sie in Kryptowährungen investiert? Geben Sie dies bitte in Prozent an.", initial = 0, blank=True)
    andere = models.StringField(label="Haben Sie in nicht oben genannte Optionen investiert? (Bitte erläutern!)", blank=True)
    freq = models.StringField(label="Wie oft tätigen Sie Investitionen?",
        choices=['Täglich', 'Wöchentlich', 'Monatlich', 'Vierteljährlich', 'Halbjährlich', 'Jährlich', 'Seltener als Jährlich', 'Nie'])
    environ = models.IntegerField(min=0, max=100, label="Wie viel Prozent Ihres Umfelds (Freunde, Verwandte, Kollegen) investieren in etwa?")
    knowledge = likertScale(
        'Als wie gut schätzen Sie Ihr Wissen über Finanzanlagen und Investitionen ein? Bitte geben Sie Ihre Antwort auf einer Skala von 0 bis 10 an, wobei 0 bedeutet, dass Sie sehr wenig wissen, und 10 bedeutet, dass Sie sehr viel wissen.',
        '', '', 10)
    covid = models.IntegerField(choices=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
    widget=widgets.RadioSelectHorizontal,
       label= 'Hat die COVID-Pandemie Ihre Wahrnehmung finanzieller Risiken verändert? Bitte geben Sie Ihre Antwort auf einer Skala von -5 bis 5 an, wobei 0 bedeutet, dass sich nichts verändert hat, -5 bedeutet, dass Sie viel risikoaverser geworden sind, und 5 bedeutet, dass sie viel risikofreudiger geworden sind.')
    investment = models.StringField(label="Für welche Investition würden Sie sich entscheiden?",
        choices=['Investition 1','Investition 2', 'Investition 3', 'Investition 4', 'Investition 5','Investition 6','Investition 7','Investition 8' ])


# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['yearOfBirth', 'male', 'education', 'country', 'study', 'politics']

class Risk_Narratives(Page):
    form_model = 'player'
    form_fields = ['TimeSurvey', 'RiskSurvey', 'AltruismSurvey', 'simplicity_1', 'simplicity_2', 'dataverbal_1', 'dataverbal_2']

class assets_ba(Page):
    form_model = 'player'
    form_fields = ['nie','sa', 'ua', 'bc', 'immo', 'invf', 'etf', 'rohst', 'krypto', 'andere']
    @staticmethod
    def error_message(player, values):
        if  values["sa"] + values["ua"] + values["bc"] + values["immo"] + values["invf"] + values["etf"] + values["rohst"] + values["krypto"] > 100:
            return 'Die Prozentpunkte ergeben in Summe mehr als 100 Prozent!'

class risk_ba(Page):
    form_model = 'player'
    form_fields = ['freq', 'environ', 'knowledge', 'covid']

class invest_ba(Page):
    form_model = 'player'
    form_fields = ['investment']
    def vars_for_template(player: Player):
        img_path = 'Download.jpg'
        return dict(
            img_path = img_path
        )

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        combined_link = player.subsession.session.config['limesurvey_link'] + f'&PAYMENTCODE={player.participant.label}'
        return dict(combined_link=combined_link)


page_sequence = [Demographics, Risk_Narratives,invest_ba, risk_ba, assets_ba, Results]
