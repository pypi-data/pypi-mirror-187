def choices_from_dict(source, prepend=True):
    """
    Convert a dict to a list of tuples for use with wtforms SelectField. It also
        optionally prepends a "Please Select" option.

    Args:
        source: dict to convert.
        prepend: Bool: prepend a "Please Select" option.

    Returns:
        list of tuples.

    Example:
        # Convert this data structure:

        STATUS = OrderedDict([
            ('active', 'Active'), \n
            ('inactive', 'Inactive'), \n
            ('pending', 'Pending'), \n
            ('deleted', 'Deleted')])

        # To this:

        choices = [
            ('', 'Please Select'),\n
            ('active', 'Active'),\n
            ('inactive', 'Inactive'),\n
            ('pending', 'Pending'),\n
            ('deleted', 'Deleted')]

    """
    choices = []

    if prepend:
        choices.append(('', 'Please Select One...'))

    for key, value in source.items():
        pair = (key, value)
        choices.append(pair)

    return choices
