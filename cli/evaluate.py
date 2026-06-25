import argparse
from db.models import Base
from db.session import SessionLocal, engine
from evaluator.run import run_evaluations


def main():
    parser = argparse.ArgumentParser(description='Run contract evaluations')
    parser.add_argument('--dry-run', action='store_true', help='Print alerts without sending ntfy or writing alert_log')
    args = parser.parse_args()

    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        alerts = run_evaluations(session, dry_run=args.dry_run)

    if not alerts:
        print('no alerts')
        return

    for alert in alerts:
        print(
            f'ALERT {alert['project_slug']} / {alert['artifact_id']}: '
            f'{alert['previous']} -> {alert['current']} ({alert['reason']})'
        )


if __name__ == '__main__':
    main()