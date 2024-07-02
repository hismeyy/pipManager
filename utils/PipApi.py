import gc
import json
import re
import subprocess
import threading
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class PipApi:
    """
    所有获取Pip数据的接口
    """

    def __init__(self):
        self.pip = 'pip'
        self.pip_url = 'https://pypi.org/simple'
        self.file_path = './data/py_package.cache'

    def get_pip_list_api(self):
        """
        获取pip列表
        :return: 列表数据对象
        """
        result = subprocess.run([self.pip, 'list'], capture_output=True, text=True)

        lines = result.stdout.strip().split('\n')
        package_lines = lines[2:]
        packages = []

        for line in package_lines:
            parts = line.split()
            name = parts[0]
            version = parts[1]
            packages.append((name, version))

        return packages

    @staticmethod
    def __get_py_packages(pip_url):
        """
        请求py包列表
        :return: 列表
        """
        try:
            response = requests.get(pip_url, stream=True)

            if response.status_code == 200:
                package_list = []

                # 使用 iter_content 分块处理响应数据
                for chunk in response.iter_content(chunk_size=2048):
                    # 部分解析HTML
                    soup = BeautifulSoup(chunk, 'html.parser')
                    for link in soup.find_all('a', href=True):
                        package_name = link.get_text(strip=True)
                        package_list.append(package_name)

                return package_list
            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
        return None

    @staticmethod
    def get_now_date():
        """
        获取当前时间
        :return:
        """
        now = datetime.now()
        return f"{now.year}-{now.month}-{now.day}"

    @staticmethod
    def __write_py_packages_cache(py_package_list, file_path):
        """
        写入缓存
        :param py_package_list:
        :param file_path:
        :return:
        """
        cache = {
            "date": PipApi.get_now_date(),
            "packages": py_package_list
        }

        cache_json = json.dumps(cache)
        with open(file_path, "w") as file:
            file.write(cache_json)
        gc.collect()

    @staticmethod
    def __read_py_packages_cache(file_path):
        """
        读取缓存
        :param file_path:
        :return:
        """
        try:
            with open(file_path, "r") as file:
                cache_json = file.read()
                cache = json.loads(cache_json)
                return cache["date"], cache["packages"]
        except FileNotFoundError:
            return None, []

    def get_py_package_list_api(self):
        """
        获取py包列表，从缓存中读取或重新加载
        :return: py包列表
        """

        # 读取缓存
        date, package_list = self.__read_py_packages_cache(self.file_path)

        # 如果缓存为空或者过期，则重新加载
        if date is None or date != PipApi.get_now_date():
            package_list = self.__get_py_packages(self.pip_url)
            write_thread = threading.Thread(target=self.__write_py_packages_cache, args=(package_list, self.file_path))
            write_thread.start()

        return package_list

    def version_key(self, version):
        # 分割版本号成各个部分，使用正则表达式匹配数字和字母
        parts = re.split(r'(\d+)', version)
        # 将数字部分转换为整数，字母部分保持为字符串
        return [int(part) if part.isdigit() else part for part in parts]

    def sort_versions(self, versions):
        return sorted(versions, key=self.version_key, reverse=True)

    def get_package_versions_api(self, package_name):
        """
        获取可安装包的版本号
        :param package_name:
        :return:
        """
        try:
            # 使用 PyPI 的 JSON API 查询包信息
            url = f'https://pypi.org/pypi/{package_name}/json'
            response = requests.get(url)
            response.raise_for_status()  # 确保请求成功

            # 解析 JSON 数据
            package_data = response.json()
            versions = list(package_data['releases'].keys())

            # 对版本号进行排序（从大到小）
            versions_sorted = self.sort_versions(versions)

            return versions_sorted
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving package information: {e}")
            return None

    def uninstall_package_api(self, package_name):
        """
        卸载指定的pip包
        :param package_name:
        :return:
        """
        result = subprocess.run([self.pip, 'uninstall', '-y', package_name], capture_output=True, text=True)

        if result.returncode == 0:
            return f"Package '{package_name}' uninstalled successfully."
        else:
            return f"Failed to uninstall package '{package_name}'. Error: {result.stderr.strip()}"

    def install_package_api(self, package_name):
        """
        安装指定的pip包
        :param package_name:
        :return:
        """
        result = subprocess.run([self.pip, 'install', package_name], capture_output=True, text=True)

        if result.returncode == 0:
            return f"Package '{package_name}' installed successfully."
        else:
            return f"Failed to install package '{package_name}'. Error: {result.stderr.strip()}"

    def show_package_info_api(self, package_name):
        """
        查看指定包的信息
        :param package_name:
        :return:
        """
        result = subprocess.run([self.pip, 'show', package_name], capture_output=True, text=True)

        return result.stdout


if __name__ == "__main__":
    pipApi = PipApi()
    pipApi.test()
