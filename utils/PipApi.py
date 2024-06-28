import json
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
        self.py_package_list = []
        self.file_path = '../data/py_package.cache'

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
            packages.append({
                'name': name,
                'version': version
            })

        return packages

    @staticmethod
    def __get_py_packages(pip_url):
        """
        请求py包列表
        :return: 列表
        """
        response = requests.get(pip_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            package_list = []
            for link in soup.find_all('a', href=True):
                package_name = link['href'].split('/')[-2]
                package_list.append(package_name)
            return package_list
        else:
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

    def get_py_packages_and_write_cache(self):
        """
        获取py包列表并且写入缓存
        :return:
        """
        get_py_package_thread = None

        def get_py_package_thread_method():
            self.py_package_list = self.__get_py_packages(self.pip_url)

        def write_py_packages_cache_thread_method():
            get_py_package_thread.join()
            if len(self.py_package_list) != 0:
                self.__write_py_packages_cache(self.py_package_list, self.file_path)

        get_py_package_thread = threading.Thread(target=get_py_package_thread_method)
        get_py_package_thread.start()
        write_py_package_cache_thread = threading.Thread(target=write_py_packages_cache_thread_method)
        write_py_package_cache_thread.start()

    def get_py_package_list_api(self):
        """
        获取py包列表
        :return:
        """

        # 读取缓存
        date, self.py_package_list = self.__read_py_packages_cache(self.file_path)

        # 第一次加载
        if date is None and len(self.py_package_list) == 0:
            self.get_py_packages_and_write_cache()

        # 缓存过期，重新加载
        if date is not None and date != PipApi.get_now_date():
            self.get_py_packages_and_write_cache()

        return self.py_package_list


if __name__ == "__main__":
    pipApi = PipApi()
    packages = pipApi.get_py_package_list_api()
    if packages:
        print(packages[:10])
    else:
        print("无法获取包列表")
