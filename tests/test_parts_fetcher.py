from src.services.parts_service import fetch_parts

def test_grade_caps():
    g1 = fetch_parts(1)
    assert all(p["grade_min"] <= 1 <= p["grade_max"] for p in g1)

    g5_elec = fetch_parts(5, "ELEC")
    assert any(p["part_id"] == "SERVO_SG90" for p in g5_elec)
    assert all(p["domain"] == "ELEC" for p in g5_elec)
