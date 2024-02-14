import dolfin as df
import pytest

from jr_dolfin_utils import mms


def test_mms_interval():
    domain = mms.MMSInterval(10)
    dx = df.Measure("dx", domain=domain, subdomain_data=domain.subdomains)
    assert df.assemble(1 * dx(1)) == pytest.approx(2 * 0.8)
    assert df.assemble(1 * dx(2)) == pytest.approx(2 * (1 - 0.8))


def test_mms_square():
    domain = mms.MMSSquare(20)
    dx = df.Measure("dx", domain=domain, subdomain_data=domain.subdomains)
    assert df.assemble(1 * dx(1)) == pytest.approx((2 * 0.8) ** 2)
    assert df.assemble(1 * dx(2)) == pytest.approx((2**2 - (2 * 0.8) ** 2))
