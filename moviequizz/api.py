"""Testing the authentication on Slack API."""
import aiohttp
import os


async def api_call(method, data=None):
    """Slack API call."""
    with aiohttp.ClientSession() as session:
        token = os.environ.get('TOKEN')
        if not token.startswith('xoxb-'):
            return 'Define the token please'
        form = aiohttp.FormData(data or {})
        form.add_field('token', token)
        async with session.post('https://slack.com/api/{0}'.format(method),data=form) as response:
            assert 200 == response.status, ('{0} with {1} failed.'.format(method, data))
            return await response.json()