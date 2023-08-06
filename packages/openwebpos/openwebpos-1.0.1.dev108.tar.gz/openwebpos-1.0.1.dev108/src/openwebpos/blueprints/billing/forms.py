from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange


class PaymentAmountForm(FlaskForm):
    """
    Form for entering payment amount.

    Extends:
        FlaskForm

    variables:
        amount -- IntegerField for entering payment amount
        submit -- SubmitField for submitting payment amount

    Returns:
        FlaskForm: Form for entering payment amount.

    Example:
        >>> form = PaymentAmountForm()
    """
    amount = FloatField('Amount',
                        validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit')
