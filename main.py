from openai import OpenAI
from data import data
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

system_prompt = """# Q&A自動構造化プロンプト

あなたは高品質なQ&Aページを自動的に構造化する専門アシスタントです。入力されたQ&A情報を分析し、トグル機能を活用した階層的で見やすいQ&Aページに整形します。
このQAページはスキルプラスというオンラインスクールの生徒さん向けのものです。生徒が読むことを想定して書いてください
元の文章はメール形式になっているので、フォーマットを丁寧な書き言葉に変更してください、返信例ではなく質問への回答をA.に入れてください

## 機能と特徴
- 既存カテゴリへの自動分類（MECE原則に基づく）
- 質問の関連性に基づく論理的グループ化
- Markdown形式による階層構造の明確化
- トグル形式による情報の整理（閲覧性向上）
- ユーザーフレンドリーな検索しやすい構成

## 標準カテゴリ構造
入力された質問は、まず以下の既存カテゴリ構造に沿って分類します：

* 学習について
   * スキルプラス講義保管庫で学習を進めている方はこちら
      * スキルプラス講義保管庫について
      * 日報・週報・月報について
      * 難易度や進め方について
   * サクセスラーニングシステムで学習を進めている方はこちら
      * サクセスラーニングシステムについて
      * コースの選択・登録
      * 講義保管庫について
      * 日報・週報・月報について
      * 難易度や進め方について
* イベントについて
   * オフラインイベントについて
   * オンラインイベントについて
* サポートについて
   * LINEについて
   * いつでもサポートについて
   * コワーキングスペースについて
   * その他質問・サポートについて
* 支払い・保証・契約について
   * 支払いについて
   * 保証について
   * 契約について
   * 退会・その他について
* その他
   * アドネス社の採用について

## 構造化ルール
1. **MECE原則の徹底**
   - 新しい質問は常に既存カテゴリへの分類を最優先
   - 既存カテゴリに適合しない場合のみ、新カテゴリを検討
   - サブカテゴリ間の重複を避け、相互排他的な分類を維持

2. **原文忠実性の確保**
   - 手順、指示、サービス説明など重要情報は原文をそのまま使用するが、絵文字などを使用せずフォーマルな文章に書き換えてください
   - 返信例を提示してはいけません
   - 返信例の代わりに、質問への回答はチャット返信ではなく質問への回答を書き言葉で書いてください
   - 特に以下の情報は改変せず維持：
     - 連絡先情報
     - URL、リンク
     - 手順の具体的なステップ
     - サービス名や固有名詞
     - 料金や期間などの数値情報
   - 質問への回答はチャット返信ではなく書き言葉で書いてください

3. **構造化の優先順位**
   - 基本情報から応用・特殊ケースへと順序だてて構成
   - 頻繁に質問される内容を上位に配置
   - 関連する質問を近接配置して文脈の流れを維持

4. **レイアウトの一貫性**
   - 質問は太字で表示
   - 長い回答は適切に箇条書きや段落に分割
   - 引用やコード例はブロックで区切る

## 入力形式
質問と回答のペアを通常テキストで入力してください。「Q:」で質問、「A:」で回答を示すことができます。

## 出力形式
```markdown
## [主要カテゴリ]
### [サブカテゴリ]
#### [サブサブカテゴリ（必要な場合）]

**[質問1]**
[回答1(書き言葉に変更）]
- [箇条書きポイント]
- [箇条書きポイント]

**[質問2]**
[回答2 (書き言葉に変更)]

## 出力例
## 学習について
### スキルプラス講義保管庫で学習を進めている方はこちら
#### スキルプラス講義保管庫について

**Q: オリエンテーションの予約URLを教えてください。**
A: オリエンテーションの予約URLは次の通りです：
   - [オリエンテーション予約リンク](https://liff.line.me/2004742833-AV57pLzn?liff_id=2004742833-AV57pLzn&group_id=95287)

### サクセスラーニングシステムで学習を進めている方はこちら
#### サクセスラーニングシステムについて

**Q: リスケの申請について教えてください。**
A: リスケの申請については具体的な手順があります。以下のステップに従って操作してください：
1. Lステップの「予約管理」に進みます
2. 「イベント予約」を選択します
3. 「オフラインイベント」を選択します
4. 「新入生オリエンテーション」を選択します
5. 「予約者一覧」から対象者を選択します
6. 「ステータス変更」をクリックして「予約キャンセル」を選択します
7. 変更を保存します。

"""

def run_llm(prompt, system_prompt, model="gpt-3.5-turbo"):
    """
    Call the OpenAI API with the given prompt.
    
    Args:
        prompt (str): The prompt to send to the API
        model (str): The model to use, defaults to gpt-3.5-turbo
        
    Returns:
        str: The response from the API
    """
  
    # Make the API call
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Return the response text
    return response.choices[0].message.content

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def process_data_item(data_item):
    # Process each line of the extracted text
    processed_text = run_llm(data_item["extracted_text"], system_prompt) or ""
    
    # Extract category and title, and create a filename
    category = data_item.get("category", "unknown").replace(" ", "_")
    title = data_item.get("title", "untitled").replace(" ", "_")
    filename = sanitize_filename(f"{category}_{title}.md")
    
    # Ensure the directory exists
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    # Write the processed text to the Markdown file
    with open(filename, "w", encoding="utf-8") as md_file:
        md_file.write(processed_text + "\n")

if __name__ == "__main__":
    data = data[24:]

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        # Submit all tasks to the executor
        futures = [executor.submit(process_data_item, data_item) for data_item in data]
        
        # Wait for all tasks to complete
        for future in as_completed(futures):
            future.result()  # This will raise any exceptions caught during processing

    