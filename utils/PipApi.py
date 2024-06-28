import subprocess
import threading

import requests
from bs4 import BeautifulSoup


class PipApi:
    """
    所有获取Pip数据的接口
    """

    def __init__(self):
        self.pip = 'pip'
        self.pip_url = 'https://pypi.org/simple'

    def get_pip_list(self):
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
    def __get_py_package(pip_url):
        """
        获取py包列表
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

    def get_py_packages(self):

        def get_py_package_thread_method():
            self.result = self.__get_py_package(self.pip_url)

        # 开启一个多线程获取数据
        get_py_package_thread = threading.Thread(target=get_py_package_thread_method)
        get_py_package_thread.start()
        get_py_package_thread.join()
        return self.result


if __name__ == "__main__":
    pipApi = PipApi()
    packages = pipApi.get_py_packages()
    if packages:
        print(packages[:10])
    else:
        print("无法获取包列表")
