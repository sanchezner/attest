import argparse
import secrets
from db.auth import hash_token
from db.models import ReporterTokenRow, Base
from db.session import SessionLocal, engine


def create_token(project_slug, reporter):
    raw_token = secrets.token_urlsafe(32)

    with SessionLocal() as session:
        session.add(ReporterTokenRow(
            project_slug=project_slug,
            reporter=reporter,
            token_hash=hash_token(raw_token),
        ))
        session.commit()

    return raw_token


def main():
    parser = argparse.ArgumentParser(
        description='Create a reporter token for observations API',
    )
    parser.add_argument('--project', required=True, help='Project slug')
    parser.add_argument('--reporter', required=True, help='Reporter name')
    args = parser.parse_args()

    Base.metadata.create_all(engine)

    raw_token = create_token(args.project, args.reporter)
    print(f'{args.project} / {args.reporter}: {raw_token}')


if __name__ == '__main__':
    main()