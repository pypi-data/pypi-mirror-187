import threading
from datetime import datetime, timedelta

from fyers_api_builder.libs.generate_payload import generate_payload
from fyers_api_builder.libs.generate_tasks import generate_tasks


class GetHistoryData:
    data_available_from = datetime.fromisoformat("2017-05-01")
    today = datetime.today()
    yesterday = today - timedelta(days=1)

    def __init__(
        self, client, symbol, resolution, date_format, fetch_from_epoch, fetch_to_epoch
    ):
        self.client = client

        self.symbol = symbol
        self.resolution = resolution
        self.date_format = date_format
        self.fetch_from_epoch = fetch_from_epoch
        self.fetch_to_epoch = fetch_to_epoch

        self.results = []

    def get_data(
        self, symbol, resolution, date_format, fetch_from_epoch, fetch_to_epoch
    ):
        payload = generate_payload(
            symbol, resolution, date_format, fetch_from_epoch, fetch_to_epoch
        )

        data = self.client.history(payload)

        items = data["candles"]

        for item in items:
            if item not in self.results:
                self.results.append(item)

    def run_filters(self):
        if self.fetch_from_epoch < int(self.data_available_from.timestamp()):
            raise Exception(
                "Data only available from %s"
                % self.data_available_from.strftime("%Y-%m-%d")
            )

    def run(self):
        self.run_filters()

        tasks = generate_tasks(self.fetch_from_epoch, self.fetch_to_epoch)

        for task in tasks:
            download_thread = threading.Thread(
                target=self.get_data,
                args=(
                    self.symbol,
                    self.resolution,
                    self.date_format,
                    task["fetch_from_epoch"],
                    task["fetch_to_epoch"],
                ),
            )

            download_thread.start()
            download_thread.join()

        return self.results
