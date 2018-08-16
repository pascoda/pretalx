from django.conf.urls import include, url

from pretalx.common.views import get_static
from pretalx.event.models.event import SLUG_CHARS

from .views import feed, schedule, sneakpeek, speaker, talk


def get_schedule_urls(regex_prefix, name_prefix=""):
    """
    given a prefix (e.g. /schedule) generate matching schedule-ruls (e.g. /schedule.json, /schedule/feed.xml, ...)
    """

    regex_prefix = regex_prefix.rstrip('/')

    return [
        url(f'{regex_prefix}{regex}', view, name=f'{name_prefix}{name}')
        for regex, view, name in [
            ('/$', schedule.ScheduleView.as_view(), 'schedule'),
            ('.xml$', schedule.ExporterView.as_view(), 'core-frab-xml'),
            ('.xcal$', schedule.ExporterView.as_view(), 'core-frab-xcal'),
            ('.json$', schedule.ExporterView.as_view(), 'core-frab-json'),
            ('.ics$', schedule.ExporterView.as_view(), 'core-iCal'),
            ('/export$', schedule.ExporterView.as_view(), 'export'),
            ('/feed.xml$', feed.ScheduleFeed(), 'feed'),
        ]
    ]


app_name = 'agenda'
urlpatterns = [
    url(
        fr'^(?P<event>[{SLUG_CHARS}]+)/',
        include(
            [
                url(
                    r'^schedule/changelog$',
                    schedule.ChangelogView.as_view(),
                    name='schedule.changelog',
                ),
                *get_schedule_urls('^schedule'),
                *get_schedule_urls('^schedule/v/(?P<version>.+)', 'versioned-'),
                url(r'^sneak/$', sneakpeek.SneakpeekView.as_view(), name='sneak'),
                url(r'^talk/(?P<slug>\w+)/$', talk.TalkView.as_view(), name='talk'),
                url(
                    r'^talk/(?P<slug>\w+)/feedback/$',
                    talk.FeedbackView.as_view(),
                    name='feedback',
                ),
                url(
                    r'^talk/(?P<slug>\w+).ics$',
                    talk.SingleICalView.as_view(),
                    name='ical',
                ),
                url(
                    r'^talk/review/(?P<slug>\w+)$',
                    talk.TalkReviewView.as_view(),
                    name='review',
                ),
                url(
                    r'^speaker/(?P<code>\w+)/$',
                    speaker.SpeakerView.as_view(),
                    name='speaker',
                ),
                url(
                    r'^speaker/(?P<code>\w+)/talks.ics$',
                    speaker.SpeakerTalksIcalView.as_view(),
                    name='speaker.talks.ical',
                ),
            ]
        ),
    ),
    url(
        r'^sw.js',
        get_static,
        {
            'path': 'agenda/js/serviceworker.js',
            'content_type': 'application/javascript',
        },
    ),
]
