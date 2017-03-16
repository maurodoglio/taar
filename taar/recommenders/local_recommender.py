import requests

ADDON_LIST_PER_LOCALE_URL =\
    "local address"
    # TODO: this should be a public s3 bucket IFF we are allowed to share this info publically.

def fetch_json(uri):
    """ Perform an HTTP GET on the given uri, return the results as json.
    If there is an error fetching the data, raise an exception.

    Args:
        uri: the string URI to fetch.

    Returns:
        A JSON object with the response.
    """
    data = requests.get(uri)
    # Raise an exception if the fetch failed.
    data.raise_for_status()
    return data.json()

class LocalRecommender:
    """ A recommender class that returns top N addons based on the geo-locale associated with the client info.
    This will load a json file containing updated top n addons in use per geo locale updated periodically
    by a separate process on airflow using Longitdudinal Telemetry data.

    This recommender may provide useful recommendations when collaborative_recommender may not work
    """
    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        # Download the JSON containing up-to-date addons per locale
        return fetch_json(ADDON_LIST_PER_LOCALE_URL)

    def can_recommend(self, client_data):
        # We can't recommend if we don't have our data files.
        if self.top_addons_per_local is None:
            return False

        if len(self.top_addons_per_local[client_data.get('settings.locale', [])]) > 0:
            return True
        # some addons are available for this locale
        return False

    def recommend(self, client_data, limit):
        client_locale = client_data.get('settings.locale')
        top_n_dict = self._load_model()
        # TODO: do we want to truncate this?
        return top_n_dict[client_locale]
