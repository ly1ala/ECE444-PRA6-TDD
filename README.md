# ECE444 PRA6 — TDD and Web App Deployment

A Flask blogging app for ECE444 PRA6. Users can view and search posts, log in and out, and add or delete posts while logged in.

Adapted from the [course tutorial](https://github.com/shuruizUofT/flaskr-tdd). The original MIT license is retained in LICENSE.

## Open the website / 如何打开网站

### Render website / 已部署的线上网站

Click [Open the live website](https://ece444-pra6-tdd-1rrg.onrender.com/) or [Open the login page](https://ece444-pra6-tdd-1rrg.onrender.com/login).

直接点击上面的链接即可使用，不需要在电脑上启动程序。免费服务休眠后，第一次打开可能需要等待约一分钟。

Hosted on Render with PostgreSQL. Use username `admin` and the current password configured privately in Render (`APP_PASSWORD`). Do not publish the password in this repository.

线上用户名为 `admin`，密码使用 Render 中设置的值。

### Local website / 在自己的电脑上打开

Open this project folder in VS Code, then open **Terminal → New Terminal**. Run the following commands from the project root on macOS/Linux:

在 VS Code 中打开项目文件夹，再打开终端，在项目根目录执行：

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python create_db.py
python -m flask --app project.app run --port 5001
```

Open [the local website](http://localhost:5001/) in your browser. Keep the terminal running; press **Ctrl+C** to stop the server. The default local login is `admin` / `admin`, unless you set `APP_USERNAME` or `APP_PASSWORD` in your terminal environment.

浏览器打开 http://localhost:5001/，保持终端运行。默认本地账号和密码都是 `admin`。本地默认使用 SQLite，与线上 PostgreSQL 的帖子数据独立。

For later visits, start the local server again from the project root:

以后再次打开本地网站，只需在项目根目录执行：

```sh
source .venv/bin/activate
python -m flask --app project.app run --port 5001
```

### Render dashboard / 部署管理页面

The owner can sign in to [Render service dashboard](https://dashboard.render.com/web/srv-dbd5luo473hc73dghn40) to inspect deployment status and logs, or open [Environment settings](https://dashboard.render.com/web/srv-dbd5luo473hc73dghn40/env) to manage environment variables.

项目所有者登录 Render 后，可在以上页面查看部署日志和环境变量。更新代码并 push 到 GitHub 后，在该服务中选择 **Manual Deploy → Deploy latest commit**，等待状态显示 **Live**，然后刷新线上网站。

The Render dashboard requires account access; it is separate from the public website. A README-only update does not require redeploying the app.

## Run tests

```sh
python -m pytest -v
```

The suite contains 13 cases covering the homepage, database, login/logout, posting, deletion, search, and login protection. Each test uses an isolated temporary SQLite database.

## Deploy on Render

- Build command: `pip install -r requirements.txt`
- Start command: `python create_db.py && gunicorn project.app:app --bind 0.0.0.0:$PORT`
- Set `DATABASE_URL` to your PostgreSQL connection URL.
- Set `SECRET_KEY`, `APP_USERNAME`, and `APP_PASSWORD` privately in Render.
- Without `DATABASE_URL`, the app uses local SQLite at `project/flaskr.db`.

See [PRA6_GUIDE.md](PRA6_GUIDE.md) for deployment instructions, test explanations, and the TA demonstration checklist. Homepage, login/logout, posting, search, deletion, and unauthorized deletion protection were verified on the live website on October 22, 2026.

## Project files

- `project/`: routes, database model, HTML templates, CSS, and JavaScript.
- `tests/`: automated tests.
- `create_db.py`: creates database tables.
- `requirements.txt`, `Procfile`, `runtime.txt`: dependencies and deployment configuration.
- `.github/workflows/test.yml`: GitHub test workflow.
- `.gitignore`: excludes virtual environments, local databases, caches, and secrets.
