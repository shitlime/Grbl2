cp bot_config.yaml grbl_config.yaml
timeout 120s python ./bot.py  # 尝试运行120s后退出
exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo "Python程序出错: （在规定时间内退出）请检查输出的信息 $exit_code"
    exit $exit_code
else
    echo "Python程序测试完成！ (在规定时间内没有退出） "
    exit 0
fi