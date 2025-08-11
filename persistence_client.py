import zmq


class PersistenceClient:
    def __init__(self, endpoint="tcp://localhost:5555"):
        self.endpoint = endpoint
        self._context = zmq.Context.instance()
        self._socket = self._context.socket(zmq.REQ)
        self._socket.connect(self.endpoint)

    def _send_request(self, data):
        """Send a request to the persistence service and wait for response."""
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

    def close(self):
        # manually close socket connection
        if hasattr(self, '_socket'):
            self._socket.close()

    def __del__(self):
        self.close()

    def save_watchlist(self, items):
        """Send list to microservice and return True if reply is "success" or otherwise return False"""
        response = self._send_request({"action": "save", "version": 1, "items": items})
        if response and response.get("status") == "success":
            return True
        return False

    def load_watchlist(self):
        """Send load request to microservice and return list if reponse is "success" otherwise return None"""
        response = self._send_request({"action": "load", "version": 1})
        if response and response.get("status") == "success":
            items = response.get("items", [])
            if isinstance(items, list):
                return items
        return None
