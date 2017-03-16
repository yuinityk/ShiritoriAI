#概要
お客さんに単語を発してもらい,それに対してしりとりをする感じに言葉を返す．
その際に他の学生に変換して発声する．

#jtalk.pyの使い方(必ずしも必要ではない)
http://qiita.com/kkoba84/items/b828229c374a249965a9 を参考に色々インストールしてください．

#virtualenvの使い方
source shi3/bin/activate で環境に入れます(mecab-python3,requests,feedparser,pyaudioが入っている)．
deactivate で環境から出られます．

#ファイル構成
shi3                      : virtualenv用フォルダ． 
README.md                 : これ． 
Shiritori.py              : メイン．色々詰まっている． 
ShiritoriAIsample.py      : 声を吹き込んだら認識結果を返してくれるサンプル． 
dic_hard,normal,easy.csv  : しりとり用辞書． 
jtalk.py                  : 発話用．関数jtalkにutf-8文字列を渡す． 
parse.py                  : 辞書構築用クローラ． 
rec.py                    : 録音． 
testtalk.py               : jtalkの使用例．

#タスク(各自自由に追加してよい)  
##久保
* 収録
* 収録した声で話すとこを組み込む
* 一連の関数をまとめたUIを作る
