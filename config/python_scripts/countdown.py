events = (
    ('james', 'jbday', datetime.datetime(year, month, day)),
    ('tina', 'tbday', datetime.datetime(year, month, day)),
    ('jackson', 'jackbday', datetime.datetime(year, month, day)),
    ('hudson', 'hbday', datetime.datetime(year, month, day)),
    ('wedding', 'waday', datetime.datetime(year, month, day)),
)

now = datetime.datetime.now()
for _, event, event_date in events:
    diff = event_date - now
    hass.states.set('.'.join(['sensor', event]), diff.days, {
        'unit_of_measurement': 'days',
        'friendly_name': 'Days until {}'.format(event),
        'icon': 'mdi:calendar'
    })
