import os
import markdown

SOURCE = 'md'
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
			if file.endswith('.md'):

				src_path = os.path.join(root, file)

				base_name = file[:-3]  # remove .md
				base_name = normalize(base_name)

				os.makedirs(norm_dir, exist_ok=True)

				out_path = os.path.join(
					norm_dir,
					base_name + '.html'
				)

				with open(src_path, 'r', encoding='utf-8') as f:
					content = f.read()

				html_body = markdown.markdown(content)

				full_html = f"""<!DOCTYPE html>
<html data-theme="dark">
<head>
<meta charset="utf-8">
<title>{base_name}</title>

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


if __name__ == '__main__':
	build()
