# dev container

## environment:開発環境について

microsoftが公開しているdev containerを利用する。
メモとして、詳細を残しておく。
```.devcontainer/devcontainer.json```に環境情報を書くことで、簡単に開発環境を開発することができる。
また、```python```, ```Rust```などdockerfileでは管理が難しいツールを簡易的に管理することができる。
例えば、[Dev container features](https://qiita.com/frozenbonito/items/b1de3980ee0553fb1c2f#:~:text=in%2DDocker%20Install%20Script%20%E3%81%8C%E6%8F%90%E4%BE%9B%E3%81%95%E3%82%8C%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99-,Dev%20container%20features%20(preview),-%E3%82%92%E4%BD%BF%E3%81%86)という機能が試験的に導入されている。
動作を確認したところ、DockerfileがBuildされた後に実行されるっぽい。（要確認）
また、[Development Container Scripts](https://qiita.com/frozenbonito/items/b1de3980ee0553fb1c2f#:~:text=%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95%E3%81%A7%E3%81%99-,Development%20Container%20Scripts,-%E3%82%92%E4%BD%BF%E3%81%86)という機能もある。
この機能は、Github上にinstall scriptが公開されており、scriptを使用することでツールをインストールすることができる。

これらの機能の有用性として、Pythonをバージョン指定でインストールする際、Root以外のUserを作成する際、最新のGitをインストールする際、自分用にアレンジしたTerminalを使用する際（Fishも使えるみたい）などに便利だと思う。


