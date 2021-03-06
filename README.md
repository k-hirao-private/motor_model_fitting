# モーターモデルフィッティング
二個以上の出力値によって一定出力駆動されたモーターの回転量の時間変化ログを用いて、モーターのパラメーターを求めます。モデルは基本の
$p=J\dot{\omega}+B\omega+C$
である。
# 使い方
## データの準備
### 実データの作成
モーターを回して出力開始からの時間、回転量をシリアルで読む。そのデータを以下のCSV形式で任意のフォルダ内に保存する。
```
モーター出力p(PWM,仮想電圧),出力開始からの時間t(s,ms),回転量θ(エンコーダ、deg)
```
データそれぞれの単位は指定しない。その単位系に合わせたパラメータが出力されるためそのパラメータを利用して制御する場合は入力したデータの単位系に合わせる。  
3次元のパラメータを推測するためpとtとθの3次元のデータが必要になる。以下の条件に気を付けてデータ取得を行う
- Jは定常速度に達すると作用しなくなるため定常速度に達するまでの時間のデータを利用する。
- pの幅を大きく複数個とる
- 同じpを複数回取得すると誤差を減らせる
### テストデータの作成
フィッティングプログラムのテスト利用やこのプログラムのデバッグ用にテストデータを作成するスクリプトを用意した。実行コマンドは以下のようである。
```
python create_test_data.py test_data_setting.json
```
test_data_setting.jsonには作成するデータに関するパラメーターがある
- t：時間刻み
    - start：開始時間
    - stop：終了時間
    - num：データ点数
- p：出力値
    - start：開始時間
    - stop：終了時間
    - num：データ点数
- J ,B ,C：モーターパラメーター
    - value：真値
    - variance：正規分布の分散
- num：1出力当たりのデータの生成回数

tとpはnp.linspace(start, stop, num)によってデータが作られるためstartからstopまでの区間で均等に分割するため20等分なら端を考慮してnum=21とするのがよい。  
J,B,Cは真値に正規分布で生成した乱数を足し合わせて利用している。  
numは同じ出力で何個のテストデータを作るかを設定でき、p["num"]=3, num=5のとき全部で15個のデータができる。

## フィッティング
CSVの入ったフォルダを指定して実行する。
```
python .\fitting.py .\test_data
```
この場合はテストデータ作成時に生成される.\test_data内のCSVファイルを読み込んでいる。
実行されるとコマンドラインにパラメータが表示され、入力データと推定されたモーターモデルの曲面がプロットされる。  

# 不具合
- フィッティングの際のディレクトリ指定で末尾にバックスラッシュを入れると失敗する。Tabを使ったディレクトリ名の自動補完を行うとWindowsの場合バックスラッシュが末尾につくがこれは消して実行すること