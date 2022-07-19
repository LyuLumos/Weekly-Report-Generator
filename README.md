# GitHub 周报生成器

## About
基于 [GitHub GraphQL API](https://docs.github.com/en/graphql)，帮你生成接近「平均水平」(doge) 的周报。


## Usage

```bash
python wr.py --account_name "GitHub Username" --token 'Your GitHub Token' 
```
也可以使用如下命令查看详细指令。

```bash
python wr.py --help
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

[GraphQL API](https://docs.github.com/en/graphql) (Github API v4) 相比于 [REST API](https://docs.github.com/en/rest) 更为优雅，但是写起来也比后者复杂一些。


## To-do

- GitLab Support
- Issues, PR, Repo as contribution


## An Example

[一个生成的「半年」报](WeeklyReport.md)



