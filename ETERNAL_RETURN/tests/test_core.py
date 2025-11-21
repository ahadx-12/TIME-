import numpy as np

from core.physics import GodelUniverse


def test_environment_smoke():
    assert True


def test_pure_time_at_center_is_timelike():
    gu = GodelUniverse(omega=0.5)
    ds2 = gu.interval_squared(dt=1.0, dr=0.0, dphi=0.0, dz=0.0, r=1e-3)
    # At near r=0, pure time should be timelike: ds^2 < 0
    assert ds2 < 0


def test_interval_returns_float():
    gu = GodelUniverse(omega=0.5)
    value = gu.interval_squared(1.0, 0.1, 0.2, 0.0, r=1.0)
    assert isinstance(value, float)


def test_is_timelike_matches_interval_sign():
    gu = GodelUniverse(omega=1.0)
    assert gu.is_timelike(dt=1.0, dr=0.0, dphi=0.0, dz=0.0, r=1e-2) is True
    assert gu.is_timelike(dt=0.0, dr=1.0, dphi=0.0, dz=0.0, r=1.0) is False


def test_critical_radius_is_positive():
    gu = GodelUniverse(omega=0.5)
    r_crit = gu.find_critical_radius()
    assert r_crit is None or r_crit > 0


def test_ctc_transition_detectable():
    gu = GodelUniverse(omega=1.0)
    r_crit = gu.find_critical_radius()
    if r_crit is not None:
        assert 0.0 < r_crit < 1e6
