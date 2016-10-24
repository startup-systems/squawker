# https://github.com/cobrateam/splinter/issues/515

from urllib import parse

from splinter.browser import _DRIVERS
from splinter.driver import flaskclient

__all__ = ['FlaskClient']


class FlaskClient(flaskclient.FlaskClient):
    """
    A patched `FlaskClient` driver that implements more standard `302`/`303`
    behaviour and that sets data for `GET` requests against the URL.
    """

    driver_name = 'flask'

    def _do_method(self, method, url, data=None):

        # Set the initial URL and client/HTTP method
        self._url = url
        func_method = getattr(self._browser, method.lower())

        # Continue to make requests until a non 30X response is recieved
        while True:
            self._last_urls.append(url)

            # If we're making a GET request set the data against the URL as a
            # query.
            if method.lower() == 'get':

                # Parse the existing URL and it's query
                url_parts = parse.urlparse(url)
                url_params = parse.parse_qs(url_parts.query)

                # Update any existing query dictionary with the `data` argument
                url_params.update(data or {})
                query = parse.urlencode(url_params, doseq=True)
                url_parts = url_parts._replace(query=query)

                # Rebuild the URL
                url = parse.urlunparse(url_parts)

                # As the `data` argument will be passed as a keyword argument to
                # the `func_method` we set it `None` to prevent it populating
                # `flask.request.form` on `GET` requests.
                data = None

            # Call the flask client
            self._response = func_method(
                url,
                headers=self._custom_headers,
                data=data,
                follow_redirects=False
            )

            # Implement more standard `302`/`303` behaviour
            if self._response.status_code in (302, 303):
                func_method = getattr(self._browser, 'get')

            # If the response was not in the `30X` range we're done
            if self._response.status_code not in (301, 302, 303, 305, 307):
                break

            # If the response was in the `30X` range get next URL to request
            url = self._response.headers['Location']

        self._url = self._last_urls[-1]
        self._post_load()


# Patch the default `FlaskClient` driver
_DRIVERS['flask'] = FlaskClient
