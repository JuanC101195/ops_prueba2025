from app.similarity import is_similar, score

def test_score_simple():
    a = "Cra 70 # 26A - 33"
    b = "Carrera 70 Numero 26A 33"
    assert score(a, b) > 80

def test_is_similar_threshold():
    a = "Carrera 70 # 26A - 33"
    b = "Kra 70 Nro 26A - 33"
    assert is_similar(a, b, threshold=80)
