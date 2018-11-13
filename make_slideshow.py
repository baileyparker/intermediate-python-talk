from mistune import Markdown, Renderer, escape
from io import StringIO
from contextlib import redirect_stdout

class CodeRunner(Renderer):
    def __init__(self):
        super().__init__()
        self._slide_started = False
        self._headers = []
        self._globals = {}

    def block_code(self, code, language):
        language_name = language
        output_block = ''

        if language == 'run:python':
            output = self._exec(code)
            if output:
                name = \
                    f'<div class="pre-name oneline"><span>output</span></div>'
                output_block = \
                    f'<pre>{name}<code>{escape(output)}</code></pre>'

            language_name = 'python'
            language = 'python'

        if language == 'python-repl':
            language_name = 'Python REPL'
            language = 'python'

            code = ''.join(self._eval(line) for line in code.split('\n'))

        name = \
            f'<div class="pre-name oneline"><span>{language_name}</span></div>'
        code_block = \
            f'<code class="{language}">{escape(code)}</code>'

        return f'\n<pre>{name}{code_block}</pre>\n{output_block}\n'

    def _exec(self, code):
        f = StringIO()

        try:
            with redirect_stdout(f):
                exec(code, self._globals)

            output = f.getvalue()
            return output if output else None
        except Exception as e:
            return str(e)

    def _eval(self, line):
        if not line.startswith('>>> '):
            return f'{line}\n'

        f = StringIO()
        with redirect_stdout(f):
            try:
                try:
                    result = eval(line[3:], self._globals)
                    output = f'{repr(result)}\n' if result is not None else ''
                except SyntaxError:
                    exec(line[4:], self._globals)
                    output = ''
            except Exception as e:
                output = f'exception: {str(e)}\n'

        output = f'{f.getvalue()}{output}'

        return f'{line}\n{output}'

    def header(self, text, level, raw=None):
        prefix = '</section>\n' if self._slide_started else ''
        self._slide_started = True

        self._headers = self._headers[:level-2]
        pre_headers = ''.join(self._headers)
        self._headers.append(f'{text}: ')
        if pre_headers:
            text = f'{pre_headers}<span class="child-header">{text}</span>'
        else:
            text = f'{pre_headers}{text}'

        level = min(3, level)
        header = f'<h{level}>{text}</h{level}>'

        return f'\n{prefix}\n<section class="slide">\n{header}\n'


def main():
    with open('slides.md') as slides:
        with open('index.template.html') as template:
            with open('index.html', 'w') as output:
                renderer = CodeRunner()
                markdown = Markdown(renderer=renderer)
                slides_html = markdown(slides.read())

                template = template.read()
                print(template.replace('<!-- SLIDES -->', format(slides_html)),
                      file=output)


if __name__ == '__main__':
    main()
