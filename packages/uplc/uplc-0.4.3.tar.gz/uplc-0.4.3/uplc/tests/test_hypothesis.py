import datetime
import unittest
import hypothesis
from hypothesis import strategies as hst
import frozenlist as fl

from .. import *


def frozenlist(l):
    l = fl.FrozenList(l)
    l.freeze()
    return l


pos_int = hst.integers(min_value=0)


uplc_data_integer = hst.builds(PlutusInteger, hst.integers())
uplc_data_bytestring = hst.builds(PlutusByteString, hst.binary())


def rec_data_strategies(uplc_data):
    uplc_data_list = hst.builds(
        lambda x: PlutusList(frozenlist(x)), hst.lists(uplc_data)
    )
    uplc_data_constr = hst.builds(
        lambda x, y: PlutusConstr(x, frozenlist(y)),
        hst.integers(min_value=0, max_value=255 - 121),
        hst.lists(uplc_data),
    )
    uplc_data_map = hst.builds(
        PlutusMap,
        hst.dictionaries(
            hst.one_of(
                uplc_data_integer, uplc_data_bytestring
            ),  # TODO technically constr is legal too, but causes hashing error
            uplc_data,
            dict_class=frozendict.frozendict,
        ),
    )
    return hst.one_of(uplc_data_map, uplc_data_list, uplc_data_constr)


uplc_data = hst.recursive(
    hst.one_of(uplc_data_bytestring, uplc_data_integer),
    rec_data_strategies,
    max_leaves=4,
)
uplc_builtin_boolean = hst.builds(BuiltinBool, hst.booleans())
uplc_builtin_integer = hst.builds(BuiltinInteger, hst.integers())
uplc_builtin_bytestring = hst.builds(BuiltinByteString, hst.binary())
uplc_builtin_string = hst.builds(
    BuiltinString, hst.from_regex(r'[^\r\n"]*', fullmatch=True)
)
uplc_builtin_unit = hst.just(BuiltinUnit())


def rec_const_strategies(uplc_constant):
    uplc_builtin_pair = hst.builds(BuiltinPair, uplc_constant, uplc_constant)
    uplc_builtin_list = hst.builds(
        lambda x, y: BuiltinList(frozenlist([x] * y), x),
        uplc_constant,
        hst.integers(min_value=0, max_value=10),
    )
    return hst.one_of(uplc_builtin_list, uplc_builtin_pair)


uplc_constant = hst.recursive(
    hst.one_of(
        uplc_builtin_unit,
        uplc_builtin_string,
        uplc_builtin_bytestring,
        uplc_builtin_integer,
        uplc_builtin_boolean,
        uplc_data,
    ),
    rec_const_strategies,
    max_leaves=4,
)
uplc_error = hst.just(Error())
uplc_name = hst.from_regex(r"[a-z_~][\w~!#]*", fullmatch=True)
uplc_builtin_fun = hst.builds(BuiltIn, hst.sampled_from(BuiltInFun))
uplc_variable = hst.builds(Variable, uplc_name)


def rec_expr_strategies(uplc_expr):
    uplc_delay = hst.builds(Delay, uplc_expr)
    uplc_force = hst.builds(Force, uplc_expr)
    uplc_apply = hst.builds(Apply, uplc_expr, uplc_expr)
    uplc_lambda = hst.builds(Lambda, uplc_name, uplc_expr)
    return hst.one_of(uplc_lambda, uplc_delay, uplc_force, uplc_apply)


uplc_expr = hst.recursive(
    hst.one_of(uplc_error, uplc_constant, uplc_builtin_fun, uplc_variable),
    rec_expr_strategies,
    max_leaves=10,
)


uplc_version = hst.builds(lambda x, y, z: f"{x}.{y}.{z}", pos_int, pos_int, pos_int)
uplc_program = hst.builds(Program, uplc_version, uplc_expr)


class MiscTest(unittest.TestCase):
    @hypothesis.given(uplc_program, hst.sampled_from(UPLCDialect))
    @hypothesis.settings(max_examples=1000)
    @hypothesis.example(
        Program(version="0.0.0", term=BuiltinByteString(value=b"")), UPLCDialect.Aiken
    )
    @hypothesis.example(
        Program(version="0.0.0", term=BuiltIn(builtin=BuiltInFun.ConstrData)),
        UPLCDialect.Aiken,
    )
    @hypothesis.example(
        Program(version="0.0.0", term=BuiltinInteger(value=0)), UPLCDialect.Aiken
    )
    def test_dumps_parse_roundtrip(self, p, dialect):
        assert parse(dumps(p, dialect)) == p
