import requests
import pytz
import datetime
import argparse


class GraphQLQuery:
    def __init__(self, account_name, token, github_endpoint, user_name=None):
        self.account_name = account_name
        self.user_name = user_name
        self.github_endpoint = github_endpoint
        self.token = token

    def run_query(self, query, variables=None):
        """
        It takes a query and variables as input, and returns the JSON response from the GitHub GraphQL API

        :param query: The query string
        :param variables: A dictionary of variables to pass to the query
        :return: A JSON object
        """
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json',
                   'Authorization': 'token {}'.format(self.token)}
        data = {'query': query, 'variables': variables}
        req = requests.post(url=self.github_endpoint,
                            json=data, headers=headers)
        return req.json()

    def query_commit_repo(self, user, lmt):
        """
        It takes a user and a time limit as input and returns a list of urls of the repositories that
        the user has committed to in the limited time.

        :param user: The user you want to query
        :param lmt: Tthe time limit for the query
        :return: A list of urls
        """
        query = '''
        query($user: String!, $time_limit: DateTime!){
          user(login: $user) {
            contributionsCollection(from: $time_limit) {
              commitContributionsByRepository {
                repository {
                  url
                }
              }
            }
          }
        }
        '''
        variables = {
            'user': user,
            'time_limit': lmt
        }
        urls_json = self.run_query(query=query, variables=variables)
        # print(urls_json)
        urls = urls_json['data']['user']['contributionsCollection']['commitContributionsByRepository']
        return [i['repository']['url'] for i in urls]

    def query_repo_defaultbranch_commits(self, owner, repo, lmt):
        """
        It takes in the owner of the repo, the repo name, and a time limit and
        returns a list, where each sublist contains the commit message and the commit URL on default branch

        :param owner: The owner of the repository
        :param repo: the name of the repository
        :param lmt: the time limit for the query
        :return: A list of lists. Each list contains the commit message and the commit URL.
        """
        query = '''
        query($owner: String!, $repo: String!, $time_limit: GitTimestamp!){
          repository(owner: $owner, name: $repo) {
            defaultBranchRef {
              target {
                ... on Commit {
                  history(since: $time_limit) {
                    nodes {
                      author {
                        name
                      }
                      commitUrl
                      message
                      committedDate
                    }
                    totalCount
                  }
                }
              }
            }
          }
        }
        '''
        variables = {
            'owner': owner,
            'repo': repo,
            'time_limit': lmt
        }
        commits_json = self.run_query(query=query, variables=variables)
        # print(commits_json)
        commits = commits_json['data']['repository']['defaultBranchRef']['target']['history']['nodes']
        return [[i['message'], i['commitUrl'], repo] for i in commits if i['author']['name'] in [self.account_name, self.user_name]]

    def query_repo_all_branches(self, owner, repo):
        """
        It takes in a repo name and owner, and returns a list of all the branches in that repo

        :param owner: The owner of the repository
        :param repo: The name of the repository
        :return: A list of branches
        """
        query = '''
        query($owner: String!, $repo: String!){
          repository(owner: $owner, name: $repo) {
            refs(refPrefix: "refs/heads/", first: 10) {
              edges {
                node {
                  branchName: name
                }
              }
            }
          }
        }
        '''
        variables = {
            'owner': owner,
            'repo': repo
        }
        branches_json = self.run_query(query=query, variables=variables)
        branches = branches_json['data']['repository']['refs']['edges']
        return [i['node']['branchName'] for i in branches]

    def query_repo_allbranch_commits(self, owner, repo, lmt, branch_name):
        query = '''
        query($owner: String!, $repo: String!, $time_limit: GitTimestamp!, $branch_name: String!){
          repository(owner: $owner, name: $repo) {
            ref(qualifiedName: $branch_name) {
              target {
                ... on Commit {
                  history(since: $time_limit) {
                    nodes {
                      author {
                        name
                      }
                      commitUrl
                      message
                      committedDate
                    }
                    totalCount
                  }
                }
              }
            }
          }
        }
        '''
        variables = {
            'owner': owner,
            'repo': repo,
            'time_limit': lmt,
            'branch_name': branch_name
        }
        commits_json = self.run_query(query=query, variables=variables)
        # print(commits_json)
        commits = commits_json['data']['repository']['ref']['target']['history']['nodes']
        return [[i['message'], i['commitUrl'], branch_name] for i in commits if i['author']['name'] in [self.account_name, self.user_name]]


def time_limit(days=7):
    """
    It takes the current time, subtracts N days from it, and returns the current time and the time N
    days ago in the format that the API expects

    :param days: The number of days to go back in time, defaults to 7 (optional)
    :return: A tuple of two strings.
    """
    current_time = datetime.datetime.now(pytz.utc)
    delta = datetime.timedelta(days=days)
    lmt = current_time - delta
    fmt = '%Y-%m-%dT%H:%M:%SZ'
    return current_time.strftime(fmt), lmt.strftime(fmt)


def gen_markdown(begin_time, end_time, res):
    """
    It takes the beginning and ending time of the week, and the result of the previous function, and
    generates a markdown file

    :param begin_time: the start time of the report
    :param end_time: the end time of the report, in the format of '%Y-%m-%dT%H:%M:%SZ'
    :param res: a dictionary of the form {repo_name: [(commit_message, commit_link, branch_name), ...], ...}
    """
    f = open("WeeklyReport.md", "w", encoding='utf-8')
    print('# Weekly Report', file=f)
    for repo, commits_info in res.items():
        print('## {repo_name}'.format(repo_name=repo), file=f)
        for commits in commits_info:
            short_title = commits[2] + '@' + commits[1].split('/')[-1][:8]
            print('- [{title}]({link}) {commit_message}'.format(title=short_title,
                  link=commits[1], commit_message=commits[0].replace('\n', ' ')), file=f)
    print(file=f)
    print('Collected from {begin_time} to {end_time}'.format(
        begin_time=begin_time, end_time=end_time), file=f)


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--account_name", help='GitHub account name')
    parser.add_argument("--user_name", default=None,
                        help='The name displayed on Github')
    parser.add_argument("--token", help='Your personal token')
    parser.add_argument("--days", type=int, default=7,
                        help='The time range of your contributions')
    parser.add_argument("--endpoint", default='https://api.github.com/graphql',
                        help='The GitHub GraphQL endpoint')
    parser.add_argument('--branch', choices=['all', 'default'], default='all',
                        help='Whether the scope covers all branches or the default branch')
    return parser.parse_args()


if __name__ == "__main__":
    args = arguments()
    cur_time, time_lmt = time_limit(args.days)
    test = GraphQLQuery(args.account_name, args.token,
                        args.endpoint, args.user_name)
    repo_urls = test.query_commit_repo(args.account_name, time_lmt)
    res = {}

    if args.branch == 'default':
        for repo_url in repo_urls:
            repo, owner = repo_url.split('/')[-1], repo_url.split('/')[-2]
            res[repo] = test.query_repo_defaultbranch_commits(
                owner, repo, time_lmt)
        print(res)
        gen_markdown(time_lmt, cur_time, res)

    elif args.branch == 'all':
        for repo_url in repo_urls:
            repo, owner = repo_url.split('/')[-1], repo_url.split('/')[-2]
            branches = test.query_repo_all_branches(owner, repo)
            res[repo] = []
            for branch in branches:
                res[repo].extend(
                    test.query_repo_allbranch_commits(
                        owner, repo, time_lmt, branch)
                )
        print(res)
        gen_markdown(time_lmt, cur_time, res)
