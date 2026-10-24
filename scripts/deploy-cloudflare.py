#!/usr/bin/env python3
"""构建并发布已提交的主页到 Cloudflare Pages；--check 只检查发布文件。"""
import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJECT = 'homepage'


def run(*args, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, **kwargs)


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.paths.append(dict(attrs)['src'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='检查构建和文件清单，不上传')
    args = parser.parse_args()
    run(sys.executable, 'build.py')
    # 只发布可追溯的已提交版本，临时纹理和原始图片不会进入上传目录。
    changed = run('git', 'diff', '--name-only', 'HEAD', '--', 'dist/', 'design/', 'build.py',
                  capture_output=True, text=True).stdout.strip()
    if changed:
        raise SystemExit('请先提交页面源文件及构建产物，再发布：\n' + changed)
    files = run('git', 'ls-tree', '-r', '--name-only', '-z', 'HEAD', 'dist/',
                capture_output=True).stdout.decode().strip('\0').split('\0')
    if 'dist/index.html' not in files:
        raise SystemExit('当前提交中没有 dist/index.html。')
    with tempfile.TemporaryDirectory(prefix='homepage-pages-') as directory:
        stage = pathlib.Path(directory)
        for name in files:
            target = stage / pathlib.Path(name).relative_to('dist')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        images = Images()
        images.feed((stage / 'index.html').read_text())
        missing = [name for name in images.paths if not (stage / name).is_file()]
        if missing:
            raise SystemExit('以下图片尚未提交，无法发布：' + ', '.join(missing))
        total = sum((stage / pathlib.Path(name).relative_to('dist')).stat().st_size for name in files)
        revision = run('git', 'rev-parse', 'HEAD', capture_output=True, text=True).stdout.strip()
        print(f'发布检查通过：{len(files)} 个文件，{total:,} 字节，版本 {revision[:7]}。', flush=True)
        if args.check:
            return
        run('npx', '--yes', 'wrangler@4', 'pages', 'deploy', str(stage),
            '--project-name', PROJECT, '--branch', 'main', '--commit-hash', revision,
            '--commit-dirty=true')


if __name__ == '__main__':
    main()
