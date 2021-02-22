import trafaret as t
import json
import pytest

from bson import ObjectId

from iternal.web.admin.exceptions import JsonValidationError
from iternal.web.admin.utils import (jsonify, validate_payload, as_dict)


def test_validate_payload():
    auth_form_text = b'{"username": "i m the sickest","password": "ducking_port"}'
    test_form = t.Dict({"username": t.String, "password": t.String})
    result = validate_payload(auth_form_text, test_form)
    assert result == {"username": "i m the sickest","password": "ducking_port"}


def test_jsonify():
    obj = {'foo': 'bar'}
    jsoned = jsonify(obj)
    assert jsoned == '{"foo": "bar"}'


def test_jsonify_object_id():
    obj = {'foo': ObjectId('1' * 24)}
    jsoned = jsonify(obj)
    assert jsoned == '{"foo": "111111111111111111111111"}'


def test_jsonify_failed():
    with pytest.raises(TypeError):
        jsonify(object())


def test_validate_payload_not_json():
    raw_data = b'foo=bar'
    schema = t.Dict({
        t.Key('foo'): t.Atom('bar')
    })

    with pytest.raises(JsonValidationError) as ctx:
        validate_payload(raw_data, schema)

    error = json.loads(ctx.value.text)
    assert error['error'] == 'Payload is not json serializable'


def test_validate_payload_not_valid_schema():
    raw_data = b'{"baz": "bar"}'
    schema = t.Dict({
        t.Key('foo'): t.Atom('bar')
    })

    with pytest.raises(JsonValidationError) as ctx:
        validate_payload(raw_data, schema)

    error = json.loads(ctx.value.text)
    assert error['error'] == 'Invalid json payload'


def test_as_dict():
    exc = t.DataError('err')
    resp = as_dict(exc)
    assert isinstance(resp, dict)

    exc = t.DataError('err')
    assert isinstance(exc.as_dict("boom"), str)

    resp = as_dict(exc, 'boom')
    assert isinstance(resp, dict)
