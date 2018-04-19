import requests
from urllib.parse import urljoin
from datetime import datetime, timedelta

from constants import (
    API_BASE,
    REPOS_PATH,
    QUERY_PARAMS
)


def build_week_ago_q_param():
    week_ago_date = datetime.today() - timedelta(days=7)
    week_ago_str = week_ago_date.strftime('%Y-%m-%d')
    q_param = 'created:>{}'.format(week_ago_str)
    return {'q': q_param}


def get_trending_repositories(url, params=None):
    response = requests.get(url, params=params)
    if not response.ok:
        return

    response_data = response.json()
    return response_data.get('items')


def print_repos(repos_list):
    print('MOST RATED REPOS')
    print('{:^90} | {:^10} | {:^10}'.format('Url', 'Stars', 'Issues'))
    print('-' * 116)
    row_template = '{url:<90} | {stars:^10} | {issues:^10}'
    for repo in repos_list:
        print(
            row_template.format(
                url=repo['html_url'],
                stars=repo['stargazers_count'],
                issues=repo['open_issues'],
            )
        )


if __name__ == '__main__':
    url = urljoin(API_BASE, REPOS_PATH)
    q_param = build_week_ago_q_param()
    params = QUERY_PARAMS.copy()
    params.update(q_param)

    repos_items = get_trending_repositories(url, params=params)
    if repos_items:
        print_repos(repos_items)
    else:
        print('There are no repositories found')
