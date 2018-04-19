import requests
from urllib.parse import urljoin
from datetime import date, timedelta
from itertools import filterfalse

from constants import (
    API_BASE,
    REPOS_PATH,
    OUTPUT_TABLE_WIDTH
)


def build_week_ago_q_param():
    week_ago_date = date.today() - timedelta(days=7)
    week_ago_str = week_ago_date.isoformat()
    q_param = 'created:>{}'.format(week_ago_str)
    return {'q': q_param}


def get_trending_repositories(url, number_repos=20):
    query_params = {
        'sort': 'stars',
        'order': 'desc',
        'per_page': number_repos
    }
    q_param = build_week_ago_q_param()
    query_params.update(q_param)

    response = requests.get(url, params=query_params)
    if not response.ok:
        return

    response_data = response.json()
    return response_data.get('items')


def get_open_issues_for_repo(repo_url):
    """ Gets number of open issues for repository without pull requests """
    full_url = '{}{}'.format(repo_url, '/issues')
    repos_response = requests.get(full_url)

    if not repos_response.ok:
        return

    repos_data = repos_response.json()
    filtered_repos_list = list(
        filterfalse(lambda issue: 'pull_request' in issue, repos_data)
    )
    return len(filtered_repos_list)


def print_repos(repos_list):
    print('THE MOST RATED FRESH REPOSITORIES')
    print('{:^90} | {:^10} | {:^10}'.format('Url', 'Stars', 'Issues'))
    print('-' * OUTPUT_TABLE_WIDTH)
    row_template = '{url:<90} | {stars:^10} | {issues:^10}'
    for repo in repos_list:
        print(
            row_template.format(
                url=repo['html_url'],
                stars=repo['stargazers_count'],
                issues=repo['open_issues_w/o_pull'],
            )
        )


def add_issues_to_repos(repos_items, no_data_placeholder='n/a'):
    for repo in repos_items:
        repo_issues_number = get_open_issues_for_repo(repo.get('url'))
        if repo_issues_number is None:
            repo['open_issues_w/o_pull'] = no_data_placeholder
        else:
            repo['open_issues_w/o_pull'] = repo_issues_number
        yield repo


if __name__ == '__main__':
    url = urljoin(API_BASE, REPOS_PATH)
    repos_items = get_trending_repositories(url)

    if not repos_items:
        exit('There are no repositories found')

    repos_to_print = add_issues_to_repos(repos_items)
    print_repos(list(repos_to_print))
