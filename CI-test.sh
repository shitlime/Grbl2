# 1. 安装pdm
python -m pip install pipx
pipx install pdm
pipx upgrade-all

# 2. 安装依赖
pdm sync

# 3. 运行项目
cp bot_config.yaml grbl_config.yaml
# 尝试运行120s后退出，若时长120s，返回0；若不足120s，返回不为0
timeout 120s pdm run ./bot.py
exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo "程序测试出错！（在规定测试时间内退出）请检查输出的信息 $exit_code"
    exit $exit_code
else
    echo "程序测试完成！ (在规定测试时间内没有退出）"
    exit 0
fi