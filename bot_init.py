# bot初始化模块
import yaml
import platform

class BotData(yaml.YAMLObject):
    yaml_tag = '!BotData'
    yaml_loader = yaml.SafeLoader
    def __init__(self) -> None:
        self.sys = platform.system()
        self.info = {}
        self.ariadne_config = {}
        self.admin = []
        self.cmd_prefix = []
        self.search_prefix = []
        self.modules = []
        self.modules_config = {}
    
    def __repr__(self):
        return f"""BotData(
            info={self.info!r},
            ariadne_config={self.ariadne_config!r},
            admin={self.admin!r},
            cmd_prefix={self.cmd_prefix!r},
            search_prefix={self.search_prefix!r},
            modules={self.modules!r},
            modules_config={self.modules_config!r}
            )"""

    def read_config(self, file_path) -> object:
        """
        file_path: 配置文件路径\n
        返回一个BotData对象
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        self.info = config.info
        self.ariadne_config = config.ariadne_config
        self.admin = config.admin
        self.cmd_prefix = config.cmd_prefix
        self.search_prefix = config.search_prefix
        self.modules = config.modules
        self.modules_config = config.modules_config

    def save_config(self, file_path) -> None:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self, f)

    def print_config(self) -> None:
        print("Bot config:")
        print(self)

    def get_modules_config(self, module_name: str) -> dict:
        return self.modules_config[module_name]

# init BOT 1 ...
BOT = BotData()
BOT.read_config('grbl_config.yaml')    # 此处填写自己的bot_config.yaml

# TEST
if __name__ == '__main__':
    gb = BotData()
    gb.read_config('bot_config.yaml')
    gb.print_config()
    print(gb.ariadne_config['qq_id'])
    print(gb.get_modules_config('SeTu'))
    #gb.save_config('save_test.config.yaml')