import httpx

from tools import PROJECT_ROOT_DIR


def main() -> None:
    sha = '43b11dca0809a3342b8281b570897e8654ffe705'
    src_root_dir = PROJECT_ROOT_DIR.joinpath('bitsnpicas', 'src', 'main', 'java', 'com', 'kreative', 'bitsnpicas')
    for file_path in src_root_dir.rglob('*.java'):
        if not file_path.is_file():
            continue

        url = f'https://raw.githubusercontent.com/kreativekorp/bitsnpicas/{sha}/main/java/BitsNPicas/src/com/kreative/bitsnpicas/{file_path.relative_to(src_root_dir)}'.replace('\\', '/')
        response = httpx.get(url)
        assert response.is_success and 'text/plain' in response.headers['Content-Type']

        lines = []
        for line in response.text.splitlines():
            line = line.replace('\t', '    ').rstrip()
            lines.append(line)
        lines.append('')
        text = '\n'.join(lines)

        if file_path == src_root_dir.joinpath('XMLUtility.java'):
            text = text.replace('InputSource(resCls.getResourceAsStream(dtdName));', 'InputSource(resCls.getResourceAsStream("/" + dtdName));')

        file_path.write_text(text, 'utf-8')
        print(f"Update: '{file_path}'")


if __name__ == '__main__':
    main()
