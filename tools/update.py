import httpx

from tools import PROJECT_ROOT_DIR


def main() -> None:
    sha = '1fbc1cbcb19f78d41110b7538a733f0dfa025baa'
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
