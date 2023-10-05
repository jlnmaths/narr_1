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
    assessment = models.IntegerField(min=0, max=100, label="Was denken Sie, ist die Wahrscheinlichkeit, dass die Hauptbeobachtung hinter dem Fragezeichen eine 1 ist?")
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

    quiz1 = models.StringField(label='Richtig oder falsch? Der Zusammenhang zwischen Hauptbeobachtung und Nebenbeobachtung ist von Zeile zu Zeile ein anderer.',
        choices=['Richtig', 'Falsch'])
    quiz2 = models.StringField(label="Richtig oder falsch?  Die Ereignisse der 10. Zeile sind definitiv nach den Ereignissen der 1. Zeile passiert.",
        choices=['Richtig', 'Falsch'])
    quiz3 = models.StringField(label="Richtig oder falsch? Die Erklärungen können wahr sein, müssen es aber nicht.",
        choices=['Richtig', 'Falsch'])
    quiz4 = models.StringField(label="Richtig oder falsch? Sie müssen einschätzen, ob sich hinter dem Fragezeichen eine 0 oder 1 verbirgt.",
        choices=['Richtig', 'Falsch'])
    quiz5 = models.StringField(label="Auszahlungsfrage Platzhalter")
    quiz6 = models.StringField(label="Was trifft zu?",
                                choices=['Empfänger und Sender sehen dieselbe Datentabelle mit Haupt- und Nebenbeobachtungen, aber die Empfänger sehen nur die Erklärungen, die ihnen von den Sendern geschickt wurden.',
                                         'Empfänger sehen die Datentabelle mit Haupt- und Nebenbeobachtungen nur, wenn die Sender sie geschickt haben.'])
    quiz7 = models.StringField(label="Was trifft zu?",
                                choices=['Empfänger können zusätzliche Daten ODER die Erklärung des anderen Senders aufdecken. Sie müssen sich also entscheiden.',
                                         'Empfänger können zusätzliche Daten UND die Erklärung des anderen Senders aufdecken. Sie können also auch beides aufdecken.'])


# functions
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        import random
        for player in subsession.get_players():
            player.participant.payround = random.randint(1,6)
            player.participant.true_y = random.randint(0,1)

def set_payoff(player: Player):
    from scipy.stats import bernoulli
    if player.round_number == player.participant.payround:
        if player.participant.true_y == 0:
            prob = 1 - (1 - player.assessment)*(1 - player.assessment)
        else:
            prob = 1 - player.assessment*player.assessment
        return bernoulli.rvs(prob, size=1) #for bonus: + truy_y[0]
    else:
        return 0 #for bonus: true_y[0]


# PAGES
class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1


class Stage1(Page):
    form_model = 'player'
    form_fields = ['assessment']

    @staticmethod
    def vars_for_template(player: Player):
        import time
        o_v = np.random.permutation([4, 5, 6, 7, 8, 9, 10, 11])
        o_h = np.random.permutation([0, 1, 2, 3])
        o = np.append(o_h, o_v)  # reordering of columns
        o = np.append(o, np.array([12]))

        present = np.random.permutation(3)

        #order of these arrays: d_balanced, d_pro, d_con, s_balanced, s_pro, s_con
        hb = np.array([1,1,0,0,1,1,1,1,0,0,0,0,2])
        nb_d1 = np.array([[1,0,0,0,1,1,1,0,0,0,0,0,1], [1,0,0,0,1,1,1,0,0,0,0,0,1],
                        [1,1,0,0,1,1,0,0,0,0,0,0,1]]) #plus
        nb_d2 = np.array([[0,0,1,0,0,0,0,0,1,1,1,0,1], [0,0,1,0,0,0,0,0,1,0,1,0,1],
                         [0,0,1,0,0,0,0,0,1,1,1,0,1]]) #minus
        nb_d3 = np.array([[1,1,1,1,1,1,1,0,1,1,1,0,1], [1,1,1,1,1,1,1,0,1,1,1,0,1],
                         [1,1,1,1,1,1,0,1,1,1,1,0,1]]) #join
        nb_s1 = np.array([[0,1,0,0,1,1,1,0,1,0,0,0,1], [0,0,0,0,1,1,1,0,1,0,0,0,1],
                        [1,0,0,0,1,1,0,0,1,0,0,0,1]]) #plus
        nb_s2 = np.array([[0,0,1,0,0,0,0,1,1,1,0,0,1], [0,0,1,0,0,0,0,1,1,1,0,0,1],
                         [0,0,1,0,0,0,0,1,1,1,1,0,1]]) #minus
        nb_s3 = np.array([[1,1,1,1,1,1,0,1,1,1,1,0,1], [1,0,1,0,1,1,1,1,1,1,1,1,1],
                         [1,0,1,0,1,1,1,1,1,1,1,1,1]]) #join
        hb = hb[o] #hb is always the same
        x = player.round_number-1
        if x > 2:
            x = x-3
        plus = nb_d1[present[x]][o] #could also be with s, see after exp1
        minus = nb_d2[present[x]][o]
        join = nb_d3[present[x]][o]

        #randomize column order

        nb = [plus, minus, join]
        rand = np.random.permutation([0, 1, 2])
        c_1 = nb[rand[0]]
        c_2 = nb[rand[1]]
        c_3 = nb[rand[2]]
        plus = np.where(rand==0)[0][0]+1
        join = np.where(rand==2)[0][0]+1
        player.starttime = int(time.time())


        return dict(
            hb=hb,
            nb_1=c_1,
            nb_2=c_2,
            nb_3=c_3,
            round=player.round_number,
            plus = plus,
            join = join,
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
        return player.round_number < 4


class Stage2(Page):
    form_model = 'player'
    form_fields = ['assessment']

    @staticmethod
    def vars_for_template(player: Player):
        import time
        o_v = np.random.permutation([4, 5, 6, 7, 8, 9, 10, 11])
        o_h = np.random.permutation([0, 1, 2, 3])
        o = np.append(o_h, o_v)  # reordering of columns
        o = np.append(o, np.array([12]))

        present = np.random.permutation(3)

        # order of these arrays: d_balanced, d_pro, d_con, s_balanced, s_pro, s_con
        hb = np.array([1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 2])
        nb_d1 = np.array([[1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
                          [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]])  # plus
        nb_d2 = np.array([[0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1], [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                          [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1]])  # minus
        nb_d3 = np.array([[1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                          [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1]])  # join
        nb_s1 = np.array([[0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1], [0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
                          [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1]])  # plus
        nb_s2 = np.array([[0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1], [0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
                          [0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1]])  # minus
        nb_s3 = np.array([[1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1], [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]])  # join
        hb = hb[o]  # hb is always the same
        x = player.round_number-1
        if x > 2:
            x = x-3
        plus = nb_d1[present[x]][o]  # could also be with s, see after exp1
        minus = nb_d2[present[x]][o]
        join = nb_d3[present[x]][o]

        # randomize column order

        nb = [plus, minus, join]
        rand = np.random.permutation([0, 1, 2])
        c_1 = nb[rand[0]]
        c_2 = nb[rand[1]]
        c_3 = nb[rand[2]]
        plus = np.where(rand == 0)[0][0] + 1
        join = np.where(rand == 2)[0][0] + 1
        player.starttime = int(time.time())

        return dict(
            hb=hb,
            nb_1=c_1,
            nb_2=c_2,
            nb_3=c_3,
            round=player.round_number,
            plus=plus,
            join=join,
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
        return player.round_number > 3


class Certainty(Page):
    form_model = 'player'
    form_fields = ['certainty']

class Quiz(Page):
    form_model = 'player'
    form_fields = ['quiz1', 'quiz2', 'quiz3', 'quiz4', 'quiz5', 'quiz6', 'quiz7']

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(quiz1='Falsch', quiz2='Falsch', quiz3='Richtig', quiz4='Richtig', quiz5='Test', quiz6='Empfänger und Sender sehen dieselbe Datentabelle mit Haupt- und Nebenbeobachtungen, aber die Empfänger sehen nur die Erklärungen, die ihnen von den Sendern geschickt wurden.', quiz7='Empfänger können zusätzliche Daten UND die Erklärung des anderen Senders aufdecken. Sie können also auch beides aufdecken.')

        if values != solutions:
            return "Eine oder mehrere Antworten waren leider falsch."

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Instructions, Instructions_rec, Instructions_payoff, Stage1, Stage2, Certainty]
