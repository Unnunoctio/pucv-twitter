from datetime import datetime


class Search:
    keyword: str | None
    account: str | None
    start_date: datetime
    end_date: datetime

    def __init__(self, keyword: str | None, account: str | None, start_date: str | None, end_date: str | None):
        self.keyword = keyword
        self.account = account

        # Validar Búsqueda
        if self.keyword is None and self.account is None:
            raise ValueError("Error: No se ha proporcionado una palabra clave ni un nombre de cuenta")

        # Validar Fecha de inicio
        if start_date is None:
            raise ValueError("Error: No se ha proporcionado una fecha de inicio")

        try:
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        except Exception:
            raise ValueError(f"Error: Fecha de inicio '{start_date}' no válida, su formato es: aaaa-mm-dd")

        # Validar Fecha de término
        if end_date is None:
            self.end_date = datetime.now()
        else:
            try:
                self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
            except Exception:
                raise ValueError(f"Error: Fecha de término '{end_date}' no válida, su formato es: aaaa-mm-dd")

        # Validar fechas
        current_date = datetime.now()
        if self.start_date > current_date:
            raise ValueError("Error: La fecha de inicio no puede ser mayor que la fecha actual")
        if self.end_date < self.start_date:
            raise ValueError("Error: La fecha de término no puede ser menor que la fecha de inicio")

    def __str__(self) -> str:
        return (f"Keyword: {self.keyword}\n"
                f"Account: {self.account}\n"
                f"Start date: {self.start_date}\n"
                f"End date: {self.end_date}")

