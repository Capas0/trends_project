import json
from pathlib import Path
from itertools import chain
from datetime import datetime
import subprocess

from app import celery_app
from .models import Session


@celery_app.task
def execute_session(session_id):
    session = Session.objects.get(id=session_id)
    params = dict([(param.key, param.value) for param in session.params.all()])

    session_dir = f'/data/{session.test.name}/{session.uuid}/'
    Path(session_dir).mkdir(parents=True, exist_ok=True)

    params_path = Path(session_dir, 'params.json')
    stdout_path = str(Path(session_dir, 'stdout.txt'))
    stderr_path = str(Path(session_dir, 'stderr.txt'))
    with open(str(params_path), 'w', encoding='utf-8') as f:
        json.dump(params, f)

    with open(stdout_path, 'w', encoding='utf-8') as out, open(stderr_path, 'w', encoding='utf-8') as err:
        subprocess.run(
            ['python', session.test.script.path, str(params_path)],
            stdout=out,
            stderr=err,
            encoding='utf-8'
        )

    params_path.unlink()

    session.finished_at = datetime.now()
    session.save(update_fields=['finished_at'])
