from services.firebase_service import init_sdk_with_service_account, add_scope
from typer import Typer, echo

typer_app = Typer()


@typer_app.command()
def make_admin(uid: str) -> None:
    init_sdk_with_service_account()
    result = add_scope(uid, "admin")
    echo(f"Admin scope added for {uid}: {result}")


@typer_app.command()
def make_editor(uid: str) -> None:
    init_sdk_with_service_account()
    result = add_scope(uid, "editor")
    echo(f"Editor scope added for {uid}: {result}")


@typer_app.command()
def new_scope(uid: str, role: str) -> None:
    init_sdk_with_service_account()
    result = add_scope(uid, role)
    echo(f"{role} scope added for {uid}: {result}")


if __name__ == "__main__":
    typer_app()
