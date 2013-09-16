expected = dict(
    name='your_app',
    dir={
        '__init__': {
            'name': '__init__.py'
        },
        'views': {
            'name': 'views.py',
        },
        'expected': {
            'name': 'expected.py',
        },
        'templates': {
            'dir': {
                'your_app': {
                    'dir': {
                        'base': {
                            'name': 'base.html',
                        }
                    }
                }
            },
        },
    },
    views={
        'functions': [
            {
                'name': 'some_view',
            }
        ],
        'classes': [
            {
                'name': 'SomeView',
            }
        ]
    },
)
