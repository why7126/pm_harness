#!/usr/bin/env python3
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
PROJECT_FILE = ROOT / 'project.yaml'
TEMPLATE_DIR = ROOT / 'templates'

OUTPUT_MAP = {
    'README.md.j2': 'README.md',
    'openspec-project.md.j2': 'openspec/project.md',
    'product-overview.md.j2': 'docs/00-product-overview.md',
    'architecture.md.j2': 'docs/01-architecture.md',
    'deployment.md.j2': 'docs/02-deployment.md',
    'compatibility-matrix.md.j2': 'docs/05-compatibility-matrix.md',
    'env.example.j2': '.env.example',
}

def main():
    data = yaml.safe_load(PROJECT_FILE.read_text(encoding='utf-8'))
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), trim_blocks=True, lstrip_blocks=True)
    for template_name, output_path in OUTPUT_MAP.items():
        template = env.get_template(template_name)
        target = ROOT / output_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(template.render(**data), encoding='utf-8')
        print(f'generated: {output_path}')

if __name__ == '__main__':
    main()
