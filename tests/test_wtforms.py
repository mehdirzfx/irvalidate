import pytest

pytest.importorskip("wtforms")

from wtforms import Form, StringField  # noqa: E402

from irvalidate.integrations.wtforms import MobileNumber, NationalId  # noqa: E402


class SignupForm(Form):
    nid = StringField(validators=[NationalId()])
    mobile = StringField(validators=[MobileNumber(message="موبایل درست نیست")])


def test_valid_form():
    form = SignupForm(data={"nid": "0013542419", "mobile": "09123456789"})
    assert form.validate()


def test_invalid_form_messages():
    form = SignupForm(data={"nid": "1234567890", "mobile": "123"})
    assert not form.validate()
    assert "کد ملی" in form.errors["nid"][0]
    assert form.errors["mobile"] == ["موبایل درست نیست"]
