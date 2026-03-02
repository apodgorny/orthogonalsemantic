import os
import shutil
import markdown

SOURCE = 'site'
OUTPUT = 'html'


def normalize(name):
	return name.replace('_', '-')


def build():
	for root, dirs, files in os.walk(SOURCE):

		rel_dir = os.path.relpath(root, SOURCE)
		rel_dir = '' if rel_dir == '.' else rel_dir

		norm_dir = os.path.join(
			OUTPUT,
			*[
				normalize(part)
				for part in rel_dir.split(os.sep)
				if part
			]
		)

		for file in files:

			src_path = os.path.join(root, file)

			name, ext = os.path.splitext(file)
			name = normalize(name)
			ext = ext.lower()

			os.makedirs(norm_dir, exist_ok=True)

			# --------------------------------------------------------------
			# Markdown → themed HTML
			# --------------------------------------------------------------
			if ext == '.md':

				out_path = os.path.join(
					norm_dir,
					name + '.html'
				)

				with open(src_path, 'r', encoding='utf-8') as f:
					content = f.read()

				html_body = markdown.markdown(content)

				full_html = f"""<!DOCTYPE html>
<html data-theme="dark">
<head>
<meta charset="utf-8">
<title>{name}</title>

<link rel="stylesheet"
 href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">

<style>
:root {{
  --pico-font-size: 15px;
  --pico-line-height: 1.55;
}}

main {{
  max-width: 760px;
  margin: auto;
}}

code, pre {{
  font-family: "JetBrains Mono", monospace;
  font-size: 0.9em;
}}
</style>

</head>
<body>
<main class="container">
{html_body}
</main>
</body>
</html>
"""

				with open(out_path, 'w', encoding='utf-8') as out:
					out.write(full_html)

			# --------------------------------------------------------------
			# Everything else → copy 1:1
			# --------------------------------------------------------------
			else:

				out_path = os.path.join(
					norm_dir,
					name + ext
				)

				shutil.copy2(src_path, out_path)


if __name__ == '__main__':
	build()