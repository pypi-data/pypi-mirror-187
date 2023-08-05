from datetime import date

import requests


class Gist:
    def __init__(self, name: str, token: str, gist_id: str, filename: str):
        self.token = token
        self.gist_id = gist_id
        self.filename = filename
        self.name = name

    def separate(self, statistics: dict, delimiter: str, length: int) -> str:
        result = ''

        for stat, value in statistics.items():
            result += stat + ' ' + (delimiter * (length - len(stat)))
            result += f' {value}\n'

        return result

    def update(self, statistics, delimiter='.', length=15):
        content = self.separate(statistics, delimiter, length)
        response = requests.patch(
            url='https://api.github.com/gists/' + self.gist_id,
            json={
                'description': 'Updated on ' + str(date.today()),
                'files': {
                    self.filename: {'content': content}
                }
            },
            auth=(self.name, self.token)
        )

        return response.status_code
