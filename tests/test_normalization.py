from app.normalization import normalize_code, normalize_text


def test_reference_normalization_ignores_spacing_and_punctuation() -> None:
    assert normalize_code("PT 43") == normalize_code("PT43") == "pt43"
    assert normalize_code("945-444-49") == "94544449"


def test_position_and_side_aliases_are_canonicalized() -> None:
    assert normalize_text("oldi LH") == "front left"
    assert normalize_text("orqa RH") == "rear right"
    assert normalize_text("передний левый") == "front left"
    assert normalize_text("задний правый") == "rear right"
    assert normalize_text("ABS") == "abs"


def test_query_sanitization_collapses_noise_without_changing_code_normalization() -> None:
    from app.normalization import sanitize_query

    assert sanitize_query("  свеча,   cobalt\\ ") == "свеча cobalt"
    assert sanitize_query('свеча cobalt\\///,;;"!!!') == "свеча cobalt"
    assert normalize_code("PT 43") == "pt43"
