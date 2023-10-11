from os import environ


SESSION_CONFIGS = [
    dict(
        name='narr_pilot',
        display_name="Narr Pilot",
        app_sequence=['narr_sender', 'narr_receiver_ex1', 'results_and_demographics'],
        num_demo_participants=100,
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    {'limesurvey_link': 'https://limesurvey.urz.uni-heidelberg.de/index.php/886665?lang=de'},
    real_world_currency_per_point=3.00, participation_fee=1.50, doc="",
)

PARTICIPANT_FIELDS = ['true_y', 'payround', 'treatment']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ROOMS = [
    dict(
        name='Narratives_Pilot',
        display_name='Pilot for Narratives Experiment',
    )
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """


SECRET_KEY = '2721008047707'

INSTALLED_APPS = ['otree']
