from otree.api import *
import numpy as np

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'narr_sender'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    treatment = models.IntegerField(initial = 5)
    n_selection = models.StringField(
        choices=['Erklärung 1 unter der gewählten Tabelle', 'Erklärung 2 unter der gewählten Tabelle'],
        widget=widgets.RadioSelect,
        label= "Welche Erklärung wollen Sie an den Empfänger schicken?"
    )
    t_selection = models.StringField(
        choices=['Tabelle 1', 'Tabelle 2'],
        widget=widgets.RadioSelect,
        label= "Welche Tabelle wollen Sie an den Empfänger schicken?"
    )
    o = models.StringField()
    lr = models.StringField()
    nb = models.StringField()

    starttime = models.IntegerField(initial=0)
    finishtime = models.IntegerField(initial=0)

    quiz1 = models.StringField(label='Richtig oder falsch? Der Zusammenhang zwischen Hauptbeobachtung und Nebenbeobachtung ist von Zeile zu Zeile ein anderer.',
        choices=['Richtig', 'Falsch'])
    quiz2 = models.StringField(label="Richtig oder falsch?  Die Ereignisse der 7. Zeile sind definitiv nach den Ereignissen der 1. Zeile passiert.",
        choices=['Richtig', 'Falsch'])
    quiz3 = models.StringField(label="Richtig oder falsch? Die Erklärungen können wahr sein, müssen es aber nicht.",
        choices=['Richtig', 'Falsch'])
    quiz4 = models.StringField(label="Sie müssen eine Erklärung auswählen.",
        choices=['Richtig', 'Falsch'])
    quiz5 = models.StringField(label="Sie wollen den Empfänger davon überzeugen, dass sich hinter dem Fragezeichen (?)...",
        choices=['...eine 0 verbirgt.', '...eine 1 verbirgt.'])
    quiz6 = models.StringField(label="Auszahlungsfrage Platzhalter", choices=['Test'])
    quiz7 = models.StringField(label="Richtig oder falsch? Empfänger erhalten eine Auszahlungseinheit, sollte sich hinter dem Fragezeichen (?) eine 1 verbergen.",
                               choices=['Richtig', 'Falsch'])


def creating_session(subsession: Subsession):
    import itertools
    treatments = itertools.cycle([0, 1])
    for player in subsession.get_players():
        player.treatment = next(treatments)

# PAGES
class Instructions(Page):
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

class Instructions_send(Page):
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

class Instructions_send_payoff_A(Page):
    def is_displayed(player: Player):
        return player.subsession.round_number == 1 and player.treatment == 0

class Instructions_send_payoff_B(Page):
    def is_displayed(player: Player):
        return player.subsession.round_number == 1 and player.treatment == 1

class MyPage_A(Page):
    form_model = 'player'
    form_fields = ['t_selection', 'n_selection']

    @staticmethod
    def vars_for_template(player: Player):
        import time
        o_v = np.random.permutation([4, 5, 6, 7, 8, 9, 10, 11])
        o_h = np.random.permutation([0, 1, 2, 3])
        lr = np.random.permutation([0, 1])[0] #answer to question: Is det on the right?
        o = np.append(o_h, o_v)  # reordering of columns
        o = np.append(o, np.array([12]))
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
        d_plus = nb_d1[player.round_number-1][o]
        d_minus = nb_d2[player.round_number-1][o]
        d_join = nb_d3[player.round_number-1][o]
        s_plus = nb_s1[player.round_number-1][o]
        s_minus = nb_s2[player.round_number-1][o]
        s_join = nb_s3[player.round_number-1][o]

        #randomize column order

        nb_d = [d_plus, d_minus, d_join]
        nb_s = [s_plus, s_minus, s_join]
        rand = np.random.permutation([0, 1, 2])
        if lr == 0:
            nb_1 = [nb_d[rand[0]], nb_s[rand[0]]]
            nb_2 = [nb_d[rand[1]], nb_s[rand[1]]]
            nb_3 = [nb_d[rand[2]], nb_s[rand[2]]]
        else:
            nb_1 = [nb_s[rand[0]], nb_d[rand[0]]]
            nb_2 = [nb_s[rand[1]], nb_d[rand[1]]]
            nb_3 = [nb_s[rand[2]], nb_d[rand[2]]]
        plus = np.where(rand==0)[0][0]+1
        join = np.where(rand==2)[0][0]+1
        player.starttime = int(time.time())

        #save player setup
        player.o = str(o)
        player.lr = str(lr)
        player.nb = str([plus, join])

        if lr == 0:
            e = ['Immer, wenn NB', 'Fast immer, wenn NB']
        else:
            e = ['Fast immer, wenn NB', 'Immer, wenn NB']

        return dict(
            hb=hb,
            nb_1=nb_1,
            nb_2=nb_2,
            nb_3=nb_3,
            round=player.round_number,
            plus = plus,
            join = join,
            lr = lr,
            lr_1 = 1-lr,
            e = e
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import time
        player.finishtime = int(time.time())


class Quiz(Page):
    form_model = 'player'
    form_fields = ['quiz1', 'quiz2', 'quiz3', 'quiz4', 'quiz5', 'quiz6', 'quiz7']

    @staticmethod
    def error_message(player: Player, values):
        if player.treatment == 0:
            solutions = dict(quiz1='Falsch', quiz2='Falsch', quiz3='Richtig', quiz4='Richtig', quiz5='...eine 1 verbirgt.', quiz6='Test', quiz7='Falsch')
        else:
            solutions = dict(quiz1='Falsch', quiz2='Falsch', quiz3='Richtig', quiz4='Richtig', quiz5='...eine 1 verbirgt.', quiz6='Test', quiz7='Richtig')

        if values != solutions:
            return "Eine oder mehrere Antworten waren leider falsch."

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Instructions, Instructions_send, Instructions_send_payoff_A, Instructions_send_payoff_B, Quiz, MyPage_A]
