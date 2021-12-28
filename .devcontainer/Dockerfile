FROM jupyter/datascience-notebook:ubuntu-20.04

# インストールなどの作業はルートで
USER root

# 作業ディレクトリを作り移動する
WORKDIR /work

# 日本語フォントのインストール
RUN apt update \ 
  && apt install fonts-noto-cjk


# 必要ライブラリ
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# インストールに使用したファイルを削除
RUN rm -rf /work/*

# 通常ユーザーに戻す
USER jovyan

# matplotlibのフォントキャッシュ削除
RUN rm -rf ~/.cache/matplotlib


CMD start-notebook.sh --NotebookApp.token=''