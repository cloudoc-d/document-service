import argparse
from commands.documents import generate_documents
from commands.styles import generate_styles
import os

def get_mongo_db_url() -> str:
    return os.getenv('MONGODB_URL')

def main():
    parser = argparse.ArgumentParser(description="Manager CLI")
    subparsers = parser.add_subparsers(title='commands', dest='command')

    # Documents command
    docs_parser = subparsers.add_parser('generate_documents', help='Generate documents')
    docs_parser.add_argument('count', type=int, help='Number of documents to generate')
    styles_parser.add_argument(
        'mongodb_url',
        type=str,
        default=get_mongo_db_url,
        help='Url to mongodb database (default: env.MONGODB_URL)'
    )
    styles_parser.add_argument(
        'database',
        type=str,
        default='cloudoc',
        help="MongoDB database name (default: cloudoc)"
    )
    styles_parser.add_argument(
        'collection',
        type=str,
        default='documents',
        help="Documents collection name (default: documents)"
    )
    docs_parser.set_defaults(func=generate_documents)

    # Styles command
    styles_parser = subparsers.add_parser('generate_styles', help='Generate styles')
    styles_parser.add_argument(
        'count',
        type=int,
        help='Number of styles to generate'
    )
    styles_parser.add_argument(
        'mongodb_url',
        type=str,
        default=get_mongo_db_url,
        help='Url to mongodb database (default: env.MONGODB_URL)'
    )
    styles_parser.set_defaults(func=generate_styles)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
