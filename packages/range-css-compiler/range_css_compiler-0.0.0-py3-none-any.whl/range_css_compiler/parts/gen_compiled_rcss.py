
# クライアント側jsを生成 (2次計画法でHTMLの動的な割り付けを実施) [gen_compiled_rcss.py]

import sys
import fies
import json
from sout import sout
import indent_template
from relpath import rel2abs

# クライアント側jsを生成 (2次計画法でHTMLの動的な割り付けを実施) [gen_compiled_rcss.py]
def gen_compiled_rcss(
	mat_def_js_code,	# 行列定義部のjavascriptコード
	css_id_ls	# css_idの一覧
):
	compiled_rcss_js_code = indent_template.replace(
		fies[rel2abs("./compiled_rcss_template.js"), "text"],
		{
			"BUNDLE": fies[rel2abs("./browserified_quadprog.js"), "text"],
			"MAT_DEF_CODE": mat_def_js_code,
			"CSS_ID_LIST": json.dumps(css_id_ls, ensure_ascii = False),
			"APPLIER_UTILS": fies[rel2abs("./applier_utils.js"), "text"],
		}
	)
	return compiled_rcss_js_code
