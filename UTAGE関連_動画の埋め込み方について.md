## 学習について
### スキルプラス講義保管庫で学習を進めている方はこちら
#### スキルプラス講義保管庫について

**Q: UTAGEの会員コンテンツサイトページ内に動画を埋め込む方法を教えてください。**
A: UTAGEの会員コンテンツサイトページ内に動画を埋め込む場合のHTMLの手順は以下の通りです：
1. UTAGE右上の名前を選択します
2. 「動画管理」を選択します
3. 「新規アップロード」を選択します
4. 指定の動画ファイルをアップロードします
5. アップロード後、埋め込み用URLをコピーします
6. 下記のHTML内の「UTAGEリンク」部分に埋め込み用URLを貼り付けます
7. 完成したHTMLを指定の場所に挿入します

```html
<style>
    .video-wrapper {
      position: relative;
      padding-top: 56.25%;
      height: 0;
      margin-bottom: 0;
    }
    .video-wrapper iframe {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
</style>
<div class="video-wrapper">
    <iframe src="UTAGEのリンク" frameborder="0" allowfullscreen></iframe>
</div>
```

他にも不明点があればいつでもご相談ください。
