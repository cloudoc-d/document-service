import argparse
from scripts.commands.documents import fill_documents_collection
from app.config import Config
import os

def get_mongo_db_url() -> str:
    return Config.MONGODB_URL

def main():
    parser = argparse.ArgumentParser(description="Manager CLI")
    subparsers = parser.add_subparsers(title='commands', dest='command')

    # Documents command
    docs_parser = subparsers.add_parser('generate_documents', help='Generate documents')
    docs_parser.add_argument('count', type=int, help='Number of documents to generate')
    docs_parser.add_argument(
        'mongodb_url',
        type=str,
        nargs='?',
        default=get_mongo_db_url(),
        help=f'Url to mongodb database (default: {get_mongo_db_url()})'
    )
    docs_parser.add_argument(
        'user_id',
        type=str,
        nargs='?',
        default=None,
        help='Document owner. If None, a random id is assigned (default: None)',
    )
    docs_parser.add_argument(
        'database',
        type=str,
        nargs='?',
        default='cloudoc',
        help="MongoDB database name (default: cloudoc)"
    )
    docs_parser.add_argument(
        'collection',
        type=str,
        nargs='?',
        default='documents',
        help="Documents collection name (default: documents)"
    )
    docs_parser.add_argument(
        'style_collection',
        type=str,
        nargs='?',
        default='styles',
        help="Styles collection name (default: styles)"
    )
    docs_parser.add_argument(
        'assign_existing_style',
        type=bool,
        nargs='?',
        default=True,
        help="Should existing style_id be assigned to document (default: true)",
    )
    docs_parser.set_defaults(func=fill_documents_collection)


    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
