def cents_to_dollars(cents: int) -> float:
    """
    Convert cents to dollars

    Args:
        cents (int): cents to convert

    Returns:
        float: dollars
    """
    return round(cents / 100, 2)


def dollars_to_cents(dollars: float) -> int:
    """
    Convert dollars to cents

    Args:
        dollars (float): dollars to convert

    Returns:
        int: cents
    """
    return round(dollars * 100)
