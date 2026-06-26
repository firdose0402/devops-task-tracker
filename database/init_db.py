from platform import version

from api import create_app, db
from task import Task

app = create_app()

with app.app_context():
    # 1. Drop existing tables if you want a clean slate (optional)
    db.drop_all()

    # 2. Create the database file and tables automatically
    db.create_all()

    # 3. Insert some default dummy tasks so it's not empty
    sample_task1 = Task(title="Setup AWS EC2", completed=False)
    sample_task2 = Task(title="Configure Kubernetes Cluster", completed=True)

    db.session.add(sample_task1)
    db.session.add(sample_task2)
    db.session.commit()

