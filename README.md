# GitHub 周报生成器

## About
基于 [GitHub GraphQL API](https://docs.github.com/en/graphql)，帮你生成接近「平均水平」(doge) 的周报。


## Usage

```bash
python wr.py --account_name 'GitHub Username' --token 'Your GitHub Token' 
```

使用 `python wr.py --help` 查看详细指令。


## Notes

- 暂不支持超过100个分支的仓库。
- 结果包括私有仓库，公开时请注意隐私安全。


## Why use GraphQL API

[GraphQL API](https://docs.github.com/en/graphql) (GitHub API v4) 相比于 [REST API](https://docs.github.com/en/rest) 更为优雅，但是写起来也比后者复杂一些。

## GitLab

这里只给出一个基于 `git log` 的实现。将 `wr.sh` 放置在根目录，然后运行即可。类似于
```
├── Weekly-Report-Generator/
│   ├── .git/
│   └── ...
├── ftp/
│   ├── .git/
│   └── ...
├── ...
└── wr.sh
```

接着执行指令

```bash
bash wr.sh
```

需要保证的是，各仓库均已拉取各分支最新的更改，可使用如下代码拉取某个仓库所有分支的更改

```bash
git branch -r | grep -v '\->' | while read remote; do git branch --track "${remote#origin/}" "$remote"; done
git fetch --all 
git pull --all
```

`wr.sh` 中的 `--author` 代表是否指定提交人的信息，生成个人周报的时候可以取消注释。

**请注意**

GitLab 常规用户拥有的权限非常有限，很难使用 `GitLab GraphQL API` 去查询 commits，`GitLab REST API` 会是更好的选择。如有需要请自行查阅 [API Docs | GitLab](https://docs.gitlab.com/ee/api/)。

另一方面，如果你的仓库内容不涉密，可以使用 [GitLab CI](https://docs.gitlab.com/ee/ci/) 等工具，在 GitLab 上更新时同步更新到 GitHub 的私有仓库中，也可以达到同样的效果。


## Create a token

需要 `token` 才能与GitHub GraphQL 服务器通信。

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


## To-do

- [ ] Issues, PR, Repo Creation as contribution


## An Example

[一个生成的「半年」报](WeeklyReport.md)



