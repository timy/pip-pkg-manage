A simple Python package manager based on the `pip` command.

On Linux platforms, some Python packages come pre-installed with the system. The system-wide upgrade with `sudo pip install package --upgrade` may break dependencies and result in serious system issues.
Therefore, it is generally recommended to use virtual environments (venv, conda, etc.) or install required Python packages only at the user level (without using `sudo` privileges). For the latter case, the system default packages and the ones from user's installation somehow are mixed, making it difficult to manage when package candidates are available for upgrade.

This script provides a simple package manager, upgrading only packages installed by users and keeping system's default packages intact. It also offers tools to
- list user-installed packages to upgrade,
- illustrate the dependencies among all packages with generated graph ([Graphviz](https://graphviz.org/)), showing system default and user-installed packages with different node colors.

一个简单的基于 pip 命令的 Python 包管理器。

Linux 平台上，系统会自带一些 Python 包，如果使用 `sudo` 权限通过 `pip` 在系统范围升级这些 Python 包，可能会形成依赖错误，造成严重的系统问题。
所以一般会考虑使用虚拟环境（venv, conda等），或仅在用户级别安装需要的 Python 包（不使用 `sudo` 权限）。
对于后者，系统自带的包与用户级别的包混杂在一起，特别是在有可升级包的时候难以区分，不易管理。

这里的脚本提供一个简单的管理方案，只升级用户个人安装的包，而不影响系统自带的包。同时还提供方便的查看工具：
- 列出将升级的包。
- 绘制所有包的依赖关系，并用节点颜色区分系统自带包与用户安装包（需安装 [Graphviz](https://graphviz.org/)）。