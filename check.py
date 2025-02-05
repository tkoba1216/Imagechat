from importlib.metadata import distributions

# インストール済みパッケージとバージョンを取得
installed_packages = [(dist.metadata['Name'], dist.version) for dist in distributions()]

# ソートして表示
for package, version in sorted(installed_packages):
    print(f"{package}=={version}")