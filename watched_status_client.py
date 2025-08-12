import zmq


class WatchedStatusClient:
    def __init__(self, endpoint="tcp://localhost:5557"):
        self.endpoint = endpoint
        self._context = zmq.Context.instance()
        self._socket = self._context.socket(zmq.REQ)
        self._socket.connect(self.endpoint)

    def _send_request(self, data):
        """Send a request to the watched status tracker service and wait for response."""
        try:
            self._socket.send_json(data)

            # wait 2 seconds for response
            if self._socket.poll(1500):
                response = self._socket.recv_json()
                return response
            else:
                return None
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"Error sending request to persistence service: {e}")
            return None

    def mark_watched(self, title, rating=None, watch_date=None):
        """Mark a movie as watched."""

        request_data = {
            "action": "mark_watched",
            "version": 1,
            "title": title
        }

        if rating is not None:
            request_data["rating"] = rating
        if watch_date is not None:
            request_data["watch_date"] = watch_date

        response = self._send_request(request_data)
        return response and response.get("status") == "success"

    def mark_unwatched(self, title, rating=None, watch_date=None):
        """Mark a movie as unwatched."""

        request_data = {
            "action": "mark_unwatched",
            "version": 1,
            "title": title
        }

        if rating is not None:
            request_data["rating"] = rating
        if watch_date is not None:
            request_data["watch_date"] = watch_date

        response = self._send_request(request_data)
        return response and response.get("status") == "success"

    def get_status(self, title):
        """Get the watch status of a movie."""
        response = self._send_request({
            "action": "get_status",
            "version": 1,
            "title": title
        })

        if response and response.get("status") == "success":
            return {
                "watched": response.get("watched", False),
                "rating": response.get("rating"),
                "watch_date": response.get("watch_date")
            }
        return None

    def get_all_movies(self):
        """Get all movies and their watch status."""
        response = self._send_request({
            "action": "get_all_movies",
            "version": 1
        })

        if response and response.get("status") == "success":
            return response.get("movies", [])
        return None

    def get_unwatched_movies(self):
        """Get a list of the unwatched movies only"""
        all_movies = self.get_all_movies()
        if all_movies is None:
            return []
        return [movie for movie in all_movies if not movie.get("watched", False)]

    def get_watched_movies(self):
        """Get a list of the watched movies only"""
        all_movies = self.get_all_movies()
        if all_movies is None:
            return []
        return [movie for movie in all_movies if movie.get("watched", False)]

    def get_unwatched_from_list(self, movie_list):
        """Filter a specific list to show the unwatched movies only."""
        response = self._send_request({
            "action": "get_unwatched_from_list",
            "version": 1,
            "movie_list": movie_list
        })

        if response and response.get("status") == "success":
            return response.get("unwatched_movies", [])
        print("Note: Watch status service unavailable. Showing all movies.")
        return movie_list

    def get_watched_from_list(self, movie_list):
        """Filter a specific list to show the watched movies only."""
        response = self._send_request({
            "action": "get_watched_from_list",
            "version": 1,
            "movie_list": movie_list
        })

        if response and response.get("status") == "success":
            return response.get("watched_movies", [])
        print("Note: Watch status service unavailable. Cannot verify watched movies.")
        return []

    def filter_by_status(self, movie_list, watched=True):
        """Filter a movie list by watch status"""
        response = self._send_request({
            "action": "filter_by_status",
            "version": 1,
            "movie_list": movie_list,
            "watched": watched
        })

        if response and response.get("status") == "success":
            return response.get("filtered_movies", [])
        return movie_list if not watched else []

    def close(self):
        if hasattr(self, '_socket'):
            self._socket.close()

    def __del__(self):
        self.close()