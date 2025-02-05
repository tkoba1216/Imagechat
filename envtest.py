import sys
import os

# 仮想環境判定（Python 3.3以降推奨）
is_venv = sys.prefix != sys.base_prefix
print(f"仮想環境アクティブ: {'✅' if is_venv else '❌'}")

# 環境変数での確認（conda非使用時）
venv_path = os.environ.get('VIRTUAL_ENV')
print(f"仮想環境パス: {venv_path if venv_path else '未検出'}")
