Title: About Hestia
Date: 2100-01-01
Category: Index

Hestiaはシナリオとスクリプトの中間表現を提供するシナリオシステムソフトウェアです。

シナリオファイルから構造データを生成し、構造データから機械的にスクリプトを生成します。
スクリプトが機械的に生成されるため、バグの混入を最小限に抑えることができます。

生成された構造データに対して*表現*を挿入することにより、**従来のスクリプト方式から*シナリオ*と*表現*とを切り離すことができます。**
これがHestiaの提供する**中間表現**という考え方です。

## 目標

一つのシナリオファイルから複数のゲームエンジンに対応することを目標にしています。

対応予定ゲームエンジン：

* KAG3
* NScripter
* RealLiveMax
* CatSystem2
* YU-RIS
* Artemis

## ライセンス

HestiaはGPLv3ライセンスが適用されます。

テンプレート部分は修正BSDライセンスが適用されます。

Hestiaを用いて生成された成果物（プロジェクトファイルやスクリプト）にGPLv3が適用されることはありません。

## HEP

HestiaはHEP(Hestia改良提案)に基づいて作成されています。

詳しくは [HEP-Index] を参照して下さい。

## 環境

以下のプラットフォームに対応しています。

* Windows (Pre Release - [v0.0.0.1] (py2exe))
* Mac OSX
* Linux

Unix/Linux環境においては、`python main.py`を実行して下さい。

以下のライブラリが必要になります。

* PyQt
* python-lxml
* python-Markdown
* python-six

`python main.py`実行前に、以下のコマンドを実行する必要があります。

```
./tools/rcc
./tools/uic
```


[HEP-Index]: /hestia/hep-index.html
[v0.0.0.1]: https://github.com/sumi-nook/hestia/releases/download/v0.0.0.1/Hestia-v0.0.0.1.zip
