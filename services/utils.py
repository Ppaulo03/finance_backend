def money(value: float) -> str:
    sinal = "-" if value < 0 else ""
    return (
        f"{sinal} R$ {abs(value):,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
