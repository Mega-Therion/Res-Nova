import retraction_preflight as rp


def test_clean_standard_mu_has_no_hit():
    text = r"\addplot {x/sqrt(1+x^2)};"
    assert rp.scan_tex(text) == []


def test_retracted_number_is_a_hit():
    hits = rp.scan_tex("boost 141.99")
    assert len(hits) == 1
    assert hits[0][0] == 1


def test_paired_form_is_a_hit():
    hits = rp.scan_tex(r"$\mu = 141.99(1 + z)^{\kappa}$")
    assert len(hits) == 1


def test_unrelated_redshift_is_not_a_hit():
    assert rp.scan_tex(r"$d_L \propto (1+z)$") == []
