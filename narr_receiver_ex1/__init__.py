from otree.api import *
import numpy as np

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'narr_receiver'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 6


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
    treatment = models.CharField(initial="A")
    assessment = models.IntegerField(min=0, max=100, label="Was, denken Sie, ist die Wahrscheinlichkeit, dass die Hauptbeobachtung hinter dem Fragezeichen eine 1 ist?")
    score = models.FloatField()
    certainty =likertScale(
        'Auf einer Skala von 1 bis 10, bei der 1 für sehr unsicher und 10 für sehr sicher steht, wie sicher sind Sie sich, dass ihre Einschätzung zutreffend war?',
        '', '', 10)
    starttime = models.IntegerField(initial=0)
    finishtime = models.IntegerField(initial=0)
    datademandtime = models.IntegerField(initial=0) #the moment the button to reveal is clicked (captcha then appears)
    narrdemandtime = models.IntegerField(initial=0) #the moment the button to reveal is clicked (captcha then appears)
    datatime = models.IntegerField(initial=0)  #the moment the data is revealed (after solving captcha)
    narrtime = models.IntegerField(initial=0)  #the moment the narr is revealed (after solving captcha)
    o = models.StringField()
    lr = models.StringField()
    nb = models.StringField()

    quiz1 = models.StringField(label='Richtig oder falsch? Der Zusammenhang zwischen Hauptbeobachtung und Nebenbeobachtung ist von Zeile zu Zeile ein anderer.',
        choices=['Richtig', 'Falsch'])
    quiz2 = models.StringField(label="Richtig oder falsch?  Die Ereignisse der 7. Zeile sind definitiv nach den Ereignissen der 1. Zeile passiert.",
        choices=['Richtig', 'Falsch'])
    quiz3 = models.StringField(label="Richtig oder falsch? Die Erklärungen können wahr sein, müssen es aber nicht.",
        choices=['Richtig', 'Falsch'])
    quiz4 = models.StringField(label="Richtig oder falsch? Sie müssen einschätzen, ob sich hinter dem Fragezeichen (?) eine 0 oder 1 verbirgt.",
        choices=['Richtig', 'Falsch'])
    quiz5 = models.StringField(label="Auszahlungsfrage Platzhalter")
    quiz6 = models.StringField(label="Was trifft zu?",
                                choices=['Empfänger und Sender sehen dieselbe Datentabellen mit Haupt- und Nebenbeobachtungen, aber die Empfänger sehen nur die Erklärungen, die ihnen von einem Sender geschickt wurden.',
                                         'Empfänger sehen die Datentabelle mit Haupt- und Nebenbeobachtungen nur, wenn die Sender sie geschickt haben.'])


# functions
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        import random
        for player in subsession.get_players():
            player.participant.payround = random.randint(1,6)
            player.participant.true_y = random.randint(0,1)
    import itertools
    treatments = itertools.cycle([0, 1, 2, 3])
    for player in subsession.get_players():
        player.treatment = next(treatments)

def set_payoff(player: Player):
    from scipy.stats import bernoulli
    if player.round_number == player.participant.payround:
        if player.participant.true_y == 0:
            prob = 1 - (1 - player.assessment/100)*(1 - player.assessment/100)
        else:
            prob = 1 - player.assessment/100*player.assessment/100
        return bernoulli.rvs(prob, size=1)[0] + player.participant.true_y
    else:
        return player.participant.true_y



# PAGES
class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

class Instructions_rec(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

class Instructions_payoff_A(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1 and (player.treatment == 0 or player.treatment == 1)

class Instructions_payoff_B(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1 and (player.treatment == 2 or player.treatment == 3)

class One_state(Page): #Two_state for other receiver treatment
    form_model = 'player'
    form_fields = ['assessment']

    @staticmethod
    def vars_for_template(player: Player):
        import time
        o_v = np.random.permutation([4, 5, 6, 7, 8, 9, 10, 11])
        o_h = np.random.permutation([0, 1, 2, 3])
        o = np.append(o_h, o_v)  # reordering of columns
        o = np.append(o, np.array([12]))

        present = np.random.permutation(6)

        #order of these arrays: d_balanced, d_pro, d_con, s_balanced, s_pro, s_con
        hb = np.array([1,1,0,0,1,1,1,1,0,0,0,0,2])
        nb_1 = np.array([[1,0,0,0,1,1,1,0,0,0,0,0,1], [1,0,0,0,1,1,1,0,0,0,0,0,1],
                        [1,1,0,0,1,1,0,0,0,0,0,0,1], [0,1,0,0,1,1,1,0,1,0,0,0,1], [0,0,0,0,1,1,1,0,1,0,0,0,1],
                        [1,0,0,0,1,1,0,0,1,0,0,0,1]]) #plus
        nb_2 = np.array([[0,0,1,0,0,0,0,0,1,1,1,0,1], [0,0,1,0,0,0,0,0,1,0,1,0,1],
                         [0,0,1,0,0,0,0,0,1,1,1,0,1], [0,0,1,0,0,0,0,1,1,1,0,0,1], [0,0,1,0,0,0,0,1,1,1,0,0,1],
                         [0,0,1,0,0,0,0,1,1,1,1,0,1]]) #minus
        nb_3 = np.array([[1,1,1,1,1,1,1,0,1,1,1,0,1], [1,1,1,1,1,1,1,0,1,1,1,0,1],
                         [1,1,1,1,1,1,0,1,1,1,1,0,1], [1,1,1,1,1,1,0,1,1,1,1,0,1], [1,0,1,0,1,1,1,1,1,1,1,1,1],
                         [1,0,1,0,1,1,1,1,1,1,1,1,1]]) #join
        hb = hb[o] #hb is always the same
        plus = nb_1[present[player.round_number-1]][o]
        minus = nb_2[present[player.round_number-1]][o]
        join = nb_3[present[player.round_number-1]][o]

        #randomize column order

        nb = [plus, minus, join]
        rand = np.random.permutation([0, 1, 2])
        c_1 = nb[rand[0]]
        c_2 = nb[rand[1]]
        c_3 = nb[rand[2]]
        plus = np.where(rand==0)[0][0]+1
        join = np.where(rand==2)[0][0]+1

        player.o = str(o)
        player.nb = str([plus, join])
        player.starttime = int(time.time())

        if present[player.round_number-1] < 3:
            e = ['Immer, wenn Nebenbedingung (NB)']
        else:
            e = ['Fast immer, wenn Nebenbedingung (NB)']

        return dict(
            hb=hb,
            nb_1=c_1,
            nb_2=c_2,
            nb_3=c_3,
            round=player.round_number,
            plus = plus,
            join = join,
            e = e
        )

    @staticmethod
    def live_method(player: Player, data):
        import time
        if int(data) == 1:
            player.datatime = int(time.time())
        if int(data) == 2:
            player.narrtime = int(time.time())
        if int(data) == 3:
            player.datademandtime = int(time.time())
        if int(data) == 4:
            player.narrdemandtime = int(time.time())
        # can just do more cases here!

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import time
        set_payoff(player)
        player.finishtime = int(time.time())

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 0 or player.treatment == 2

class Two_state(Page): #Two_state for other receiver treatment
    form_model = 'player'
    form_fields = ['assessment']

    @staticmethod
    def vars_for_template(player: Player):
        import time
        o_v = np.random.permutation([4, 5, 6, 7, 8, 9, 10, 11])
        o_h = np.random.permutation([0, 1, 2, 3])
        o = np.append(o_h, o_v)  # reordering of columns
        o = np.append(o, np.array([12]))

        present = np.random.permutation(6)

        #order of these arrays: d_balanced, d_pro, d_con, s_balanced, s_pro, s_con
        hb = np.array([1,1,0,0,1,1,1,1,0,0,0,0,2])
        nb_1 = np.array([[1,0,0,0,1,1,1,0,0,0,0,0,1], [1,0,0,0,1,1,1,0,0,0,0,0,1],
                        [1,1,0,0,1,1,0,0,0,0,0,0,1], [0,1,0,0,1,1,1,0,1,0,0,0,1], [0,0,0,0,1,1,1,0,1,0,0,0,1],
                        [1,0,0,0,1,1,0,0,1,0,0,0,1]]) #plus
        nb_2 = np.array([[0,0,1,0,0,0,0,0,1,1,1,0,1], [0,0,1,0,0,0,0,0,1,0,1,0,1],
                         [0,0,1,0,0,0,0,0,1,1,1,0,1], [0,0,1,0,0,0,0,1,1,1,0,0,1], [0,0,1,0,0,0,0,1,1,1,0,0,1],
                         [0,0,1,0,0,0,0,1,1,1,1,0,1]]) #minus
        nb_3 = np.array([[1,1,1,1,1,1,1,0,1,1,1,0,1], [1,1,1,1,1,1,1,0,1,1,1,0,1],
                         [1,1,1,1,1,1,0,1,1,1,1,0,1], [1,1,1,1,1,1,0,1,1,1,1,0,1], [1,0,1,0,1,1,1,1,1,1,1,1,1],
                         [1,0,1,0,1,1,1,1,1,1,1,1,1]]) #join
        hb = hb[o] #hb is always the same
        plus = nb_1[present[player.round_number-1]][o]
        minus = nb_2[present[player.round_number-1]][o]
        join = nb_3[present[player.round_number-1]][o]

        #randomize column order

        nb = [plus, minus, join]
        rand = np.random.permutation([0, 1, 2])
        c_1 = nb[rand[0]]
        c_2 = nb[rand[1]]
        c_3 = nb[rand[2]]
        plus = np.where(rand==0)[0][0]+1
        join = np.where(rand==2)[0][0]+1

        player.o = str(o)
        player.nb = str([plus, join])
        player.starttime = int(time.time())

        if present[player.round_number-1] < 3:
            e = ['Immer, wenn Nebenbedingung (NB)']
        else:
            e = ['Fast immer, wenn Nebenbedingung (NB)']

        return dict(
            hb=hb,
            nb_1=c_1,
            nb_2=c_2,
            nb_3=c_3,
            round=player.round_number,
            plus = plus,
            join = join,
            e = e
        )

    @staticmethod
    def live_method(player: Player, data):
        import time
        if int(data) == 1:
            player.datatime = int(time.time())
        if int(data) == 2:
            player.narrtime = int(time.time())
        if int(data) == 3:
            player.datademandtime = int(time.time())
        if int(data) == 4:
            player.narrdemandtime = int(time.time())
        # can just do more cases here!

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import time
        set_payoff(player)
        player.finishtime = int(time.time())

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 1 or player.treatment == 3

class Certainty(Page):
    form_model = 'player'
    form_fields = ['certainty']

class Quiz(Page):
    form_model = 'player'
    form_fields = ['quiz1', 'quiz2', 'quiz3', 'quiz4', 'quiz5', 'quiz6']

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(quiz1='Falsch', quiz2='Falsch', quiz3='Richtig', quiz4='Richtig', quiz5='Test', quiz6='Empfänger sehen die Datentabelle mit Haupt- und Nebenbeobachtungen nur, wenn die Sender sie geschickt haben.')

        if values != solutions:
            return "Eine oder mehrere Antworten waren leider falsch."

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Instructions, Instructions_rec, Instructions_payoff_A, Instructions_payoff_B, Quiz, One_state, Two_State, Certainty]
