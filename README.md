# GitHub 周报生成器

## About
基于 [GitHub GraphQL API](https://docs.github.com/en/graphql)，帮你生成接近「平均水平」(doge) 的周报。


## Usage

```bash
python wr.py --account_name 'GitHub Username' --token 'Your GitHub Token' 
```

详细指令如下


```
usage: wr.py [-h] [--account_name ACCOUNT_NAME] [--user_name USER_NAME]
             [--token TOKEN] [--days DAYS] [--endpoint ENDPOINT]
             [--branch {all,default}]

optional arguments:
  -h, --help            show this help message and exit
  --account_name ACCOUNT_NAME
                        GitHub account name
  --user_name USER_NAME
                        The name displayed on GitHub
  --token TOKEN         Your personal token
  --days DAYS           The time range of your contributions
  --endpoint ENDPOINT   The GitHub GraphQL endpoint
  --branch {all,default}
                        Whether the scope covers all branches or the default
                        branch
```

## Notes

- 暂不支持超过100个分支的仓库，如有需要可自行进行修改。
- 结果包括私有仓库，公开时请注意隐私安全。


## Create a token

需要 `token` 才能与 GraphQL 服务器通信。

`Settings` > `Developer settings` > `Personal access tokens` > `Generate new token`

生成时需要勾选的项
```
repo
repo_deployment
read:packages
read:org
read:public_key
read:repo_hook
user
read:discussion
read:enterprise
read:gpg_key
```


## Why use GraphQL API

[GraphQL API](https://docs.github.com/en/graphql) (GitHub API v4) 相比于 [REST API](https://docs.github.com/en/rest) 更为优雅，但是写起来也比后者复杂一些。

## GitLab: Not Support

当前仓库不支持 GitLab。GitLab 常规用户拥有的权限非常有限，很难使用 `GitLab GraphQL API` 去查询 commits，`GitLab REST API` 会是更好的选择。如有需要请自行查阅 [API Docs | GitLab](https://docs.gitlab.com/ee/api/)。

另一方面，如果你的仓库内容不涉密，可以使用 [GitLab CI](https://docs.gitlab.com/ee/ci/) 等工具，在 GitLab 上更新时同步更新到 GitHub 的私有仓库中，也可以达到同样的效果。



## To-do

- [ ] Issues, PR, Repo Creation as contribution


## An Example

[一个生成的「半年」报](WeeklyReport.md)



