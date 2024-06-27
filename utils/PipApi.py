import subprocess


def get_pip_list():
    """
    获取pip列表
    :return: 列表数据对象
    """
    result = subprocess.run(['pip', 'list'], capture_output=True, text=True)

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


if __name__ == "__main__":
    print(get_pip_list())
