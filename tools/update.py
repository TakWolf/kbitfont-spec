import httpx

from tools import project_root_dir


def main():
    hash_name = '6d1e7d96f0ad3f253d961e52922a2b15b95f853d'
    src_root_dir = project_root_dir.joinpath('bitsnpicas', 'src', 'main', 'java', 'com', 'kreative', 'bitsnpicas')
    for file_dir, _, file_names in src_root_dir.walk():
        for file_name in file_names:
            if not file_name.endswith('.java'):
                continue

            file_path = file_dir.joinpath(file_name)
            url = f'https://raw.githubusercontent.com/kreativekorp/bitsnpicas/{hash_name}/main/java/BitsNPicas/src/com/kreative/bitsnpicas/{file_path.relative_to(src_root_dir)}'.replace('\\', '/')
            response = httpx.get(url)
            assert response.is_success and 'text/plain' in response.headers['Content-Type']

            text = response.text
            if file_dir == src_root_dir and file_name == 'XMLUtility.java':
                text = text.replace('InputSource(resCls.getResourceAsStream(dtdName));', 'InputSource(resCls.getResourceAsStream("/" + dtdName));')

            file_path.write_text(text, 'utf-8')
            print(f"Update: '{file_path}'")


if __name__ == '__main__':
    main()
