MarkerClipManager — DaVinci Resolve用タイムライン&クリップマーカーマネージャー
==============================================================================
Author: Tommaso Feraboli — Film Editor
Version: 1.4.8
MIT License — see the script header

機能説明
--------
Resolveタイムラインのすべてのマーカーを表示および管理する単一ウィンドウ:
ルーラー(タイムラインレベル)マーカーと個別クリップに配置されたマーカーの両方、
すべてのビデオおよびオーディオトラック上。

各マーカーについて表示: マーカーグラフィック(Resolveと同じネイティブ形状)、
トラック、TC開始、TC終了、デュレーション、色、名前、キーワード、ノート。

機能
----
- 1つまたは複数のマーカーを選択して、色の変更、トラックの変更
  ("TIMELINE"ルーラーとの間の移動を含む)、削除ができます
- 名前、キーワード、ノートは表の中で直接編集でき(ダブルクリック)、
  選択した複数のマーカーにまとめて適用されます
- Deleteキーは削除ボタンと同じ働きをします。確認ダイアログはオフにできます
- Cmd+Z / Ctrl+Zで取り消しとやり直しができ、Historyパネルでは前の段階を
  ダブルクリックすると直接そこまで戻れます。対象は現在のセッションのみで、
  スクリプトを閉じると消去されます
- 色、トラック、作成者/名前、キーワードで絞り込めます
- マーカーをCSVで書き出し、読み込みできます
- 行をクリックすると、タイムラインの再生ヘッドがそのマーカーに移動します
- インターフェースは12言語に対応しています。該当するものがあればシステムの
  言語で起動し、なければ英語で起動します。ウィンドウ上部のメニューで変更
  できます(スクリプトの再起動後に反映されます)

必要な環境
----------
- DaVinci Resolve 19/20 (macOS)
- システムにインストールされたPython 3
- PySide6(以下のセットアップスクリプトで自動インストール — 手動操作は不要)

インストール(1回のみ)
---------------------
1. お使いのシステム用のインストーラーをダウンロードします
2. macOS: .commandファイルを右クリックして「開く」を選びます。ダブル
   クリックではありません。このファイルはAppleの開発者証明書で署名されて
   いないため、ダブルクリックではmacOSがブロックします
   Windows: .cmdファイルをダブルクリックします。SmartScreenの警告が出たら
   「詳細情報」から「実行」を選びます
3. インストーラーはファイルをコピーしたあと、スクリプトに必要なPython環境を
   用意します(この部分にはインターネット接続が必要で、1分ほどかかります)
4. その2番目の部分が失敗した場合(接続がない、Pythonがないなど)でも、
   ファイルは正しくインストールされています。インストール先のフォルダーを
   開き、都合のよいときに"MarkerClipManager_Setup.command"(macOS)または
   "MarkerClipManager_Setup_Windows.cmd"(Windows)を実行してください
5. 完了です。更新も同じ手順で、以前のバージョンの上から入れられます。
   設定はそのまま残ります

使用方法
--------
DaVinci Resolveで: Workspace > Scripts > Comp > MarkerClipManager > MarkerClipManager
(スクリプトはComp内の"MarkerClipManager"サブフォルダに存在するため、
メニューに同じ名前のサブメニューとして表示されます)

既知の制限事項
--------------
- テーブルのマーカーはスクリプトで描画された再作成アイコンであり、
  Resolveの公式アイコンではありません(APIで公開されていません)。色はユーザーが
  提供した正確な16進数値 — アイコンの形状のみ近似
- "キーワード"はネイティブResolveマーカーフィールドではありません: 内部
  マーカーフィールド(customData)に保存され、Resolveのネイティブマーカーパネルに
  非表示 — このスクリプトでのみ読み取り/書き込み可能
- タイムコードはプロジェクトアクティブタイムラインから直接fpsおよび
  Drop Frame/Non-Drop Frameモードを読み取ります(29.97および59.94 DFは標準
  SMPTEアルゴリズムで正しく処理); 非標準fpsでは計算は近似
- EDLインポート/エクスポートはこのスクリプトでは処理されません: Resolveの
  ネイティブ機能を使用(Timeline > Markers > Export/Import)
- マーカーをビデオ/オーディオトラックに移動するには、クリップが既にその
  位置に存在する必要があります

サポート
--------
バグレポート: アプリの🐛ボタンを使用(tomfilmeditor.tools@gmail.comへ事前入力
メール開く)
開発をサポートしたい場合: アプリの☕ボタン、または
https://paypal.me/acoffeefortom

⚠️  Note on translations: This documentation is available in multiple languages.
These translations were generated automatically. If you find any errors or typos,
please report them to the contact listed in the SUPPORT section above.
