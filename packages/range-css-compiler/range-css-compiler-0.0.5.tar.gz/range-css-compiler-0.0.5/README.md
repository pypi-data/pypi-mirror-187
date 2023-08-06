# range-css-compiler

下の方に日本語の説明があります

## Overview
- More intuitive HTML placement and assignment tool than CSS.
- Intuitive HTML alignment instructions with "Specify by Range".
- Works by equational handling of assignment mutual binding of upper and lower levels of hierarchy like CAD.
- under construction

## Usage
Please use the following command in the console to use it:
```sh
rcss compile RangeCSS_format_filename.yml
```

Refer to `## rcss_format.yml Writing Method` for the way to write a RangeCSS format file.

You can also specify the output file name as an argument with an option.

```sh
rcss compile RangeCSS_format_filename.yml output_filename.js
```

## rcss_format.yml Writing Method
```yaml
rcss_frame: # The rcss_id of the element (the outermost element must be 'rcss_frame')
  css_id: rcss_frame # The id of the element in html
  children: [header, main] # List of rcss_id of child elements
  align: vertical # Alignment of child elements (vertical(default) or horizontal)
header:
  children: []
  css_id: header
  margin_y0: 10px # Top margin in the vertical direction (omitted if 0. Not shared with the top element's margin)
  width: "~" # Width of the element. Refer to `## Range-based specification format` for the method of specifying it.
  height: 70px # Height of the element
main:
  children: [some_other_element]
  align: horizontal
  css_id: main
  margin_y0: 10px
  margin_y1: 10px # Bottom margin in the vertical direction
  width: "~"
  height: "~"
```

## Range-based specification format

- Absolute value specification: `10px`
- Range specification: `10px~20px`
- Range specification without lower limit: `~20px`
- Range specification without upper and lower limit: `~`
- Basic value specification: `10px~100px[50px]`

## Reference: List of attributes
`(default: ...)` means default value without specification
```
css_id: The id of the element in html
children: List of rcss_id of child elements (default: [])
align: Alignment direction of child elements (default: vertical)
width: Width of the element (default: ~)
height: Height of the element (default: ~)
margin_x0: Left margin in the horizontal direction (default: 0px)
margin_x1: Right margin in the horizontal direction (default: 0px)
margin_y0: Top margin in the vertical direction (default: 0px)
margin_y1: Bottom margin in the vertical direction (default: 0px)
```

## license info
The npm tool 'quadprog' is used under the MIT license. (https://www.npmjs.com/package/quadprog)


## 概略
- CSSよりも直感的なHTMLの配置・割り付けツール
- 「範囲による指定」でHTMLの配置を直感的に指示できる
- 上位・下位階層の割り付け相互束縛をCADのように方程式的に取り扱うことで動作する。
- 説明文は執筆中です

## 利用例
コンソールで下記のように呼び出して利用してください:
```sh
rcss compile RangeCSS_format_filename.yml
```

RangeCSS フォーマットファイルの書き方は `## rcss_format.yml の書き方` を参照してください

※オプションで出力先ファイル名を引数に加えることができます。
```sh
rcss compile RangeCSS_format_filename.yml output_filename.js
```

## rcss_format.yml の書き方
```yaml
rcss_frame:	# その要素のrcss_id (一番外側は`rcss_frame`である必要がある)
  css_id: rcss_frame	# html内のその要素のid
  children: [header, main]	# 子要素のrcss_idのリスト
  align: vertical	# 子要素の配置 (vertical(default) もしくは horizontal)
header:
  children: []
  css_id: header
  margin_y0: 10px	# 縦方向の上側のマージン (省略されると0となる。上要素のマージンと共有されない)
  width: "~"	# 要素の幅。`~`などの指定方法は、`## 範囲による指定の形式` を参照
  height: 70px	# 要素の高さ
main:
  children: [some_other_element]
  align: horizontal
  css_id: main
  margin_y0: 10px
  margin_y1: 10px	# 縦方向の下側のマージン
  width: "~"
  height: "~"
```

## 範囲による指定の形式
- 絶対値指定: `10px`
- 範囲指定: `10px~20px`
- 下限のない範囲指定: `~20px`
- 上限・下限なし: `~`
- 基本値の指定: `10px~100px[50px]`

## 参考: 属性の一覧
`(default: ...)`は指定なしの場合のデフォルト値

```
css_id: html内のその要素のid
children: 子要素のrcss_idのリスト (default: [])
align: 子要素の配置方向 (default: vertical)
width: 要素の幅 (default: ~)
height: 要素の高さ (default: ~)
margin_x0: 横方向の左側のマージン (default: 0px)
margin_x1: 横方向の右側のマージン (default: 0px)
margin_y0: 縦方向の上側のマージン (default: 0px)
margin_y1: 縦方向の下側のマージン (default: 0px)
```
