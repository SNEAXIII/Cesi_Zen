from datetime import datetime
from itertools import product
from random import randint
from faker import Faker
from sqlmodel import create_engine, Session
from typing import List
from enum import Enum
from src.enums.Roles import Roles
from src.security.secrets import SECRET
from src.services.PasswordService import crypt_context
from src.models import Article, Category, User, LoginLog, ExerciseCoherenceCardiac

sync_engine = create_engine(
    f"mysql+pymysql://{SECRET.MARIADB_USER}:{SECRET.MARIADB_PASSWORD}@{SECRET.MARIADB_HOST}/{SECRET.MARIADB_DATABASE}",
    # echo=True,
)

fake = Faker(locale="en")


class States(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    DELETED = "deleted"


PASSWORD = "test"
NOW = datetime.now()


def hash_with_low_security(password: str) -> str:
    return crypt_context.hash(password)


admin = User(
    email="admin@email.com",
    login="admin",
    hashed_password=hash_with_low_security(PASSWORD),
    role=Roles.ADMIN,
)
user = User(
    email="user@email.com",
    login="user",
    hashed_password=hash_with_low_security(PASSWORD),
    role=Roles.USER,
)


def create_sample_users(rolls: int) -> List[User]:
    states = States.__members__.values()
    roles = Roles.__members__.values()

    users = []
    for role, state, index in product(roles, states, range(rolls)):
        id_bonus = f"{randint(0, 9999)}".zfill(4)
        name = f"{(fake.first_name())}_{id_bonus}"
        email = f"{name}@gmail.com"
        password = hash_with_low_security(PASSWORD)
        user = User(
            login=name,
            email=email,
            role=role,
            hashed_password=password,
            created_at=fake.date_time(end_datetime=NOW),
        )
        match state:
            case States.DELETED:
                user.deleted_at = fake.date_time(end_datetime=NOW)
            case States.DISABLED:
                user.disabled_at = fake.date_time(end_datetime=NOW)
        users.append(user)
    return users


def get_admins(users: List[User]) -> List[User]:
    return [_user for _user in users if _user.role == Roles.ADMIN.value]


def create_sample_categories():
    return [
        Category(label="Actualités"),
        Category(label="Bien-être"),
        Category(label="Conseils"),
        Category(label="Méditation"),
        Category(label="Respiration"),
        Category(label="Spiritualité"),
    ]


def create_sample_articles(
    users: List[User], categories: List[Category], rolls: int
) -> List[Article]:
    articles = []
    for user, category, index in product(users, categories, range(rolls)):
        article = Article(
            title=fake.text(max_nb_chars=50),
            content=fake.text(max_nb_chars=100),
            created_at=fake.date_time(end_datetime=NOW),
            id_user=user.id,
            id_category=category.id,
        )
        articles.append(article)
    return articles


def create_sample_exercises() -> List[ExerciseCoherenceCardiac]:
    return [
        ExerciseCoherenceCardiac(
            name="Respiration 748",
            duration_inspiration=7,
            duration_apnea=4,
            duration_expiration=8,
            number_cycles=15,  # (7+4+8)*15 ~= 300 seconds
        ),
        ExerciseCoherenceCardiac(
            name="Respiration 505",
            duration_inspiration=5,
            duration_apnea=0,
            duration_expiration=5.0,
            number_cycles=30,  # (5+5)*30 ~= 300 seconds
        ),
        ExerciseCoherenceCardiac(
            name="Respiration 406",
            duration_inspiration=5,
            duration_apnea=0,
            duration_expiration=5.0,
            number_cycles=30,  # (4+6)*30 ~= 300 seconds
        ),
    ]


def create_sample_login_logs(users: List[User], rolls: int) -> List[LoginLog]:
    logs = []
    for user, _ in product(users, range(rolls)):
        date = fake.date_time(end_datetime=NOW)
        user.last_login_date = date
        logs.append(
            LoginLog(
                id_user=user.id,
                date_connexion=fake.date_time(end_datetime=NOW),
            )
        )
    return logs


def load_sample_data():
    try:
        with Session(sync_engine) as session:
            session.add(admin)
            session.add(user)
            print("🚀 Creating users")
            all_users = create_sample_users(rolls=5)
            admins = get_admins(all_users)
            for elem in all_users:
                session.add(elem)
            session.commit()
            print("✅ Users loaded with success !")
            categories = create_sample_categories()
            for elem in categories:
                session.add(elem)
            session.commit()
            print("✅ Categories loaded with success !")
            articles = create_sample_articles(admins, categories, rolls=1)
            for elem in articles:
                session.add(elem)
            session.commit()
            print("✅ Articles loaded with success !")
            login_logs = create_sample_login_logs(all_users, rolls=4)
            exercises = create_sample_exercises()
            for elem in exercises:
                session.add(elem)
            session.commit()
            print("✅ Exercises loaded with success !")
            for elem in login_logs:
                session.add(elem)
            session.commit()
            print("✅ Login logs loaded with success !")

        print("✅ Sample data loaded with success !")

    except Exception as e:
        session.rollback()
        print(f"❌ Error loading sample data : {e}")
        raise


if __name__ == "__main__":
    load_sample_data()
